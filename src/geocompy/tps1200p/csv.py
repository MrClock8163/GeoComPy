"""
Description
===========

Module: ``geocompy.tps1200p.csv``

Definitions for the TPS1200+ Central services subsystem.

Types
-----

- ``TPS1200PCSV``

"""
from __future__ import annotations

from enum import Enum, Flag
from datetime import datetime

from ..data import (
    Byte,
    parsestr,
    enumparser
)
from ..protocols import (
    GeoComSubsystem,
    GeoComResponse
)


class TPS1200PCSV(GeoComSubsystem):
    """
    Central services subsystem of the TPS1200+ GeoCom protocol.

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
        CLASS_1202 = 200  #: TPS1200 2"
        CLASS_1203 = 201  #: TPS1200 3"
        CLASS_1205 = 202  #: TPS1200 5"
        CLASS_1201 = 203  #: TPS1200 1"
        CLASS_Tx30 = 300  #: TS30, MS30 0.5"
        CLASS_Tx31 = 301  #: TS30, MS30 1"

    class DEVICETYPE(Flag):
        T = 0x00000  #: Theodolite
        MOT = 0x00004  #: Motorized
        ATR = 0x00008  #: ATR
        EGL = 0x00010  #: Guide Light
        DB = 0x00020  #: Database
        DL = 0x00040  #: Diode laser
        LP = 0x00080  #: Laser plumb
        # TC1 = 0x00001 # TPS1000
        # TC2 = 0x00002 # TPS1000
        TC = 0x00001  #: Tachymeter
        TCR = 0x00002  #: Tachymeter (red laser)
        ATC = 0x00100  #: Autocollimation lamp
        LPNT = 0x00200  #: Laserpointer
        RLEXT = 0x00400  #: Reflectorless EDM
        PS = 0x00800  # Powersearch
        # SIM = 0x04000 # TPSSim

    class REFLESSCLASS(Enum):
        NONE = 0
        R100 = 1
        R300 = 2
        R400 = 3

    class POWERSOURCE(Enum):
        CURRENT = 0
        EXTERNAL = 1
        INTERNAL = 2

    def get_instrument_no(self) -> GeoComResponse[int]:
        """
        RPC 5003, ``CSV_GetInstrumentNo``

        Gets the serial number of the instrument.

        Returns
        -------
        GeoComResponse
            Params:
                - `int`: Serial number.

        """
        return self._request(
            5003,
            parsers=int
        )

    def get_instrument_name(self) -> GeoComResponse[str]:
        """
        RPC 5004, ``CSV_GetInstrumentName``

        Gets the name of the instrument.

        Returns
        -------
        GeoComResponse
            Params:
                - `str`: Instrument name.

        """
        return self._request(
            5004,
            parsers=parsestr
        )

    def get_device_config(
        self
    ) -> GeoComResponse[tuple[DEVICECLASS, DEVICETYPE]]:
        """
        RPC 5035, ``CSV_GetDeviceConfig``

        Gets class of the instrument, as well as information about
        the capatilities of the configuration.

        Returns
        -------
        GeoComResponse
            Params:
                - `DEVICECLASS`: Class of the instrument.
                - `DEVICETYPE`: Configurations of the
                  components.

        """
        return self._request(
            5035,
            parsers=(
                enumparser(self.DEVICECLASS),
                enumparser(self.DEVICETYPE)
            )
        )

    def get_reflectorless_class(self) -> GeoComResponse[REFLESSCLASS]:
        """
        RPC 5100, ``CSV_GetReflectorlessClass``

        Gets the class of the reflectorless EDM module, if the instrument
        is equipped with one.

        Returns
        -------
        GeoComResponse
            Params:
                - `REFLESSCLASS`: Class of the
                  reflectorless EDM module.

        """
        return self._request(
            5100,
            parsers=enumparser(self.REFLESSCLASS)
        )

    def get_date_time(self) -> GeoComResponse[datetime]:
        """
        RPC 5008, ``CSV_GetDateTime``

        Gets the current date and time set on the instrument.

        Returns
        -------
        GeoComResponse
            Params:
                - `datetime`: Current date and time.

        See Also
        --------
        set_date_time
        get_date_time_centisec

        """
        def make_datetime(
            params: tuple[int, Byte, Byte, Byte, Byte, Byte] | None
        ) -> datetime | None:
            if params is None:
                return None

            return datetime(
                params[0],
                int(params[1]),
                int(params[2]),
                int(params[3]),
                int(params[4]),
                int(params[5])
            )

        response: GeoComResponse[
            tuple[int, Byte, Byte, Byte, Byte, Byte]
        ] = self._request(
            5008,
            parsers=(
                int,
                Byte.parse,
                Byte.parse,
                Byte.parse,
                Byte.parse,
                Byte.parse
            )
        )

        return response.map_params(make_datetime)

    def set_date_time(
        self,
        time: datetime
    ) -> GeoComResponse[None]:
        """
        RPC 5007, ``CSV_SetDateTime``

        Sets the date and time on the instrument.

        Parameters
        ----------
        time : datetime
            New date and time to set.

        Returns
        -------
        GeoComResponse

        See Also
        --------
        get_date_time

        """
        return self._request(
            5007,
            [
                time.year, Byte(time.month), Byte(time.day),
                Byte(time.hour), Byte(time.minute), Byte(time.second)
            ]
        )

    def get_sw_version(self) -> GeoComResponse[tuple[int, int, int]]:
        """
        RPC 5034, ``CSV_GetSWVersion``

        Gets the system software version running on the instrument.

        Returns
        -------
        GeoComResponse
            Params:
                - `int`: Release number.
                - `int`: Version number.
                - `int`: Subversion number.

        """
        return self._request(
            5034,
            parsers=(int, int, int)
        )

    def check_power(
        self
    ) -> GeoComResponse[tuple[int, POWERSOURCE, POWERSOURCE]]:
        """
        RPC 5039, ``CSV_CheckPower``

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

    def get_int_temp(self) -> GeoComResponse[int]:
        """
        RPC 5011, ``CSV_GetIntTemp``

        Gets internal temperature of the instrument, measured on the
        main board.

        Returns
        -------
        GeoComResponse
            Params:
                - `int`: Internal temperature [°C].

        """
        return self._request(
            5011,
            parsers=int
        )

    def get_date_time_centisec(self) -> GeoComResponse[datetime]:
        """
        RPC 5117, ``CSV_GetDateTimeCentiSec``

        Gets the current date and time set on the instrument in
        centiseconds resolution.

        Returns
        -------
        GeoComResponse
            Params:
                - `datetime`: Current date and time.

        See Also
        --------
        get_date_time
        set_date_time

        """
        def make_datetime(
            params: tuple[int, int, int, int, int, int, int] | None
        ) -> datetime | None:
            if params is None:
                return None

            return datetime(
                params[0],
                int(params[1]),
                int(params[2]),
                int(params[3]),
                int(params[4]),
                int(params[5]),
                int(params[5]) * 10000
            )

        response = self._request(
            5117,
            parsers=(
                int,
                int,
                int,
                int,
                int,
                int,
                int
            )
        )
        return response.map_params(make_datetime)
