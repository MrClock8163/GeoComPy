from __future__ import annotations

from .. import GeoComResponse
from ..tps1200p.tmc import TPS1200PTMC


class VivaTPSTMC(TPS1200PTMC):
    def set_prism_corr(
        self,
        const: float
    ) -> GeoComResponse:
        return self._request(
            2024,
            [const]
        )
