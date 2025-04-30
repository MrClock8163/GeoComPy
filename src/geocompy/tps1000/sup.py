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

from ..data import (
    toenum,
    enumparser,
    parsebool,
    AUTOPOWER
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

    def get_config(self) -> GeoComResponse[tuple[bool, AUTOPOWER, int]]:
        """
        RPC 14001, ``SUP_GetConfig``

        Gets the current poweroff and timing configuration.

        Returns
        -------
        GeoComResponse
            Params:
                - `bool`: Low temperature shutdown enabled.
                - `AUTOPOWER`: Current shutdown mechanism.
                - `int`: Idling timeout [ms].

        See Also
        --------
        set_config

        """
        return self._request(
            14001,
            parsers=(
                parsebool,
                enumparser(AUTOPOWER),
                int
            )
        )

    def set_config(
        self,
        lowtemp: bool,
        autopower: AUTOPOWER | str = AUTOPOWER.SHUTDOWN,
        timeout: int = 600_000
    ) -> GeoComResponse[None]:
        """
        RPC 14002, ``SUP_SetConfig``

        Sets the poweroff and timing configuration.

        Parameters
        ----------
        lowtemp : bool
            Enable low temperature shutdown.
        autopower : AUTOPOWER | str, optional
            Automatic poweroff action, by default AUTOPOWER.SHUTDOWN
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
        _autopower = toenum(AUTOPOWER, autopower)
        return self._request(
            14002,
            [lowtemp, _autopower.value, timeout]
        )

    def switch_low_temp_control(
        self,
        enabled: bool
    ) -> GeoComResponse[None]:
        """
        RPC 14003, ``SUP_SwitchLowTempControl``

        Enables or disables the low temperature shutdown mechanism. When
        active, the mechanism will shut the instrument down, if the
        internal temperature falls below -30 degree celsius.

        Parameters
        ----------
        enabled : bool
            Enable low temperature shutdown.

        Returns
        -------
        GeoComResponse

        See Also
        --------
        get_config
        set_config

        """
        return self._request(
            14003,
            [enabled]
        )
