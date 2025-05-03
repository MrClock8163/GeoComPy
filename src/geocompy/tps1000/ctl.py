"""
Description
===========

Module: ``geocompy.tps1000.ctl``

Definitions for the TPS1000 Control task subsystem.

Types
-----

- ``TPS1000CTL``

"""
from __future__ import annotations

from ..protocols import (
    GeoComSubsystem,
    GeoComResponse
)


class TPS1000CTL(GeoComSubsystem):
    """
    Control task subsystem of the TPS1000 GeoCom protocol.
    """

    def get_wakeup_counter(self) -> GeoComResponse[tuple[int, int]]:
        """
        RPC 12003, ``CTL_GetUpCounter``

        Retrieves how many times has the instrument been switched on, or
        awakened from sleep mode.

        Returns
        -------
        GeoComResponse
            Params:
                - `int`: Switch on count.
                - `int`: Wake up count.

        Note
        ----
        The counters are reset to zero, once the command is executed.

        See Also
        --------
        com.switch_off
        """
        return self._request(
            12003,
            parsers=(
                int,
                int
            )
        )
