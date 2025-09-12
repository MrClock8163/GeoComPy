"""
Description
===========

Module: ``geocompy.geo.tmc``

Definitions for the GeoCom Theodolite measurement and calculation
subsystem.

Types
-----

- ``GeoComTMC``

"""
from __future__ import annotations
from typing import SupportsFloat

from ..data import (
    Angle,
    Coordinate,
    get_enum,
    get_enum_parser,
    parse_bool
)
from .gcdata import (
    EDMModeV1,
    EDMModeV2,
    Face,
    Inclination,
    Measurement
)
from .gctypes import (
    GeoComSubsystem,
    GeoComResponse
)


class GeoComTMC(GeoComSubsystem):
    """
    Theodolite measurement and calculation subsystem of the GeoCom
    protocol.

    This subsystem is the central module of measurement, calculation and
    geodetic control.

    The module handles:
        - measurement functions
        - measurement control functions
        - data setup functions
        - information functions
        - configuration functions

    Possible return codes:
        System
            General use codes.
        Informative/Warning
            Function terminated with success, but some restrictions may
            apply (e.g.: angle measurement succeded, distance measurement
            failed).
        Error
            Non-successful function termination.

    """

    def get_coordinate(
        self,
        wait: int = 5,
        mode: Inclination | str = Inclination.AUTO
    ) -> GeoComResponse[tuple[Coordinate, int, Coordinate, int]]:
        """
        RPC 2082, ``TMC_GetCoordinate``

        Takes an angular measurement with the selected inclination
        correction mode, and calculates coordinates from an previously
        measured distance. The distance has to be measured in advance.
        As the distance measurement takes some time to complete, a wait
        time can be specified for the calculation, to wait for the
        completion of the measurement.

        Parameters
        ----------
        wait : int, optional
            Wait time for EDM process [s], by default 5
        mode : Inclination | str, optional
            Inclination correction mode, by default Inclination.AUTO

        Returns
        -------
        GeoComResponse
            Params:
                - `COORDINATE`: Calculated coordinate.
                - `int`: Time of the coordinate acquisition.
                - `COORDINATE`: Continuously calculated
                  coordinate.
                - `int`: Time of the coordinate
                  acquisition.
            Warning codes:
                - ``TMC_ACCURACY_GUARANTEE``: Accuracy is not guaranteed,
                  because the measurement contains data with unverified
                  accuracy. Coordinates are available.
                - ``TMC_NO_FULL_CORRECTION``: Results are not corrected by
                  all sensors. Coordinates are available. Run check
                  commands to determine the missing correction.
            Error codes:
                - ``TMC_ANGLE_OK``: Angles are measured, but no valid
                  distance was found.
                - ``TMC_ANGLE_NO_FULL_CORRECTION``: Only angles are
                  measured, but the accuracy cannot be guaranteed. Tilt
                  measurement might not be available.
                - ``TMC_DIST_ERROR``: Error is distance measurement,
                  target not found. Repeat sighting and measurement!
                - ``TMC_DIST_PPM``: Wrong EDM settings.
                - ``TMC_ANGLE_ERROR``: Angle or inclination measurement
                  error. Check inclination mode!
                - ``TMC_BUSY``: TMC is currently busy. Repeat measurement!
                - ``ABORT``: Measurement aborted.
                - ``SHUT_DOWN``: System shutdown.

        See Also
        --------
        do_measurement
        was_not_atr_corrected
        was_not_inclination_corrected

        """
        def transform(
            params: tuple[
                float, float, float, int,
                float, float, float, int
            ] | None
        ) -> tuple[Coordinate, int, Coordinate, int] | None:
            if params is None:
                return None

            coord = Coordinate(
                params[0],
                params[1],
                params[2]
            )
            coord_cont = Coordinate(
                params[4],
                params[5],
                params[6]
            )
            return (
                coord,
                params[3],
                coord_cont,
                params[7]
            )

        _mode = get_enum(Inclination, mode)
        response = self._request(
            2082,
            [int(wait * 1000), _mode.value],
            (
                float,
                float,
                float,
                int,
                float,
                float,
                float,
                int
            )
        )

        return response.map_params(transform)

    def get_simple_measurement(
        self,
        wait: int = 5,
        mode: Inclination | str = Inclination.AUTO
    ) -> GeoComResponse[tuple[Angle, Angle, float]]:
        """
        RPC 2108, ``TMC_GetSimpleMea``

        Takes an angular measurement with the selected inclination
        correction mode, and returns measurements with a previously
        measured distance. The distance has to be measured in advance.
        As the distance measurement takes some time to complete, a wait
        time can be specified for the process, to wait for the completion
        of the measurement.

        Parameters
        ----------
        wait : int, optional
            Wait time for EDM process [s], by default 5
        mode : Inclination | str, optional
            Inclination correction mode, by default Inclination.AUTO

        Returns
        -------
        GeoComResponse
            Params:
                - `Angle`: Horizontal angle.
                - `Angle`: Vertical angle.
                - `float`: Slope distance.

            Warning codes:
                - ``TMC_ACCURACY_GUARANTEE``: Accuracy is not guaranteed,
                  because the measurement contains data with unverified
                  accuracy. Coordinates are available.
                - ``TMC_NO_FULL_CORRECTION``: Results are not corrected by
                  all sensors. Coordinates are available. Run check
                  commands to determine the missing correction.
                - ``TMC_ANGLE_NO_FULL_CORRECTION``: Only angles are
                  measured, but the accuracy cannot be guaranteed. Tilt
                  measurement might not be available.
                - ``TMC_ANGLE_OK``: Angles are measured, but no valid
                  distance was found.
                - ``TMC_ANGLE_NO_ACC_GUARANTY``: Only angle measurement
                  is valid, but the accuracy cannot be guaranteed.

            Error codes:
                - ``TMC_DIST_ERROR``: Error is distance measurement,
                  target not found. Repeat sighting and measurement!
                - ``TMC_DIST_PPM``: Wrong EDM settings.
                - ``TMC_ANGLE_ERROR``: Angle or inclination measurement
                  error. Check inclination mode!
                - ``TMC_BUSY``: TMC is currently busy. Repeat measurement!
                - ``ABORT``: Measurement aborted.
                - ``SHUT_DOWN``: System shutdown.

        See Also
        --------
        do_measurement
        get_angle

        """
        _mode = get_enum(Inclination, mode)
        return self._request(
            2108,
            [int(wait * 1000), _mode.value],
            (
                Angle.parse,
                Angle.parse,
                float
            )
        )

    def get_angle_inclination(
        self,
        mode: Inclination | str = Inclination.AUTO
    ) -> GeoComResponse[
        tuple[
            Angle, Angle, Angle, int,
            Angle, Angle, Angle, int,
            Face
        ]
    ]:
        """
        RPC 2003, ``TMC_GetAngle``

        Takes an angular measurement with the selected inclination
        measurement mode.

        Parameters
        ----------
        mode : INCLINEPRG | str, optional
            Inclination meaurement mode, by default INCLINEPRG.AUTO

        Returns
        -------
        GeoComResponse
            Params:
                - `Angle`: Horizontal angle.
                - `Angle`: Vertical angle.
                - `Angle`: Angular accuracy.
                - `int`: Time of angle measurement.
                - `Angle`: Cross inclination.
                - `Angle`: Lengthwise inclination.
                - `Angle`: Inclination accuracy.
                - `int`: Time of inclination measurement.
                - `Face`: Instrument face.

            Warning codes:
                - ``TMC_ACCURACY_GUARANTEE``: Accuracy is not guaranteed,
                  because the measurement contains data with unverified
                  accuracy. Coordinates are available.
                - ``TMC_NO_FULL_CORRECTION``: Results are not corrected by
                  all sensors. Coordinates are available. Run check
                  commands to determine the missing correction.
                - ``TMC_ANGLE_NO_FULL_CORRECTION``: Only angles are
                  measured, but the accuracy cannot be guaranteed. Tilt
                  measurement might not be available.
                - ``TMC_ANGLE_OK``: Angles are measured, but no valid
                  distance was found.
                - ``TMC_ANGLE_NO_ACC_GUARANTY``: Only angle measurement
                  is valid, but the accuracy cannot be guaranteed.

            Error codes:
                - ``TMC_DIST_ERROR``: Error is distance measurement,
                  target not found. Repeat sighting and measurement!
                - ``TMC_DIST_PPM``: Wrong EDM settings.
                - ``TMC_ANGLE_ERROR``: Angle or inclination measurement
                  error. Check inclination mode!
                - ``TMC_BUSY``: TMC is currently busy. Repeat measurement!
                - ``ABORT``: Measurement aborted.
                - ``SHUT_DOWN``: System shutdown.

        See Also
        --------
        get_angle
        get_simple_measurement

        """
        _mode = get_enum(Inclination, mode)
        return self._request(
            2003,
            [_mode.value],
            (
                Angle.parse,
                Angle.parse,
                Angle.parse,
                int,
                Angle.parse,
                Angle.parse,
                Angle.parse,
                int,
                get_enum_parser(Face)
            )
        )

    def get_angle(
        self,
        mode: Inclination | str = Inclination.AUTO
    ) -> GeoComResponse[tuple[Angle, Angle]]:
        """
        RPC 2107, ``TMC_GetAngle5``

        Takes an angular measurement with the selected inclination
        correction mode.

        Parameters
        ----------
        mode : Inclination | str, optional
            Inclination correction mode, by default Inclination.AUTO

        Returns
        -------
        GeoComResponse
            Params:
                - `Angle`: Horizontal angle.
                - `Angle`: Vertical angle.

            Warning codes:
                - ``TMC_ACCURACY_GUARANTEE``: Accuracy is not guaranteed,
                  because the measurement contains data with unverified
                  accuracy. Coordinates are available.
                - ``TMC_NO_FULL_CORRECTION``: Results are not corrected by
                  all sensors. Coordinates are available. Run check
                  commands to determine the missing correction.
                - ``TMC_ANGLE_NO_FULL_CORRECTION``: Only angles are
                  measured, but the accuracy cannot be guaranteed. Tilt
                  measurement might not be available.
                - ``TMC_ANGLE_OK``: Angles are measured, but no valid
                  distance was found.
                - ``TMC_ANGLE_NO_ACC_GUARANTY``: Only angle measurement
                  is valid, but the accuracy cannot be guaranteed.

            Error codes:
                - ``TMC_DIST_ERROR``: Error is distance measurement,
                  target not found. Repeat sighting and measurement!
                - ``TMC_DIST_PPM``: Wrong EDM settings.
                - ``TMC_ANGLE_ERROR``: Angle or inclination measurement
                  error. Check inclination mode!
                - ``TMC_BUSY``: TMC is currently busy. Repeat measurement!
                - ``ABORT``: Measurement aborted.
                - ``SHUT_DOWN``: System shutdown.

        See Also
        --------
        do_measurement
        get_simple_measurement

        """
        _mode = get_enum(Inclination, mode)
        return self._request(
            2107,
            [_mode.value],
            (
                Angle.parse,
                Angle.parse
            )
        )

    def quick_distance(self) -> GeoComResponse[tuple[Angle, Angle, float]]:
        """
        RPC 2117, ``TMC_QuickDist``

        Starts an EDM tracking measurement and waits until a distance is
        measured.

        Returns
        -------
        GeoComResponse
            Params:
                - `Angle`: Horizontal angle.
                - `Angle`: Vertical angle.
                - `float`: Slope distance.

            Warning codes:
                - ``TMC_ACCURACY_GUARANTEE``: Accuracy is not guaranteed,
                  because the measurement contains data with unverified
                  accuracy. Coordinates are available.
                - ``TMC_NO_FULL_CORRECTION``: Results are not corrected by
                  all sensors. Coordinates are available. Run check
                  commands to determine the missing correction.
                - ``TMC_ANGLE_NO_FULL_CORRECTION``: Only angles are
                  measured, but the accuracy cannot be guaranteed. Tilt
                  measurement might not be available.
                - ``TMC_ANGLE_OK``: Angles are measured, but no valid
                  distance was found.
                - ``TMC_ANGLE_NO_ACC_GUARANTY``: Only angle measurement
                  is valid, but the accuracy cannot be guaranteed.

            Error codes:
                - ``TMC_DIST_ERROR``: Error is distance measurement,
                  target not found. Repeat sighting and measurement!
                - ``TMC_DIST_PPM``: Wrong EDM settings.
                - ``TMC_ANGLE_ERROR``: Angle or inclination measurement
                  error. Check inclination mode!
                - ``TMC_BUSY``: TMC is currently busy. Repeat measurement!
                - ``ABORT``: Measurement aborted.
                - ``SHUT_DOWN``: System shutdown.

        See Also
        --------
        get_angle_inclination,
        do_measurement
        was_not_atr_corrected
        was_not_inclination_corrected

        """
        return self._request(
            2117,
            parsers=(
                Angle.parse,
                Angle.parse,
                float
            )
        )

    def get_complete_measurement(
        self,
        wait: int = 5,
        mode: Inclination | str = Inclination.AUTO
    ) -> GeoComResponse[tuple[Angle, Angle, float]]:
        """
        RPC 2167, ``TMC_GetFullMeas``

        .. versionadded:: GeoCom-TPS1200-1.50

        Takes an angular measurement with the selected inclination
        correction mode, and returns measurements with a previously
        measured distance, as well as accuracy indicators. The distance
        has to be measured in advance. As the distance measurement takes
        some time to complete, a wait time can be specified for the
        process, to wait for the completion of the measurement.

        Parameters
        ----------
        wait : int, optional
            Wait time for EDM process [s], by default 5
        mode : Inclination | str, optional
            Inclination correction mode, by default Inclination.AUTO

        Returns
        -------
        GeoComResponse
            Params:
                - `Angle`: Horizontal angle.
                - `Angle`: Vertical angle.
                - `Angle`: Angular accuracy.
                - `Angle`: Cross inclination.
                - `Angle`: Lengthwise inclination.
                - `Angle`: Inclination accuracy.
                - `float`: Slope distance.
                - `float`: Distance measurement time [ms].

            Warning codes:
                - ``TMC_ACCURACY_GUARANTEE``: Accuracy is not guaranteed,
                  because the measurement contains data with unverified
                  accuracy. Coordinates are available.
                - ``TMC_NO_FULL_CORRECTION``: Results are not corrected by
                  all sensors. Coordinates are available. Run check
                  commands to determine the missing correction.
                - ``TMC_ANGLE_NO_FULL_CORRECTION``: Only angles are
                  measured, but the accuracy cannot be guaranteed. Tilt
                  measurement might not be available.
                - ``TMC_ANGLE_OK``: Angles are measured, but no valid
                  distance was found.
                - ``TMC_ANGLE_NO_ACC_GUARANTY``: Only angle measurement
                  is valid, but the accuracy cannot be guaranteed.

            Error codes:
                - ``TMC_DIST_ERROR``: Error is distance measurement,
                  target not found. Repeat sighting and measurement!
                - ``TMC_DIST_PPM``: Wrong EDM settings.
                - ``TMC_ANGLE_ERROR``: Angle or inclination measurement
                  error. Check inclination mode!
                - ``TMC_BUSY``: TMC is currently busy. Repeat measurement!
                - ``ABORT``: Measurement aborted.
                - ``SHUT_DOWN``: System shutdown.

        See Also
        --------
        do_measurement
        get_angle

        """
        _mode = get_enum(Inclination, mode)
        return self._request(
            2167,
            [int(wait * 1000), _mode.value],
            (
                Angle.parse,
                Angle.parse,
                Angle.parse,
                Angle.parse,
                Angle.parse,
                Angle.parse,
                float,
                float
            )
        )

    def do_measurement(
        self,
        command: Measurement | str = Measurement.DISTANCE,
        inclination: Inclination | str = Inclination.AUTO
    ) -> GeoComResponse[None]:
        """
        RPC 2008, ``TMC_DoMeasure``

        Carries out a distance measurement with the specified measurement
        program and inclination correction mode. The results are not
        returned, but kept in memory until the next measurement command.

        Parameters
        ----------
        command: Measurement | str, optional
            Distance measurement program, by default Measurement.DISTANCE
        inclination : Inclination | str, optional
            Inclination correction mode, by default Inclination.AUTO

        Returns
        -------
        GeoComResponse

        See Also
        --------
        set_edm_mode_v1
        set_edm_mode_v2
        get_coordinate
        get_simple_measurement
        get_angle
        get_angle_inclination

        """
        _cmd = get_enum(Measurement, command)
        _mode = get_enum(Inclination, inclination)
        return self._request(
            2008,
            [_cmd.value, _mode.value]
        )

    def set_manual_distance(
        self,
        distance: float,
        offset: float,
        inclination: Inclination | str = Inclination.AUTO
    ) -> GeoComResponse[None]:
        """
        RPC 2019, ``TMC_SetHandDist``

        Sets slope distance and height offset from separately measured
        values. An angular and an inclination measurement is taken
        automatically to calculate the position of the target.

        Parameters
        ----------
        distance : float
            Slope distance to set.
        offset : float,
            Height offset.
        inclination : Inclination | str, optional
            Inclination correction mode, by default Inclination.AUTO

        Returns
        -------
        GeoComResponse
            Warning codes:
                - ``TMC_ACCURACY_GUARANTEE``: Accuracy is not guaranteed,
                  because the measurement contains data with unverified
                  accuracy. Coordinates are available.
                - ``TMC_NO_FULL_CORRECTION``: Results are not corrected by
                  all sensors. Coordinates are available. Run check
                  commands to determine the missing correction.
                - ``TMC_ANGLE_NO_FULL_CORRECTION``: Only angles are
                  measured, but the accuracy cannot be guaranteed. Tilt
                  measurement might not be available.
                - ``TMC_ANGLE_OK``: Angles are measured, but no valid
                  distance was found.
                - ``TMC_ANGLE_NO_ACC_GUARANTY``: Only angle measurement
                  is valid, but the accuracy cannot be guaranteed.
            Error codes:
                - ``TMC_DIST_ERROR``: Error is distance measurement,
                  target not found. Repeat sighting and measurement!
                - ``TMC_DIST_PPM``: Wrong EDM settings.
                - ``TMC_ANGLE_ERROR``: Angle or inclination measurement
                  error. Check inclination mode!
                - ``TMC_BUSY``: TMC is currently busy. Repeat measurement!
                - ``ABORT``: Measurement aborted.
                - ``SHUT_DOWN``: System shutdown.

        See Also
        --------
        was_not_atr_corrected
        was_not_inclination_corrected

        """
        _mode = get_enum(Inclination, inclination)
        return self._request(
            2019,
            [distance, offset, _mode.value]
        )

    def get_target_height(self) -> GeoComResponse[float]:
        """
        RPC 2011, ``TMC_GetHeight``

        Gets the current target height.

        Returns
        -------
        GeoComResponse
            Params:
                - `float`: Current target height.

        See Also
        --------
        set_target_height

        """
        return self._request(
            2011,
            parsers=float
        )

    def set_target_height(
        self,
        height: float
    ) -> GeoComResponse[None]:
        """
        RPC 2012, ``TMC_SetHeight``

        Sets the target height.

        Parameters
        ----------
        height : float
            New target height to set.

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``TMC_BUSY``: TMC is currently busy, or target height
                  is not yet set.
                - ``IVPARAM``: Invalid target height.

        See Also
        --------
        get_target_height

        """
        return self._request(
            2012,
            [height]
        )

    def get_atmospheric_corrections(
        self
    ) -> GeoComResponse[tuple[float, float, float, float]]:
        """
        RPC 2029, ``TMC_GetAtmCorr``

        Gets current parameters of the atmospheric correction.

        Returns
        -------
        GeoComResponse
            Params:
                - `float`: EDM transmitter wavelength.
                - `float`: Atmospheric pressure [mbar].
                - `float`: Dry temperature [°C].
                - `float`: Wet temperature [°C].

        See Also
        --------
        set_atmospheric_corrections

        """
        return self._request(
            2029,
            parsers=(
                float,
                float,
                float,
                float
            )
        )

    def set_atmospheric_corrections(
        self,
        wavelength: float,
        pressure: float,
        drytemp: float,
        wettemp: float
    ) -> GeoComResponse[None]:
        """
        RPC 2028, ``TMC_SetAtmCorr``

        Sets the parameters of the atmospheric correction.

        Parameters
        ----------
        wavelength : float
            EDM transmitter wavelength.
        pressure : float
            Atmospheric pressure [mbar].
        drytemp : float
            Dry temperature [°C],
        wettemp : float
            Wet temperature [°C],

        Returns
        -------
        GeoComResponse

        See Also
        --------
        get_atmospheric_corrections

        """
        return self._request(
            2028,
            [wavelength, pressure, drytemp, wettemp]
        )

    def set_azimuth(
        self,
        azimuth: SupportsFloat
    ) -> GeoComResponse[None]:
        """
        RPC 2113, ``TMC_SetOrientation``

        Sets the internal horizontal orientation offset so that the
        angular measurement reads the same as the provided angle.
        Previously measured distances must be cleared before orienting.

        Parameters
        ----------
        azimuth : SupportsFloat
            Azimuth angle to set.

        Returns
        -------
        GeoComResponse
            Warning codes:
                - ``TMC_ACCURACY_GUARANTEE``: Accuracy is not guaranteed,
                  because the measurement contains data with unverified
                  accuracy. Coordinates are available.
                - ``TMC_NO_FULL_CORRECTION``: Results are not corrected by
                  all sensors. Coordinates are available. Run check
                  commands to determine the missing correction.
                - ``TMC_ANGLE_NO_FULL_CORRECTION``: Only angles are
                  measured, but the accuracy cannot be guaranteed. Tilt
                  measurement might not be available.
                - ``TMC_ANGLE_OK``: Angles are measured, but no valid
                  distance was found.
                - ``TMC_ANGLE_NO_ACC_GUARANTY``: Only angle measurement
                  is valid, but the accuracy cannot be guaranteed.
            Error codes:
                - ``TMC_DIST_ERROR``: Error is distance measurement,
                  target not found. Repeat sighting and measurement!
                - ``TMC_DIST_PPM``: Wrong EDM settings.
                - ``TMC_ANGLE_ERROR``: Angle or inclination measurement
                  error. Check inclination mode!
                - ``TMC_BUSY``: TMC is currently busy. Repeat measurement!
                - ``ABORT``: Measurement aborted.
                - ``SHUT_DOWN``: System shutdown.

        See Also
        --------
        was_not_atr_corrected
        was_not_inclination_corrected
        do_measurement

        """
        return self._request(
            2113,
            [float(azimuth)]
        )

    def get_prism_correction(self) -> GeoComResponse[float]:
        """
        RPC 2023, ``TMC_GetPrismCorr``

        Gets the current prism constant.

        Returns
        -------
        GeoComResponse
            Params:
                - `float`: Prism constant.

        See Also
        --------
        set_prism_correction

        """
        return self._request(
            2023,
            parsers=float
        )

    def set_prism_correction(
        self,
        const: float
    ) -> GeoComResponse[None]:
        """
        RPC 2024, ``TMC_SetPrismCorr``

        Sets the prism constant.

        Parameters
        ----------
        const : float
            Prism constant.

        See Also
        --------
        get_prism_correction

        """
        return self._request(
            2024,
            [const]
        )

    def get_refractive_correction(
        self
    ) -> GeoComResponse[tuple[bool, float, float]]:
        """
        RPC 2031, ``TMC_GetRefractiveCorr``

        Gets current refraction correction coefficients.

        Returns
        -------
        GeoComResponse
            Params:
                - `bool`: Refraction correction enabled.
                - `float`: Radius of the Earth.
                - `float`: Refraction coefficient.

        See Also
        --------
        set_refractive_correction

        """
        return self._request(
            2031,
            parsers=(
                parse_bool,
                float,
                float
            )
        )

    def set_refractive_correction(
        self,
        enabled: bool,
        earthradius: float = 6_378_000,
        coef: float = 0.13
    ) -> GeoComResponse[None]:
        """
        RPC 2030, ``TMC_SetRefractiveCorr``

        Sets the refraction correction coefficients.

        Parameters
        ----------
        enabled : bool
            Refraction correction enabled.
        earthradius : float, optional
            Radius of the Earth, by default 6378000
        coef : float, optional
            Refraction coefficient, by default 0.13

        Returns
        -------
        GeoComResponse

        See Also
        --------
        get_refractive_correction

        """
        return self._request(
            2030,
            [enabled, earthradius, coef]
        )

    def get_refractive_method(self) -> GeoComResponse[int]:
        """
        RPC 2091, ``TMC_GetRefractiveMethod``

        Gets the current refraction mode.

        Returns
        -------
        GeoComResponse
            Params:
                - `int`: Refraction method.

        See Also
        --------
        set_refractive_method

        """
        return self._request(
            2091,
            parsers=int
        )

    def set_refractive_method(
        self,
        method: int
    ) -> GeoComResponse[None]:
        """
        RPC 2090, ``TMC_SetRefractiveMethod``

        Sets the refraction mode.

        Parameters
        ----------
        method : int
            Refraction method to set (2: Australia, 1: rest of the world).

        Returns
        -------
        GeoComResponse

        See Also
        --------
        get_refractive_method

        """
        return self._request(
            2090,
            [method]
        )

    def get_station(self) -> GeoComResponse[tuple[Coordinate, float]]:
        """
        RPC 2009, ``TMC_GetStation``

        Gets the current station coordinates and instrument height.

        Returns
        -------
        GeoComResponse
            Params:
                - `Coordinate`: Station coordinates.
                - `float`: Height of instrument.

        See Also
        --------
        set_station

        """
        def transform(
            params: tuple[float, float, float, float] | None
        ) -> tuple[Coordinate, float] | None:
            if params is None:
                return None
            return (
                Coordinate(
                    params[0],
                    params[1],
                    params[2]
                ),
                params[3]
            )

        response = self._request(
            2009,
            parsers=(
                float,
                float,
                float,
                float
            )
        )
        return response.map_params(transform)

    def set_station(
        self,
        station: Coordinate,
        hi: float
    ) -> GeoComResponse[None]:
        """
        RPC 2010, ``TMC_SetStation``

        Sets the station coordinates and instrument height. Existing
        distance measurements must be cleared from memory in advance.

        Parameters
        ----------
        station : Coordinate
            New station coordinates.
        hi : float
            Height of instrument.

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``TMC_BUSY``: TMC is busy or distance was not cleared.

        See Also
        --------
        get_station
        do_measurement

        """
        return self._request(
            2010,
            [station.x, station.y, station.z, hi]
        )

    def get_face(self) -> GeoComResponse[Face]:
        """
        RPC 2026, ``TMC_GetFace``

        Gets which face the telescope is corrently positioned in. The face
        information is only valid, if the instrument is in active state.

        Returns
        -------
        GeoComResponse
            Params:
                - `Face`: Current face.

        See Also
        --------
        aut.change_face

        """
        return self._request(
            2026,
            parsers=get_enum_parser(Face)
        )

    def get_signal(self) -> GeoComResponse[tuple[float, int]]:
        """
        RPC 2022, ``TMC_GetSignal``

        Gets information about the intensity of the EDM signal. The EDM
        most be started in signal measuring mode in advance, and has to
        be cleared afterwards.

        Returns
        -------
        GeoComResponse
            Params:
                - `float`: Return signal intensity [%].
                - `int`: Time of the signal measurement.

            Error codes:
                - ``TMC_SIGNAL_ERROR``: Error in signal measurement.
                - ``ABORT``: Measurement was aborted.
                - ``SHUT_DOWN``: System shutdown.

        See Also
        --------
        do_measurement

        """
        return self._request(
            2022,
            parsers=(
                float,
                int
            )
        )

    def get_angle_correction(
        self
    ) -> GeoComResponse[tuple[bool, bool, bool, bool]]:
        """
        RPC 2014, ``TMC_GetAngSwitch``

        Gets the current status of the angular corrections.

        Returns
        -------
        GeoComResponse
            Params:
                - `bool`: Inclination correction.
                - `bool`: Standing axis correction.
                - `bool`: Collimation error correction.
                - `bool`: Tilting axis correction.

        See Also
        --------
        set_angle_correction

        """
        return self._request(
            2014,
            parsers=(
                parse_bool,
                parse_bool,
                parse_bool,
                parse_bool
            )
        )

    def get_compensator_status(self) -> GeoComResponse[bool]:
        """
        RPC 2007, ``TMC_GetInclineSwitch``

        Gets the current status of the dual axis compensator.

        Returns
        -------
        GeoComResponse
            Params:
                - `bool`: Compensator is enabled.

        See Also
        --------
        switch_compensator

        """
        return self._request(
            2007,
            parsers=parse_bool
        )

    def switch_compensator(
        self,
        enabled: bool
    ) -> GeoComResponse[None]:
        """
        RPC 2006, ``TMC_SetInclineSwitch``

        Sets the status of the dual axis compensator.

        Parameters
        ----------
        enabled : bool
            Compensator is enabled.

        Returns
        -------
        GeoComResponse

        See Also
        --------
        get_compensator_status

        """
        return self._request(
            2006,
            [enabled]
        )

    def get_edm_mode_v1(self) -> GeoComResponse[EDMModeV1]:
        """
        RPC 2021, ``TMC_GetEdmMode``

        .. versionremoved:: GeoCom-TPS1100

        Gets the current EDM measurement mode.

        Returns
        -------
        GeoComResponse
            Params:
                - `EDMMode`: Current EDM mode (EDMModeV1).

        See Also
        --------
        set_edm_mode_v1

        """
        return self._request(
            2021,
            parsers=get_enum_parser(EDMModeV1)
        )

    def set_edm_mode_v1(
        self,
        mode: EDMModeV1 | str
    ) -> GeoComResponse[None]:
        """
        RPC 2020, ``TMC_SetEdmMode``

        .. versionremoved:: GeoCom-TPS1100

        Sets the EDM measurement mode.

        Parameters
        ----------
        mode : EDMModeV1 | str
            EDM mode to activate (expects `EDMModeV1`).

        Returns
        -------
        GeoComResponse

        See Also
        --------
        get_edm_mode_v1

        """
        _mode = get_enum(EDMModeV1, mode)
        return self._request(
            2020,
            [_mode.value]
        )

    def get_edm_mode_v2(self) -> GeoComResponse[EDMModeV2]:
        """
        RPC 2021, ``TMC_GetEdmMode``

        .. versionadded:: GeoCom-TPS1100

        Gets the current EDM measurement mode.

        Returns
        -------
        GeoComResponse
            Params:
                - `EDMMode`: Current EDM mode (EDMModeV2).

        See Also
        --------
        set_edm_mode_v2

        """
        return self._request(
            2021,
            parsers=get_enum_parser(EDMModeV2)
        )

    def set_edm_mode_v2(
        self,
        mode: EDMModeV2 | str
    ) -> GeoComResponse[None]:
        """
        RPC 2020, ``TMC_SetEdmMode``

        .. versionadded:: GeoCom-TPS1100

        Sets the EDM measurement mode.

        Parameters
        ----------
        mode : EDMModeV2 | str
            EDM mode to activate (expects `EDMModeV2`).

        Returns
        -------
        GeoComResponse

        See Also
        --------
        get_edm_mode_v2

        """
        _mode = get_enum(EDMModeV2, mode)
        return self._request(
            2020,
            [_mode.value]
        )

    def get_simple_coordinate(
        self,
        wait: int = 5,
        inclination: Inclination | str = Inclination.AUTO
    ) -> GeoComResponse[Coordinate]:
        """
        RPC 2116, ``TMC_GetSimpleCoord``

        Takes an angular measurement with the selected inclination
        correction mode, and calculates coordinates from an previously
        measured distance. The distance has to be measured in advance.
        As the distance measurement takes some time to complete, a wait
        time can be specified for the calculation, to wait for the
        completion of the measurement.

        Parameters
        ----------
        wait : int, optional
            Wait time for EDM process [s], by default 5
        inclination : Inclination | str, optional
            Inclination correction mode, by default Inclination.AUTO

        Returns
        -------
        GeoComResponse
            Params:
                - `Coordinate`: Calculated coordinate.

            Warning codes:
                - ``TMC_ACCURACY_GUARANTEE``: Accuracy is not guaranteed,
                  because the measurement contains data with unverified
                  accuracy. Coordinates are available.
                - ``TMC_NO_FULL_CORRECTION``: Results are not corrected by
                  all sensors. Coordinates are available. Run check
                  commands to determine the missing correction.
            Error codes:
                - ``TMC_ANGLE_OK``: Angles are measured, but no valid
                  distance was found.
                - ``TMC_ANGLE_NO_FULL_CORRECTION``: Only angles are
                  measured, but the accuracy cannot be guaranteed. Tilt
                  measurement might not be available.
                - ``TMC_DIST_ERROR``: Error is distance measurement,
                  target not found. Repeat sighting and measurement!
                - ``TMC_DIST_PPM``: Wrong EDM settings.
                - ``TMC_ANGLE_ERROR``: Angle or inclination measurement
                  error. Check inclination mode!
                - ``TMC_BUSY``: TMC is currently busy. Repeat measurement!
                - ``ABORT``: Measurement aborted.
                - ``SHUT_DOWN``: System shutdown.

        See Also
        --------
        get_coordinate
        was_not_atr_corrected
        was_not_inclination_corrected

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

        _mode = get_enum(Inclination, inclination)
        response = self._request(
            2116,
            [int(wait * 1000), _mode.value],
            parsers=(
                float,
                float,
                float
            )
        )

        return response.map_params(transform)

    def was_not_atr_corrected(self) -> GeoComResponse[bool]:
        """
        RPC 2114, ``TMC_IfDataAzeCorrError``

        Gets status of the ATR correction in the last measurement.

        Returns
        -------
        GeoComResponse
            Params:
                - `bool`: Last data record was not
                  corrected with ATR deviation.

        See Also
        --------
        was_not_inclination_corrected

        """
        return self._request(
            2114,
            parsers=parse_bool
        )

    def was_not_inclination_corrected(self) -> GeoComResponse[bool]:
        """
        RPC 2115, ``TMC_IfDataIncCorrError``

        Gets status of the inclination correction in the last measurement.

        Returns
        -------
        GeoComResponse
            Params:
                - `bool`: Last data record was not
                  corrected with inclination correction.

        See Also
        --------
        was_not_inclination_corrected

        """
        return self._request(
            2115,
            parsers=parse_bool
        )

    def set_angle_correction(
        self,
        inclinecorr: bool,
        stdaxiscorr: bool,
        collimcorr: bool,
        tiltaxiscorr: bool
    ) -> GeoComResponse[None]:
        """
        RPC 2014, ``TMC_SetAngSwitch``

        Sets the status of the angular corrections.

        Parameters
        ----------
        inclinecorr : bool
            Inclination correction.
        stdaxiscorr : bool
            Standing axis correction.
        collimcorr : bool
            Collimation error correction.
        tiltaxiscorr : bool
            Tilting axis correction,

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``TMC_BUSY``: TMC is busy.

        See Also
        --------
        do_measurement
        get_angle_correction

        """
        return self._request(
            2016,
            [inclinecorr, stdaxiscorr, collimcorr, tiltaxiscorr]
        )

    def get_distance_correction(
        self
    ) -> GeoComResponse[tuple[float, float]]:
        """
        RPC 2126, ``TMC_GetSlopDistCorr``

        .. versionadded:: GeoCom-TPS1100

        Gets the total correction (atmospheric + geometric) applied to the
        distance measurements, as well as the current prism constant.

        Returns
        -------
        GeoComResponse
            Params:
                - `float`: Total corrections [ppm].
                - `float`: Prism constant.

        See Also
        --------
        get_prism_correction
        set_prism_correction

        """
        return self._request(
            2126,
            parsers=(
                float,
                float
            )
        )

    def get_atmospheric_correction_ppm(self) -> GeoComResponse[float]:
        """
        RPC 2151, ``TMC_GetAtmPpm``

        .. versionadded:: GeoCom-TPS1200

        Gets the current atmospheric correction factor.

        Returns
        -------
        GeoComResponse
            Params:
                - `float`: Atmospheric correction factor [ppm].

        See Also
        --------
        set_atmospheric_correction_ppm
        get_geometric_correction_ppm
        set_geometric_correction_ppm
        get_prism_correction
        set_prism_correction

        """
        return self._request(
            2151,
            parsers=float
        )

    def set_atmospheric_correction_ppm(
        self,
        ppm: float
    ) -> GeoComResponse[None]:
        """
        RPC 2148, ``TMC_SetAtmPpm``

        .. versionadded:: GeoCom-TPS1200

        Sets the atmospheric correction factor.

        Parameters
        ----------
        ppm : float
            Atmospheric correction factor [ppm].

        Returns
        -------
        GeoComResponse

        See Also
        --------
        get_atmospheric_correction_ppm
        get_geometric_correction_ppm
        set_geometric_correction_ppm
        get_prism_correction
        set_prism_correction

        """
        return self._request(
            2148,
            [ppm]
        )

    def get_geometric_correction_ppm(
        self
    ) -> GeoComResponse[tuple[bool, float, float, float, float]]:
        """
        RPC 2154, ``TMC_GetGeoPpm``

        .. versionadded:: GeoCom-TPS1200

        Gets the current geometric correction factors.

        Returns
        -------
        GeoComResponse
            Params:
                - `bool`: Autmatically apply geometric
                  corrections.
                - `float`: Scale factor on central
                  meridian.
                - `float`: Offset from central
                  meridian.
                - `float`: Length reduction from projection
                  to reference level.
                - `float`: Individual correction [ppm].

        See Also
        --------
        get_atmospheric_correction_ppm
        set_atmospheric_correction_ppm
        set_geometric_correction_ppm
        get_prism_correction
        set_prism_correction

        """
        return self._request(
            2154,
            parsers=(
                parse_bool,
                float,
                float,
                float,
                float
            )
        )

    def set_geometric_correction_ppm(
        self,
        automatic: bool,
        meridianscale: float,
        meridianoffset: float,
        reduction: float,
        individual: float
    ) -> GeoComResponse[None]:
        """
        RPC 2153, ``TMC_SetGeoPpm``

        .. versionadded:: GeoCom-TPS1200

        Sets the geometric correction factors.

        Parameters
        ----------
        automatic : bool
            Automatically apply geometric corrections.
        meridianscale : float
            Scale factor on central meridian.
        meridianoffset : float
            Offset from central meridian.
        reduction : float
            Length reduction from projection to reference level [ppm].
        individual : float
            Individual correction [ppm].

        Returns
        -------
        GeoComResponse

        See Also
        --------
        get_atmospheric_correction_ppm
        set_atmospheric_correction_ppm
        get_geometric_correction_ppm
        get_prism_correction
        set_prism_correction

        """
        return self._request(
            2153,
            [
                automatic,
                meridianscale, meridianoffset,
                reduction, individual
            ]
        )
