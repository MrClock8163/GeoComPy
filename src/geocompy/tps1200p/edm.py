from __future__ import annotations

from enum import Enum

from .. import (
    GeoComSubsystem,
    GeoComResponse
)
from ..communication import toenum


class TPS1200PEDM(GeoComSubsystem):
    class ONOFF(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PEDM.ONOFF:
            return cls(int(value))

        OFF = 0
        ON = 1

    class EGLINTENSITYTYPE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PEDM.EGLINTENSITYTYPE:
            return cls(int(value))

        OFF = 0
        LOW = 1
        MID = 2
        HIGH = 3

    def laserpointer(
        self,
        laser: ONOFF | str
    ) -> GeoComResponse:
        _laser = toenum(self.ONOFF, laser)
        return self._request(
            1004,
            [_laser.value]
        )

    def get_egl_intensity(self) -> GeoComResponse:
        return self._request(
            1058,
            parsers={
                "intensity": self.EGLINTENSITYTYPE.parse
            }
        )

    def set_egl_intensity(
        self,
        intensity: EGLINTENSITYTYPE | str
    ) -> GeoComResponse:
        _intesity = toenum(self.EGLINTENSITYTYPE, intensity)
        return self._request(
            1059,
            [_intesity.value]
        )
