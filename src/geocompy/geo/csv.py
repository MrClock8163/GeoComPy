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
    parsebool,
    enumparser,
    toenum
)
from .gcdata import (
    Capabilities,
    DeviceClass,
    PowerSource,
    Reflectorless,
    Property
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

        .. versionremoved:: GeoCom-TPS1100

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

        .. versionremoved:: GeoCom-TPS1100

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

    def get_firmware_creation_date(self) -> GeoComResponse[str]:
        """
        RPC 5038, ``CSV_GetSWCreationDate``

        .. versionadded:: GeoComp-TPS1200

        Gets the creation date of the system software version running on
        the instrument.

        Returns
        -------
        GeoComResponse
            Params:
                - `str`: Creation date.

        """
        # def transformer(value: str | None) -> datetime | None:
        #     if value is None:
        #         return None

        #     return datetime.strptime(value, "%Y-%m-%d")

        response = self._request(
            5038,
            parsers=str
        )
        return response

    def get_voltage_battery(self) -> GeoComResponse[float]:
        """
        RPC 5009, ``CSV_GetVBat``

        .. deprecated:: GeoCom-TPS1100-1.05
            The command is still available, but should not be used with
            instruments that support the new `check_power` command.

        .. versionremoved:: GeoCom-TPS1200

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

        .. versionremoved:: GeoCom-TPS1200

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

    def get_internal_temperature(self) -> GeoComResponse[float]:
        """
        RPC 5011, ``CSV_GetIntTemp``

        Gets internal temperature of the instrument, measured on the
        main board.

        Returns
        -------
        GeoComResponse
            Params:
                - `float`: Internal temperature [°C].

        """
        return self._request(
            5011,
            parsers=float
        )

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

    def get_reflectorless_class(self) -> GeoComResponse[Reflectorless]:
        """
        RPC 5100, ``CSV_GetReflectorlessClass``

        .. versionadded:: GeoCom-TPS1200

        Gets the class of the reflectorless EDM module, if the instrument
        is equipped with one.

        Returns
        -------
        GeoComResponse
            Params:
                - `Reflectorless`: Class of the reflectorless EDM module.

        """
        return self._request(
            5100,
            parsers=enumparser(Reflectorless)
        )

    def get_datetime_precise(self) -> GeoComResponse[datetime]:
        """
        RPC 5117, ``CSV_GetDateTimeCentiSec``

        .. versionadded:: GeoCom-TPS1200

        Gets the current date and time set on the instrument in
        centiseconds resolution.

        Returns
        -------
        GeoComResponse
            Params:
                - `datetime`: Current date and time.

        See Also
        --------
        get_datetime
        set_datetime

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

    def switch_startup_message(
        self,
        enabled: bool
    ) -> GeoComResponse[None]:
        """
        RPC 5155, ``CSV_SetStartupMessageMode``

        .. versionadded:: GeoCom-VivaTPS

        Enables or disables the startup message mode on the instrument.

        Parameters
        ----------
        enabled : bool
            Startup message mode is enabled.

        Returns
        -------
        GeoComResponse

        """
        return self._request(
            5155,
            [enabled]
        )

    def get_startup_message_status(self) -> GeoComResponse[bool]:
        """
        RPC 5156, ``CSV_GetStartupMessageMode``

        .. versionadded:: GeoCom-VivaTPS

        Gets the current status of the startup message mode on the
        instrument.

        Returns
        -------
        GeoComResponse
            Params:
                - `bool`: Startup message is enabled.

        """
        return self._request(
            5156,
            parsers=parsebool
        )

    def switch_laserplummet(
        self,
        active: bool
    ) -> GeoComResponse[None]:
        """
        RPC 5043, ``CSV_SwitchLaserlot``

        .. versionadded:: GeoCom-VivaTPS

        Sets the state of the laser plummet.

        Parameters
        ----------
        active : bool
            Activate laser plummet.

        Returns
        -------
        GeoComResponse

        """
        return self._request(
            5043,
            [active]
        )

    def get_laserplummet_status(self) -> GeoComResponse[bool]:
        """
        RPC 5042, ``CSV_GetLaserlotStatus``

        .. versionadded:: GeoCom-VivaTPS

        Gets the current state of the laser plummet.

        Returns
        -------
        GeoComResponse
            Params:
                - `bool`: Laser plummet is active.

        """
        return self._request(
            5042,
            parsers=parsebool
        )

    def set_laserplummet_intensity(
        self,
        intensity: int
    ) -> GeoComResponse[None]:
        """
        RPC 5040, ``CSV_SetLaserlotIntens``

        .. versionadded:: GeoCom-VivaTPS

        Sets the intensity of the laser plummet.

        Parameters
        ----------
        intensity : int
            New laser plummet intensity to set.

        Returns
        -------
        GeoComResponse

        """
        return self._request(
            5040,
            [intensity]
        )

    def get_laserplummet_intensity(self) -> GeoComResponse[int]:
        """
        RPC 5041, ``CSV_GetLaserlotIntens``

        .. versionadded:: GeoCom-VivaTPS

        Gets the current intensity of the laser plummet.

        Returns
        -------
        GeoComResponse
            Params:
                - `int`: Current laser plummet intensity.

        """
        return self._request(
            5041,
            parsers=int
        )

    def check_property(
        self,
        property: Property | str
    ) -> GeoComResponse[bool]:
        """
        RPC 5039, ``CSV_CheckProperty``

        .. versionadded:: GeoCom-VivaTPS

        Checks if a specific license is available on the instrument.

        Parameters
        ----------
        property : Property | str
            License to check.

        Returns
        -------
        GeoComResponse
            Params:
                - `bool`: License is available.

        """
        _prop = toenum(Property, property)
        return self._request(
            5139,
            [_prop.value],
            parsebool
        )

    def get_voltage(self) -> GeoComResponse[int]:
        """
        RPC 5165, ``CSV_GetVoltage``

        .. versionadded:: GeoCom-VivaTPS

        Gets the instrument voltage.

        Returns
        -------
        GeoComResponse
            Params:
                - `int`: Instrument voltage [mV].

        """
        return self._request(
            5165,
            parsers=int
        )

    def switch_charging(
        self,
        activate: bool
    ) -> GeoComResponse[None]:
        """
        RPC 5161, ``CSV_SetCharging``

        .. versionadded:: GeoCom-VivaTPS

        Sets the state of the charger.

        Parameters
        ----------
        activate : bool
            Activate charger.

        Returns
        -------
        GeoComResponse

        """
        return self._request(
            5161,
            [activate]
        )

    def get_charging_status(self) -> GeoComResponse[bool]:
        """
        RPC 5162, ``CSV_GetCharging``

        .. versionadded:: GeoCom-VivaTPS

        Gets the current state of the charger.

        Returns
        -------
        GeoComResponse
            Params:
                - `bool`: Charger is active.

        """
        return self._request(
            5162,
            parsers=parsebool
        )

    def set_preferred_powersource(
        self,
        source: PowerSource | str
    ) -> GeoComResponse[None]:
        """
        RPC 5163, ``CSV_SetPreferredPowersource``

        .. versionadded:: GeoCom-VivaTPS

        Sets the preferred power source.

        Parameters
        ----------
        source : PowerSource | str
            New preferred power source to set.

        """
        _source = toenum(PowerSource, source)
        return self._request(
            5163,
            [_source.value]
        )

    def get_preferred_powersource(self) -> GeoComResponse[PowerSource]:
        """
        RPC 5164, ``CSV_GetPreferredPowersource``

        .. versionadded:: GeoCom-VivaTPS

        Gets the current preferred power source.

        Returns
        -------
        GeoComResponse
            Params:
                - `PowerSource`: Preferred power source.

        """
        return self._request(
            5164,  # Mistyped as 5163 in the GeoCom reference
            parsers=enumparser(PowerSource)
        )

    def get_datetime_new(self) -> GeoComResponse[datetime]:
        """
        RPC 5051, ``CSV_GetDateTime2``

        .. versionadded:: GeoComp-TPS1200

        Gets the current date and time set on the instrument.

        Returns
        -------
        GeoComResponse
            Params:
                - `datetime`: Current date and time.

        See Also
        --------
        set_datetime_new

        """
        def make_datetime(
            params: tuple[int, int, int, int, int, int] | None
        ) -> datetime | None:
            if params is None:
                return None

            return datetime(
                params[0],
                params[1],
                params[2],
                params[3],
                params[4],
                params[5]
            )

        response: GeoComResponse[
            tuple[int, int, int, int, int, int]
        ] = self._request(
            5051,
            parsers=(
                int,
                int,
                int,
                int,
                int,
                int
            )
        )

        return response.map_params(make_datetime)

    def set_datetime_new(
        self,
        time: datetime
    ) -> GeoComResponse[None]:
        """
        RPC 5050, ``CSV_SetDateTime2``

        .. versionadded:: GeoComp-VivaTPS

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
        get_datetime_new

        """
        return self._request(
            5050,
            [
                time.year, time.month, time.day,
                time.hour, time.minute, time.second
            ]
        )

    def setup_listing(self) -> GeoComResponse[None]:
        """
        RPC 5072, ``CSV_SetupList``

        Prepares listing of the jobs in memory.

        Returns
        -------
        GeoComResponse

        See Also
        --------
        list

        """
        return self._request(
            5072
        )

    def list(self) -> GeoComResponse[tuple[str, str, int, int, str]]:
        """
        RPC 5073, ``CSV_List``

        Gets the next job listing entry.

        Returns
        -------
        GeoComResponse
            Params:
                - `str`: Job name.
                - `str`: File name (`-01`: job, `-02`: code list).
                - `int`: Unknown.
                - `int`: Unknown.
                - `str`: Unknown.

        See Also
        --------
        setup_listing

        """
        return self._request(
            5073,
            parsers=(
                parsestr,
                parsestr,
                int,
                int,
                parsestr
            )
        )

    def get_maintenance_end(self) -> GeoComResponse[datetime]:
        """
        RPC 5114, ``CSV_GetMaintenanceEnd``

        Gets the date when the software maintenance service ends.

        Returns
        -------
        GeoComResponse
            Params:
                - `datetime`: Software maintenance end date.

        """
        def transform(
            params: tuple[int, Byte, Byte] | None
        ) -> datetime | None:
            if params is None:
                return None

            return datetime(
                params[0],
                int(params[1]),
                int(params[2])
            )

        response = self._request(
            5114,
            parsers=[
                int,
                Byte.parse,
                Byte.parse
            ]
        )

        return response.map_params(transform)
