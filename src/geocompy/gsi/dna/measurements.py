"""
Description
===========

Module: ``geocompy.gsi.dna.measurements``

Definitions for the DNA measurements subsystem.

Types
-----

- ``GsiOnlineDNAMeasurements``
"""
from __future__ import annotations

from datetime import datetime
from typing import Any

from ..gsitypes import (
    GsiOnlineSubsystem,
    GsiOnlineResponse
)
from .. import gsiformat as gsi


def _word_value(value: gsi.GsiValueWord | None) -> Any:
    if value is None:
        return None

    return value.value


class GsiOnlineDNAMeasurements(GsiOnlineSubsystem):
    """
    Measurements subsystem of the DNA GSI Online protocol.

    This subsystem gives access to measurement data. The communication
    (both get and set) is done through GSI data words.
    """

    def get_point_id(self) -> GsiOnlineResponse[str]:
        """
        ``GET 11``

        Gets the current running point ID.

        Returns
        -------
        GsiOnlineResponse
            Point ID.
        """
        return self._getrequest(
            "M",
            gsi.GsiPointNameWord
        ).map_value(_word_value)

    def set_point_id(
        self,
        ptid: str
    ) -> GsiOnlineResponse[bool]:
        """
        ``PUT 11``

        Sets the running point ID.

        Parameters
        ----------
        ptid : str
            Point ID.

        Returns
        -------
        GsiOnlineResponse
            Success of the change.
        """

        return self._putrequest(gsi.GsiPointNameWord(ptid))

    def get_note(self) -> GsiOnlineResponse[str]:
        """
        ``GET 71``

        Gets the current point note/remark.

        Returns
        -------
        GsiOnlineResponse
            Point note.
        """
        return self._getrequest(
            "M",
            gsi.GsiRemark1Word
        ).map_value(_word_value)

    def set_note(
        self,
        note: str
    ) -> GsiOnlineResponse[bool]:
        """
        ``PUT 71``

        Sets the point note/remark.

        Parameters
        ----------
        note : str
            Point note.

        Returns
        -------
        GsiOnlineResponse
            Success of the change.
        """

        return self._putrequest(gsi.GsiRemark1Word(note))

    def get_time(self) -> GsiOnlineResponse[datetime]:
        """
        ``GET 560``

        Gets the current time.

        Returns
        -------
        GsiOnlineResponse
            Current time wrapped in a datetime object
            (year, month and day should be ignored).

        """
        return self._getrequest(
            "I",
            gsi.GsiNewTimeWord
        ).map_value(_word_value)

    def set_time(
        self,
        time: datetime
    ) -> GsiOnlineResponse[bool]:
        """
        ``PUT 560``

        Sets the hours, minutes and seconds on the instrument.

        Parameters
        ----------
        time : datetime
            New time to set.

        Returns
        -------
        GsiOnlineResponse
            Success of the change.
        """
        return self._putrequest(gsi.GsiNewTimeWord(time))

    def get_date(self) -> GsiOnlineResponse[datetime]:
        """
        ``GET 561``

        Gets the current month and day.

        Returns
        -------
        GsiOnlineResponse
            Current month and day wrapped in a datetime object
            (year should be ignored).
        """
        return self._getrequest(
            "I",
            gsi.GsiNewDateWord
        ).map_value(_word_value)

    def set_date(
        self,
        date: datetime
    ) -> GsiOnlineResponse[bool]:
        """
        ``PUT 561``

        Sets the month and day.

        Parameters
        ----------
        date : datetime

        Returns
        -------
        GsiOnlineResponse
            Success of the change.
        """
        return self._putrequest(gsi.GsiNewDateWord(date))

    def get_year(self) -> GsiOnlineResponse[datetime]:
        """
        ``GET 562``

        Gets the current year.

        Returns
        -------
        GsiOnlineResponse
            Current year wrapped in a datetime object
            (month and day should be ignored).

        """
        return self._getrequest(
            "I",
            gsi.GsiNewYearWord
        ).map_value(_word_value)

    def set_year(
        self,
        year: datetime
    ) -> GsiOnlineResponse[bool]:
        """
        ``PUT 562``

        Sets the year.

        Parameters
        ----------
        year : datetime

        Returns
        -------
        GsiOnlineResponse
            Success of the change.
        """

        return self._putrequest(gsi.GsiNewYearWord(year))

    def get_distance(self) -> GsiOnlineResponse[float]:
        """
        ``GET 32``

        Measures the distance from the aimed levelling staff in meters.

        Returns
        -------
        GsiOnlineResponse
            Distance.
        """
        return self._getrequest(
            "M",
            gsi.GsiStaffDistanceWord
        ).map_value(_word_value)

    def get_reading(self) -> GsiOnlineResponse[float]:
        """
        ``GET 330``

        Takes a reading on the aimed levelling staff in meters.

        Returns
        -------
        GsiOnlineResponse
            Staff reading.
        """
        return self._getrequest(
            "M",
            gsi.GsiSimpleStaffReadingWord
        ).map_value(_word_value)

    def get_temperature(self) -> GsiOnlineResponse[float]:
        """
        ``GET 95``

        Measures and returns the internal temperature in Celsius degrees.

        Returns
        -------
        GsiOnlineResponse
            Internal temperature.
        """
        return self._getrequest(
            "M",
            gsi.GsiTemperatureWord
        ).map_value(_word_value)

    def get_serialnumber(self) -> GsiOnlineResponse[str]:
        """
        ``GET 12``

        Gets the serial number of the instrument.

        Returns
        -------
        GsiOnlineResponse
            Serial number.
        """
        return self._getrequest(
            "I",
            gsi.GsiSerialnumberWord
        ).map_value(_word_value)

    def get_instrument_type(self) -> GsiOnlineResponse[str]:
        """
        ``GET 13``

        Gets the instrument type name.

        Returns
        -------
        GsiOnlineResponse
            Instrument type.
        """
        return self._getrequest(
            "I",
            gsi.GsiInstrumentTypeWord
        ).map_value(_word_value)

    def get_full_date(self) -> GsiOnlineResponse[datetime]:
        """
        ``GET 17``

        Gets the current full date (year, month, day).

        Returns
        -------
        GsiOnlineResponse
            Full date.
        """
        return self._getrequest(
            "I",
            gsi.GsiDateWord
        ).map_value(_word_value)

    def get_day_time(self) -> GsiOnlineResponse[datetime]:
        """
        ``GET 19``

        Gets the current month, day and time.

        Returns
        -------
        GsiOnlineResponse
            Month, day and time wrapped in a datetime object
            (year should be ignored).
        """
        return self._getrequest(
            "I",
            gsi.GsiTimeWord
        ).map_value(_word_value)

    def get_software_version(
        self
    ) -> GsiOnlineResponse[float]:
        """
        ``GET 599``

        Gets the software version of the instrument.

        Returns
        -------
        GsiOnlineResponse
            Software version as float
            (integer part is major,
            fractional part is minor version with 4 decimals maximum).
        """
        return self._getrequest(
            "I",
            gsi.GsiSoftwareVersionWord
        ).map_value(_word_value)
