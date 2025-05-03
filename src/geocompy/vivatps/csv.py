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

from ..data import (
    toenum,
    enumparser,
    parsebool
)
from ..data_geocom import (
    PowerSource,
    Property
)
from ..protocols import GeoComResponse
from ..tps1200p.csv import TPS1200PCSV


class VivaTPSCSV(TPS1200PCSV):
    """
    Central services subsystem of the VivaTPS GeoCom protocol.

    This subsystem contains functions to maintain centralised data
    and configuration of the instruments.

    """

    def switch_startup_message(
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

    def get_startup_message_status(self) -> GeoComResponse[bool]:
        """
        RPC 5156, ``CSV_GetStartupMessageMode``

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

    def switch_laserlot(
        self,
        active: bool
    ) -> GeoComResponse[None]:
        """
        RPC 5043, ``CSV_SwitchLaserlot``

        Sets the state of the laserlot.

        Parameters
        ----------
        active : bool
            Activate laserlot.

        Returns
        -------
        GeoComResponse

        """
        return self._request(
            5043,
            [active]
        )

    def get_laserlot_status(self) -> GeoComResponse[bool]:
        """
        RPC 5042, ``CSV_GetLaserlotStatus``

        Gets the current state of the laserlot.

        Returns
        -------
        GeoComResponse
            Params:
                - `bool`: Laserlot is active.

        """
        return self._request(
            5042,
            parsers=parsebool
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
            Params:
                - `int`: Current laserlot intensity.

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
