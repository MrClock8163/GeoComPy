"""
Description
===========

Module: ``geocompy.tps1000.tmc``

Definitions for the TPS1000 Theodolite measurement and calculation
subsystem.

Types
-----

- ``TPS1000TMC``

"""
from __future__ import annotations

from ..data import (
    Angle,
    Coordinate,
    toenum,
    enumparser,
    parsebool,
    INCLINATION,
    MEASUREMENT,
    EDMMODE,
    EDMMODEV1,
    FACE
)
from ..protocols import (
    GeoComSubsystem,
    GeoComResponse
)


class TPS1000TMC(GeoComSubsystem):
    """
    Theodolite measurement and calculation subsystem of the TPS1000
    GeoCom protocol.

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
        wait: int = 5000,
        mode: INCLINATION | str = INCLINATION.AUTO
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
            Wait time for EDM process [ms], by default 5000
        mode : INCLINATION | str, optional
            Inclination correction mode, by default INCLINATION.AUTO

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
        do_measure
        if_data_aze_corr_error
        if_data_inc_corr_error

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

        _mode = toenum(INCLINATION, mode)
        response = self._request(
            2082,
            [wait, _mode.value],
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

    def get_simple_mea(
        self,
        wait: int = 5000,
        mode: INCLINATION | str = INCLINATION.AUTO
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
            Wait time for EDM process [ms], by default 5000
        mode : INCLINATION | str, optional
            Inclination correction mode, by default INCLINATION.AUTO

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
        do_measure
        get_angle

        """
        _mode = toenum(INCLINATION, mode)
        return self._request(
            2108,
            [wait, _mode.value],
            (
                Angle.parse,
                Angle.parse,
                float
            )
        )

    def get_angle_incline(
        self,
        mode: INCLINATION | str = INCLINATION.AUTO
    ) -> GeoComResponse[
        tuple[
            Angle, Angle, Angle, int,
            Angle, Angle, Angle, int,
            FACE
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
                - `FACEDEF`: Instrument face.
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
        get_simple_mea

        """
        _mode = toenum(INCLINATION, mode)
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
                enumparser(FACE)
            )
        )

    def get_angle(
        self,
        mode: INCLINATION | str = INCLINATION.AUTO
    ) -> GeoComResponse[tuple[Angle, Angle]]:
        """
        RPC 2107, ``TMC_GetAngle5``

        Takes an angular measurement with the selected inclination
        correction mode.

        Parameters
        ----------
        mode : INCLINATION | str, optional
            Inclination correction mode, by default INCLINATION.AUTO

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
        do_measure
        get_simple_mea

        """
        _mode = toenum(INCLINATION, mode)
        return self._request(
            2107,
            [_mode.value],
            (
                Angle.parse,
                Angle.parse
            )
        )

    def quick_dist(self) -> GeoComResponse[tuple[Angle, Angle, float]]:
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
        get_angle_incline,
        do_measure
        if_data_aze_corr_error
        if_data_inc_corr_error

        """
        return self._request(
            2117,
            parsers=(
                Angle.parse,
                Angle.parse,
                float
            )
        )

    def do_measure(
        self,
        command: MEASUREMENT | str = MEASUREMENT.DISTANCE,
        inclination: INCLINATION | str = INCLINATION.AUTO
    ) -> GeoComResponse[None]:
        """
        RPC 2008, ``TMC_DoMeasure``

        Carries out a distance measurement with the specified measurement
        program and inclination correction mode. The results are not
        returned, but kept in memory until the next measurement command.

        Parameters
        ----------
        command: MEASURE | str, optional
            Distance measurement program, by default MEASURE.DISTANCE
        inclination : INCLINATION | str, optional
            Inclination correction mode, by default INCLINATION.AUTO

        Returns
        -------
        GeoComResponse

        See Also
        --------
        set_edm_mode
        get_coordinate
        get_simple_mea
        get_angle
        get_angle_incline

        """
        _cmd = toenum(MEASUREMENT, command)
        _mode = toenum(INCLINATION, inclination)
        return self._request(
            2008,
            [_cmd.value, _mode.value]
        )

    def set_hand_dist(
        self,
        distance: float,
        offset: float,
        inclination: INCLINATION | str = INCLINATION.AUTO
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
        inclination : INCLINATION | str, optional
            Inclination correction mode, by default INCLINATION.AUTO

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
        if_data_aze_corr_error
        if_data_inc_corr_error

        """
        _mode = toenum(INCLINATION, inclination)
        return self._request(
            2019,
            [distance, offset, _mode.value]
        )

    def get_height(self) -> GeoComResponse[float]:
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
        set_height

        """
        return self._request(
            2011,
            parsers=float
        )

    def set_height(
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
        get_height

        """
        return self._request(
            2012,
            [height]
        )

    def get_atm_corr(
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
        set_atm_corr

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

    def set_atm_corr(
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
        get_atm_corr

        """
        return self._request(
            2028,
            [wavelength, pressure, drytemp, wettemp]
        )

    def set_orientation(
        self,
        azimut: float
    ) -> GeoComResponse[None]:
        """
        RPC 2113, ``TMC_SetOrientation``

        Sets the internal horizontal orientation offset so that the
        angular measurement reads the same as the provided angle.
        Previously measured distances must be cleared before orienting.

        Parameters
        ----------
        azimut : Angle
            Azimut angle to set.

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
        if_data_aze_corr_error
        if_data_inc_corr_error
        do_measure

        """
        return self._request(
            2113,
            [azimut]
        )

    def get_prism_corr(self) -> GeoComResponse[float]:
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
        set_prism_corr

        """
        return self._request(
            2023,
            parsers=float
        )

    def set_prism_corr(
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
        get_prism_corr

        """
        return self._request(
            2024,
            [const]
        )

    def get_refractive_corr(self) -> GeoComResponse[tuple[bool, float, float]]:
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
        set_refractive_corr

        """
        return self._request(
            2031,
            parsers=(
                parsebool,
                float,
                float
            )
        )

    def set_refractive_corr(
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
        get_refractive_corr

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
        do_measure

        """
        return self._request(
            2010,
            [station.x, station.y, station.z, hi]
        )

    def get_face(self) -> GeoComResponse[FACE]:
        """
        RPC 2026, ``TMC_GetFace``

        Gets which face the telescope is corrently positioned in. The face
        information is only valid, if the instrument is in active state.

        Returns
        -------
        GeoComResponse
            Params:
                - `FACE`: Current face.

        See Also
        --------
        aut.change_face

        """
        return self._request(
            2026,
            parsers=enumparser(FACE)
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
        do_measure

        """
        return self._request(
            2022,
            parsers=(
                float,
                int
            )
        )

    def get_angle_switch(
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
        set_angle_switch

        """
        return self._request(
            2014,
            parsers=(
                parsebool,
                parsebool,
                parsebool,
                parsebool
            )
        )

    def get_incline_switch(self) -> GeoComResponse[bool]:
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
        set_incline_switch

        """
        return self._request(
            2007,
            parsers=parsebool
        )

    def set_incline_switch(
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
        get_incline_switch

        """
        return self._request(
            2006,
            [enabled]
        )

    def get_edm_mode(self) -> GeoComResponse[EDMMODE]:
        """
        RPC 2021, ``TMC_GetEdmMode``

        Gets the current EDM measurement mode.

        Returns
        -------
        GeoComResponse
            Params:
                - `EDMMODEV1`: Current EDM mode.

        See Also
        --------
        set_edm_mode

        """
        return self._request(
            2021,
            parsers=enumparser(EDMMODEV1)
        )

    def set_edm_mode(
        self,
        mode: EDMMODE | str
    ) -> GeoComResponse[None]:
        """
        RPC 2020, ``TMC_SetEdmMode``

        Sets the EDM measurement mode.

        Parameters
        ----------
        mode : EDMMODEV1 | str
            EDM mode to activate.

        Returns
        -------
        GeoComResponse

        See Also
        --------
        get_edm_mode

        """
        _mode = toenum(EDMMODEV1, mode)
        return self._request(
            2020,
            [_mode.value]
        )

    def get_simple_coord(
        self,
        wait: int = 5000,
        inclination: INCLINATION | str = INCLINATION.AUTO
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
            Wait time for EDM process [ms], by default 5000
        inclination : INCLINATION | str, optional
            Inclination correction mode, by default INCLINATION.AUTO

        Returns
        -------
        GeoComResponse
            Params:
                - `COORDINATE`: Calculated coordinate.
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
        if_data_aze_corr_error
        if_data_inc_corr_error

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

        _mode = toenum(INCLINATION, inclination)
        response = self._request(
            2116,
            [wait, _mode.value],
            parsers=(
                float,
                float,
                float
            )
        )

        return response.map_params(transform)

    def if_data_aze_corr_error(self) -> GeoComResponse[bool]:
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
        if_data_inc_corr_error

        """
        return self._request(
            2114,
            parsers=parsebool
        )

    def if_data_inc_corr_error(self) -> GeoComResponse[bool]:
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
        if_data_inc_corr_error

        """
        return self._request(
            2115,
            parsers=parsebool
        )

    def set_angle_switch(
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
        do_measure
        get_angle_switch

        """
        return self._request(
            2016,
            [inclinecorr, stdaxiscorr, collimcorr, tiltaxiscorr]
        )
