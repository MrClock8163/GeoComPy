"""
Description
===========

Module: ``geocompy.geo.cam``

Definitions for the GeoCom Camera subsystem.

Types
-----

- ``GeoComCAM``

"""
from __future__ import annotations

from ..data import (
    Coordinate,
    Vector,
    Angle,
    get_enum,
    get_enum_parser,
    parse_bool
)
from .gcdata import (
    Camera,
    Compression,
    JPEGQuality,
    Resolution,
    WhiteBalance,
    Zoom
)
from .gctypes import (
    GeoComSubsystem,
    GeoComResponse
)


class GeoComCAM(GeoComSubsystem):
    """
    Camera subsystem of the GeoCom protocol.

    This subsystem performs tasks relating to the overview camera and
    (on Nova instruments) the telescope mounted camera

    All functions require a valid GeoCom Imaging license.

    .. versionadded:: GeoCom-VivaTPS
    """

    def set_zoom(
        self,
        zoom: Zoom | str,
        camera: Camera | str = Camera.OVERVIEW
    ) -> GeoComResponse[None]:
        """
        RPC 23608, ``CAM_SetZoomFactor``

        Sets the specified zoom factor on a camera device.

        Parameters
        ----------
        zoom : Zoom | str
            Zoom level to set.
        camera : Camera | str, optional
            Camera device, by default OVERVIEW

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``NA``: Imaging license not found.

        """
        _zoom = get_enum(Zoom, zoom)
        _camera = get_enum(Camera, camera)
        return self._request(
            23608,
            [_camera, _zoom]
        )

    def get_zoom(
        self,
        camera: Camera | str = Camera.OVERVIEW
    ) -> GeoComResponse[Zoom]:
        """
        RPC 23609, ``CAM_GetZoomFactor``

        Sets the current zoom factor on a camera device.

        Parameters
        ----------
        camera : Camera | str, optional
            Camera device, by default OVERVIEW

        Returns
        -------
        GeoComResponse
            Params:
                - `Zoom`: Current zoom level.

            Error codes:
                - ``NA``: Imaging license not found.

        """
        _camera = get_enum(Camera, camera)
        return self._request(
            23609,
            [_camera],
            get_enum_parser(Zoom)
        )

    def get_camera_position(
        self,
        camera: Camera | str = Camera.OVERVIEW
    ) -> GeoComResponse[Coordinate]:
        """
        RPC 23611, ``CAM_GetCamPos``

        Gets the position of the overview camera, relative to the station
        coordinates.

        Parameters
        ----------
        camera : Camera | str, optional
            Camera device, by default OVERVIEW

        Returns
        -------
        GeoComResponse
            Params:
                - `Coordinate`: Relative coordinates of the
                  camera.
            Error codes:
                - ``NA``: Imaging license not found.

        See Also
        --------
        tmc.get_station
        get_camera_direction
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

        _camera = get_enum(Camera, camera)
        response = self._request(
            23611,
            [_camera],
            (
                float,
                float,
                float
            )
        )
        return response.map_params(transform)

    def get_camera_direction(
        self,
        dist: float,
        camera: Camera | str = Camera.OVERVIEW
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
        camera : Camera | str, optional
            Camera device, by default OVERVIEW

        Returns
        -------
        GeoComResponse
            Params:
                - `Coordinate`: Viewing vector.

            Error codes:
                - ``NA``: Imaging license not found.

        See Also
        --------
        get_camera_position
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

        _camera = get_enum(Camera, camera)
        response = self._request(
            23613,
            [_camera, dist],
            (
                float,
                float,
                float
            )
        )

        return response.map_params(transform)

    def get_camera_fov(
        self,
        camera: Camera | str = Camera.OVERVIEW,
        zoom: Zoom | str = Zoom.X1
    ) -> GeoComResponse[tuple[Angle, Angle]]:
        """
        RPC 23619, ``CAM_GetCameraFoV``

        Gets field of view of the overview camera for a given zoom level.

        Parameters
        ----------
        camera : Camera | str, optional
            Camera device, by default OVERVIEW
        zoom : Zoom | str, optional
            Zoom level, by default X1

        Returns
        -------
        GeoComResponse
            Params:
                - `Angle`: Horizontal field of view.
                - `Angle`: Vertical field of view.

            Error codes:
                - ``IVPARAM``: Invalid parameter.
                - ``NA``: Imaging license not found.

        """
        _camera = get_enum(Camera, camera)
        _zoom = get_enum(Zoom, zoom)
        return self._request(
            23619,
            [_camera, _zoom],
            (
                Angle.parse,
                Angle.parse
            )
        )

    def set_actual_image_name(
        self,
        name: str,
        number: int,
        camera: Camera | str = Camera.OVERVIEW
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
        camera : Camera | str, optional
            Camera device, by default OVERVIEW

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``NA``: Imaging license not found.

        See Also
        --------
        take_image
        """
        _camera = get_enum(Camera, camera)
        return self._request(
            23622,
            [_camera, name, number]
        )

    def take_image(
        self,
        camera: Camera | str = Camera.OVERVIEW
    ) -> GeoComResponse[None]:
        """
        RPC 23623, ``CAM_TakeImage``

        Takes a new image with the selected camera.

        Parameters
        ----------
        camera : Camera | str, optional
            Camera device, by default OVERVIEW

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``CAM_IMAGE_SAVING_ERROR``: Error while saving, SD card
                  might not be available.
                - ``NA``: Imaging license not found.

        See Also
        --------
        is_camera_ready
        set_camera_properties
        set_actual_image_name
        """
        _camera = get_enum(Camera, camera)
        return self._request(
            23623,
            [_camera]
        )

    def get_overview_crosshair(self) -> GeoComResponse[tuple[float, float]]:
        """
        RPC 23624, ``CAM_GetActCameraCenter``

        Calculates the position of the optical crosshair on the overview
        camera image, at a previously set distance.

        Returns
        -------
        GeoComResponse
            Params:
                - `float`: Horizontal position of corsshair on
                  image.
                - `float`: Vertical position of corsshair on
                  image.
            Error codes:
                - ``NA``: Imaging license not found.

        See Also
        --------
        set_overview_distance
        set_camera_properties
        """
        return self._request(
            23624,
            parsers=(
                float,
                float
            )
        )

    def set_overview_distance(
        self,
        dist: float,
        face1: bool = True
    ) -> GeoComResponse[None]:
        """
        RPC 23625, ``CAM_GetActDistance``

        Sets distance to the current target.

        Parameters
        ----------
        dist : float
            Target distance.
        face1 : float
            Telescope is in face 1 position.

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``NA``: Imaging license not found.

        See Also
        --------
        get_overview_crosshair
        """
        return self._request(
            23625,
            [dist, face1]
        )

    def set_whitebalance(
        self,
        whitebalance: WhiteBalance | str = WhiteBalance.AUTO,
        camera: Camera | str = Camera.OVERVIEW
    ) -> GeoComResponse[None]:
        """
        RPC 23626, ``CAM_SetWhiteBalanceMode``

        Sets the white balance mode for a camera device.

        Parameters
        ----------
        whitebalance : WhiteBalance | str, optional
            White balance mode, by default WhiteBalance.AUTO
        camera : Camera | str, optional
            Camera device, by default OVERVIEW

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``NA``: Imaging license not found.

        See Also
        --------
        take_image
        """
        _wb = get_enum(WhiteBalance, whitebalance)
        _camera = get_enum(Camera, camera)
        return self._request(
            23626,
            [_camera, _wb]
        )

    def is_camera_ready(
        self,
        camera: Camera | str = Camera.OVERVIEW
    ) -> GeoComResponse[None]:
        """
        RPC 23627, ``CAM_IsCameraReady``

        Checks if a camera is ready for use.

        Parameters
        ----------
        camera : Camera | str, optional
            Camera device, by default OVERVIEW

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``NA``: Imaging license not found.
                - ``CAM_NOT_READY``: Camera is turned off, or currently
                  starting up.

        See Also
        --------
        get_camera_power_status
        switch_camera_power
        wait_for_camera_ready
        """
        _camera = get_enum(Camera, camera)
        return self._request(
            23627,
            [_camera]
        )

    def set_camera_properties(
        self,
        resolution: Resolution | str,
        compression: Compression | str,
        jpegquality: JPEGQuality | str,
        camera: Camera | str = Camera.OVERVIEW
    ) -> GeoComResponse[None]:
        """
        RPC 23633, ``CAM_SetCameraProperties``

        Sets camera parameters.

        Parameters
        ----------
        resolution : Resolution | str
            Image resolution.
        compression : Compression | str
            Image compression.
        jpegquality : JPEGQuality | str
            JPEG image compression quality.
        camera : Camera | str, optional
            Camera device, by default OVERVIEW

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``NA``: Imaging license not found.

        See Also
        --------
        is_camera_ready
        set_actual_image_name
        take_image
        """
        _res = get_enum(Resolution, resolution)
        _comp = get_enum(Compression, compression)
        _qual = get_enum(JPEGQuality, jpegquality)
        _camera = get_enum(Camera, camera)
        return self._request(
            23633,
            [_camera, _res, _comp, _qual]
        )

    def get_camera_power_status(
        self,
        camera: Camera | str = Camera.OVERVIEW
    ) -> GeoComResponse[bool]:
        """
        RPC 23636, ``CAM_GetCameraPowerSwitch``

        Gets the current state of the camera.

        Parameters
        ----------
        camera : Camera | str, optional
            Camera device, by default OVERVIEW

        Returns
        -------
        GeoComResponse
            Params:
                - `bool`: Camera is powered and active.

            Error codes:
                - ``NA``: Imaging license not found.

        See Also
        --------
        is_camera_ready
        switch_camera_power
        wait_for_camera_ready
        """
        _camera = get_enum(Camera, camera)
        return self._request(
            23636,
            [_camera],
            parse_bool
        )

    def switch_camera_power(
        self,
        activate: bool,
        camera: Camera | str = Camera.OVERVIEW
    ) -> GeoComResponse[None]:
        """
        RPC 23637, ``CAM_SetCameraPowerSwitch``

        Sets the state of the camera.

        Parameters
        ----------
        activate : bool
            Power up and activate camera.
        camera : Camera | str, optional
            Camera device, by default OVERVIEW

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``NA``: Imaging license not found.

        See Also
        --------
        is_camera_ready
        get_camera_power_status
        wait_for_camera_ready
        """
        _camera = get_enum(Camera, camera)
        return self._request(
            23637,
            [_camera, activate]
        )

    def wait_for_camera_ready(
        self,
        wait: int = 30,
        camera: Camera | str = Camera.OVERVIEW
    ) -> GeoComResponse[None]:
        """
        RPC 23638, ``CAM_WaitForCameraReady``

        Waits for the camera device to become ready for use.

        Parameters
        ----------
        wait : int, optional
            Time to wait for the camera to come online [s].
        camera : Camera | str, optional
            Camera device, by default OVERVIEW

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``NA``: Imaging license not found.
                - ``TIMEOUT``: Camera did not become usable within the
                  specified time.

        See Also
        --------
        is_camera_ready
        get_camera_power_status
        switch_camera_power
        """
        _camera = get_enum(Camera, camera)
        return self._request(
            23638,
            [_camera, int(wait * 1000)]
        )

    def set_autofocus_position(
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
            Error codes:
                - ``NA``: Imaging license not found.

        See Also
        --------
        get_autofocus_position
        """
        return self._request(
            23645,
            [position]
        )

    def get_autofocus_position(self) -> GeoComResponse[int]:
        """
        RPC 23644, ``CAM_AF_GetMotorPosition``

        Gets the current position of the autofocus motor.

        Returns
        -------
        GeoComResponse
            Params:
                - `int`: Autofocus motor position.

            Error codes:
                - ``NA``: Imaging license not found.

        See Also
        --------
        set_autofocus_position
        """
        return self._request(
            23644,
            parsers=int
        )

    def switch_continuous_autofocus(
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
            Error codes:
                - ``NA``: Imaging license not found.

        """
        return self._request(
            23669,
            [start]
        )

    def set_focus_to_distance(
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
            Error codes:
                - ``NA``: Imaging license not found.

        """
        return self._request(
            23652,
            [dist]
        )

    def set_focus_to_infinity(self) -> GeoComResponse[None]:
        """
        RPC 23677, ``CAM_AF_PositFocusMotorToInfinity``

        Sets the autofocus motor to focus to infinity.

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``NA``: Imaging license not found.

        """
        return self._request(23677)

    def set_focus_to_target(self) -> GeoComResponse[None]:
        """
        RPC 23662, ``CAM_AF_SingleShotAutofocus``

        Focuses current target.

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``NA``: Imaging license not found.

        """
        return self._request(23662)

    def set_focus_to_target_contrast(
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
            Error codes:
                - ``NA``: Imaging license not found.

        """
        return self._request(
            23663,
            [steps]
        )

    def get_sensor_size(
        self,
        camera: Camera | str = Camera.OVERVIEW
    ) -> GeoComResponse[tuple[float, float]]:
        """
        RPC 23668, ``CAM_GetChipWindowSize``

        Gets the size of the camera chip.

        Parameters
        ----------
        camera : Camera | str, optional
            Camera device, by default OVERVIEW

        Returns
        -------
        GeoComResponse
            Params:
                - `float`: Sensor width.
                - `float`: Sensor height.

            Error codes:
                - ``NA``: Imaging license not found.

        """
        _camera = get_enum(Camera, camera)
        return self._request(
            23668,
            [_camera],
            (
                float,
                float
            )
        )

    def get_telescopic_crosshair(self) -> GeoComResponse[tuple[int, int]]:
        """
        RPC 23671, ``CAM_OAC_GetCrossHairPos``

        Gets the position of the crosshair in the actual camera resolution.

        Returns
        -------
        GeoComResponse
            Params:
                - `int`: Horizontal position.
                - `int`: Vertical position.

            Error codes:
                - ``NA``: Imaging license not found.

        """
        return self._request(
            23671,
            parsers=(
                int,
                int
            )
        )

    def get_overview_interior_orientation(
        self,
        calibrated: bool = True
    ) -> GeoComResponse[tuple[float, float, float, float]]:
        """
        RPC 23602, ``CAM_OVC_ReadInterOrient``

        Gets the interior orientation parameters of the camera.

        Parameters
        ----------
        calibrated : bool, optional
            Use calibrated data.

        Returns
        -------
        GeoComResponse
            Params:
                - `float`: Horizontal position of principal point.
                - `float`: Vertical position of principal point.
                - `float`: Focus length.
                - `float`: Pixel size.

            Error codes:
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

    def get_overview_exterior_orientation(
        self,
        calibrated: bool = True
    ) -> GeoComResponse[tuple[Coordinate, Angle, Angle, Angle]]:
        """
        RPC 23603, ``CAM_OVC_ReadExterOrient``

        Gets the exterior orientation parameters of the camera.

        Parameters
        ----------
        calibrated : bool, optional
            Use calibrated data.

        Returns
        -------
        GeoComResponse
            Params:
                - `Coordinate`: Camera coordinates.
                - `Angle`: Azimut angle.
                - `Angle`: Zenith angle.
                - `Angle`: Tilt angle.

            Error codes:
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
        camera: Camera | str = Camera.OVERVIEW
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
        camera : Camera | str, optional
            Camera device, by default OVERVIEW

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``NA``: Imaging license not found.

        """
        _camera = get_enum(Camera, camera)
        return self._request(
            23675,
            [_camera, fps, bitrate]
        )

    def stop_remote_video(self) -> GeoComResponse[None]:
        """
        RPC 23676, ``CAM_StopRemoteVideo``

        Stops the remote video stream.

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``NA``: Imaging license not found.

        """
        return self._request(23676)
