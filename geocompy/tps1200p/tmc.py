from __future__ import annotations

from enum import Enum

from .. import (
    GeoComSubsystem,
    GeoComResponse
)
from ..data import Angle, Coordinate
from ..communication import toenum


class TPS1200PTMC(GeoComSubsystem):
    class ONOFF(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PTMC.ONOFF:
            return cls(int(value))

        OFF = 0
        ON = 1

    class INCLINEPRG(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PTMC.INCLINEPRG:
            return cls(int(value))

        MEA = 0
        AUTO = 1
        PLANE = 2

    class MEASUREPRG(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PTMC.MEASUREPRG:
            return cls(int(value))

        STOP = 0
        DEFDIST = 1
        CLEAR = 3
        SIGNAL = 4
        DOMEASURE = 6
        RTRKDIST = 8
        REDTRKDIST = 10
        FREQUENCY = 11

    class EMDMODE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PTMC.EMDMODE:
            return cls(int(value))

        NOTUSED = 0
        SINGLE_TAPE = 1
        SINGLE_STANDARD = 2
        SINGLE_FAST = 3
        SINGLE_LRANGE = 4
        SINGLE_SRANGE = 5
        CONT_STANDARD = 6
        CONT_DYNAMIC = 7
        CONT_REFLESS = 8
        CONT_FAST = 9
        AVERAGE_IR = 10
        AVERAGE_SR = 11
        AVERAGE_LR = 12
        PRECISE_IR = 13  # TS30, MS30
        PRECISE_TAPE = 14  # TS30, MS30

    class FACEDEF(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PTMC.FACEDEF:
            return cls(int(value))

        NORMAL = 0
        TURN = 1

    class FACE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PTMC.FACE:
            return cls(int(value))

        FACE1 = 0
        FACE2 = 1

    def get_coordinate(
        self,
        wait: int = 5000,
        mode: INCLINEPRG | str = INCLINEPRG.AUTO
    ) -> GeoComResponse:
        _mode = toenum(self.INCLINEPRG, mode)
        response = self._request(
            2082,
            [wait, _mode.value],
            {
                "east": float,
                "north": float,
                "height": float,
                "time": int,
                "east_cont": float,
                "north_cont": float,
                "height_cont": float,
                "time_cont": int
            }
        )
        coord = Coordinate(
            response.params["east"],
            response.params["north"],
            response.params["height"]
        )
        coord_cont = Coordinate(
            response.params["east_cont"],
            response.params["north_cont"],
            response.params["height_cont"]
        )
        response.params = {
            "coord": coord,
            "time": response.params["time"],
            "coord_cont": coord_cont,
            "time_cont": response.params["time_cont"]
        }
        return response

    def get_simple_mea(
        self,
        wait: int = 5000,
        mode: INCLINEPRG | str = INCLINEPRG.AUTO
    ) -> GeoComResponse:
        _mode = toenum(self.INCLINEPRG, mode)
        return self._request(
            2108,
            [wait, _mode.value],
            {
                "hz": Angle.parse,
                "v": Angle.parse,
                "dist": float
            }
        )

    def get_angle_incline(
        self,
        mode: INCLINEPRG | str = INCLINEPRG.AUTO
    ) -> GeoComResponse:
        _mode = toenum(self.INCLINEPRG, mode)
        return self._request(
            2003,
            [_mode.value],
            {
                "hz": Angle.parse,
                "v": Angle.parse,
                "angleaccuracy": Angle.parse,
                "angletime": int,
                "crossincline": Angle.parse,
                "lengthincline": Angle.parse,
                "inclineaccuracy": Angle.parse,
                "inclinetime": int,
                "face": self.FACEDEF.parse
            }
        )

    def get_angle(
        self,
        mode: INCLINEPRG | str = INCLINEPRG.AUTO
    ) -> GeoComResponse:
        _mode = toenum(self.INCLINEPRG, mode)
        return self._request(
            2107,
            [_mode.value],
            {
                "hz": Angle.parse,
                "v": Angle.parse
            }
        )

    def quick_dist(self) -> GeoComResponse:
        return self._request(
            2117,
            parsers={
                "hz": Angle.parse,
                "v": Angle.parse,
                "dist": float
            }
        )

    def get_full_meas(
        self,
        wait: int = 5000,
        mode: INCLINEPRG | str = INCLINEPRG.AUTO
    ) -> GeoComResponse:
        _mode = toenum(self.INCLINEPRG, mode)
        return self._request(
            2167,
            [wait, _mode.value],
            {
                "hz": float,
                "v": float,
                "angleaccuracy": float,
                "crossincline": float,
                "lengthincline": float,
                "inclineaccuracy": float,
                "dist": float,
                "disttime": float
            }
        )

    def do_measure(
        self,
        command: MEASUREPRG | str = MEASUREPRG.DEFDIST,
        mode: INCLINEPRG | str = INCLINEPRG.AUTO
    ) -> GeoComResponse:
        _cmd = toenum(self.MEASUREPRG, command)
        _mode = toenum(self.INCLINEPRG, mode)
        return self._request(
            2008,
            [_cmd.value, _mode.value]
        )

    def set_hand_dist(
        self,
        distance: float,
        offset: float,
        mode: INCLINEPRG | str = INCLINEPRG.AUTO
    ) -> GeoComResponse:
        _mode = toenum(self.INCLINEPRG, mode)
        return self._request(
            2019,
            [distance, offset, _mode.value]
        )

    def get_height(self) -> GeoComResponse:
        return self._request(
            2011,
            parsers={
                "height": float
            }
        )

    def set_height(
        self,
        height: float
    ) -> GeoComResponse:
        return self._request(
            2012,
            [height]
        )

    def get_atm_corr(self) -> GeoComResponse:
        return self._request(
            2029,
            parsers={
                "wavelength": float,
                "pressure": float,
                "drytemp": float,
                "wettemp": float
            }
        )

    def set_atm_corr(
        self,
        wavelength: float,
        pressure: float,
        drytemp: float,
        wettemp: float
    ) -> GeoComResponse:
        return self._request(
            2028,
            [wavelength, pressure, drytemp, wettemp]
        )

    def set_orientation(
        self,
        orientation: float
    ) -> GeoComResponse:
        return self._request(
            2113,
            [orientation]
        )

    def get_prism_corr(self) -> GeoComResponse:
        return self._request(
            2023,
            parsers={
                "const": float
            }
        )

    def get_refractive_corr(self) -> GeoComResponse:
        return self._request(
            2031,
            parsers={
                "enabled": bool,
                "earthradius": float,
                "scale": float
            }
        )

    def set_refractive_corr(
        self,
        enabled: bool,
        earthradius: float,
        scale: float
    ) -> GeoComResponse:
        return self._request(
            2030,
            [enabled, earthradius, scale]
        )

    def get_refractive_method(self) -> GeoComResponse:
        return self._request(
            2091,
            parsers={
                "method": int
            }
        )

    def set_refractive_method(
        self,
        method: int
    ) -> GeoComResponse:
        return self._request(
            2090,
            [method]
        )

    def get_station(self) -> GeoComResponse:
        response = self._request(
            2009,
            parsers={
                "east": float,
                "north": float,
                "height": float,
                "hi": float
            }
        )
        coord = Coordinate(
            response.params["east"],
            response.params["north"],
            response.params["height"]
        )
        response.params = {
            "coord": coord,
            "hi": response.params["hi"]
        }
        return response

    def set_station(
        self,
        coord: Coordinate,
        hi: float
    ) -> GeoComResponse:
        return self._request(
            2010,
            [coord.x, coord.y, coord.z, hi]
        )

    def get_atm_ppm(self) -> GeoComResponse:
        return self._request(
            2151,
            parsers={
                "ppm": float
            }
        )

    def set_atm_ppm(
        self,
        ppm: float
    ) -> GeoComResponse:
        return self._request(
            2148,
            [ppm]
        )

    def get_geo_ppm(self) -> GeoComResponse:
        return self._request(
            2154,
            parsers={
                "automatic": bool,
                "meridianscale": float,
                "meridianoffset": float,
                "heightreduction": float,
                "individual": float
            }
        )

    def set_geo_ppm(
        self,
        automatic: bool,
        meridianscale: float,
        meridianoffset: float,
        heightreduction: float,
        individual: float
    ) -> GeoComResponse:
        return self._request(
            2153,
            [
                automatic,
                meridianscale, meridianoffset,
                heightreduction, individual
            ]
        )

    def get_face(self) -> GeoComResponse:
        return self._request(
            2026,
            parsers={
                "face": self.FACE.parse
            }
        )

    def get_signal(self) -> GeoComResponse:
        return self._request(
            2022,
            parsers={
                "intensity": float,
                "time": int
            }
        )

    def get_ang_switch(self) -> GeoComResponse:
        return self._request(
            2014,
            parsers={
                "inclinecorr": bool,
                "stdaxiscorr": bool,
                "collimcorr": bool,
                "tiltaxiscorr": bool
            }
        )

    def get_incline_switch(self) -> GeoComResponse:
        return self._request(
            2007,
            parsers={
                "correction": self.ONOFF.parse
            }
        )

    def set_incline_switch(
        self,
        correction: ONOFF | str
    ) -> GeoComResponse:
        _corr = toenum(self.ONOFF, correction)
        return self._request(
            2006,
            [_corr.value]
        )

    def get_edm_mode(self) -> GeoComResponse:
        return self._request(
            2021,
            parsers={
                "mode": self.EMDMODE.parse
            }
        )

    def set_edm_mode(
        self,
        mode: EMDMODE | str
    ) -> GeoComResponse:
        _mode = toenum(self.EMDMODE, mode)
        return self._request(
            2020,
            [_mode.value]
        )

    def get_simple_coord(
        self,
        wait: int = 5000,
        mode: INCLINEPRG | str = INCLINEPRG.AUTO
    ) -> GeoComResponse:
        _mode = toenum(self.INCLINEPRG, mode)
        return self._request(
            2116,
            parsers={
                "east": float,
                "north": float,
                "height": float
            }
        )

    def if_data_atr_corr_error(self) -> GeoComResponse:
        return self._request(
            2114,
            parsers={
                "atrerror": bool
            }
        )

    def if_data_inc_corr_error(self) -> GeoComResponse:
        return self._request(
            2115,
            parsers={
                "inclineerror": bool
            }
        )

    def set_ang_switch(
        self,
        inclinecorr: bool,
        stdaxiscorr: bool,
        collimcorr: bool,
        tiltaxiscorr: bool
    ) -> GeoComResponse:
        return self._request(
            2016,
            [inclinecorr, stdaxiscorr, collimcorr, tiltaxiscorr]
        )

    def get_slope_dist_corr(self) -> GeoComResponse:
        return self._request(
            2126,
            parsers={
                "ppmcorr": float,
                "prismcorr": float
            }
        )
