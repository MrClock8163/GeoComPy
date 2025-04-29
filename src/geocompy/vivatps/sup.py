"""
Description
===========

Module: ``geocompy.vivatps.sup``

Definitions for the VivaTPS Supervisor subsystem.

Types
-----

- ``VivaTPSSUP``

"""
from __future__ import annotations

from ..protocols import GeoComResponse
from ..tps1200p.sup import TPS1200PSUP


class VivaTPSSUP(TPS1200PSUP):
    """
    Supervisor subsystem of the VivaTPS GeoCom protocol.

    This subsystem controls the continuous operation of the system, and it
    allows to automatically display status information.

    """

    def set_power_fail_autorestart(
        self,
        autorestart: bool
    ) -> GeoComResponse[None]:
        """
        RPC 14006, ``SUP_SetPowerFailAutoRestart``

        Configure the instrument to automatically restard if power is
        restored after an irregular shutdown.

        Parameters
        ----------
        autorestart : bool
            Enable automatic restart.

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``NA``: Command not available.

        """
        return self._request(
            14006,
            [autorestart]
        )
