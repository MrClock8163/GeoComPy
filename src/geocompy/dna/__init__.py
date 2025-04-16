from __future__ import annotations

from enum import Enum
import re
from typing import Callable, TypeVar
from traceback import format_exc
import logging

from .. import (
    GsiOnlineProtocol,
    GsiOnlineResponse
)
from ..communication import Connection
from ..data import (
    toenum
)
from .meta import (
    param_descriptions,
    word_descriptions,
    DNAErrors
)
from .settings import DNASettings
from .measurements import DNAMeasurements


_T = TypeVar("_T")


class DNA(GsiOnlineProtocol):
    _CONFPAT = re.compile(
        r"^(?:\d{4})/"
        r"(?:\d{4})$"
    )
    _GSIPAT = re.compile(
        r"^\*?"
        r"(?:[0-9\.]{6})"
        r"(?:\+|\-)"
        r"(?:[a-zA-Z0-9]{8}|[a-zA-Z0-9]{16}) $"
    )

    class BEEPTYPE(Enum):
        SHORT = 0
        LONG = 1
        ALARM = 2

    def __init__(
        self,
        connection: Connection,
        logger: logging.Logger | None = None
    ):
        super().__init__(connection, logger)
        self.settings: DNASettings = DNASettings(self)
        self.measurements: DNAMeasurements = DNAMeasurements(self)

    def setrequest(
        self,
        param: int,
        value: int
    ) -> GsiOnlineResponse[bool]:
        cmd = f"SET/{param:d}/{value:d}"
        comment = ""
        try:
            answer = self._conn.exchange1(cmd)
        except Exception:
            self._logger.error(format_exc())
            answer = DNAErrors.E_UNKNOWN.value
            comment = "EXCHANGE"

        return GsiOnlineResponse(
            param_descriptions.get(param, ""),
            cmd,
            answer,
            answer == "?",
            comment
        )

    def confrequest(
        self,
        param: int,
        parser: Callable[[str], _T]
    ) -> GsiOnlineResponse[_T | None]:
        cmd = f"CONF/{param:d}"
        comment = ""
        try:
            answer = self._conn.exchange1(cmd)
        except Exception:
            self._logger.error(format_exc())
            answer = DNAErrors.E_UNKNOWN.value
            comment = "EXCHANGE"

        success = bool(self._CONFPAT.match(answer))
        value = None
        if success:
            try:
                value = parser(answer.split("/")[1])
            except Exception:
                comment = "PARSE"
        else:
            comment = "INSTRUMENT"

        return GsiOnlineResponse(
            param_descriptions.get(param, ""),
            cmd,
            answer,
            value,
            comment
        )

    def putrequest(
        self,
        wordindex: int,
        word: str
    ) -> GsiOnlineResponse[bool]:
        cmd = f"PUT/{word:s}"
        comment = ""
        try:
            answer = self._conn.exchange1(cmd)
        except Exception:
            self._logger.error(format_exc())
            answer = DNAErrors.E_UNKNOWN.value
            comment = "failed to exchange messages"

        return GsiOnlineResponse(
            word_descriptions.get(wordindex, ""),
            cmd,
            answer,
            answer == "?",
            comment
        )

    def getrequest(
        self,
        mode: str,
        wordindex: int,
        parser: Callable[[str], _T]
    ) -> GsiOnlineResponse[_T | None]:
        cmd = f"GET/{mode:s}/WI{wordindex:d}"
        comment = ""
        try:
            answer = self._conn.exchange1(cmd)
        except Exception:
            self._logger.error(format_exc())
            answer = DNAErrors.E_UNKNOWN.value
            comment = "EXCHANGE"

        success = bool(self._GSIPAT.match(answer))
        value = None
        if success:
            try:
                value = parser(answer)
            except Exception:
                comment = "PARSE"
        else:
            comment = "INSTRUMENT"

        return GsiOnlineResponse(
            word_descriptions.get(wordindex, ""),
            cmd,
            answer,
            value,
            comment
        )

    def beep(
        self,
        beeptype: BEEPTYPE | str
    ) -> GsiOnlineResponse[bool]:
        _beeptype = toenum(self.BEEPTYPE, beeptype)
        cmd = f"BEEP/{_beeptype.value:d}"
        comment = ""
        try:
            answer = self._conn.exchange1(cmd)
        except Exception:
            self._logger.error(format_exc())
            answer = DNAErrors.E_UNKNOWN.value
            comment = "EXCHANGE"

        return GsiOnlineResponse(
            "Beep",
            cmd,
            answer,
            answer == "?",
            comment
        )
