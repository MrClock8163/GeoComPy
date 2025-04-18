"""
``geocompy.vivatps.kdm``
=========================

Definitions for the VivaTPS Keyboard display unit subsystem.

Types
-----

- ``VivaTPSKDM``

"""
from __future__ import annotations

from .. import (
    GeoComSubsystem,
    GeoComResponse
)


class VivaTPSKDM(GeoComSubsystem):
    """
    Keyboard display unit subsystem of the VivaTPS GeoCom protocol.

    This subsystem controls the keyboard and display functions.

    """

    def set_lcd_power(
        self,
        alwayson: bool
    ) -> GeoComResponse:
        """
        RPC 23107, ``KDM_SetLcdPower``

        Sets the status of the diplay power.

        Parameters
        ----------
        alwayson : bool
            Keep display turned on, do not go into screensaver mode.

        Returns
        -------
        GeoComResponse

        """
        return self._request(
            23107,
            [alwayson]
        )

    def get_lcd_power(self) -> GeoComResponse:
        """
        RPC 23108, ``KDM_GetLcdPower``

        Gets the current status of the diplay power.

        Returns
        -------
        GeoComResponse
            - Params:
                - **alwayson** (`bool`): Keep display turned on, do not go
                  into screensaver mode.

        """
        return self._request(
            23108,
            parsers={
                "alwayson": bool
            }
        )
