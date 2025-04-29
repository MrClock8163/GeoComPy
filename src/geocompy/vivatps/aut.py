"""
Description
===========

Module: ``geocompy.vivatps.aut``

Definitions for the VivaTPS Automation subsystem.

Types
-----

- ``VivaTPSAUT``

"""
from __future__ import annotations

from enum import Enum

from ..data import (
    toenum,
    enumparser
)
from ..protocols import (
    GeoComResponse
)
from ..tps1200p.aut import TPS1200PAUT
from .cam import VivaTPSCAM


class VivaTPSAUT(TPS1200PAUT):
    """
    Automation subsystem of the VivaTPS GeoCom protocol.

    This subsystem controls most of the motorized functions of
    a total station, such as positioning of the axes, target search,
    target lock, etc.

    """
    class ONOFF(Enum):
        OFF = 0
        ON = 1

    def set_lock_fly_mode(
        self,
        state: ONOFF | str
    ) -> GeoComResponse[None]:
        """
        RPC 9103, ``AUT_SetLockFlyMode``

        Sets the state of the fly mode for the lock mode.

        Parameters
        ----------
        state : ONOFF | str
            New state to set for fly mode.

        Returns
        -------
        GeoComResponse

        See Also
        --------
        get_lock_fly_mode
        """
        _state = toenum(self.ONOFF, state)
        return self._request(
            9103,
            [_state.value]
        )

    def get_lock_fly_mode(self) -> GeoComResponse[ONOFF]:
        """
        RPC 9102, ``AUT_GetLockFlyMode``

        Gets the current state of the fly mode for the lock mode.

        Returns
        -------
        GeoComResponse
            Params:
                - `ONOFF`: Current state of the fly mode.

        See Also
        --------
        get_lock_fly_mode
        """
        return self._request(
            9102,
            parsers=enumparser(self.ONOFF)
        )

    def cam_posit_to_pixel_coord(
        self,
        x: int,
        y: int,
        camtype: VivaTPSCAM.CAMTYPE | str = VivaTPSCAM.CAMTYPE.OVC
    ) -> GeoComResponse[None]:
        """
        RPC 9081, ``AUT_CAM_PositToPixelCoord``

        Turns the instrument to face the coordinates specified in the
        image coordinates.

        Parameters
        ----------
        x : int
            Horizontal pixel coordinate.
        y : int
            Vertical pixel coordinate.
        camtype : ~VivaTPSCAM.CAMTYPE, optional
            Camera device, by default CAMTYPE.OVC

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``NA``: Imaging license not found.
                - ``AUT_SIDECOVER_ERR``: Sidecover is open.

        """
        _camtype = toenum(VivaTPSCAM.CAMTYPE, camtype)
        return self._request(
            9081,
            [_camtype.value, x, y]
        )
