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

from ..data import (
    toenum,
    parsebool
)
from ..data_geocom import Camera
from ..protocols import GeoComResponse
from ..tps1200p.aut import TPS1200PAUT


class VivaTPSAUT(TPS1200PAUT):
    """
    Automation subsystem of the VivaTPS GeoCom protocol.

    This subsystem controls most of the motorized functions of
    a total station, such as positioning of the axes, target search,
    target lock, etc.

    """

    def switch_lock_onthefly(
        self,
        enabled: bool
    ) -> GeoComResponse[None]:
        """
        RPC 9103, ``AUT_SetLockFlyMode``

        Sets the state of on-the-fly mode for the lock mode.

        Parameters
        ----------
        enabled : bool
            Enable on-the-fly lock mode.

        Returns
        -------
        GeoComResponse

        See Also
        --------
        get_lock_onthefly_status
        """
        return self._request(
            9103,
            [enabled]
        )

    def get_lock_onthefly_status(self) -> GeoComResponse[bool]:
        """
        RPC 9102, ``AUT_GetLockFlyMode``

        Gets the current state of the on-the-fly lock mode.

        Returns
        -------
        GeoComResponse
            Params:
                - `bool`: On-the-fly lock mode is enabled.

        See Also
        --------
        get_lock_onthefly_status
        """
        return self._request(
            9102,
            parsers=parsebool
        )

    def aim_at_pixel(
        self,
        x: int,
        y: int,
        camera: Camera | str = Camera.OVERVIEW
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
        camera : Camera, optional
            Camera device, by default OVERVIEW

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``NA``: Imaging license not found.
                - ``AUT_SIDECOVER_ERR``: Sidecover is open.

        """
        _camera = toenum(Camera, camera)
        return self._request(
            9081,
            [_camera.value, x, y]
        )
