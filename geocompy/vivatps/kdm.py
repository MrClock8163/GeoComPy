from __future__ import annotations

from .. import (
    GeoComSubsystem,
    GeoComResponse
)


class VivaTPSKDM(GeoComSubsystem):    
    def set_lcd_power(
        self,
        alwayson: bool
    ) -> GeoComResponse:
        return self._request(
            23107,
            [alwayson]
        )
    
    def get_lcd_power(self) -> GeoComResponse:
        return self._request(
            23108,
            parsers={
                "alwayson": bool
            }
        )
