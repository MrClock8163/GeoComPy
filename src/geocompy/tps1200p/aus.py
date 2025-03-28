from __future__ import annotations

from enum import Enum

from .. import (
    GeoComSubsystem,
    GeoComResponse
)
from ..communication import toenum


class TPS1200PAUS(GeoComSubsystem):
    class ONOFF(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PAUS.ONOFF:
            return cls(int(value))

        OFF = 0
        ON = 1

    def get_user_atr_state(self) -> GeoComResponse:
        return self._request(
            18006,
            parsers={
                "state": self.ONOFF.parse
            }
        )

    def set_user_atr_state(
        self,
        state: ONOFF | str
    ) -> GeoComResponse:
        _state = toenum(self.ONOFF, state)
        return self._request(18005, [_state.value])

    def get_user_lock_state(self) -> GeoComResponse:
        return self._request(
            18008,
            parsers={
                "state": self.ONOFF.parse
            }
        )

    def set_user_lock_state(
        self,
        state: ONOFF | str
    ) -> GeoComResponse:
        _state = toenum(self.ONOFF, state)
        return self._request(
            18007,
            [_state.value]
        )
