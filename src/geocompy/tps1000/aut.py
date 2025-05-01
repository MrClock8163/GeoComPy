"""
Description
===========

Module: ``geocompy.tps1000.aut``

Definitions for the TPS1100 Automation subsystem.

Types
-----

- ``TPS1000AUT``

"""
from __future__ import annotations

from ..data import (
    Angle,
    toenum,
    enumparser,
    parsebool,
    POSITION,
    ADJUST,
    ATR
)
from ..protocols import (
    GeoComSubsystem,
    GeoComResponse
)


class TPS1000AUT(GeoComSubsystem):
    """
    Automation subsystem of the TPS1100 GeoCom protocol.

    This subsystem controls most of the motorized functions of
    a total station, such as positioning of the axes, target search,
    target lock, etc.

    """

    def get_atr_status(self) -> GeoComResponse[bool]:
        """
        RPC 9019, ``AUT_GetATRStatus``

        Gets whether or not the ATR mode is active.

        Returns
        -------
        GeoComResponse
            Params:
                - `bool`: ATR mode is active.

            Error codes:
                - ``NOT_IMPL``: ATR is not available.

        Notes
        -----
        This command does not indicate if the ATR has acquired a prism.

        See Also
        --------
        set_atr_status
        """
        return self._request(
            9019,
            parsers=parsebool
        )

    def set_atr_status(
        self,
        activate: bool
    ) -> GeoComResponse[None]:
        """
        RPC 9018, ``AUT_SetATRStatus``

        Activates or deactivates the ATR mode.

        Parameters
        ----------
        activate : bool
            Set ATR to active.

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``NOT_IMPL``: ATR is not available.

        Notes
        -----
        If LOCK mode is active when the ATR is activated, then LOCK mode
        changes to ATR mode.

        If the ATR is deactivated, the LOCK mode does not change.

        See Also
        --------
        get_atr_status
        get_lock_status
        set_lock_status
        """
        return self._request(9018, [activate])

    def get_lock_status(self) -> GeoComResponse[bool]:
        """
        RPC 9021, ``AUT_GetLockStatus``

        Gets whether or not the lock mode is active.

        Returns
        -------
        GeoComResponse
            Params:
                - `bool`: Lock mode is active.

            Error codes:
                - ``NOT_IMPL``: ATR is not available.

        See Also
        --------
        set_lock_status
        mot.read_lock_status
        """
        return self._request(
            9021,
            parsers=parsebool
        )

    def set_lock_status(
        self,
        activate: bool
    ) -> GeoComResponse[None]:
        """
        RPC 9020, ``AUT_SetLockStatus``

        Activates or deactivates the LOCK mode.

        Parameters
        ----------
        activate : bool
            LOCK state to set

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``NOT_IMPL``: ATR is not available.

        Notes
        -----
        Activating the LOCK mode does not mean that the instrument is
        automatically locked onto a prism.

        See Also
        --------
        get_lock_status
        get_atr_status
        lock_in
        """
        return self._request(
            9020,
            [activate]
        )

    def read_tol(self) -> GeoComResponse[tuple[Angle, Angle]]:
        """
        RPC 9008, ``AUT_ReadTol``

        Gets the positioning tolerances on the Hz and V axes.

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``NA``: GeoCom Robotic license not found.

            Params:
                - `Angle`: Horizontal tolerance.
                - `Angle`: Vertical tolerance.

        See Also
        --------
        set_tol
        """
        return self._request(
            9008,
            parsers=(Angle.parse, Angle.parse)
        )

    def set_tol(
        self,
        hz: Angle,
        v: Angle
    ) -> GeoComResponse[None]:
        """
        RPC 9007, ``AUT_SetTol``

        Sets the positioning tolerances on the Hz and V axes.

        Parameters
        ----------
        hz : Angle
            Horizontal tolerance.
        v : Angle
            Vertical tolerance.

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``NA``: GeoCom Robotic license not found.
                - ``IVPARAM``: Tolerances are out of the valid range.
                - ``MOT_UNREADY``: Instrument has no motorization.

        See Also
        --------
        read_tol
        """
        return self._request(9007, [hz, v])

    def read_timeout(self) -> GeoComResponse[tuple[float, float]]:
        """
        RPC 9012, ``AUT_ReadTimeout``

        Gets the positioning timeout for the Hz and V axes.

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``NA``: GeoCom Robotic license not found.

            Params:
                - `float`: Horizontal timeout [sec].
                - `float`: Vertical timeout [sec].

        See Also
        --------
        set_timeout
        """
        return self._request(
            9012,
            parsers=(float, float)
        )

    def set_timeout(
        self,
        hz: float,
        v: float
    ) -> GeoComResponse[None]:
        """
        RPC 9011, ``AUT_SetTimeout``

        Sets the positioning timeout for the Hz and V axes.

        Parameters
        ----------
        hz : float
            Horizontal timeout [sec].
        v : float
            Vertical timeout [sec]

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``NA``: GeoCom Robotic license not found.
                - ``IVPARAM``: Timeout values are not in the [7; 60] range.

        See Also
        --------
        read_timeout
        """
        return self._request(
            9011,
            [hz, v]
        )

    def make_positioning(
        self,
        hz: Angle,
        v: Angle,
        posmode: POSITION | str = POSITION.NORMAL,
        atrmode: ATR | str = ATR.POSITION
    ) -> GeoComResponse[None]:
        """
        RPC 9027, ``AUT_MakePositioning``

        Turns the telescope to the specified angular positions.

        Parameters
        ----------
        hz : Angle
            Horizontal position.
        v : Angle
            Vertical position.
        posmode : POSITION | str, optional
            Positioning precision mode, by default POSITION.NORMAL
        atrmode : ATR | str, optional
            ATR mode, by default ATR.POSITION

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``IVPARAM``: Invalid parameter
                - ``AUT_TIMEOUT``: Positioning timed out.
                - ``AUT_MOTOR_ERROR``: Instrument has no motorization.
                - ``AUT_ANGLE_ERROR``: Angle measurement error.
                - ``AUT_INACC``: Inexact position.
                - ``ABORT``: Function aborted.
                - ``COM_TIMEDOUT``: Communication timeout.
                - ``AUT_NO_TARGET``: No ATR target found.
                - ``AUT_MULTIPLE_TARGETS``: Multiple ATR targets found.
                - ``AUT_BAD_ENVIRONMENT``: Inadequate environmental
                  conditions.
                - ``AUT_ACCURACY``: Position is not within tolerances.
                  Repeat positioning!
                - ``AUT_DEV_ERROR``: Angle deviation calculation error.
                  Repeat positioning!
                - ``AUT_NOT_ENABLED``: ATR mode is not active.

        See Also
        --------
        get_atr_status
        set_atr_status
        get_lock_status
        set_lock_status
        read_tol
        set_tol
        read_timeout
        set_timeout
        com.get_timeout
        com.set_timeout
        """
        _posmode = toenum(POSITION, posmode)
        _atrmode = toenum(ATR, atrmode)
        return self._request(
            9027,
            [hz, v, _posmode.value, _atrmode.value, 0]
        )

    def change_face(
        self,
        posmode: POSITION | str = POSITION.NORMAL,
        atrmode: ATR | str = ATR.POSITION
    ) -> GeoComResponse[None]:
        """
        RPC 9028, ``AUT_ChangeFace``

        Turns the telescope to the opposite face.

        Parameters
        ----------
        posmode : POSITION | str, optional
            Positioning precision mode, by default POSITION.NORMAL
        atrmode : ATR | str, optional
            ATR mode, by default ATR.POSITION

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``IVPARAM``: Invalid parameter
                - ``AUT_TIMEOUT``: Positioning timed out.
                - ``AUT_MOTOR_ERROR``: Instrument has no motorization.
                - ``AUT_ANGLE_ERROR``: Angle measurement error.
                - ``AUT_INACC``: Inexact position.
                - ``ABORT``: Function aborted.
                - ``COM_TIMEDOUT``: Communication timeout.
                - ``AUT_NO_TARGET``: No ATR target found.
                - ``AUT_MULTIPLE_TARGETS``: Multiple ATR targets found.
                - ``AUT_BAD_ENVIRONMENT``: Inadequate environmental
                  conditions.
                - ``AUT_ACCURACY``: Position is not within tolerances.
                  Repeat positioning!
                - ``AUT_DEV_ERROR``: Angle deviation calculation error.
                  Repeat positioning!
                - ``AUT_NOT_ENABLED``: ATR mode is not active.

        See Also
        --------
        get_atr_status
        set_atr_status
        get_lock_status
        set_lock_status
        read_tol
        set_tol
        read_timeout
        set_timeout
        com.get_timeout
        com.set_timeout
        tmc.get_face
        """
        _posmode = toenum(POSITION, posmode)
        _atrmode = toenum(ATR, atrmode)
        return self._request(
            9028,
            [_posmode.value, _atrmode.value, 0]
        )

    def fine_adjust(
        self,
        width: Angle,
        height: Angle
    ) -> GeoComResponse[None]:
        """
        RPC 9037, ``AUT_FineAdjust``

        Precisely targets a prism. If the prism is not within the view of
        the ATR, a target search is executed in the specified window.

        Parameters
        ----------
        width : Angle
            Width of target search window.
        height : Angle
            Heigth of target search window.

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``NA``: GeoCom Robotic license not found.
                - ``IVPARAM``: Invalid parameter
                - ``AUT_TIMEOUT``: Positioning timed out.
                - ``AUT_MOTOR_ERROR``: Instrument has no motorization.
                - ``FATAL``: Fatal error.
                - ``ABORT``: Function aborted.
                - ``COM_TIMEDOUT``: Communication timeout.
                - ``AUT_NO_TARGET``: No ATR target found.
                - ``AUT_MULTIPLE_TARGETS``: Multiple ATR targets found.
                - ``AUT_BAD_ENVIRONMENT``: Inadequate environmental
                  conditions.
                - ``AUT_DEV_ERROR``: Angle deviation calculation error.
                  Repeat positioning!
                - ``AUT_NOT_ENABLED``: ATR mode is not active.
                - ``AUT_DETECTOR_ERROR``: Error in target acquisition.

        See Also
        --------
        get_atr_status
        set_atr_status
        get_fine_adjust_mode
        set_fine_adjust_mode
        """
        return self._request(
            9037,
            [width, height, 0]
        )

    def search(
        self,
        width: Angle,
        height: Angle
    ) -> GeoComResponse[None]:
        """
        RPC 9029, ``AUT_Search``

        Search for target in the specified search window. The search is
        terminated once a prism appears in the view of the ATR. Fine
        adjustment must be executed afterwards.

        Parameters
        ----------
        width : Angle
            Width of target search window.
        height : Angle
            Heigth of target search window.

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``IVPARAM``: Invalid parameter
                - ``AUT_MOTOR_ERROR``: Instrument has no motorization.
                - ``TMC_NO_FULL_CORRECTION``: Instrument might not be
                  properly levelled.
                - ``FATAL``: Fatal error.
                - ``ABORT``: Function aborted.
                - ``COM_TIMEDOUT``: Communication timeout.
                - ``AUT_NO_TARGET``: No ATR target found.
                - ``AUT_BAD_ENVIRONMENT``: Inadequate environmental
                  conditions.
                - ``AUT_NOT_ENABLED``: ATR mode is not active.
                - ``AUT_DETECTOR_ERROR``: Error in target acquisition.

        See Also
        --------
        get_atr_status
        set_atr_status
        fine_adjust
        """
        return self._request(
            9029,
            [width, height, 0]
        )

    def get_fine_adjust_mode(self) -> GeoComResponse[ADJUST]:
        """
        RPC 9030, ``AUT_GetFineAdjustMode``

        Gets the fine adjustment mode.

        Returns
        -------
        GeoComResponse
            Params:
                - `ADJUST`: Current fine adjustment mode.

        See Also
        --------
        set_fine_adjust_mode
        """
        return self._request(
            9030,
            parsers=enumparser(ADJUST)
        )

    def set_fine_adjust_mode(
        self,
        mode: ADJUST | str
    ) -> GeoComResponse[None]:
        """
        RPC 9031, ``AUT_SetFineAdjustMode``

        Sets the fine adjustment mode.

        Parameters
        ----------
        mode : ADJUST | str

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``NA``: GeoCom Robotic license not found.
                - ``IVPARAM``: Invalid mode

        See Also
        --------
        get_fine_adjust_mode
        """
        _mode = toenum(ADJUST, mode)
        return self._request(
            9031,
            [_mode.value]
        )

    def lock_in(self) -> GeoComResponse[None]:
        """
        RPC 9013, ``AUT_LockIn``

        Locks onto target prism and starts tracking. LOCK mode must be
        active, and fine adjustment must have been completed, before
        executing this command.

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``AUT_NOT_ENABLED``: ATR mode is not active.
                - ``AUT_MOTOR_ERROR``: Instrument has not motorization.
                - ``AUT_DETECTOR_ERROR``: Error in target acquisition.
                - ``AUT_NO_TARGET``: No ATR target found.
                - ``AUT_BAD_ENVIRONMENT``: Inadequate environmental
                  conditions.

        See Also
        --------
        get_lock_status
        set_lock_status
        mot.read_lock_status
        """
        return self._request(9013)
