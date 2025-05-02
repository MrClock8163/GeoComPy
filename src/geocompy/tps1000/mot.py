"""
Description
===========

Module: ``geocompy.tps1000.mot``

Definitions for the TPS1000 Motorization subsystem.

Types
-----

- ``TPS1000MOT``

"""
from __future__ import annotations

from ..data import (
    Angle,
    toenum,
    enumparser
)
from ..data_geocom import (
    ATRLock,
    Controller,
    Stop
)
from ..protocols import (
    GeoComSubsystem,
    GeoComResponse
)


class TPS1000MOT(GeoComSubsystem):
    """
    Motorization subsystem of the TPS1000 GeoCom protocol.

    This subsystem provides access to motoriztaion parameters and control.

    """

    def read_lock_status(self) -> GeoComResponse[ATRLock]:
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
            parsers=enumparser(ATRLock)
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
        _mode = toenum(Controller, mode)
        return self._request(
            6001,
            [_mode.value]
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
        aus.set_user_lock_state

        """
        _mode = toenum(Stop, mode)
        return self._request(
            6002,
            [_mode.value]
        )

    def set_velocity(
        self,
        hz: Angle,
        v: Angle
    ) -> GeoComResponse[None]:
        """
        RPC 6004, ``MOT_SetVelocity``

        Starts the motors at a constant speed. The motor controller must
        be set accordingly in advance.

        Parameters
        ----------
        hz : Angle
            Horizontal angle to turn in a second [-0.79; +0.79]rad.
        v : Angle
            Vertical angle to turn in a second [-0.79; +0.79]rad.

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

        See Also
        --------
        set_velocity
        start_controller
        aus.set_user_lock_state

        """
        _horizontal = min(0.79, max(-0.79, float(hz)))
        _vertical = min(0.79, max(-0.79, float(v)))
        return self._request(
            6004,
            [_horizontal, _vertical]
        )
