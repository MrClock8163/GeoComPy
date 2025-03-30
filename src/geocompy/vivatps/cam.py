from __future__ import annotations

from enum import Enum, Flag

from .. import (
    GeoComSubsystem,
    GeoComResponse
)
from ..data import (
    Coordinate,
    Angle,
    toenum
)


class VivaTPSCAM(GeoComSubsystem):
    class ONOFF(Enum):
        @classmethod
        def parse(cls, value: str) -> VivaTPSCAM.ONOFF:
            return cls(int(value))

        OFF = 0
        ON = 1

    class CAMTYPE(Enum):
        @classmethod
        def parse(cls, value: str) -> VivaTPSCAM.CAMTYPE:
            return cls(int(value))
        
        OVC = 0
        OAC = 1

    class ZOOM(Enum):
        @classmethod
        def parse(cls, value: str) -> VivaTPSCAM.ZOOM:
            return cls(int(value))
        
        X1 = 1
        X2 = 2
        X4 = 4
        X8 = 8

    class RESOLUTION(Enum):
        @classmethod
        def parse(cls, value: str) -> VivaTPSCAM.RESOLUTION:
            return cls(int(value))
        
        P2560X1920 = 0
        P1280X960 = 3
        P640X480 = 4
        P720X240 = 5

    class COMPRESSION(Enum):
        @classmethod
        def parse(cls, value: str) -> VivaTPSCAM.COMPRESSION:
            return cls(int(value))

        JPEG = 0
        RAW = 1

    class WHITEBALANCE(Enum):
        @classmethod
        def parse(cls, value: str) -> VivaTPSCAM.WHITEBALANCE:
            return cls(int(value))

        AUTO = 0
        INDOOR = 1
        OUTDOOR = 2

    class JPEGQUALITY(Enum):
        @classmethod
        def parse(cls, value: str) -> VivaTPSCAM.JPEGQUALITY:
            return cls(int(value))

        STANDARD = 0
        BEST = 1
        IGNORE = 2
    
    def set_zoom_factor(
        self,
        zoom: ZOOM | str,
        camtype: CAMTYPE | str = CAMTYPE.OVC
    ) -> GeoComResponse:
        _zoom = toenum(self.ZOOM, zoom)
        _camtype = toenum(self.CAMTYPE, camtype)
        return self._request(
            23608,
            [_camtype.value, _zoom.value]
        )

    def get_zoom_factor(
        self,
        camtype: CAMTYPE | str = CAMTYPE.OVC
    ) -> GeoComResponse:
        _camtype = toenum(self.CAMTYPE, camtype)
        return self._request(
            23609,
            [_camtype.value],
            {
                "zoom": self.ZOOM.parse
            }
        )

    def get_cam_pos(
        self,
        camtype: CAMTYPE | str = CAMTYPE.OVC
    ) -> GeoComResponse:
        _camtype = toenum(self.CAMTYPE, camtype)
        response = self._request(
            23611,
            [_camtype.value],
            {
                "east": float,
                "north": float,
                "height": float
            }
        )
        coord = Coordinate(
            response.params["east"],
            response.params["north"],
            response.params["height"]
        )
        response.params = {
            "coord": coord
        }

        return response
    
    def get_cam_viewing_dir(
        self,
        dist: float,
        camtype: CAMTYPE | str = CAMTYPE.OVC
    ) -> GeoComResponse:
        _camtype = toenum(self.CAMTYPE, camtype)
        response = self._request(
            23613,
            [_camtype.value, dist],
            {
                "east": float,
                "north": float,
                "height": float
            }
        )
        coord = Coordinate(
            response.params["east"],
            response.params["north"],
            response.params["height"]
        )
        response.params = {
            "coord": coord
        }

        return response

    def get_camera_fov(
        self,
        camtype: CAMTYPE | str = CAMTYPE.OVC,
        zoom: ZOOM | str = ZOOM.X1
    ) -> GeoComResponse:
        _camtype = toenum(self.CAMTYPE, camtype)
        _zoom = toenum(self.ZOOM, zoom)
        return self._request(
            23619,
            [_camtype.value, _zoom.value],
            {
                "hz": Angle.parse,
                "v": Angle.parse
            }
        )
    
    def set_actual_image_name(
        self,
        name: str,
        number: int,
        camtype: CAMTYPE | str = CAMTYPE.OVC
    ) -> GeoComResponse:
        _camtype = toenum(self.CAMTYPE, camtype)
        return self._request(
            23622,
            [_camtype.value, name, number]
        )

    def take_image(
        self,
        camtype: CAMTYPE | str = CAMTYPE.OVC
    ) -> GeoComResponse:
        _camtype = toenum(self.CAMTYPE, camtype)
        return self._request(
            23623,
            [_camtype]
        )
    
    def ovc_get_act_camera_center(self) -> GeoComResponse:
        return self._request(
            23624,
            parsers={
                "x": float,
                "y": float
            }
        )

    def ovc_set_act_distance(
        self,
        dist: float,
        isface1: bool = True
    ) -> GeoComResponse:
        return self._request(
            23625,
            [dist, isface1]
        )
    
    def set_whitebalance_mode(
        self,
        whitebalance: WHITEBALANCE | str = WHITEBALANCE.AUTO,
        camtype: CAMTYPE | str = CAMTYPE.OVC
    ) -> GeoComResponse:
        _wb = toenum(self.WHITEBALANCE, whitebalance)
        _camtype = toenum(self.CAMTYPE, camtype)
        return self._request(
            23626,
            [_camtype.value, _wb.value]
        )
    
    def is_camera_ready(
        self,
        camtype: CAMTYPE | str = CAMTYPE.OVC
    ) -> GeoComResponse:
        _camtype = toenum(self.CAMTYPE, camtype)
        return self._request(
            23627,
            [_camtype.value]
        )
    
    def set_camera_properties(
        self,
        resolution: RESOLUTION | str,
        compression: COMPRESSION | str,
        jpegquality: JPEGQUALITY | str,
        camtype: CAMTYPE | str = CAMTYPE.OVC   
    ) -> GeoComResponse:
        _res = toenum(self.RESOLUTION, resolution)
        _comp = toenum(self.COMPRESSION, compression)
        _qual = toenum(self.JPEGQUALITY, jpegquality)
        _camtype = toenum(self.CAMTYPE, camtype)
        return self._request(
            236233,
            [_camtype.value, _res.value, _comp.value, _qual.value]
        )
    
    def get_camera_power_switch(
        self,
        camtype: CAMTYPE | str = CAMTYPE.OVC
    ) -> GeoComResponse:
        _camtype = toenum(self.CAMTYPE, camtype)
        return self._request(
            23636,
            [_camtype.value],
            {
                "state": self.ONOFF.parse
            }
        )
    
    def set_camera_power_switch(
        self,
        state: ONOFF | str,
        camtype: CAMTYPE | str = CAMTYPE.OVC
    ) -> GeoComResponse:
        _state = toenum(self.ONOFF, state)
        _camtype = toenum(self.CAMTYPE, camtype)
        return self._request(
            23637,
            [_camtype.value, _state.value]
        )
    
    def wait_for_camera_ready(
        self,
        wait: int = 30_000,
        camtype: CAMTYPE | str = CAMTYPE.OVC
    ) -> GeoComResponse:
        _camtype = toenum(self.CAMTYPE, camtype)
        return self._request(
            23638,
            [_camtype.value, wait]
        )

    def af_set_motor_position(
        self,
        position: int
    ) -> GeoComResponse:
        return self._request(
            23645,
            [position]
        )
    
    def af_get_motor_position(self) -> GeoComResponse:
        return self._request(
            23644,
            parsers={
                "position": int
            }
        )
    
    def af_continuous_autofocus(
        self,
        start: bool
    ) -> GeoComResponse:
        return self._request(
            23669,
            [start]
        )
    
    def af_posit_focus_motor_to_dist(
        self,
        dist: float
    ) -> GeoComResponse:
        return self._request(
            23652,
            [dist]
        )
    
    def af_posit_focus_motor_to_infinity(self) -> GeoComResponse:
        return self._request(23677)
    
    def at_singleshot_autofocus(self) -> GeoComResponse:
        return self._request(23662)
    
    def af_focus_contrast_around_current(
        self,
        steps: int
    ) -> GeoComResponse:
        return self._request(
            23663,
            [steps]
        )
    
    def get_chip_window_size(
        self,
        camtype: CAMTYPE | str = CAMTYPE.OVC
    ) -> GeoComResponse:
        _camtype = toenum(self.CAMTYPE, camtype)
        return self._request(
            23668,
            [_camtype.value],
            {
                "width": float,
                "height": float
            }
        )
    
    def oac_get_crosshair_pos(self) -> GeoComResponse:
        return self._request(
            23671,
            parsers={
                "x": float,
                "y": float
            }
        )
    
    def ovc_read_inter_orient(
        self,
        calibration: bool = True
    ) -> GeoComResponse:
        return self._request(
            23602,
            [calibration],
            {
                "x": float,
                "y": float,
                "f": float,
                "p": float
            }
        )
    
    def ovc_read_exter_orient(
        self,
        calibration: bool = True
    ) -> GeoComResponse:
        response = self._request(
            23603,
            [calibration],
            {
                "x": float,
                "y": float,
                "z": float,
                "phi": Angle.parse,
                "theta": Angle.parse,
                "kappa": Angle.parse
            }
        )
        coord = Coordinate(
            response.params["x"],
            response.params["y"],
            response.params["z"]
        )
        response.params = {
            "coord": coord,
            "phi": response.params["phi"],
            "theta": response.params["theta"],
            "kappa": response.params["kappa"]
        }

        return response
    
    def start_remote_video(
        self,
        fps: int,
        bitrate: int,
        camtype: CAMTYPE | str = CAMTYPE.OVC
    ) -> GeoComResponse:
        _camtype = toenum(self.CAMTYPE, camtype)
        return self._request(
            23675,
            [_camtype.value, fps, bitrate]
        )
    
    def stop_remote_video(self) -> GeoComResponse:
        return self._request(23676)
