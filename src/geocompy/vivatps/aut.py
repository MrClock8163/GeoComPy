from __future__ import annotations

from enum import Enum

from .. import (
    GeoComResponse
)
from ..data import toenum
from .cam import VivaTPSCAM
from ..tps1200p.aut import TPS1200PAUT


class VivaTPSAUT(TPS1200PAUT):
    class ONOFF(Enum):
        @classmethod
        def parse(cls, value: str) -> VivaTPSAUT.ONOFF:
            return cls(int(value))

        OFF = 0
        ON = 1

    class POSMODE(Enum):
        @classmethod
        def parse(cls, value: str) -> VivaTPSAUT.POSMODE:
            return cls(int(value))

        NORMAL = 0
        PRECISE = 1
        FAST = 2  # TS30 / MS30
    
    def set_lock_fly_mode(
        self,
        state: ONOFF | str
    ) -> GeoComResponse:
        _state = toenum(self.ONOFF, state)
        return self._request(
            9103,
            [_state.value]
        )
    
    def get_lock_fly_mode(self) -> GeoComResponse:
        return self._request(
            9102,
            parsers={
                "state": self.ONOFF.parse
            }
        )
    
    def cam_posit_to_pixel_coord(
        self,
        x: int,
        y: int,
        camtype: VivaTPSCAM.CAMTYPE | str = VivaTPSCAM.CAMTYPE.OVC
    ) -> GeoComResponse:
        _camtype = toenum(VivaTPSCAM.CAMTYPE, camtype)
        return self._request(
            9081,
            [_camtype.value, x, y]
        )
