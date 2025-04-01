"""
``geocompy.vivatps.bap``
=========================

Definitions for the VivaTPS Basic applications subsystem.

Types
-----

- ``VivaTPSBAP``

"""
from __future__ import annotations

from enum import Enum

from ..data import (
    toenum,
    enumparser
)
from .. import GeoComResponse
from ..tps1200p.bap import TPS1200PBAP


class VivaTPSBAP(TPS1200PBAP):
    """
    Basic applications subsystem of the VivaTPS GeoCom protocol.

    This subsystem contains high-level functions that are also accessible
    through the user interface. The commands combine several subcommands
    for ease of operation.

    """
    class ONOFF(Enum):
        OFF = 0
        ON = 1
    
    def get_atr_precise(self) -> GeoComResponse:
        """
        RPC 17039, ``BAP_GetATRPrecise``

        Gets the current state of the precise ATR mode.

        Returns
        -------
        GeoComResponse
            - Params:
                - **state** (`ONOFF`): Current state of precise ATR mode.

        See Also
        --------
        set_atr_precise
        """
        return self._request(
            17039,
            parsers={
                "state": enumparser(self.ONOFF)
            }
        )

    def set_atr_precise(
        self,
        state: ONOFF | str
    ) -> GeoComResponse:
        """
        RPC 17040, ``BAP_SetATRPrecise``

        Sets the state of the precise ATR mode.

        Parameters
        ----------
        state : ONOFF | str
            Precise ATR mode state to set.

        Returns
        -------
        GeoComResponse

        See Also
        --------
        get_atr_precise
        """
        _state = toenum(self.ONOFF, state)
        return self._request(
            17040,
            [_state.value]
        )
