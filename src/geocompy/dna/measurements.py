from __future__ import annotations

from datetime import time, datetime

from .. import (
    GsiOnlineSubsystem,
    GsiOnlineResponse
)
from ..data import gsiword


class DNAMeasurements(GsiOnlineSubsystem):
    def get_point_id(self) -> GsiOnlineResponse[str | None]:
        return self._getrequest(
            "M",
            11,
            lambda v: v.strip("* ")[7:].lstrip("0")
        )

    def set_point_id(
        self,
        ptid: str
    ) -> GsiOnlineResponse[bool]:
        wi = 11
        word = gsiword(wi, ptid, gsi16=self._parent._gsi16)

        return self._putrequest(
            wi,
            word
        )

    def get_note(self) -> GsiOnlineResponse[str | None]:
        return self._getrequest(
            "M",
            71,
            lambda v: v.strip("* ")[7:].lstrip("0")
        )

    def set_note(
        self,
        note: str
    ) -> GsiOnlineResponse[bool]:
        wi = 71
        word = gsiword(wi, note, gsi16=self._parent._gsi16)

        return self._putrequest(
            wi,
            word
        )

    def get_time(self) -> GsiOnlineResponse[time | None]:
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
        wi = 560
        word = gsiword(
            wi,
            f"{value.hour:02d}{value.minute:02d}{value.second:02d}",
            info="6",
            gsi16=self._parent._gsi16
        )

        return self._putrequest(
            wi,
            word
        )

    def get_date(self) -> GsiOnlineResponse[tuple[int, int] | None]:
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
        wi = 561
        word = gsiword(
            wi,
            f"{month:02d}{day:02d}00",
            info="6",
            gsi16=self._parent._gsi16
        )

        return self._putrequest(
            wi,
            word
        )

    def get_year(self) -> GsiOnlineResponse[int | None]:
        return self._getrequest(
            "I",
            562,
            lambda v: int(v.strip("* ")[7:].lstrip("0"))
        )

    def set_year(
        self,
        year: int
    ) -> GsiOnlineResponse[bool]:
        wi = 562
        word = gsiword(
            wi,
            str(year),
            gsi16=self._parent._gsi16
        )

        return self._putrequest(
            wi,
            word
        )

    def get_distance(self) -> GsiOnlineResponse[float | None]:
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
        return self._getrequest(
            "M",
            95,
            lambda v: int(v.strip("* ")[6:]) / 10000
        )

    def get_serialnumber(self) -> GsiOnlineResponse[str | None]:
        return self._getrequest(
            "I",
            12,
            lambda v: v.strip("* ")[7:].lstrip("0")
        )

    def get_instrument_type(self) -> GsiOnlineResponse[str | None]:
        return self._getrequest(
            "I",
            13,
            lambda v: v.strip("* ")[7:].lstrip("0")
        )

    def get_full_date(self) -> GsiOnlineResponse[datetime | None]:
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

    def get_software_version(self) -> GsiOnlineResponse[str | None]:
        return self._getrequest(
            "I",
            599,
            lambda v: v.strip("* ")[7:].lstrip("0")
        )
