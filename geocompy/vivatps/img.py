from __future__ import annotations

from enum import Enum

from .. import GeoComResponse
from ..tps1200p.img import TPS1200PIMG


class VivaTPSIMG(TPS1200PIMG):
    class MEMTYPE(Enum):
        @classmethod
        def parse(cls, value: str) -> VivaTPSIMG.MEMTYPE:
            return cls(int(value))

        INTERNAL = 0x0
        PCCARD = 0x1
        SDCARD = 0x2
    
    def set_tcc_exposure_time(
        self,
        time: int
    ) -> GeoComResponse:
        return self._request(
            23403,
            [time]
        )
