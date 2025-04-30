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

from enum import Enum

from ..data import (
    toenum,
    enumparser
)
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
    class ONOFF(Enum):
        OFF = 0
        ON = 1

    def get_user_atr_state(self) -> GeoComResponse[ONOFF]:
        """
        RPC 18006, ``AUS_GetUserAtrState``

        Gets the current state of the ATR mode.

        Returns
        -------
        GeoComResponse
            Params:
                - `ONOFF`: current ATR state

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
            parsers=enumparser(self.ONOFF)
        )

    def set_user_atr_state(
        self,
        state: ONOFF | str
    ) -> GeoComResponse[None]:
        """
        RPC 18005, ``AUS_SetUserAtrState``

        Activates or deactivates the ATR mode.

        Parameters
        ----------
        state : ONOFF | str
            ATR state to set

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
        _state = toenum(self.ONOFF, state)
        return self._request(18005, [_state.value])

    def get_user_lock_state(self) -> GeoComResponse[ONOFF]:
        """
        RPC 18005, ``AUS_GetUserLockState``

        Gets the current state of the LOCK mode.

        Returns
        -------
        GeoComResponse
            Params:
                - `ONOFF`: current ATR state

            Error codes:
                - ``NOT_IMPL``: ATR is not available.

        See Also
        --------
        set_user_lock_state
        mot.read_lock_status
        """
        return self._request(
            18008,
            parsers=enumparser(self.ONOFF)
        )

    def set_user_lock_state(
        self,
        state: ONOFF | str
    ) -> GeoComResponse[None]:
        """
        RPC 18007, ``AUS_SetUserLockState``

        Activates or deactivates the LOCK mode.

        Parameters
        ----------
        state : ONOFF | str
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
        get_user_lock_state
        get_user_atr_state
        aut.lock_in
        """
        _state = toenum(self.ONOFF, state)
        return self._request(
            18007,
            [_state.value]
        )

    def get_rcs_search_switch(self) -> GeoComResponse[ONOFF]:
        """
        RPC 18010, ``AUS_GetRcsSearchSwitch``

        Gets the current state of the RCS search mode.

        Returns
        -------
        GeoComResponse
            Params:
                - `ONOFF`: Current RCS state.

            Error codes:
                - ``NOT_IMPL``: ATR is not available.

        """
        return self._request(
            18008,
            parsers=enumparser(self.ONOFF)
        )

    def switch_rcs_search(
        self,
        state: ONOFF | str
    ) -> GeoComResponse[None]:
        """
        RPC 18009, ``AUS_SwitchRcsSearch``

        Enables or disables the RCS searching mode.

        Parameters
        ----------
        state : ONOFF | str
            New state of the RCS search mode.

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``NOT_IMPL``: ATR is not available.

        """
        _state = toenum(self.ONOFF, state)
        return self._request(
            18009,
            [_state.value]
        )
