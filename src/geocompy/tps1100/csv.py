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

from enum import Enum, Flag
from typing_extensions import deprecated

from ..data import enumparser
from ..protocols import GeoComResponse
from ..tps1000.csv import TPS1000CSV


class TPS1100CSV(TPS1000CSV):
    """
    Central services subsystem of the TPS1100 GeoCom protocol.

    This subsystem contains functions to maintain centralised data
    and configuration of the instruments.

    """
    class DEVICECLASS(Enum):
        CLASS_1100 = 0  #: TPS1000 3"
        CLASS_1700 = 1  #: TPS1000 1.5"
        CLASS_1800 = 2  #: TPS1000 1"
        CLASS_5000 = 3  #: TPS2000
        CLASS_6000 = 4  #: TPS2000
        CLASS_1500 = 5  #: TPS1000
        CLASS_2003 = 6  #: TPS2000
        CLASS_5005 = 7  #: TPS5000
        CLASS_5100 = 8  #: TPS5000
        CLASS_1102 = 100  #: TPS1100 2"
        CLASS_1103 = 101  #: TPS1100 3"
        CLASS_1105 = 102  #: TPS1100 5"
        CLASS_1101 = 103  #: TPS1100 1"

    class DEVICETYPE(Flag):
        T = 0x00000  #: Theodolite
        TC1 = 0x00001  # TPS1000
        TC2 = 0x00002  # TPS1000
        MOT = 0x00004  #: Motorized
        ATR = 0x00008  #: ATR
        EGL = 0x00010  #: Guide Light
        DB = 0x00020  #: Database
        DL = 0x00040  #: Diode laser
        LP = 0x00080  #: Laser plumb
        ATC = 0x00100  #: Autocollimation lamp
        LPNT = 0x00200  #: Laserpointer
        RLEXT = 0x00400  #: Reflectorless EDM
        # SIM = 0x04000 # TPSSim

    class POWERSOURCE(Enum):
        CURRENT = 0
        EXTERNAL = 1
        INTERNAL = 2

    @deprecated(
        "The `CSV_GetVBat` command was superceded by `CSV_CheckPower` "
        "in v1.05 of GeoCom. Use the new command on instruments that "
        "support it!"
    )
    def get_v_bat(self) -> GeoComResponse[float]:
        """
        RPC 5009, ``CSV_GetVBat``

        .. deprecated:: GeoCom-1.05
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
        return super().get_v_bat()

    def check_power(
        self
    ) -> GeoComResponse[tuple[int, POWERSOURCE, POWERSOURCE]]:
        """
        RPC 5039, ``CSV_CheckPower``

        .. versionadded:: GeoCom-1.05

        Gets the remaining capacity of the active power source.

        Returns
        -------
        GeoComResponse
            Params:
                - `int`: Remaining capacity [%].
                - `POWERSOURCE`: Active power source.
                - `POWERSOURCE`: Suggested power source.

        """
        return self._request(
            5039,
            parsers=(
                int,
                enumparser(self.POWERSOURCE),
                enumparser(self.POWERSOURCE)
            )
        )

    @deprecated("This command was removed for TPS1100 instruments")
    def get_user_instrument_name(self) -> GeoComResponse[str]:
        """
        RPC 5006, ``CSV_GetUserInstrumentName``

        .. versionremoved:: GeoCom-1.00

        Raises
        ------
        AttributeError
        """
        raise AttributeError()

    @deprecated("This command was removed for TPS1100 instruments")
    def set_user_instrument_name(
        self,
        name: str
    ) -> GeoComResponse[None]:
        """
        RPC 5005, ``CSV_SetUserInstrumentName``

        .. versionremoved:: GeoCom-1.00

        Raises
        ------
        AttributeError
        """
        raise AttributeError()
