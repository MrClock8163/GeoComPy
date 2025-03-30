from __future__ import annotations

from enum import Enum

from .. import (
    GeoComSubsystem,
    GeoComResponse
)
from ..data import toenum


class TPS1200PSUP(GeoComSubsystem):
    class ONOFF(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PSUP.ONOFF:
            return cls(int(value))

        OFF = 0
        ON = 1

    class AUTOPOWER(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PSUP.AUTOPOWER:
            return cls(int(value))

        DISABLED = 0
        OFF = 2

    def get_config(self) -> GeoComResponse:
        return self._request(
            14001,
            parsers={
                "reserved": int,
                "autopower": self.AUTOPOWER.parse,
                "timeout": int
            }
        )

    def set_config(
        self,
        autopower: AUTOPOWER | str = AUTOPOWER.OFF,
        timeout: int = 3_600_000,
        reserved: ONOFF | str = ONOFF.ON
    ) -> GeoComResponse:
        _autopower = toenum(self.AUTOPOWER, autopower)
        _reserved = toenum(self.ONOFF, reserved)
        return self._request(
            14002,
            [_reserved.value, _autopower.value, timeout]
        )
