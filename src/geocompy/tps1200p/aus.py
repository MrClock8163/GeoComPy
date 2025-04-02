"""
``geocompy.tps1200p.aus``
=========================

Definitions for the TPS1200+ Alt user subsystem.

Types
-----

- ``TPS1200PAUS``

"""
from __future__ import annotations

from enum import Enum

from .. import (
    GeoComSubsystem,
    GeoComResponse
)
from ..data import (
    toenum,
    enumparser
)


class TPS1200PAUS(GeoComSubsystem):
    """
    Alt user subsystem of the TPS1200+ GeoCom protocol.

    This subsystem can be used to set and query the ATR and LOCK
    automation modes.

    """
    class ONOFF(Enum):
        OFF = 0
        ON = 1

    def get_user_atr_state(self) -> GeoComResponse:
        """
        RPC 18006, ``AUS_GetUserAtrState``

        Gets the current state of the ATR mode.

        Returns
        -------
        GeoComResponse
            - Params:
                - **state** (`ONOFF`): current ATR state

            - Error codes:
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
            parsers={
                "state": enumparser(self.ONOFF)
            }
        )

    def set_user_atr_state(
        self,
        state: ONOFF | str
    ) -> GeoComResponse:
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
            - Error codes:
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

    def get_user_lock_state(self) -> GeoComResponse:
        """
        RPC 18005, ``AUS_GetUserLockState``

        Gets the current state of the LOCK mode.

        Returns
        -------
        GeoComResponse
            - Params:
                - **state** (`ONOFF`): current ATR state

            - Error codes:
                - ``NOT_IMPL``: ATR is not available.

        See Also
        --------
        set_user_lock_state
        mot.read_lock_status
        """
        return self._request(
            18008,
            parsers={
                "state": enumparser(self.ONOFF)
            }
        )

    def set_user_lock_state(
        self,
        state: ONOFF | str
    ) -> GeoComResponse:
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
            - Error codes:
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
