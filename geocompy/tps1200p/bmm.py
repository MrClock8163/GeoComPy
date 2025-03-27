from __future__ import annotations

from .. import (
    GeoComSubsystem,
    GeoComResponse
)


class TPS1200PBMM(GeoComSubsystem):
    def beep_alarm(self) -> GeoComResponse:
        return self._request(11004)

    def beep_normal(self) -> GeoComResponse:
        return self._request(11003)

    def beep_on(
        self,
        intensity: int
    ) -> GeoComResponse:
        return self._request(
            20001,
            [intensity]
        )

    def beep_off(self) -> GeoComResponse:
        return self._request(20000)
