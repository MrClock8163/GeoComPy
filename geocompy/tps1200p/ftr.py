from __future__ import annotations

from enum import Enum
from datetime import datetime

from .. import (
    GeoComSubsystem,
    GeoComResponse
)
from ..data import Byte
from ..communication import toenum, parsestr


class TPS1200PFTR(GeoComSubsystem):
    class DEVICETYPE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PFTR.DEVICETYPE:
            return cls(int(value))

        INTERNAL = 0
        PCPARD = 1

    class FILETYPE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PFTR.FILETYPE:
            return cls(int(value))

        UNKNOWN = 0  # ?
        IMAGE = 170

    def setup_list(
        self,
        device: DEVICETYPE | str = DEVICETYPE.PCPARD,
        filetype: FILETYPE | str = FILETYPE.UNKNOWN,
        path: str = "/root"
    ) -> GeoComResponse:
        _device = toenum(self.DEVICETYPE, device)
        _filetype = toenum(self.FILETYPE, filetype)
        return self._request(
            23306,
            [_device.value, _filetype.value, path]
        )

    def list(
        self,
        next: bool = False
    ) -> GeoComResponse:
        response = self._request(
            23307,
            [next],
            {
                "last": bool,
                "filename": parsestr,
                "size": int,
                "hour": Byte.parse,
                "minute": Byte.parse,
                "second": Byte.parse,
                "centisec": Byte.parse,
                "day": Byte.parse,
                "month": Byte.parse,
                "year": Byte.parse
            }
        )
        time: datetime | None = None
        if (
            response.comcode
            and response.rpccode
            and response.params["filename"] != ""
        ):
            time = datetime(
                int(response.params["year"]) + 2000,
                int(response.params["month"]),
                int(response.params["day"]),
                int(response.params["hour"]),
                int(response.params["minute"]),
                int(response.params["second"]),
                int(response.params["centisec"]) * 10000
            )
        response.params = {
            "last": response.params["last"],
            "filename": response.params["filename"],
            "size": response.params["size"],
            "modified": time
        }
        return response

    def abort_list(self) -> GeoComResponse:
        return self._request(23308)

    def setup_download(
        self,
        filename: str,
        blocksize: int,
        device: DEVICETYPE | str = DEVICETYPE.PCPARD,
        filetype: FILETYPE | str = FILETYPE.UNKNOWN,
    ) -> GeoComResponse:
        _device = toenum(self.DEVICETYPE, device)
        _filetype = toenum(self.FILETYPE, filetype)
        return self._request(
            23303,
            [_device.value, _filetype.value, filename, blocksize],
            {
                "blockcount": int
            }
        )

    def download(
        self,
        block: int
    ) -> GeoComResponse:
        return self._request(
            23304,
            [block],
            {
                "value": parsestr,
                "length": int
            }
        )

    def abort_download(self) -> GeoComResponse:
        return self._request(23305)

    def delete(
        self,
        filename: str,
        time: datetime | None = None,
        device: DEVICETYPE | str = DEVICETYPE.PCPARD,
        filetype: FILETYPE | str = FILETYPE.UNKNOWN
    ) -> GeoComResponse:
        _device = toenum(self.DEVICETYPE, device)
        _filetype = toenum(self.FILETYPE, filetype)
        if time is None:
            params = [
                _device.value, _filetype.value,
                Byte(0), Byte(0), Byte(0),
                filename
            ]
        else:
            params = [
                _device.value, _filetype.value,
                Byte(time.day), Byte(time.month), Byte(time.year - 2000),
                filename
            ]
        return self._request(
            23309,
            params,
            {
                "deleted": int
            }
        )
