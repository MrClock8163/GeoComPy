from __future__ import annotations

from enum import Enum, Flag

from .. import (
    GeoComSubsystem,
    GeoComResponse
)
from ..communication import toenum


class TPS1200PIMG(GeoComSubsystem):
    class MEMTYPE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PIMG.MEMTYPE:
            return cls(int(value))

        INTERNAL = 0x0
        PCCARD = 0x1

    class SUBFUNC(Flag):
        @classmethod
        def parse(cls, value: str) -> TPS1200PIMG.SUBFUNC:
            return cls(int(value))

        TESTIMG = 1
        AUTOEXPTIME = 2
        SS2 = 4
        SS4 = 8

    def get_tcc_config(
        self,
        memtype: MEMTYPE | str = MEMTYPE.PCCARD
    ) -> GeoComResponse:
        _memtype = toenum(self.MEMTYPE, memtype)
        return self._request(
            23400,
            parsers={
                "imgnumber": int,
                "quality": int,
                "subfunc": lambda x: self.SUBFUNC(int(x)),
                "prefix": str
            }
        )

    def set_tcc_config(
        self,
        imgnumber: int,
        quality: int,
        subfunc: SUBFUNC | int,
        memtype: MEMTYPE | str = MEMTYPE.PCCARD,
    ) -> GeoComResponse:
        _memtype = toenum(self.MEMTYPE, memtype)
        if isinstance(subfunc, self.SUBFUNC):
            subfunc = subfunc.value
        return self._request(
            23401,
            [_memtype.value, imgnumber, quality, subfunc]
        )

    def take_tcc_img(
        self,
        memtype: MEMTYPE | str = MEMTYPE.PCCARD
    ) -> GeoComResponse:
        _memtype = toenum(self.MEMTYPE, memtype)
        return self._request(
            23402,
            [_memtype.value],
            {
                "imgnumber": int
            }
        )
