"""
Description
===========

Module: ``geocompy.geo.mot``

Definitions for the GeoCOM Motorization subsystem.

Types
-----

- ``GeoComMOT``

"""
from __future__ import annotations

from math import pi
from typing import SupportsFloat

from ..data import (
    get_enum,
    get_enum_parser
)
from .gcdata import (
    ATRLock,
    Controller,
    Stop
)
from .gctypes import (
    GeoComSubsystem,
    GeoComResponse
)


class GeoComMOT(GeoComSubsystem):
    """
    Motorization subsystem of the GeoCOM protocol.

    This subsystem provides access to motoriztaion parameters and control.

    """

    def get_lockon_status(self) -> GeoComResponse[ATRLock]:
        """
        RPC 6021, ``MOT_ReadLockStatus``

        Gets the current status of the ATR target lock.

        Returns
        -------
        GeoComResponse
            Params:
                - `ATRLock`: ATR lock status.

            Error codes:
                - ``NOT_IMPL``: Motorization not available.

        See Also
        --------
        aut.lock_in

        """
        return self._request(
            6021,
            parsers=get_enum_parser(ATRLock)
        )

    def start_controller(
        self,
        mode: Controller | str = Controller.MANUAL
    ) -> GeoComResponse[None]:
        """
        RPC 6001, ``MOT_StartController``

        Starts the motor controller in the specified mode.

        Parameters
        ----------
        mode : Controller | str, optional
            Controller mode, by default Controller.MANUAL

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``IVPARAM``: Control mode is not appropriate for velocity
                  control.
                - ``NOT_IMPL``: Motorization not available.
                - ``MOT_BUSY``: Subsystem is busy, controller already
                  started.
                - ``MOT_UNREADY``: Subsystem is not initialized.

        See Also
        --------
        set_velocity
        stop_controller

        """
        _mode = get_enum(Controller, mode)
        return self._request(
            6001,
            [_mode]
        )

    def stop_controller(
        self,
        mode: Stop | str = Stop.NORMAL
    ) -> GeoComResponse[None]:
        """
        RPC 6002, ``MOT_StopController``

        Stops the active motor controller mode.

        Parameters
        ----------
        mode : Stop | str, optional
            Controller mode, by default Stop.NORMAL

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``MOT_NOT_BUSY``: Controller is not active.

        See Also
        --------
        set_velocity
        start_controller
        aus.switch_user_lock

        """
        _mode = get_enum(Stop, mode)
        return self._request(
            6002,
            [_mode]
        )

    def set_velocity(
        self,
        hz: SupportsFloat,
        v: SupportsFloat
    ) -> GeoComResponse[None]:
        """
        RPC 6004, ``MOT_SetVelocity``

        Starts the motors at a constant speed. The motor controller must
        be set accordingly in advance.

        Parameters
        ----------
        hz : SupportsFloat
            Horizontal angle to turn in a second [-pi; +pi]rad.
        v : SupportsFloat
            Vertical angle to turn in a second [-pi; +pi]rad.

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``IVPARAM``: Velocities not within acceptable range.
                - ``MOT_NOT_CONFIG``: Motor controller was not started,
                  or is already busy with continuous task.
                - ``MOT_NOT_OCOST``: Controller is not set to constant
                  speed.
                - ``NOT_IMPL``: Motorization is not available.

        Note
        ----
        Instruments with piezo motors support velocities up to 180 deg/sec.
        Stations with traditional motor drives support velocoties up to
        45 deg/sec.

        See Also
        --------
        set_velocity
        start_controller
        aus.switch_user_lock

        """
        _horizontal = min(pi, max(-pi, float(hz)))
        _vertical = min(pi, max(-pi, float(v)))
        return self._request(
            6004,
            [_horizontal, _vertical]
        )
