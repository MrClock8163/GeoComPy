from __future__ import annotations

from .. import GeoComResponse
from ..tps1200p.sup import TPS1200PSUP


class VivaTPSSUP(TPS1200PSUP):
    def set_power_fail_autorestart(
        self,
        autorestart: bool
    ) -> GeoComResponse:
        return self._request(
            14006,
            [autorestart]
        )
