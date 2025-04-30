"""
Description
===========

Module: ``geocompy.tps1000.sup``

Definitions for the TPS1000 Supervisor subsystem.

Types
-----

- ``TPS1000SUP``

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


class TPS1000SUP(GeoComSubsystem):
    """
    Supervisor subsystem of the TPS1000 GeoCom protocol.

    This subsystem controls the continuous operation of the system, and it
    allows to automatically display status information.

    """
    class ONOFF(Enum):
        OFF = 0
        ON = 1

    class AUTOPOWER(Enum):
        DISABLED = 0  # : Automatic poweroff disabled.
        SLEEP = 1  # : Put instument into sleep mode.
        OFF = 2  # : Poweroff instrument.

    def get_config(self) -> GeoComResponse[tuple[ONOFF, AUTOPOWER, int]]:
        """
        RPC 14001, ``SUP_GetConfig``

        Gets the current poweroff and timing configuration.

        Returns
        -------
        GeoComResponse
            Params:
                - `ONOFF`: Low temperature shutdown.
                - `AUTOPOWER`: Current shutdown mechanism.
                - `int`: Idling timeout [ms].

        See Also
        --------
        set_config

        """
        return self._request(
            14001,
            parsers=(
                enumparser(self.ONOFF),
                enumparser(self.AUTOPOWER),
                int
            )
        )

    def set_config(
        self,
        lowtemp: ONOFF | str,
        autopower: AUTOPOWER | str = AUTOPOWER.OFF,
        timeout: int = 600_000
    ) -> GeoComResponse[None]:
        """
        RPC 14002, ``SUP_SetConfig``

        Sets the poweroff and timing configuration.

        Parameters
        ----------
        lowtemp : ONOFF | str
            Low temperature shutdown.
        autopower : AUTOPOWER | str, optional
            Automatic poweroff action.
        timeout : int, optional
            Idling timeout [60000, 6000000] [ms], by default 600000

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``IVPARAM``: Invalid timeout parameter.

        See Also
        --------
        get_config

        """
        _autopower = toenum(self.AUTOPOWER, autopower)
        _lowtemp = toenum(self.ONOFF, lowtemp)
        return self._request(
            14002,
            [_lowtemp.value, _autopower.value, timeout]
        )

    def switch_low_temp_control(
        self,
        state: ONOFF | str
    ) -> GeoComResponse[None]:
        """
        RPC 14003, ``SUP_SwitchLowTempControl``

        Enables or disables the low temperature shutdown mechanism. When
        active, the mechanism will shut the instrument down, if the
        internal temperature falls below -30 degree celsius.

        Parameters
        ----------
        state : ONOFF | str
            Low temperature shutdown.

        Returns
        -------
        GeoComResponse

        See Also
        --------
        get_config
        set_config

        """
        _state = toenum(self.ONOFF, state)
        return self._request(
            14003,
            [_state.value]
        )
