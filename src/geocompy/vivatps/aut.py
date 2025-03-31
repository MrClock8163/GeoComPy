"""
``geocompy.vivatps.aut``
=========================

Definitions for the VivaTPS Automation subsystem.

Types
-----

- ``VivaTPSAUT``

"""
from __future__ import annotations

from enum import Enum

from .. import (
    GeoComResponse
)
from ..data import toenum
from .cam import VivaTPSCAM
from ..tps1200p.aut import TPS1200PAUT


class VivaTPSAUT(TPS1200PAUT):
    """
    Automation subsystem of the VivaTPS GeoCom protocol.

    This subsystem controls most of the motorized functions of
    a total station, such as positioning of the axes, target search,
    target lock, etc.

    """
    class ONOFF(Enum):
        @classmethod
        def parse(cls, value: str) -> VivaTPSAUT.ONOFF:
            """
            Parses enum member from serialized enum value.

            Parameters
            ----------
            value : str
                Serialized enum value.

            Returns
            -------
            ~VivaTPSAUT.ONOFF
                Parsed enum member.
            """
            return cls(int(value))

        OFF = 0
        ON = 1
    
    def set_lock_fly_mode(
        self,
        state: ONOFF | str
    ) -> GeoComResponse:
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
    
    def get_lock_fly_mode(self) -> GeoComResponse:
        """
        RPC 9102, ``AUT_GetLockFlyMode``

        Gets the current state of the fly mode for the lock mode.

        Returns
        -------
        GeoComResponse
            - Params:
                - **state** (`ONOFF`): Current state of the fly mode.

        See Also
        --------
        get_lock_fly_mode
        """
        return self._request(
            9102,
            parsers={
                "state": self.ONOFF.parse
            }
        )
    
    def cam_posit_to_pixel_coord(
        self,
        x: int,
        y: int,
        camtype: VivaTPSCAM.CAMTYPE | str = VivaTPSCAM.CAMTYPE.OVC
    ) -> GeoComResponse:
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
            - Error codes:
                - ``NA``: Imaging license not found.
                - ``AUT_SIDECOVER_ERR``: Sidecover is open.

        """
        _camtype = toenum(VivaTPSCAM.CAMTYPE, camtype)
        return self._request(
            9081,
            [_camtype.value, x, y]
        )
