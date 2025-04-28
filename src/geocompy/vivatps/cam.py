"""
Description
===========

Module: ``geocompy.vivatps.cam``

Definitions for the VivaTPS Camera subsystem.

Types
-----

- ``VivaTPSCAM``

"""
from __future__ import annotations

from enum import Enum

from ..data import (
    Coordinate,
    Vector,
    Angle,
    toenum,
    enumparser
)
from ..protocols import (
    GeoComSubsystem,
    GeoComResponse
)


class VivaTPSCAM(GeoComSubsystem):
    """
    Camera subsystem of the VivaTPS GeoCom protocol.

    This subsystem performs tasks relating to the overview camera and
    (on Nova instruments) the telescope mounted camera

    All functions require a valid GeoCom Imaging license.

    """
    class ONOFF(Enum):
        OFF = 0
        ON = 1

    class CAMTYPE(Enum):
        OVC = 0  # : Overview camera.
        OAC = 1  # : Telescope camera.

    class ZOOM(Enum):
        X1 = 1
        X2 = 2
        X4 = 4
        X8 = 8

    class RESOLUTION(Enum):
        P2560X1920 = 0
        P1280X960 = 3
        P640X480 = 4
        P720X240 = 5

    class COMPRESSION(Enum):
        JPEG = 0
        RAW = 1

    class WHITEBALANCE(Enum):
        AUTO = 0
        INDOOR = 1
        OUTDOOR = 2

    class JPEGQUALITY(Enum):
        STANDARD = 0
        BEST = 1
        IGNORE = 2

    def set_zoom_factor(
        self,
        zoom: ZOOM | str,
        camtype: CAMTYPE | str = CAMTYPE.OVC
    ) -> GeoComResponse[None]:
        """
        RPC 23608, ``CAM_SetZoomFactor``

        Sets the specified zoom factor on a camera device.

        Parameters
        ----------
        zoom : ZOOM | str
            Zoom level to set.
        camtype : CAMTYPE | str, optional
            Camera device, by default OVC

        Returns
        -------
        GeoComResponse
            - Error codes:
                - ``NA``: Imaging license not found.

        """
        _zoom = toenum(self.ZOOM, zoom)
        _camtype = toenum(self.CAMTYPE, camtype)
        return self._request(
            23608,
            [_camtype.value, _zoom.value]
        )

    def get_zoom_factor(
        self,
        camtype: CAMTYPE | str = CAMTYPE.OVC
    ) -> GeoComResponse[ZOOM]:
        """
        RPC 23609, ``CAM_GetZoomFactor``

        Sets the current zoom factor on a camera device.

        Parameters
        ----------
        camtype : CAMTYPE | str, optional
            Camera device, by default OVC

        Returns
        -------
        GeoComResponse
            - Params:
                - **zoom** (`ZOOM`): Current zoom level.
            - Error codes:
                - ``NA``: Imaging license not found.

        """
        _camtype = toenum(self.CAMTYPE, camtype)
        return self._request(
            23609,
            [_camtype.value],
            enumparser(self.ZOOM)
        )

    def get_cam_pos(
        self,
        camtype: CAMTYPE | str = CAMTYPE.OVC
    ) -> GeoComResponse[Coordinate]:
        """
        RPC 23611, ``CAM_GetCamPos``

        Gets the position of the overview camera, relative to the station
        coordinates.

        Parameters
        ----------
        camtype : CAMTYPE | str, optional
            Camera device, by default OVC

        Returns
        -------
        GeoComResponse
            - Params:
                - **coord** (`Coordinate`): Relative coordinates of the
                  camera.
            - Error codes:
                - ``NA``: Imaging license not found.

        See Also
        --------
        tmc.get_station
        get_cam_viewing_dir
        """
        def transform(
            params: tuple[float, float, float] | None
        ) -> Coordinate | None:
            if params is None:
                return None

            return Coordinate(
                params[0],
                params[1],
                params[2]
            )

        _camtype = toenum(self.CAMTYPE, camtype)
        response = self._request(
            23611,
            [_camtype.value],
            (
                float,
                float,
                float
            )
        )
        return response.map_params(transform)

    def get_cam_viewing_dir(
        self,
        dist: float,
        camtype: CAMTYPE | str = CAMTYPE.OVC
    ) -> GeoComResponse[Vector]:
        """
        RPC 23611, ``CAM_GetCamViewingDir``

        Gets the view vector of the overview camera relative to its
        coordinates. The viewing vector is a 3D vector along the optical
        axis of the camera, with the given slope distance length.

        Parameters
        ----------
        dist : float
            View vector length.
        camtype : CAMTYPE | str, optional
            Camera device, by default OVC

        Returns
        -------
        GeoComResponse
            - Params:
                - **coord** (`Coordinate`): Viewing vector.
            - Error codes:
                - ``NA``: Imaging license not found.

        See Also
        --------
        get_cam_pos
        """
        def transform(
            params: tuple[float, float, float] | None
        ) -> Vector | None:
            if params is None:
                return None

            return Vector(
                params[0],
                params[1],
                params[2]
            )

        _camtype = toenum(self.CAMTYPE, camtype)
        response = self._request(
            23613,
            [_camtype.value, dist],
            (
                float,
                float,
                float
            )
        )

        return response.map_params(transform)

    def get_camera_fov(
        self,
        camtype: CAMTYPE | str = CAMTYPE.OVC,
        zoom: ZOOM | str = ZOOM.X1
    ) -> GeoComResponse[tuple[Angle, Angle]]:
        """
        RPC 23619, ``CAM_GetCameraFoV``

        Gets field of view of the overview camera for a given zoom level.

        Parameters
        ----------
        camtype : CAMTYPE | str, optional
            Camera device, by default OVC
        zoom : ZOOM | str, optional
            Zoom level, by default X1

        Returns
        -------
        GeoComResponse
            - Params:
                - **hz** (`Angle`): Horizontal field of view.
                - **v** (`Angle`): Vertical field of view.
            - Error codes:
                - ``IVPARAM``: Invalid parameter.
                - ``NA``: Imaging license not found.

        """
        _camtype = toenum(self.CAMTYPE, camtype)
        _zoom = toenum(self.ZOOM, zoom)
        return self._request(
            23619,
            [_camtype.value, _zoom.value],
            (
                Angle.parse,
                Angle.parse
            )
        )

    def set_actual_image_name(
        self,
        name: str,
        number: int,
        camtype: CAMTYPE | str = CAMTYPE.OVC
    ) -> GeoComResponse[None]:
        """
        RPC 23619, ``CAM_SetActualImageName``

        Sets the name and number of the next image to be taken.

        Parameters
        ----------
        name : str
            Image name.
        number : int
            Image number.
        camtype : CAMTYPE | str, optional
            Camera device, by default OVC

        Returns
        -------
        GeoComResponse
            - Error codes:
                - ``NA``: Imaging license not found.

        See Also
        --------
        take_image
        """
        _camtype = toenum(self.CAMTYPE, camtype)
        return self._request(
            23622,
            [_camtype.value, name, number]
        )

    def take_image(
        self,
        camtype: CAMTYPE | str = CAMTYPE.OVC
    ) -> GeoComResponse[None]:
        """
        RPC 23623, ``CAM_TakeImage``

        Takes a new image with the selected camera.

        Parameters
        ----------
        camtype : CAMTYPE | str, optional
            Camera device, by default OVC

        Returns
        -------
        GeoComResponse
            - Error codes:
                - ``CAM_IMAGE_SAVING_ERROR``: Error while saving, SD card
                  might not be available.
                - ``NA``: Imaging license not found.

        See Also
        --------
        is_camera_ready
        set_camera_properties
        set_actual_image_name
        """
        _camtype = toenum(self.CAMTYPE, camtype)
        return self._request(
            23623,
            [_camtype.value]
        )

    def ovc_get_act_camera_center(self) -> GeoComResponse[tuple[float, float]]:
        """
        RPC 23624, ``CAM_GetActCameraCenter``

        Calculates the position of the optical crosshair on the overview
        camera image, at a previously set distance.

        Returns
        -------
        GeoComResponse
            - Params:
                - **x** (`float`): Horizontal position of corsshair on
                  image.
                - **y** (`float`): Vertical position of corsshair on
                  image.
            - Error codes:
                - ``NA``: Imaging license not found.

        See Also
        --------
        ovc_set_act_distance
        set_camera_properties
        """
        return self._request(
            23624,
            parsers=(
                float,
                float
            )
        )

    def ovc_set_act_distance(
        self,
        dist: float,
        isface1: bool = True
    ) -> GeoComResponse[None]:
        """
        RPC 23625, ``CAM_GetActDistance``

        Sets distance to the current target.

        Parameters
        ----------
        dist : float
            Target distance.
        isface1 : float
            Telescope is in face 1 position.

        Returns
        -------
        GeoComResponse
            - Error codes:
                - ``NA``: Imaging license not found.

        See Also
        --------
        ovc_get_act_camera_center
        """
        return self._request(
            23625,
            [dist, isface1]
        )

    def set_whitebalance_mode(
        self,
        whitebalance: WHITEBALANCE | str = WHITEBALANCE.AUTO,
        camtype: CAMTYPE | str = CAMTYPE.OVC
    ) -> GeoComResponse[None]:
        """
        RPC 23626, ``CAM_SetWhiteBalanceMode``

        Sets the white balance mode for a camera device.

        Parameters
        ----------
        whitebalance : WHITEBALANCE | str, optional
            White balance mode, by default WHITEBALANCE.AUTO
        camtype : CAMTYPE | str, optional
            Camera device, by default OVC

        Returns
        -------
        GeoComResponse
            - Error codes:
                - ``NA``: Imaging license not found.

        See Also
        --------
        take_image
        """
        _wb = toenum(self.WHITEBALANCE, whitebalance)
        _camtype = toenum(self.CAMTYPE, camtype)
        return self._request(
            23626,
            [_camtype.value, _wb.value]
        )

    def is_camera_ready(
        self,
        camtype: CAMTYPE | str = CAMTYPE.OVC
    ) -> GeoComResponse[None]:
        """
        RPC 23627, ``CAM_IsCameraReady``

        Checks if a camera is ready for use.

        Parameters
        ----------
        camtype : CAMTYPE | str, optional
            Camera device, by default OVC

        Returns
        -------
        GeoComResponse
            - Error codes:
                - ``NA``: Imaging license not found.
                - ``CAM_NOT_READY``: Camera is turned off, or currently
                  starting up.

        See Also
        --------
        get_camera_power_switch
        set_camera_power_switch
        wait_for_camera_ready
        """
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
    ) -> GeoComResponse[None]:
        """
        RPC 23633, ``CAM_SetCameraProperties``

        Sets camera parameters.

        Parameters
        ----------
        resolution : RESOLUTION | str
            Image resolution.
        compression : COMPRESSION | str
            Image compression.
        jpegquality : JPEGQUALITY | str
            JPEG image compression quality.
        camtype : CAMTYPE | str, optional
            Camera device, by default OVC

        Returns
        -------
        GeoComResponse
            - Error codes:
                - ``NA``: Imaging license not found.

        See Also
        --------
        is_camera_ready
        set_actual_image_name
        take_image
        """
        _res = toenum(self.RESOLUTION, resolution)
        _comp = toenum(self.COMPRESSION, compression)
        _qual = toenum(self.JPEGQUALITY, jpegquality)
        _camtype = toenum(self.CAMTYPE, camtype)
        return self._request(
            23633,
            [_camtype.value, _res.value, _comp.value, _qual.value]
        )

    def get_camera_power_switch(
        self,
        camtype: CAMTYPE | str = CAMTYPE.OVC
    ) -> GeoComResponse[ONOFF]:
        """
        RPC 23636, ``CAM_GetCameraPowerSwitch``

        Gets the current state of the camera.

        Parameters
        ----------
        camtype : CAMTYPE | str, optional
            Camera device, by default OVC

        Returns
        -------
        GeoComResponse
            - Params:
                - **state** (`ONOFF`): Current state of camera.
            - Error codes:
                - ``NA``: Imaging license not found.

        See Also
        --------
        is_camera_ready
        set_camera_power_switch
        wait_for_camera_ready
        """
        _camtype = toenum(self.CAMTYPE, camtype)
        return self._request(
            23636,
            [_camtype.value],
            enumparser(self.ONOFF)
        )

    def set_camera_power_switch(
        self,
        state: ONOFF | str,
        camtype: CAMTYPE | str = CAMTYPE.OVC
    ) -> GeoComResponse[None]:
        """
        RPC 23637, ``CAM_SetCameraPowerSwitch``

        Sets the state of the camera.

        Parameters
        ----------
        state : ONOFF | str
            New state of the camera.
        camtype : CAMTYPE | str, optional
            Camera device, by default OVC

        Returns
        -------
        GeoComResponse
            - Error codes:
                - ``NA``: Imaging license not found.

        See Also
        --------
        is_camera_ready
        get_camera_power_switch
        wait_for_camera_ready
        """
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
    ) -> GeoComResponse[None]:
        """
        RPC 23638, ``CAM_WaitForCameraReady``

        Waits for the camera device to become ready for use.

        Parameters
        ----------
        wait : int, optional
            Time to wait for the camera to come online.
        camtype : CAMTYPE | str, optional
            Camera device, by default OVC

        Returns
        -------
        GeoComResponse
            - Error codes:
                - ``NA``: Imaging license not found.
                - ``TIMEOUT``: Camera did not become usable within the
                  specified time.

        See Also
        --------
        is_camera_ready
        get_camera_power_switch
        set_camera_power_switch
        """
        _camtype = toenum(self.CAMTYPE, camtype)
        return self._request(
            23638,
            [_camtype.value, wait]
        )

    def af_set_motor_position(
        self,
        position: int
    ) -> GeoComResponse[None]:
        """
        RPC 23645, ``CAM_AF_SetMotorPosition``

        Sets the autofocus motor to a specific position.

        Parameters
        ----------
        position : int
            Autofocus motor position.

        Returns
        -------
        GeoComResponse
            - Error codes:
                - ``NA``: Imaging license not found.

        See Also
        --------
        af_get_motor_position
        """
        return self._request(
            23645,
            [position]
        )

    def af_get_motor_position(self) -> GeoComResponse[int]:
        """
        RPC 23644, ``CAM_AF_GetMotorPosition``

        Gets the current position of the autofocus motor.

        Returns
        -------
        GeoComResponse
            - Params:
                - **position** (`int`): Autofocus motor position.
            - Error codes:
                - ``NA``: Imaging license not found.

        See Also
        --------
        af_set_motor_position
        """
        return self._request(
            23644,
            parsers=int
        )

    def af_continuous_autofocus(
        self,
        start: bool
    ) -> GeoComResponse[None]:
        """
        RPC 23669, ``CAM_AF_ContinuousAutofocus``

        Starts or stops the continuous autofocus.

        Parameters
        ----------
        start : bool
            Start the continuous autofocus.

        Returns
        -------
        GeoComResponse
            - Error codes:
                - ``NA``: Imaging license not found.

        """
        return self._request(
            23669,
            [start]
        )

    def af_posit_focus_motor_to_dist(
        self,
        dist: float
    ) -> GeoComResponse[None]:
        """
        RPC 23652, ``CAM_AF_PositFocusMotorToDist``

        Sets the autofocus motor to the specified distance.

        Parameters
        ----------
        dist : float
            Distance to focus to.

        Returns
        -------
        GeoComResponse
            - Error codes:
                - ``NA``: Imaging license not found.

        """
        return self._request(
            23652,
            [dist]
        )

    def af_posit_focus_motor_to_infinity(self) -> GeoComResponse[None]:
        """
        RPC 23677, ``CAM_AF_PositFocusMotorToInfinity``

        Sets the autofocus motor to focus to infinity.

        Returns
        -------
        GeoComResponse
            - Error codes:
                - ``NA``: Imaging license not found.

        """
        return self._request(23677)

    def at_singleshot_autofocus(self) -> GeoComResponse[None]:
        """
        RPC 23677, ``CAM_AF_SingleShotAutofocus``

        Focuses current target.

        Returns
        -------
        GeoComResponse
            - Error codes:
                - ``NA``: Imaging license not found.

        """
        return self._request(23662)

    def af_focus_contrast_around_current(
        self,
        steps: int
    ) -> GeoComResponse[None]:
        """
        RPC 23663, ``CAM_AF_FocusContrastAroundCurrent``

        Focuses current target by contrast around target.

        Parameters
        ----------
        steps : int
            Focus iteration steps.

        Returns
        -------
        GeoComResponse
            - Error codes:
                - ``NA``: Imaging license not found.

        """
        return self._request(
            23663,
            [steps]
        )

    def get_chip_window_size(
        self,
        camtype: CAMTYPE | str = CAMTYPE.OVC
    ) -> GeoComResponse[tuple[float, float]]:
        """
        RPC 23668, ``CAM_GetChipWindowSize``

        Gets the size of the camera chip.

        Parameters
        ----------
        camtype : CAMTYPE | str, optional
            Camera device, by default OVC

        Returns
        -------
        GeoComResponse
            - Params:
                - **width** (`float`): Sensor width.
                - **height** (`float`): Sensor height.
            - Error codes:
                - ``NA``: Imaging license not found.

        """
        _camtype = toenum(self.CAMTYPE, camtype)
        return self._request(
            23668,
            [_camtype.value],
            (
                float,
                float
            )
        )

    def oac_get_crosshair_pos(self) -> GeoComResponse[tuple[int, int]]:
        """
        RPC 23671, ``CAM_OAC_GetCrossHairPos``

        Gets the position of the crosshair in the actual camera resolution.

        Returns
        -------
        GeoComResponse
            - Params:
                - **x** (`int`): Horizontal position.
                - **y** (`int`): Vertical position.
            - Error codes:
                - ``NA``: Imaging license not found.

        """
        return self._request(
            23671,
            parsers=(
                int,
                int
            )
        )

    def ovc_read_inter_orient(
        self,
        calibrated: bool = True
    ) -> GeoComResponse[tuple[float, float, float, float]]:
        """
        RPC 23602, ``CAM_OAC_ReadInterOrient``

        Gets the interior orientation parameters of the camera.

        Parameters
        ----------
        calibrated : bool, optional
            Use calibrated data.

        Returns
        -------
        GeoComResponse
            - Params:
                - **x** (`float`): Horizontal position of principal point.
                - **y** (`float`): Vertical position of principal point.
                - **f** (`float`): Focus length.
                - **p** (`float`): Pixel size.
            - Error codes:
                - ``NA``: Imaging license not found.

        """
        return self._request(
            23602,
            [calibrated],
            (
                float,
                float,
                float,
                float
            )
        )

    def ovc_read_exter_orient(
        self,
        calibrated: bool = True
    ) -> GeoComResponse[tuple[Coordinate, Angle, Angle, Angle]]:
        """
        RPC 23603, ``CAM_OAC_ReadExterOrient``

        Gets the exterior orientation parameters of the camera.

        Parameters
        ----------
        calibrated : bool, optional
            Use calibrated data.

        Returns
        -------
        GeoComResponse
            - Params:
                - **coord** (`Coordinate`): Camera coordinates.
                - **phi** (`Angle`): Azimut angle.
                - **theta** (`Angle`): Zenith angle.
                - **kappa** (`Angle`): Tilt angle.
            - Error codes:
                - ``NA``: Imaging license not found.

        """
        def transform(
            params: tuple[float, float, float, Angle, Angle, Angle] | None
        ) -> tuple[Coordinate, Angle, Angle, Angle] | None:
            if params is None:
                return None
            return (
                Coordinate(
                    params[0],
                    params[1],
                    params[2]
                ),
                params[3],
                params[4],
                params[5]
            )

        response = self._request(
            23603,
            [calibrated],
            (
                float,
                float,
                float,
                Angle.parse,
                Angle.parse,
                Angle.parse
            )
        )

        return response.map_params(transform)

    def start_remote_video(
        self,
        fps: int,
        bitrate: int,
        camtype: CAMTYPE | str = CAMTYPE.OVC
    ) -> GeoComResponse[None]:
        """
        RPC 23675, ``CAM_StartRemoteVideo``

        Starts a remote video stream that can be watched when connected
        wirelessly to the instrument. Networkstrea:
        ``rtsp://192.168.254.3/TSCame``.

        Parameters
        ----------
        fps : int
            Frame rate 3/5/10 [Hz].
        bitrate : int
            Video bit rate in [100; 6144] range [kbps].
        camtype : CAMTYPE | str, optional
            Camera device, by default OVC

        Returns
        -------
        GeoComResponse
            - Error codes:
                - ``NA``: Imaging license not found.

        """
        _camtype = toenum(self.CAMTYPE, camtype)
        return self._request(
            23675,
            [_camtype.value, fps, bitrate]
        )

    def stop_remote_video(self) -> GeoComResponse[None]:
        """
        RPC 23676, ``CAM_StopRemoteVideo``

        Stops the remote video stream.

        Returns
        -------
        GeoComResponse
            - Error codes:
                - ``NA``: Imaging license not found.

        """
        return self._request(23676)
