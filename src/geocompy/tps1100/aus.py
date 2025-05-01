"""
Description
===========

Module: ``geocompy.tps1100.aus``

Definitions for the TPS1100 Alt user subsystem.

Types
-----

- ``TPS1100AUS``

"""
from __future__ import annotations

from ..data import parsebool
from ..protocols import (
    GeoComSubsystem,
    GeoComResponse
)


class TPS1100AUS(GeoComSubsystem):
    """
    Alt user subsystem of the TPS1100 GeoCom protocol.

    .. versionadded:: GeoCom-1.04

    This subsystem can be used to set and query the ATR and LOCK
    automation modes.

    """

    def get_user_atr_state(self) -> GeoComResponse[bool]:
        """
        RPC 18006, ``AUS_GetUserAtrState``

        Gets the current state of the ATR mode.

        Returns
        -------
        GeoComResponse
            Params:
                - `bool`: ATR is enabled.

            Error codes:
                - ``NOT_IMPL``: ATR is not available.

        Notes
        -----
        This command does not indicate if the ATR has acquired a prism.

        See Also
        --------
        set_user_atr_state
        """
        return self._request(
            18006,
            parsers=parsebool
        )

    def set_user_atr_state(
        self,
        enabled: bool
    ) -> GeoComResponse[None]:
        """
        RPC 18005, ``AUS_SetUserAtrState``

        Activates or deactivates the ATR mode.

        Parameters
        ----------
        enabled : bool
            ATR is enabled.

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
        get_user_atr_state
        get_user_lock_state
        set_user_lock_state
        """
        return self._request(18005, [enabled])

    def get_user_lock_state(self) -> GeoComResponse[bool]:
        """
        RPC 18005, ``AUS_GetUserLockState``

        Gets the current state of the LOCK mode.

        Returns
        -------
        GeoComResponse
            Params:
                - `bool`: ATR lock is enabled.

            Error codes:
                - ``NOT_IMPL``: ATR is not available.

        See Also
        --------
        set_user_lock_state
        mot.read_lock_status
        """
        return self._request(
            18008,
            parsers=parsebool
        )

    def set_user_lock_state(
        self,
        enabled: bool
    ) -> GeoComResponse[None]:
        """
        RPC 18007, ``AUS_SetUserLockState``

        Activates or deactivates the LOCK mode.

        Parameters
        ----------
        enabled : bool
            ATR lock is enabled.

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
        get_user_lock_state
        get_user_atr_state
        aut.lock_in
        """
        return self._request(
            18007,
            [enabled]
        )

    def get_rcs_search_switch(self) -> GeoComResponse[bool]:
        """
        RPC 18010, ``AUS_GetRcsSearchSwitch``

        Gets the current state of the RCS search mode.

        Returns
        -------
        GeoComResponse
            Params:
                - `bool`: RCS-style search is enabled.

            Error codes:
                - ``NOT_IMPL``: ATR is not available.

        """
        return self._request(
            18008,
            parsers=parsebool
        )

    def switch_rcs_search(
        self,
        enabled: bool
    ) -> GeoComResponse[None]:
        """
        RPC 18009, ``AUS_SwitchRcsSearch``

        Enables or disables the RCS searching mode.

        Parameters
        ----------
        enabled : bool
            RCS-style search is enabled.

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``NOT_IMPL``: ATR is not available.

        """
        return self._request(
            18009,
            [enabled]
        )
