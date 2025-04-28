"""
Description
===========

Module: ``geocompy.vivatps.csv``

Definitions for the VivaTPS Central services subsystem.

Types
-----

- ``VivaTPSCSV``

"""
from __future__ import annotations

from enum import Enum

from ..data import (
    toenum,
    enumparser,
    parsebool
)
from ..protocols import GeoComResponse
from ..tps1200p.csv import TPS1200PCSV


class VivaTPSCSV(TPS1200PCSV):
    """
    Central services subsystem of the VivaTPS GeoCom protocol.

    This subsystem contains functions to maintain centralised data
    and configuration of the instruments.

    """
    class ONOFF(Enum):
        OFF = 0
        ON = 1

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
        CLASS_TDRA = 350  #: TDRA 0.5"
        CLASS_TS01 = 500  #: 1"
        CLASS_TS02 = 501  #: 2"
        CLASS_TS03 = 502  #: 3"
        CLASS_TS05 = 503  #: 5"
        CLASS_TS06 = 504  #: 6"
        CLASS_TS07 = 505  #: 7"
        CLASS_TS10 = 506  #: 10"
        CLASS_TS1X_1 = 600  #: Viva 1"
        CLASS_TS1X_2 = 601  #: Viva 2"
        CLASS_TS1X_3 = 602  #: Viva 3"
        CLASS_TS1X_4 = 603  #: Viva 4"
        CLASS_TS1X_5 = 604  #: Viva 5"
        CLASS_TS50_05 = 650  #: TPS1300 TS50/TM50, 0.5"
        CLASS_TS50_1 = 651  #: TPS1300 TS50/TM50, 1"

    class REFLESSCLASS(Enum):
        NONE = 0
        R100 = 1
        R300 = 2
        R400 = 3
        R1000 = 4
        R30 = 5

    class POWERSOURCE(Enum):
        CURRENT = 0
        EXTERNAL = 1
        INTERNAL = 2

    class PROPERTY(Enum):
        PURCHASE_MODE_NORMAL = 0
        PURCHASE_MODE_PREPAY = 1
        RTK_RANGE_5000 = 2
        RTK_RANGE_UNLIMITED = 3
        RTK_NETWORK = 4
        RTK_REFERENCE_STN = 5
        RTK_LEICA_LITE = 6
        RTK_NETWORK_LOCKDOWN = 7
        POSITION_RATE_5HZ = 8
        POSITION_RATE_20HZ = 9
        GPS_L2 = 10
        GPS_L5 = 11
        GLONASS = 12
        GALILEO = 13
        RAWDATA_LOGGING = 14
        RINEX_LOGGING = 15
        NMEA_OUT = 16
        DGPS_RTCM = 17
        OWI = 18
        NETWORK_PROVIDER_ACCESS_RESET = 19
        NO_AREA_LIMITATION = 20
        SMARTWORX_FULL = 21
        SMARTWORX_LITE = 22
        DEMO_LICENSE = 23
        INTERNAL_WIT2450 = 24
        GEOCOM_ROBOTICS = 25
        GEOCOM_IMAGING = 26
        GEOCOM_GPS = 27
        GEOCOM_LIMITED_AUT = 28
        IMAGING_WITH_OVC = 29
        SERIAL_NUMBER = 30
        PRODUCTION_FLAG = 31
        SYSTEMTIME_VALID = 32

    def set_startup_message_mode(
        self,
        enabled: bool
    ) -> GeoComResponse[None]:
        """
        RPC 5155, ``CSV_SetStartupMessageMode``

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

    def get_startup_message_mode(self) -> GeoComResponse[bool]:
        """
        RPC 5156, ``CSV_GetStartupMessageMode``

        Gets the current status of the startup message mode on the
        instrument.

        Returns
        -------
        GeoComResponse
            - Params:
                - **enabled** (`bool`): Startup message is enabled.

        """
        return self._request(
            5156,
            parsers=parsebool
        )

    def switch_laserlot(
        self,
        state: ONOFF | str
    ) -> GeoComResponse[None]:
        """
        RPC 5043, ``CSV_SwitchLaserlot``

        Sets the state of the laserlot.

        Parameters
        ----------
        state : ONOFF
            State to set for laserlot.

        Returns
        -------
        GeoComResponse

        """
        _state = toenum(self.ONOFF, state)
        return self._request(
            5043,
            [_state.value]
        )

    def get_laserlot_status(self) -> GeoComResponse[ONOFF]:
        """
        RPC 5042, ``CSV_GetLaserlotStatus``

        Gets the current state of the laserlot.

        Returns
        -------
        GeoComResponse
            - Params:
                - **enabled** (`bool`): Startup message mode is enabled.

        """
        return self._request(
            5042,
            parsers=enumparser(self.ONOFF)
        )

    def set_laserlot_intensity(
        self,
        intensity: int
    ) -> GeoComResponse[None]:
        """
        RPC 5040, ``CSV_SetLaserlotIntens``

        Sets the intensity of the laserlot.

        Parameters
        ----------
        intensity : int
            New laserlot intensity to set.

        Returns
        -------
        GeoComResponse

        """
        return self._request(
            5040,
            [intensity]
        )

    def get_laserlot_intensity(self) -> GeoComResponse[int]:
        """
        RPC 5041, ``CSV_GetLaserlotIntens``

        Gets the current intensity of the laserlot.

        Returns
        -------
        GeoComResponse
            - Params:
                - **intensity** (`int`): Current laserlot intensity.

        """
        return self._request(
            5041,
            parsers=int
        )

    def check_property(
        self,
        property: PROPERTY | str
    ) -> GeoComResponse[bool]:
        """
        RPC 5039, ``CSV_CheckProperty``

        Checks if a specific license is available on the instrument.

        Parameters
        ----------
        property : PROPERTY | str
            License to check.

        Returns
        -------
        GeoComResponse
            - Params:
                - **available** (`bool`): License is available.

        """
        _prop = toenum(self.PROPERTY, property)
        return self._request(
            5139,
            [_prop.value],
            parsebool
        )

    def get_voltage(self) -> GeoComResponse[int]:
        """
        RPC 5165, ``CSV_GetVoltage``

        Gets the instrument voltage.

        Returns
        -------
        GeoComResponse
            - Params:
                - **voltage** (`int`): Instrument voltage [mV].

        """
        return self._request(
            5165,
            parsers=int
        )

    def set_charging(
        self,
        state: ONOFF | str
    ) -> GeoComResponse[None]:
        """
        RPC 5161, ``CSV_SetCharging``

        Sets the state of the charger.

        Parameters
        ----------
        state : ONOFF | str
            New state to set for charger.

        Returns
        -------
        GeoComResponse

        """
        _state = toenum(self.ONOFF, state)
        return self._request(
            5161,
            [_state.value]
        )

    def get_charging(self) -> GeoComResponse[ONOFF]:
        """
        RPC 5162, ``CSV_GetCharging``

        Gets the current state of the charger.

        Returns
        -------
        GeoComResponse
            - Params:
                - **state** (`ONOFF`): Current state of the charger.

        """
        return self._request(
            5162,
            parsers=enumparser(self.ONOFF)
        )

    def set_preferred_powersource(
        self,
        source: POWERSOURCE | str
    ) -> GeoComResponse[None]:
        """
        RPC 5163, ``CSV_SetPreferredPowersource``

        Sets the preferred power source.

        Parameters
        ----------
        source : POWERSOURCE | str
            New preferred power source to set.

        """
        _source = toenum(self.POWERSOURCE, source)
        return self._request(
            5163,
            [_source.value]
        )

    def get_preferred_powersource(self) -> GeoComResponse[POWERSOURCE]:
        """
        RPC 5164, ``CSV_GetPreferredPowersource``

        Gets the current preferred power source.

        Returns
        -------
        GeoComResponse
            - Params:
                - **source** (`POWERSOURCE`): Preferred power source.

        """
        return self._request(
            5164,  # Mistyped as 5163 in the GeoCom reference
            parsers=enumparser(self.POWERSOURCE)
        )
