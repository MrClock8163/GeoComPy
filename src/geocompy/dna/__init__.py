from __future__ import annotations

from enum import Enum
import re
from typing import Callable, TypeVar
from traceback import format_exc

from .. import (
    GsiOnlineProtocol,
    GsiOnlineResponse
)
from ..data import (
    enumparser,
    toenum
)
from .meta import (
    param_descriptions,
    word_descriptions,
    DNAErrors
)


_T = TypeVar("_T")


class DNA(GsiOnlineProtocol):
    _CONFPAT = re.compile(
        r"^(?P<conf>\d{4})/"
        r"(?P<value>\d{4})$"
    )

    class BEEP(Enum):
        OFF = 0
        MEDIUM = 1
        LOUD = 2
    
    def setrequest(
        self,
        param: int,
        value: int
    ) -> GsiOnlineResponse[bool | None]:
        cmd = f"SET/{param:d}/{value:d}"
        try:
            answer = self._conn.exchange1(cmd)
        except:
            self._logger.error(format_exc())
            answer = DNAErrors.E_UNKNOWN.value
        
        return GsiOnlineResponse(
            param_descriptions.get(param, ""),
            cmd,
            answer,
            answer == "?"
        )

    def confrequest(
        self,
        param: int,
        parser: Callable[[str], _T]
    ) -> GsiOnlineResponse[_T | None]:
        cmd = f"CONF/{param:d}"
        try:
            answer = self._conn.exchange1(cmd)
        except:
            self._logger.error(format_exc())
            answer = DNAErrors.E_UNKNOWN.value
        
        success = bool(self._CONFPAT.match(answer))
        return GsiOnlineResponse(
            param_descriptions.get(param, ""),
            cmd,
            answer,
            parser(answer.split("/")[1]) if success else None
        )

    def putrequest(
        self,
        wordindex: int,
        word: str
    ) -> GsiOnlineResponse[bool | None]:
        cmd = f"PUT/{word:s} "
        answer = self._conn.exchange1(cmd)
        return GsiOnlineResponse(
            param_descriptions.get(wordindex, ""),
            cmd,
            answer,
            answer == "?"
        )
    
    def getrequest(
        self,
        mode: str,
        wordindex: int,
        parser: Callable[[str], _T]
    ) -> GsiOnlineResponse[_T | None]:
        cmd = f"GET/{mode:s}/WI{wordindex:d} "
        answer = self._conn.exchange1(cmd)
        success = bool(self._CONFPAT.match(answer))
        return GsiOnlineResponse(
            param_descriptions.get(wordindex, ""),
            cmd,
            answer,
            parser(answer) if success else None
        )

    def set_beep(
        self,
        status: BEEP | str
    ) -> GsiOnlineResponse[bool | None]:
        _status = toenum(self.BEEP, status)
        return self.setrequest(30, _status.value)

    def conf_beep(self) -> GsiOnlineResponse[BEEP | None]:
        return self.confrequest(
            30,
            enumparser(self.BEEP)
        )
