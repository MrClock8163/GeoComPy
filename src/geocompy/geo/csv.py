"""
Description
===========

Module: ``geocompy.geo.csv``

Definitions for the GeoCom Central services subsystem.

Types
-----

- ``GeoComCSV``

"""
from __future__ import annotations

from datetime import datetime

from ..data import (
    Byte,
    parsestr,
    enumparser
)
from ..data_geocom import (
    Capabilities,
    DeviceClass
)
from .gctypes import (
    GeoComSubsystem,
    GeoComResponse
)


class GeoComCSV(GeoComSubsystem):
    """
    Central services subsystem of the GeoCom protocol.

    This subsystem contains functions to maintain centralised data
    and configuration of the instruments.

    """

    def get_serial_number(self) -> GeoComResponse[int]:
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

    def get_user_instrument_name(self) -> GeoComResponse[str]:
        """
        RPC 5006, ``CSV_GetUserInstrumentName``

        Gets the user defined name of the instrument.

        Returns
        -------
        GeoComResponse
            Params:
                - `str`: Instrument name.

        """
        return self._request(
            5006,
            parsers=parsestr
        )

    def set_user_instrument_name(
        self,
        name: str
    ) -> GeoComResponse[None]:
        """
        RPC 5005, ``CSV_SetUserInstrumentName``

        Parameters
        ----------
        name : str
            Instrument name.

        Returns
        -------
        GeoComResponse
        """
        return self._request(
            5005,
            [name]
        )

    def get_instrument_configuration(
        self
    ) -> GeoComResponse[tuple[DeviceClass, Capabilities]]:
        """
        RPC 5035, ``CSV_GetDeviceConfig``

        Gets class of the instrument, as well as information about
        the capatilities of the configuration.

        Returns
        -------
        GeoComResponse
            Params:
                - `DeviceClass`: Class of the instrument.
                - `Capabilities`: Configuration of the components.
            Error codes:
                - ``UNDEFINED``: Precision class is undefined.

        """
        return self._request(
            5035,
            parsers=(
                enumparser(DeviceClass),
                enumparser(Capabilities)
            )
        )

    def get_datetime(self) -> GeoComResponse[datetime]:
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
        set_datetime

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

    def set_datetime(
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
        get_datetime

        """
        return self._request(
            5007,
            [
                time.year, Byte(time.month), Byte(time.day),
                Byte(time.hour), Byte(time.minute), Byte(time.second)
            ]
        )

    def get_firmware_version(self) -> GeoComResponse[tuple[int, int, int]]:
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

    def get_voltage_battery(self) -> GeoComResponse[float]:
        """
        RPC 5009, ``CSV_GetVBat``

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
        return self._request(
            5009,
            parsers=float
        )

    def get_voltage_memory(self) -> GeoComResponse[float]:
        """
        RPC 5009, ``CSV_GetVMem``

        Gets the voltage of the memory backup power supply.

        Voltage above 3.1 V is OK.

        Returns
        -------
        GeoComResponse
            Params:
                - `float`: Power source voltage [V].

        """
        return self._request(
            5009,
            parsers=float
        )

    def get_internal_temperature(self) -> GeoComResponse[int]:
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
