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

from datetime import time, datetime

from ..gsitypes import (
    GsiOnlineSubsystem,
    GsiOnlineResponse
)
from ...data import gsiword


class GsiOnlineDNAMeasurements(GsiOnlineSubsystem):
    """
    Measurements subsystem of the DNA GSI Online protocol.

    This subsystem gives access to measurement data. The communication
    (both get and set) is done through GSI data words.
    """

    def get_point_id(self) -> GsiOnlineResponse[str | None]:
        """
        ``GET 11``

        Gets the current running point ID.

        Returns
        -------
        GsiOnlineResponse
            Point ID.

        Note
        ----
        The value in the response is ``None`` if the value could not be
        retrieved (i.e. an error occured during the request).
        """
        return self._getrequest(
            "M",
            11,
            lambda v: v.strip("* ")[7:].lstrip("0")
        )

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
        wi = 11
        word = gsiword(wi, ptid, gsi16=self._parent.is_client_gsi16)

        return self._putrequest(
            wi,
            word
        )

    def get_note(self) -> GsiOnlineResponse[str | None]:
        """
        ``GET 71``

        Gets the current point note/remark.

        Returns
        -------
        GsiOnlineResponse
            Point note.

        Note
        ----
        The value in the response is ``None`` if the value could not be
        retrieved (i.e. an error occured during the request).
        """
        return self._getrequest(
            "M",
            71,
            lambda v: v.strip("* ")[7:].lstrip("0")
        )

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
        wi = 71
        word = gsiword(wi, note, gsi16=self._parent.is_client_gsi16)

        return self._putrequest(
            wi,
            word
        )

    def get_time(self) -> GsiOnlineResponse[time | None]:
        """
        ``GET 560``

        Gets the current time.

        Returns
        -------
        GsiOnlineResponse
            Current time.

        Note
        ----
        The value in the response is ``None`` if the value could not be
        retrieved (i.e. an error occured during the request).
        """
        def parsetime(value: str) -> time:
            value = value.strip("* ")
            return time(
                int(value[-6:-4]),
                int(value[-4:-2]),
                int(value[-2:])
            )

        return self._getrequest(
            "I",
            560,
            parsetime
        )

    def set_time(
        self,
        value: time
    ) -> GsiOnlineResponse[bool]:
        """
        ``PUT 560``

        Sets the time on the instrument.

        Parameters
        ----------
        value : time
            New time to set.

        Returns
        -------
        GsiOnlineResponse
            Success of the change.
        """
        wi = 560
        word = gsiword(
            wi,
            f"{value.hour:02d}{value.minute:02d}{value.second:02d}",
            info="6",
            gsi16=self._parent.is_client_gsi16
        )

        return self._putrequest(
            wi,
            word
        )

    def get_date(self) -> GsiOnlineResponse[tuple[int, int] | None]:
        """
        ``GET 561``

        Gets the current month and day.

        Returns
        -------
        GsiOnlineResponse
            Current month and day.

        Note
        ----
        The value in the response is ``None`` if the value could not be
        retrieved (i.e. an error occured during the request).
        """
        def parsedate(value: str) -> tuple[int, int]:
            value = value.strip("* ")
            return int(value[-6:-4]), int(value[-4:-2])

        return self._getrequest(
            "I",
            561,
            parsedate
        )

    def set_date(
        self,
        month: int,
        day: int
    ) -> GsiOnlineResponse[bool]:
        """
        ``PUT 561``

        Sets the month and day.

        Parameters
        ----------
        month : int
        day : int

        Returns
        -------
        GsiOnlineResponse
            Success of the change.
        """
        wi = 561
        word = gsiword(
            wi,
            f"{month:02d}{day:02d}00",
            info="6",
            gsi16=self._parent.is_client_gsi16
        )

        return self._putrequest(
            wi,
            word
        )

    def get_year(self) -> GsiOnlineResponse[int | None]:
        """
        ``GET 562``

        Gets the current year.

        Returns
        -------
        GsiOnlineResponse
            Current year.

        Note
        ----
        The value in the response is ``None`` if the value could not be
        retrieved (i.e. an error occured during the request).
        """
        return self._getrequest(
            "I",
            562,
            lambda v: int(v.strip("* ")[7:].lstrip("0"))
        )

    def set_year(
        self,
        year: int
    ) -> GsiOnlineResponse[bool]:
        """
        ``PUT 562``

        Sets the year.

        Parameters
        ----------
        year : int

        Returns
        -------
        GsiOnlineResponse
            Success of the change.
        """
        wi = 562
        word = gsiword(
            wi,
            str(year),
            gsi16=self._parent.is_client_gsi16
        )

        return self._putrequest(
            wi,
            word
        )

    def get_distance(self) -> GsiOnlineResponse[float | None]:
        """
        ``GET 32``

        Measures the distance from the aimed levelling staff in the
        currently set distance unit.

        Returns
        -------
        GsiOnlineResponse
            Distance.

        Note
        ----
        The value in the response is ``None`` if the value could not be
        retrieved (i.e. an error occured during the request).
        """
        def parsedist(value: str) -> float:
            value = value.strip("* ")
            data = float(value[6:])
            match value[5]:
                case "0" | "1":
                    data /= 1000
                case "6" | "7":
                    data /= 10000
                case "8":
                    data /= 100000

            return data

        return self._getrequest(
            "M",
            32,
            parsedist
        )

    def get_reading(self) -> GsiOnlineResponse[float | None]:
        """
        ``GET 330``

        Takes a reading on the aimed levelling staff in the currently set
        distance unit.

        Returns
        -------
        GsiOnlineResponse
            Staff reading.

        Note
        ----
        The value in the response is ``None`` if the value could not be
        retrieved (i.e. an error occured during the request).
        """
        def parsereading(value: str) -> float:
            value = value.strip("* ")
            data = float(value[6:])
            match value[5]:
                case "0" | "1":
                    data /= 1000
                case "6" | "7":
                    data /= 10000
                case "8":
                    data /= 100000

            return data

        return self._getrequest(
            "M",
            330,
            parsereading
        )

    def get_temperature(self) -> GsiOnlineResponse[float | None]:
        """
        ``GET 95``

        Measures and returns the internal temperature in the currently set
        temperature units.

        Returns
        -------
        GsiOnlineResponse
            Internal temperature.

        Note
        ----
        The value in the response is ``None`` if the value could not be
        retrieved (i.e. an error occured during the request).
        """
        return self._getrequest(
            "M",
            95,
            lambda v: int(v.strip("* ")[6:]) / 10000
        )

    def get_serialnumber(self) -> GsiOnlineResponse[str | None]:
        """
        ``GET 12``

        Gets the serial number of the instrument.

        Returns
        -------
        GsiOnlineResponse
            Serial number.

        Note
        ----
        The value in the response is ``None`` if the value could not be
        retrieved (i.e. an error occured during the request).
        """
        return self._getrequest(
            "I",
            12,
            lambda v: v.strip("* ")[7:].lstrip("0")
        )

    def get_instrument_type(self) -> GsiOnlineResponse[str | None]:
        """
        ``GET 13``

        Gets the instrument type.

        Returns
        -------
        GsiOnlineResponse
            Instrument type.

        Note
        ----
        The value in the response is ``None`` if the value could not be
        retrieved (i.e. an error occured during the request).
        """
        return self._getrequest(
            "I",
            13,
            lambda v: v.strip("* ")[7:].lstrip("0")
        )

    def get_full_date(self) -> GsiOnlineResponse[datetime | None]:
        """
        ``GET 17``

        Gets the current full date (year, month, day).

        Returns
        -------
        GsiOnlineResponse
            Full date.

        Note
        ----
        The value in the response is ``None`` if the value could not be
        retrieved (i.e. an error occured during the request).
        """
        def parsedate(value: str) -> datetime:
            value = value.strip("* ")
            return datetime(
                int(value[-4:]),
                int(value[-6:-4]),
                int(value[-8:-6])
            )

        return self._getrequest(
            "I",
            17,
            parsedate
        )

    def get_day_time(self) -> GsiOnlineResponse[tuple[int, int, time] | None]:
        """
        ``GET 19``

        Gets the current month, day and time.

        Returns
        -------
        GsiOnlineResponse
            Month, day and time.

        Note
        ----
        The value in the response is ``None`` if the value could not be
        retrieved (i.e. an error occured during the request).
        """
        def parse(value: str) -> tuple[int, int, time]:
            value = value.strip("* ")
            return (
                int(value[-8:-6]),
                int(value[-6:-4]),
                time(
                    int(value[-4:-2]),
                    int(value[-2:])
                )
            )

        return self._getrequest(
            "I",
            19,
            parse
        )

    def get_software_version(
        self
    ) -> GsiOnlineResponse[tuple[int, int] | None]:
        """
        ``GET 599``

        Gets the software version of the instrument.

        Returns
        -------
        GsiOnlineResponse
            Software version.

        Note
        ----
        The value in the response is ``None`` if the value could not be
        retrieved (i.e. an error occured during the request).
        """
        def parse(value: str) -> tuple[int, int]:
            value = value.strip("* ")[7:]
            return int(value[:-4]), int(value[-4:])

        return self._getrequest(
            "I",
            599,
            parse
        )
