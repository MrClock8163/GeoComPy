"""
``geocompy.tps1200p.aut``
=========================

Definitions for the TPS1200+ Automation subsystem.

Types
-----

- ``TPS1200PAUT``

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


class TPS1200PAUT(GeoComSubsystem):
    """
    Automation subsystem of the TPS1200+ GeoCom protocol.

    This subsystem controls most of the motorized functions of
    a total station, such as positioning of the axes, target search,
    target lock, etc.

    """
    class POSMODE(Enum):
        NORMAL = 0
        PRECISE = 1
        FAST = 2  # TS30 / MS30

    class ADJMODE(Enum):
        NORMAL = 0
        POINT = 1
        DEFINE = 2

    class ATRMODE(Enum):
        POSITION = 0
        TARGET = 1

    class DIRECTION(Enum):
        CLOCKWISE = 1
        ANTICLOCKWISE = -1

    def read_tol(self) -> GeoComResponse:
        """
        RPC 9008, ``AUT_ReadTol``

        Gets the positioning tolerances on the Hz and V axes.

        Returns
        -------
        GeoComResponse
            - Error codes:
                - ``NA``: GeoCom Robotic license not found.

            - Params:
                - **hz** (`Angle`): Horizontal tolerance.
                - **v** (`Angle`): Vertical tolerance.

        See Also
        --------
        set_tol
        """
        return self._request(
            9008,
            parsers={
                "hz": Angle.parse,
                "v": Angle.parse
            }
        )

    def set_tol(
        self,
        hz: Angle,
        v: Angle
    ) -> GeoComResponse:
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
            - Error codes:
                - ``NA``: GeoCom Robotic license not found.
                - ``IVPARAM``: Tolerances are out of the valid range.
                - ``MOT_UNREADY``: Instrument has no motorization.

        See Also
        --------
        read_tol
        """
        return self._request(9007, [hz, v])

    def read_timeout(self) -> GeoComResponse:
        """
        RPC 9012, ``AUT_ReadTimeout``

        Gets the positioning timeout for the Hz and V axes.

        Returns
        -------
        GeoComResponse
            - Error codes:
                - ``NA``: GeoCom Robotic license not found.

            - Params:
                - **hz** (`float`): Horizontal timeout [sec].
                - **v** (`float`): Vertical timeout [sec].

        See Also
        --------
        set_timeout
        """
        return self._request(
            9012,
            parsers={
                "hz": float,
                "v": float
            }
        )

    def set_timeout(
        self,
        hz: float,
        v: float
    ) -> GeoComResponse:
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
            - Error codes:
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
        posmode: POSMODE | str = POSMODE.NORMAL,
        atrmode: ATRMODE | str = ATRMODE.POSITION
    ) -> GeoComResponse:
        """
        RPC 9027, ``AUT_MakePositioning``

        Turns the telescope to the specified angular positions.

        Parameters
        ----------
        hz : Angle
            Horizontal position.
        v : Angle
            Vertical position.
        posmode : POSMODE | str, optional
            Positioning precision mode, by default POSMODE.NORMAL
        atrmode : ATRMODE | str, optional
            ATR mode, by default ATRMODE.TARGET

        Returns
        -------
        GeoComResponse
            - Error codes:
                - ``NA``: GeoCom Robotic license not found.
                - ``IVPARAM``: Invalid parameter
                - ``AUT_TIMEOUT``: Positioning timed out.
                - ``AUT_MOTOR_ERROR``: Instrument has no motorization.
                - ``TMC_NO_FULL_CORRECTION``: Instrument might not be
                  properly levelled.
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
        aus.get_user_atr_state
        aus.set_user_atr_state
        aus.get_user_lock_state
        aus.set_user_lock_state
        read_tol
        set_tol
        read_timeout
        set_timeout
        com.get_timeout
        com.set_timeout
        """
        _posmode = toenum(self.POSMODE, posmode)
        _atrmode = toenum(self.ATRMODE, atrmode)
        return self._request(
            9027,
            [hz, v, _posmode.value, _atrmode.value, 0]
        )

    def change_face(
        self,
        posmode: POSMODE | str = POSMODE.NORMAL,
        atrmode: ATRMODE | str = ATRMODE.POSITION
    ) -> GeoComResponse:
        """
        RPC 9028, ``AUT_ChangeFace``

        Turns the telescope to the opposite face.

        Parameters
        ----------
        posmode : POSMODE | str, optional
            Positioning precision mode, by default POSMODE.NORMAL
        atrmode : ATRMODE | str, optional
            ATR mode, by default ATRMODE.TARGET

        Returns
        -------
        GeoComResponse
            - Error codes:
                - ``NA``: GeoCom Robotic license not found.
                - ``IVPARAM``: Invalid parameter
                - ``AUT_TIMEOUT``: Positioning timed out.
                - ``AUT_MOTOR_ERROR``: Instrument has no motorization.
                - ``TMC_NO_FULL_CORRECTION``: Instrument might not be
                  properly levelled.
                - ``FATAL``: Fatal error.
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
        aus.get_user_atr_state
        aus.set_user_atr_state
        aus.get_user_lock_state
        aus.set_user_lock_state
        read_tol
        set_tol
        read_timeout
        set_timeout
        com.get_timeout
        com.set_timeout
        tmc.get_face
        """
        _posmode = toenum(self.POSMODE, posmode)
        _atrmode = toenum(self.ATRMODE, atrmode)
        return self._request(
            9028,
            [_posmode.value, _atrmode.value, 0]
        )

    def fine_adjust(
        self,
        width: Angle,
        height: Angle
    ) -> GeoComResponse:
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
            - Error codes:
                - ``NA``: GeoCom Robotic license not found.
                - ``IVPARAM``: Invalid parameter
                - ``AUT_TIMEOUT``: Positioning timed out.
                - ``AUT_MOTOR_ERROR``: Instrument has no motorization.
                - ``TMC_NO_FULL_CORRECTION``: Instrument might not be
                  properly levelled.
                - ``FATAL``: Fatal error.
                - ``ABORT``: Function aborted.
                - ``COM_TIMEDOUT``: Communication timeout.
                - ``AUT_NO_TARGET``: No ATR target found.
                - ``AUT_MULTIPLE_TARGETS``: Multiple ATR targets found.
                - ``AUT_BAD_ENVIRONMENT``: Inadequate environmental
                  conditions.
                - ``AUT_DEV_ERROR``: Angle deviation calculation error.
                  Repeat positioning!
                - ``AUT_DETECTOR_ERROR``: Error in target acquisition.

        See Also
        --------
        aus.get_user_atr_state
        aus.set_user_atr_state
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
    ) -> GeoComResponse:
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
            - Error codes:
                - ``NA``: GeoCom Robotic license not found.
                - ``IVPARAM``: Invalid parameter
                - ``AUT_MOTOR_ERROR``: Instrument has no motorization.
                - ``TMC_NO_FULL_CORRECTION``: Instrument might not be
                  properly levelled.
                - ``FATAL``: Fatal error.
                - ``ABORT``: Function aborted.
                - ``COM_TIMEDOUT``: Communication timeout.
                - ``AUT_NO_TARGET``: No ATR target found.
                - ``AUT_MULTIPLE_TARGETS``: Multiple ATR targets found.
                - ``AUT_BAD_ENVIRONMENT``: Inadequate environmental
                  conditions.
                - ``AUT_DETECTOR_ERROR``: Error in target acquisition.

        See Also
        --------
        aus.get_user_atr_state
        aus.set_user_atr_state
        fine_adjust
        """
        return self._request(
            9029,
            [width, height, 0]
        )

    def get_fine_adjust_mode(self) -> GeoComResponse:
        """
        RPC 9030, ``AUT_GetFineAdjustMode``

        Gets the fine adjustment mode.

        Returns
        -------
        GeoComResponse
            - Params:
                - **adjmode** (`ADJMODE`): current fine adjustment mode
            - Error codes:
                - ``NA``: GeoCom Robotic license not found.

        See Also
        --------
        set_fine_adjust_mode
        """
        return self._request(
            9030,
            parsers={
                "adjmode": enumparser(self.ADJMODE)
            }
        )

    def set_fine_adjust_mode(
        self,
        adjmode: ADJMODE | str
    ) -> GeoComResponse:
        """
        RPC 9031, ``AUT_SetFineAdjustMode``

        Sets the fine adjustment mode.

        Parameters
        ----------
        adjmode : ADJMODE | str

        Returns
        -------
        GeoComResponse
            - Error codes:
                - ``NA``: GeoCom Robotic license not found.
                - ``IVPARAM``: Invalid mode

        See Also
        --------
        aus.get_fine_adjust_mode
        """
        _adjmode = toenum(self.ADJMODE, adjmode)
        return self._request(
            9031,
            [_adjmode.value]
        )

    def lock_in(self) -> GeoComResponse:
        """
        RPC 9013, ``AUT_LockIn``

        Locks onto target prism and starts tracking. LOCK mode must be
        active, and fine adjustment must have been completed, before
        executing this command.

        Returns
        -------
        GeoComResponse
            - Error codes:
                - ``NA``: GeoCom Robotic license not found.
                - ``AUT_MOTOR_ERROR``: Instrument has not motorization.
                - ``AUT_DETECTOR_ERROR``: Error in target acquisition.
                - ``AUT_NO_TARGET``: No ATR target found.
                - ``AUT_BAD_ENVIRONMENT``: Inadequate environmental
                  conditions.
                - ``ATA_STRANGE_LIGHT``: No target detected, fine
                  adjustment was not performed.

        See Also
        --------
        aus.get_user_lock_state
        aus.set_user_lock_state
        mot.read_lock_status
        """
        return self._request(9013)

    def get_search_area(self) -> GeoComResponse:
        """
        RPC 9042, ``AUT_GetSearchArea``

        Gets current position and size of the PowerSearch window.

        Returns
        -------
        GeoComResponse
            - Params:
                - **hz** (`Angle`): Horizontal center of window.
                - **v** (`Angle`): Vertical center of window.
                - **width** (`Angle`): Width of window.
                - **height** (`Angle`): Height of window.
                - **enabled** (`bool`): If window is enabled.
            - Error codes:
                - ``NA``: GeoCom Robotic license not found.

        See Also
        --------
        set_search_area
        bap.search_target
        """
        return self._request(
            9042,
            parsers={
                "hz": Angle.parse,
                "v": Angle.parse,
                "width": Angle.parse,
                "height": Angle.parse,
                "enabled": bool
            }
        )

    def set_search_area(
        self,
        hz: Angle,
        v: Angle,
        width: Angle,
        height: Angle,
        enabled: bool = True
    ) -> GeoComResponse:
        """
        RPC 9043, ``AUT_SetSearchArea``

        Sets position and size of the PowerSearch window.

        Parameters
        ----------
        hz : Angle
            Horizontal center of search window.
        v : Angle
            Vertical center of search window.
        width : Angle
            Width of search window.
        height : Angle
            Height of search window.
        enabled : bool
            Activation state of search window.

        Returns
        -------
        GeoComResponse
            - Error codes:
                - ``NA``: GeoCom Robotic license not found.

        See Also
        --------
        get_search_area
        bap.search_target
        """
        return self._request(
            9043,
            [hz, v, width, height, enabled]
        )

    def get_user_spiral(self) -> GeoComResponse:
        """
        RPC 9040, ``AUT_GetUserSpiral``

        Gets the size of the PowerSearch window.

        Returns
        -------
        GeoComResponse
            - Params:
                - **width** (`Angle`): Width of window.
                - **height** (`Angle`): Height of window.
            - Error codes:
                - ``NA``: GeoCom Robotic license not found.

        See Also
        --------
        set_user_spiral
        bap.search_target
        """
        return self._request(
            9040,
            parsers={
                "width": Angle.parse,
                "height": Angle.parse
            }
        )

    def set_user_spiral(
        self,
        width: Angle,
        height: Angle
    ) -> GeoComResponse:
        """
        RPC 9041, ``AUT_SetUserSpiral``

        Sets the size of the PowerSearch window.

        Parameters
        ----------
        width : Angle
            Width of the search window.
        height : Angle
            Height of the search window.

        Returns
        -------
        GeoComResponse
            - Error codes:
                - ``NA``: GeoCom Robotic license not found.

        See Also
        --------
        get_user_spiral
        bap.search_target
        """
        return self._request(
            9041,
            [width, height]
        )

    def ps_enable_range(
        self,
        enable: bool
    ) -> GeoComResponse:
        """
        RPC 9048, ``AUT_PS_EnableRange``

        Enables or disables the PowerSearch window and range limit.

        Parameters
        ----------
        enable : bool
            Enable predefined PowerSearch window and range limits.
            Defaults to [0; 400] range when disabled.

        Returns
        -------
        GeoComResponse
            - Error codes:
                - ``NA``: GeoCom Robotic license not found.

        See Also
        --------
        ps_set_range
        set_search_area
        """
        return self._request(
            9048,
            [enable]
        )

    def ps_set_range(
        self,
        closest: int,
        farthest: int
    ) -> GeoComResponse:
        """
        RPC 9044, ``AUT_PS_SetRange``

        Sets the PowerSearch range limits.

        Parameters
        ----------
        closest : int
            Minimum distance to prism [0; ...].
        farthest : int
            Maxmimum distance to prism [closest + 10; 400].

        Returns
        -------
        GeoComResponse
            - Error codes:
                - ``NA``: GeoCom Robotic license not found.
                - ``IVPARAM``: Invalid parameters.

        See Also
        --------
        ps_enable_range
        ps_search_window
        set_search_area
        """
        return self._request(
            9047,
            [closest, farthest]
        )

    def ps_search_window(self) -> GeoComResponse:
        """
        RPC 9052, ``AUT_PS_SearchWindow``

        Executes PowerSearch in the predefined search window.

        Returns
        -------
        GeoComResponse
            - Error codes:
                - ``NA``: GeoCom Robotic license not found.
                - ``AUT_NO_WORKING_AREA``: Search window is not defined.
                - ``AUT_NO_TARGET``: Target was not found.

        See Also
        --------
        ps_enable_range
        ps_set_range
        ps_search_next
        set_search_area
        """
        return self._request(9052)

    def ps_search_next(
        self,
        direction: DIRECTION | str,
        swing: bool
    ) -> GeoComResponse:
        """
        RPC 9051, ``AUT_PS_SearchNext``

        Executes 360° default PowerSearch to find the next target.

        Parameters
        ----------
        direction : DIRECTION | str
            Turning direction during PowerSearch.
        swing : bool
            Search starts -10 GON to the given turn direction.

        Returns
        -------
        GeoComResponse
            - Error codes:
                - ``NA``: GeoCom Robotic license not found.
                - ``AUT_NO_TARGET``: Target was not found.
                - ``IVPARAM``: Invalid parameters.

        See Also
        --------
        ps_enable_range
        ps_search_window
        """
        _direction = toenum(self.DIRECTION, direction)
        return self._request(
            9051,
            [_direction.value, swing]
        )
