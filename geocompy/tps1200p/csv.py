from __future__ import annotations

from enum import Enum, Flag
from datetime import datetime

from .. import (
    GeoComSubsystem,
    GeoComResponse
)
from ..data import Byte
from ..communication import parsestr


class TPS1200PCSV(GeoComSubsystem):
    class DEVICECLASS(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PCSV.DEVICECLASS:
            return cls(int(value))

        CLASS_1100 = 0  # TPS1000 3"
        CLASS_1700 = 1  # TPS1000 1.5"
        CLASS_1800 = 2  # TPS1000 1"
        CLASS_5000 = 3  # TPS2000
        CLASS_6000 = 4  # TPS2000
        CLASS_1500 = 5  # TPS1000
        CLASS_2003 = 6  # TPS2000
        CLASS_5005 = 7  # TPS5000
        CLASS_5100 = 8  # TPS5000
        CLASS_1102 = 100  # TPS1100 2"
        CLASS_1103 = 101  # TPS1100 3"
        CLASS_1105 = 102  # TPS1100 5"
        CLASS_1101 = 103  # TPS1100 1"
        CLASS_1202 = 200  # TPS1200 2"
        CLASS_1203 = 201  # TPS1200 3"
        CLASS_1205 = 202  # TPS1200 5"
        CLASS_1201 = 203  # TPS1200 1"
        CLASS_Tx30 = 300  # TS30, MS30 0.5"
        CLASS_Tx31 = 301  # TS30, MS30 1"

    class DEVICETYPE(Flag):
        @classmethod
        def parse(cls, value: str) -> TPS1200PCSV.DEVICETYPE:
            return cls(int(value))

        T = 0x00000  # Theodolites
        MOT = 0x00004  # Motorized
        ATR = 0x00008  # ATR
        EGL = 0x00010  # Guide Light
        DB = 0x00020  # Database
        DL = 0x00040  # Diode laser
        LP = 0x00080  # Laser plumbed
        # TC1 = 0x00001 # TPS1000
        # TC2 = 0x00002 # TPS1000
        TC = 0x00001  # Tachymeter
        TCR = 0x00002  # Tachymeter (red laser)
        ATC = 0x00100  # Autocollimation lamp
        LPNT = 0x00200  # Laserpointer
        RLEXT = 0x00400  # Powersearch
        PS = 0x00800  # Powersearch
        # SIM = 0x04000 # TPSSim

    class REFLESSCLASS(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PCSV.REFLESSCLASS:
            return cls(int(value))

        NONE = 0
        R100 = 1
        R300 = 2
        R400 = 3
        R1000 = 4

    class POWERSOURCE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PCSV.POWERSOURCE:
            return cls(int(value))

        CURRENT = 0
        EXTERNAL = 1
        INTERNAL = 2

    def get_instrument_no(self) -> GeoComResponse:
        return self._request(
            5003,
            parsers={
                "serial": int
            }
        )

    def get_instrument_name(self) -> GeoComResponse:
        return self._request(
            5004,
            parsers={
                "name": parsestr
            }
        )

    def get_device_config(self) -> GeoComResponse:
        return self._request(
            5035,
            parsers={
                "deviceclass": self.DEVICECLASS.parse,
                "devicetype": lambda x: self.DEVICETYPE(int(x))
            }
        )

    def get_reflectorless_class(self) -> GeoComResponse:
        return self._request(
            5100,
            parsers={
                "reflessclass": self.REFLESSCLASS.parse
            }
        )

    def get_date_time(self) -> GeoComResponse:
        response = self._request(
            5008,
            parsers={
                "year": int,
                "month": Byte.parse,
                "day": Byte.parse,
                "hour": Byte.parse,
                "minute": Byte.parse,
                "second": Byte.parse
            }
        )
        time = datetime(
            int(response.params["year"]),
            int(response.params["month"]),
            int(response.params["day"]),
            int(response.params["hour"]),
            int(response.params["minute"]),
            int(response.params["second"])
        )
        response.params = {"time": time}
        return response

    def set_date_time(
        self,
        time: datetime
    ) -> GeoComResponse:
        return self._request(
            5007,
            [
                time.year, Byte(time.month), Byte(time.day),
                Byte(time.hour), Byte(time.minute), Byte(time.second)
            ]
        )

    def get_sw_version(self) -> GeoComResponse:
        return self._request(
            5034,
            parsers={
                "release": int,
                "version": int,
                "subversion": int
            }
        )

    def check_power(self) -> GeoComResponse:
        return self._request(
            5039,
            parsers={
                "capacity": int,
                "source": self.POWERSOURCE.parse,
                "suggested": self.POWERSOURCE.parse
            }
        )

    def get_int_temp(self) -> GeoComResponse:
        return self._request(
            5011,
            parsers={
                "temp": int
            }
        )

    def get_date_time_centisec(self) -> GeoComResponse:
        response = self._request(
            5117,
            parsers={
                "year": int,
                "month": int,
                "day": int,
                "hour": int,
                "minute": int,
                "second": int,
                "centisec": int
            }
        )
        time = datetime(
            response.params["year"],
            response.params["month"],
            response.params["day"],
            response.params["hour"],
            response.params["minute"],
            response.params["second"],
            response.params["centisec"] * 10000
        )
        response.params = {"time": time}
        return response
