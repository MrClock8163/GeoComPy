from __future__ import annotations

from enum import Enum

from .. import GeoComResponse
from ..communication import toenum
from ..tps1200p.edm import TPS1200PEDM


class VivaTPSEDM(TPS1200PEDM):
    class ONOFF(Enum):
        @classmethod
        def parse(cls, value: str) -> VivaTPSEDM.ONOFF:
            return cls(int(value))

        OFF = 0
        ON = 1
    
    class MEASUREMENTTYPE(Enum):
        @classmethod
        def parse(cls, value: str) -> VivaTPSEDM.MEASUREMENTTYPE:
            return cls(int(value))
    
        SIGNAL = 1
        FREQ = 2
        DIST = 3
        ANY = 4

    def is_cont_meas_active(
        self,
        mode: MEASUREMENTTYPE | str
    ) -> GeoComResponse:
        _mode = toenum(self.MEASUREMENTTYPE, mode)
        return self._request(
            1070,
            [_mode.value],
            {
                "active": bool
            }
        )
    
    def set_boomerang_filter(
        self,
        state: ONOFF | str
    ) -> GeoComResponse:
        _state = toenum(self.ONOFF, state)
        return self._request(
            1061,
            [_state.value]
        )
