from __future__ import annotations

from enum import Enum

from .. import (
    GeoComSubsystem,
    GeoComResponse
)
from ..communication import toenum


class TPS1200PCOM(GeoComSubsystem):
    class STOPMODE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PCOM.STOPMODE:
            return cls(int(value))

        SHUTDOWN = 0
        SLEEP = 1

    class STARTUPMODE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PCOM.STARTUPMODE:
            return cls(int(value))

        LOCAL = 0
        REMOTE = 1

    def get_sw_version(self) -> GeoComResponse:
        return self._request(
            110,
            parsers={
                "release": int,
                "version": int,
                "subversion": int
            }
        )

    def switch_on(
        self,
        onmode: STARTUPMODE | str = STARTUPMODE.LOCAL
    ) -> GeoComResponse:
        _onmode = toenum(self.STARTUPMODE, onmode)
        return self._request(
            111,
            [_onmode.value]
        )

    def switch_off(
        self,
        offmode: STOPMODE | str = STOPMODE.SHUTDOWN
    ) -> GeoComResponse:
        _offmode = toenum(self.STOPMODE, offmode)
        return self._request(
            112,
            [_offmode.value]
        )

    def nullproc(self) -> GeoComResponse:
        return self._request(0)

    def get_binary_available(self) -> GeoComResponse:
        return self._request(
            113,
            parsers={
                "available": bool
            }
        )

    def set_binary_available(
        self,
        available: bool
    ) -> GeoComResponse:
        return self._request(
            114,
            [available]
        )
