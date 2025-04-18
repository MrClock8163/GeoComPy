"""
``geocompy.tps1200p.sup``
=========================

Definitions for the TPS1200+ Supervisor subsystem.

Types
-----

- ``TPS1200PSUP``

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


class TPS1200PSUP(GeoComSubsystem):
    """
    Supervisor subsystem of the TPS1200+ GeoCom protocol.

    This subsystem controls the continuous operation of the system, and it
    allows to automatically display status information.

    """
    class ONOFF(Enum):
        OFF = 0
        ON = 1

    class AUTOPOWER(Enum):
        DISABLED = 0  # : Automatic poweroff disabled.
        OFF = 2  # : Poweroff instrument.

    def get_config(self) -> GeoComResponse:
        """
        RPC 14001, ``SUP_GetConfig``

        Gets the current poweroff and timing configuration.

        Returns
        -------
        GeoComResponse
            - Params:
                - **reserved** (`ONOFF`): Reserved.
                - **autopower** (`AUTOPOWER`): Current showdown mechanism.
                - **timeout** (`int`): Idling timeout [ms].

        See Also
        --------
        set_config

        """
        return self._request(
            14001,
            parsers={
                "reserved": enumparser(self.ONOFF),
                "autopower": enumparser(self.AUTOPOWER),
                "timeout": int
            }
        )

    def set_config(
        self,
        autopower: AUTOPOWER | str = AUTOPOWER.OFF,
        timeout: int = 600_000,
        reserved: ONOFF | str = ONOFF.ON
    ) -> GeoComResponse:
        """
        RPC 14002, ``SUP_SetConfig``

        Sets the poweroff and timing configuration.

        Parameters
        ----------
        autopower : AUTOPOWER | str, optional
            Automatic poweroff action.
        timeout : int, optional
            Idling timeout [60000, 6000000] [ms], by default 600000

        Returns
        -------
        GeoComResponse
            - Error codes:
                - ``IVPARAM``: Invalid timeout parameter.

        See Also
        --------
        get_config

        """
        _autopower = toenum(self.AUTOPOWER, autopower)
        _reserved = toenum(self.ONOFF, reserved)
        return self._request(
            14002,
            [_reserved.value, _autopower.value, timeout]
        )
