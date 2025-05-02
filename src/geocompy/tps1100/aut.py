"""
Description
===========

Module: ``geocompy.tps1100.aut``

Definitions for the TPS1100 Automation subsystem.

Types
-----

- ``TPS1100AUT``

"""
from __future__ import annotations

from typing_extensions import deprecated

from ..data import (
    Angle,
    parsebool
)
from ..protocols import GeoComResponse
from ..tps1000.aut import TPS1000AUT


class TPS1100AUT(TPS1000AUT):
    """
    Automation subsystem of the TPS1100 GeoCom protocol.

    This subsystem controls most of the motorized functions of
    a total station, such as positioning of the axes, target search,
    target lock, etc.

    """
    @deprecated(
        "The 'AUT_GetATRStatus' command was superseded by "
        "'AUS_GetUserAtrState' in v1.04 of TPS1100 GeoCom. Use the new "
        "command on instruments, that support it!"
    )
    def get_atr_status(self) -> GeoComResponse[bool]:
        """
        RPC 9019, ``AUT_GetATRStatus``

        .. deprecated:: GeoCom-TPS1100-1.04
            The command is still available, but should not be used with
            instruments that support the new `aus.get_user_atr_state`
            command.

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
        return super().get_atr_status()

    @deprecated(
        "The 'AUT_SetATRStatus' command was superseded by "
        "'AUS_SetUserAtrState' in v1.04 of TPS1100 GeoCom. Use the new "
        "command on instruments, that support it!"
    )
    def set_atr_status(
        self,
        activate: bool
    ) -> GeoComResponse[None]:
        """
        RPC 9018, ``AUT_SetATRStatus``

        .. deprecated:: GeoCom-TPS1100-1.04
            The command is still available, but should not be used with
            instruments that support the new `aus.set_user_atr_state`
            command.

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
        return super().set_atr_status(activate)

    @deprecated(
        "The 'AUT_GetLockStatus' command was superseded by "
        "'AUS_GetUserLockState' in v1.04 of TPS1100 GeoCom. Use the new "
        "command on instruments, that support it!"
    )
    def get_lock_status(self) -> GeoComResponse[bool]:
        """
        RPC 9021, ``AUT_GetLockStatus``

        .. deprecated:: GeoCom-TPS1100-1.04
            The command is still available, but should not be used with
            instruments that support the new `aus.get_user_lock_state`
            command.

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
        return super().get_lock_status()

    @deprecated(
        "The 'AUT_SetLockStatus' command was superseded by "
        "'AUS_SetUserLockState' in v1.04 of TPS1100 GeoCom. Use the new "
        "command on instruments, that support it!"
    )
    def set_lock_status(
        self,
        activate: bool
    ) -> GeoComResponse[None]:
        """
        RPC 9020, ``AUT_SetLockStatus``

        .. deprecated:: GeoCom-TPS1100-1.04
            The command is still available, but should not be used with
            instruments that support the new `aus.set_user_lock_state`
            command.

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
        return super().set_lock_status(activate)

    def get_search_area(
        self
    ) -> GeoComResponse[tuple[Angle, Angle, Angle, Angle, bool]]:
        """
        RPC 9042, ``AUT_GetSearchArea``

        .. versionadded:: GeoCom-TPS1100-1.04

        Gets current position and size of the PowerSearch window.

        Returns
        -------
        GeoComResponse
            Params:
                - `Angle`: Horizontal center of window.
                - `Angle`: Vertical center of window.
                - `Angle`: Width of window.
                - `Angle`: Height of window.
                - `bool`: If window is enabled.
            Error codes:
                - ``NA``: GeoCom Robotic license not found.

        See Also
        --------
        set_search_area
        bap.search_target
        """
        return self._request(
            9042,
            parsers=(
                Angle.parse,
                Angle.parse,
                Angle.parse,
                Angle.parse,
                parsebool
            )
        )

    def set_search_area(
        self,
        hz: Angle,
        v: Angle,
        width: Angle,
        height: Angle,
        enabled: bool = True
    ) -> GeoComResponse[None]:
        """
        RPC 9043, ``AUT_SetSearchArea``

        .. versionadded:: GeoCom-TPS1100-1.04

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
            Error codes:
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

    def get_spiral(self) -> GeoComResponse[tuple[Angle, Angle]]:
        """
        RPC 9040, ``AUT_GetUserSpiral``

        .. versionadded:: GeoCom-TPS1100-1.04

        Gets the size of the PowerSearch window.

        Returns
        -------
        GeoComResponse
            Params:
                - `Angle`: Width of window.
                - `Angle`: Height of window.
            Error codes:
                - ``NA``: GeoCom Robotic license not found.

        See Also
        --------
        set_spiral
        bap.search_target
        """
        return self._request(
            9040,
            parsers=(Angle.parse, Angle.parse)
        )

    def set_spiral(
        self,
        width: Angle,
        height: Angle
    ) -> GeoComResponse[None]:
        """
        RPC 9041, ``AUT_SetUserSpiral``

        .. versionadded:: GeoCom-TPS1100-1.04

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
            Error codes:
                - ``NA``: GeoCom Robotic license not found.

        See Also
        --------
        get_spiral
        bap.search_target
        """
        return self._request(
            9041,
            [width, height]
        )
