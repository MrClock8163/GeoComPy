"""
Description
===========

Module: ``geocompy.tps1200p.mot``

Definitions for the TPS1200+ Motorization subsystem.

Types
-----

- ``TPS1200PMOT``

"""
from __future__ import annotations

from enum import Enum

from ..data import (
    Angle,
    toenum,
    enumparser
)
from ..protocols import (
    GeoComSubsystem,
    GeoComResponse
)


class TPS1200PMOT(GeoComSubsystem):
    """
    Motorization subsystem of the TPS1200+ GeoCom protocol.

    This subsystem provides access to motoriztaion parameters and control.

    """
    class LOCKSTATUS(Enum):
        LOCKEDOUT = 0
        LOCKEDIN = 1
        PREDICTION = 2

    class STOPMODE(Enum):
        NORMAL = 0  # : Slow down with current acceleration.
        SHUTDOWN = 1  # : Slow down by motor power termination.

    class MODE(Enum):
        POSIT = 0  # : Relative positioning.
        OCONST = 1  # : Constant speed.
        MANUPOS = 2  # : Manual positioning.
        LOCK = 3  # : Lock-in controller.
        BREAK = 4  # : Break controller.
        # 5, 6 do not use (why?)
        TERM = 7  # : Terminate current task.

    def read_lock_status(self) -> GeoComResponse[LOCKSTATUS]:
        """
        RPC 23400, ``IMG_GetTccConfig``

        Gets the current status of the ATR target lock.

        Returns
        -------
        GeoComResponse
            - Params:
                - **status** (`LOCKSTATUS`): ATR lock status.
            - Error codes:
                - ``NOT_IMPL``: Motorization not available.

        See Also
        --------
        aut.lock_in

        """
        return self._request(
            6021,
            parsers=enumparser(self.LOCKSTATUS)
        )

    def start_controller(
        self,
        mode: MODE | str = MODE.MANUPOS
    ) -> GeoComResponse[None]:
        """
        RPC 6001, ``MOT_StartController``

        Starts the motor controller in the specified mode.

        Parameters
        ----------
        mode : MODE | str, optional
            Controller mode, by default MANUPOS

        Returns
        -------
        GeoComResponse
            - Error codes:
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
        _mode = toenum(self.MODE, mode)
        return self._request(
            6001,
            [_mode.value]
        )

    def stop_controller(
        self,
        mode: STOPMODE | str = STOPMODE.NORMAL
    ) -> GeoComResponse[None]:
        """
        RPC 6002, ``MOT_StopController``

        Stops the active motor controller mode.

        Parameters
        ----------
        mode : MODE | str, optional
            Controller mode, by default MANUPOS

        Returns
        -------
        GeoComResponse
            - Error codes:
                - ``MOT_NOT_BUSY``: Controller is not active.

        See Also
        --------
        set_velocity
        start_controller
        aus.set_user_lock_state

        """
        _mode = toenum(TPS1200PMOT.STOPMODE, mode)
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
            - Error codes:
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
