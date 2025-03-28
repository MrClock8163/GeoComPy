from __future__ import annotations

from enum import Enum

from ..communication import toenum
from .. import GeoComResponse
from ..tps1200p.bap import TPS1200PBAP


class VivaTPSBAP(TPS1200PBAP):
    class ONOFF(Enum):
        @classmethod
        def parse(cls, value: str) -> VivaTPSBAP.ONOFF:
            return cls(int(value))

        OFF = 0
        ON = 1
    
    def get_atr_precise(self) -> GeoComResponse:
        return self._request(
            17039,
            parsers={
                "state": self.ONOFF.parse
            }
        )

    def set_atr_precise(
        self,
        state: ONOFF | str
    ) -> GeoComResponse:
        _state = toenum(self.ONOFF, state)
        return self._request(
            17040,
            [_state.value]
        )
