"""
Description
===========

Module: ``geocompy.tps1100.csv``

Definitions for the TPS1100 Central services subsystem.

Types
-----

- ``TPS1100CSV``

"""
from __future__ import annotations

from typing import Never, Any
from typing_extensions import deprecated

from ..data import enumparser
from ..data_geocom import PowerSource
from ..protocols import GeoComResponse
from ..tps1000.csv import TPS1000CSV


class TPS1100CSV(TPS1000CSV):
    """
    Central services subsystem of the TPS1100 GeoCom protocol.

    This subsystem contains functions to maintain centralised data
    and configuration of the instruments.

    """

    @deprecated(
        "The `CSV_GetVBat` command was superseded by `CSV_CheckPower` "
        "in v1.05 of GeoCom. Use the new command on instruments that "
        "support it!"
    )
    def get_voltage_battery(self) -> GeoComResponse[float]:
        """
        RPC 5009, ``CSV_GetVBat``

        .. deprecated:: GeoCom-TPS1100-1.05
            The command is still available, but should not be used with
            instruments that support the new `check_power` command.

        Gets the voltage of the power supply.

        | 12,7 V < voltage            full
        | 12,4 V < voltage < 12,7 V   near full
        | 11,1 V < voltage < 12,4 V   good
        | 10,5 V < voltage < 11,1 V   empty
        |          voltage < 10,5 V   powered off

        Returns
        -------
        GeoComResponse
            Params:
                - `float`: Power source voltage [V].

        """
        return super().get_voltage_battery()

    def check_power(
        self
    ) -> GeoComResponse[tuple[int, PowerSource, PowerSource]]:
        """
        RPC 5039, ``CSV_CheckPower``

        .. versionadded:: GeoCom-TPS1100-1.05

        Gets the remaining capacity of the active power source.

        Returns
        -------
        GeoComResponse
            Params:
                - `int`: Remaining capacity [%].
                - `PowerSource`: Active power source.
                - `PowerSource`: Suggested power source.

        """
        return self._request(
            5039,
            parsers=(
                int,
                enumparser(PowerSource),
                enumparser(PowerSource)
            )
        )

    @deprecated("This command was removed for TPS1100 instruments")
    def get_user_instrument_name(self) -> Never:
        """
        RPC 5006, ``CSV_GetUserInstrumentName``

        .. versionremoved:: GeoCom-TPS1100-1.00

        Raises
        ------
        AttributeError
        """
        raise AttributeError()

    @deprecated("This command was removed for TPS1100 instruments")
    def set_user_instrument_name(
        self,
        *args: Any,
        **kwargs: Any
    ) -> Never:
        """
        RPC 5005, ``CSV_SetUserInstrumentName``

        .. versionremoved:: GeoCom-TPS1100-1.00

        Raises
        ------
        AttributeError
        """
        raise AttributeError()
