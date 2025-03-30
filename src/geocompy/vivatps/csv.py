from __future__ import annotations

from enum import Enum

from .. import GeoComResponse
from ..data import toenum
from ..tps1200p.csv import TPS1200PCSV


class VivaTPSCSV(TPS1200PCSV):
    class ONOFF(Enum):
        @classmethod
        def parse(cls, value: str) -> VivaTPSCSV.ONOFF:
            return cls(int(value))

        OFF = 0
        ON = 1
    
    class DEVICECLASS(Enum):
        @classmethod
        def parse(cls, value: str) -> VivaTPSCSV.DEVICECLASS:
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
        CLASS_TDRA = 350  # TDRA 0.5"
        CLASS_TS01 = 500  # 1"
        CLASS_TS02 = 501  # 2"
        CLASS_TS03 = 502  # 3"
        CLASS_TS05 = 503  # 5"
        CLASS_TS06 = 504  # 6"
        CLASS_TS07 = 505  # 7"
        CLASS_TS10 = 506  # 10"
        CLASS_TS1X_1 = 600  # Viva 1"
        CLASS_TS1X_2 = 601  # Viva 2"
        CLASS_TS1X_3 = 602  # Viva 3"
        CLASS_TS1X_4 = 603  # Viva 4"
        CLASS_TS1X_5 = 604  # Viva 5"
        CLASS_TS50_05 = 650  # TPS1300 TS50/TM50, 0.5"
        CLASS_TS50_1 = 651  # TPS1300 TS50/TM50, 1"
    
    class REFLESSCLASS(Enum):
        @classmethod
        def parse(cls, value: str) -> VivaTPSCSV.REFLESSCLASS:
            return cls(int(value))

        NONE = 0
        R100 = 1
        R300 = 2
        R400 = 3
        R1000 = 4
        R30 = 5

    class POWERSOURCE(Enum):
        @classmethod
        def parse(cls, value: str) -> VivaTPSCSV.POWERSOURCE:
            return cls(int(value))

        CURRENT = 0
        EXTERNAL = 1
        INTERNAL = 2
    
    class PROPERTY(Enum):
        @classmethod
        def parse(cls, value: str) -> VivaTPSCSV.PROPERTY:
            return cls(int(value))
        
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
    ) -> GeoComResponse:
        return self._request(
            5155,
            [enabled]
        )
    
    def get_startup_message_mode(self) -> GeoComResponse:
        return self._request(
            5156,
            parsers={
                "enabled": bool
            }
        )

    def switch_laserlot(
        self,
        state: ONOFF | str
    ) -> GeoComResponse:
        _state = toenum(self.ONOFF, state)
        return self._request(
            5043,
            [_state.value]
        )
    
    def get_laserlot_status(self) -> GeoComResponse:
        return self._request(
            5042,
            parsers={
                "state": self.ONOFF.parse
            }
        )
    
    def set_laserlot_intensity(
        self,
        intensity: int
    ) -> GeoComResponse:
        return self._request(
            5040,
            [intensity]
        )
    
    def get_laserlot_intensity(self) -> GeoComResponse:
        return self._request(
            5041,
            parsers={
                "intensity": int
            }
        )
    
    def check_property(
        self,
        property: PROPERTY | str
    ) -> GeoComResponse:
        _prop = toenum(self.PROPERTY, property)
        return self._request(
            5139,
            [_prop.value],
            {
                "available": bool
            }
        )
    
    def get_voltage(self) -> GeoComResponse:
        return self._request(
            5165,
            parsers={
                "millivolts": int
            }
        )
    
    def set_charging(
        self,
        state: ONOFF | str
    ) -> GeoComResponse:
        _state = toenum(self.ONOFF, state)
        return self._request(
            5161,
            [_state.value]
        )

    def get_charging(self) -> GeoComResponse:
        return self._request(
            5162,
            parsers={
                "state": self.ONOFF.parse
            }
        )
    
    def set_preferred_powersource(
        self,
        source: POWERSOURCE | str
    ) -> GeoComResponse:
        _source = toenum(self.POWERSOURCE, source)
        return self._request(
            5163,
            [_source.value]
        )

    def get_preferred_powersource(self) -> GeoComResponse:
        return self._request(
            5164, # Mistyped as 5163 in the GeoCom reference
            parsers={
                "source": self.POWERSOURCE.parse
            }
        )
