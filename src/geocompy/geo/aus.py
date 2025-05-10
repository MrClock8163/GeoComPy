"""
Description
===========

Module: ``geocompy.geo.aus``

Definitions for the GeoCom Alt user subsystem.

Types
-----

- ``GeoComAUS``

"""
from __future__ import annotations

from ..data import parsebool
from .gctypes import (
    GeoComSubsystem,
    GeoComResponse
)


class GeoComAUS(GeoComSubsystem):
    """
    Alt user subsystem of the GeoCom protocol.

    .. versionadded:: GeoCom-TPS1100-1.04

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
        switch_user_atr
        """
        return self._request(
            18006,
            parsers=parsebool
        )

    def switch_user_atr(
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
        switch_user_lock
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
        switch_user_lock
        mot.get_lockon_status
        """
        return self._request(
            18008,
            parsers=parsebool
        )

    def switch_user_lock(
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

    def get_rcs_search_status(self) -> GeoComResponse[bool]:
        """
        RPC 18010, ``AUS_GetRcsSearchSwitch``

        .. versionadded:: GeoCom-TPS1100-1.05

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

        .. versionadded:: GeoCom-TPS1100-1.05

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
