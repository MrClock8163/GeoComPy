from __future__ import annotations

from enum import Enum
from datetime import datetime

from .. import GeoComResponse
from ..data import (
    Byte,
    parsestr,
    toenum
)
from ..tps1200p.ftr import TPS1200PFTR


class VivaTPSFTR(TPS1200PFTR):
    class DEVICETYPE(Enum):
        @classmethod
        def parse(cls, value: str) -> VivaTPSFTR.DEVICETYPE:
            return cls(int(value))

        INTERNAL = 0
        PCPARD = 1
        SDCARD = 4
        USB = 5
        RAM = 6
        
    class FILETYPE(Enum):
        @classmethod
        def parse(cls, value: str) -> VivaTPSFTR.FILETYPE:
            return cls(int(value))

        POINTRELATEDDB = 103
        IMAGES = 170
        IMAGES_OVC_JPG = 171
        IMAGES_OVC_BMP = 172
        IMAGES_OAV_JPG = 173
        IMAGES_OAV_BMP = 174
        SCANS = 175,
        UNKNOWN = 200
        LAST = 201
    
    def delete_dir(
        self,
        dirname: str,
        time: datetime | None = None,
        device: DEVICETYPE | str = DEVICETYPE.INTERNAL
    ) -> GeoComResponse:
        _device = toenum(self.DEVICETYPE, device)
        _filetype = self.FILETYPE.POINTRELATEDDB

        if time is None:
            params = [
                _device.value, _filetype.value,
                Byte(0), Byte(0), Byte(0),
                dirname
            ]
        else:
            params = [
                _device.value, _filetype.value,
                Byte(time.day), Byte(time.month), Byte(time.year - 2000),
                dirname
            ]
        return self._request(
            23309,
            params,
            {
                "deleted": int
            }
        )

    def setup_download_large(
        self,
        filename: str,
        blocksize: int,
        device: DEVICETYPE | str = DEVICETYPE.INTERNAL,
        filetype: FILETYPE | str = FILETYPE.UNKNOWN
    ) -> GeoComResponse:
        _device = toenum(self.DEVICETYPE, device)
        _filetype = toenum(self.FILETYPE, filetype)
        return self._request(
            23313,
            [_device.value, _filetype.value, filename, blocksize],
            {
                "blockcount": int
            }
        )

    def download_xl(
        self,
        block: int
    ) -> GeoComResponse:
        return self._request(
            23314,
            [block],
            {
                "value": parsestr,
                "length": int
            }
        )
