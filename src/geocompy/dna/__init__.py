from __future__ import annotations

from enum import IntEnum
import re
from typing import Callable, TypeVar
from traceback import format_exc
import logging
from time import sleep

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

    class BEEPTYPE(IntEnum):
        SHORT = 0
        LONG = 1
        ALARM = 2

    def __init__(
        self,
        connection: Connection,
        logger: logging.Logger | None = None,
        retry: int = 2
    ):
        super().__init__(connection, logger)
        self.settings: DNASettings = DNASettings(self)
        self.measurements: DNAMeasurements = DNAMeasurements(self)

        for i in range(retry):
            try:
                reply = self._conn.exchange1("a")
                if reply == "?":
                    break
            except Exception:
                pass

            sleep(1)
        else:
            raise ConnectionError(
                "could not establish connection to instrument"
            )

        self.settings.get_format()  # Sync format setting

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

        response = GsiOnlineResponse(
            param_descriptions.get(param, ""),
            cmd,
            answer,
            value,
            comment
        )
        self._logger.debug(response)
        return response

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

        response = GsiOnlineResponse(
            word_descriptions.get(wordindex, ""),
            cmd,
            answer,
            answer == "?",
            comment
        )
        self._logger.debug(response)
        return response

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

        response = GsiOnlineResponse(
            word_descriptions.get(wordindex, ""),
            cmd,
            answer,
            value,
            comment
        )
        self._logger.debug(response)
        return response

    def request(
        self,
        cmd: str
    ) -> GsiOnlineResponse[bool]:
        comment = ""
        try:
            answer = self._conn.exchange1(cmd)
        except Exception:
            self._logger.error(format_exc())
            answer = DNAErrors.E_UNKNOWN.value
            comment = "EXCHANGE"

        response = GsiOnlineResponse(
            "",
            cmd,
            answer,
            answer == "?",
            comment
        )
        self._logger.debug(response)
        return response

    def beep(
        self,
        beeptype: BEEPTYPE | str
    ) -> GsiOnlineResponse[bool]:
        _beeptype = toenum(self.BEEPTYPE, beeptype)
        cmd = f"BEEP/{_beeptype.value:d}"
        response = self.request(cmd)
        response.desc = "Beep"
        return response

    def wakeup(self) -> GsiOnlineResponse[bool]:
        response = self.request("a")
        response.desc = "Wakeup"
        return response

    def shutdown(self) -> GsiOnlineResponse[bool]:
        response = self.request("b")
        response.desc = "Shutdown"
        return response

    def clear(self) -> GsiOnlineResponse[bool]:

        response = self.request("c")
        response.desc = "Clear"
        return response
