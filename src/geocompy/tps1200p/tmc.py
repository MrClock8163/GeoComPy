"""
Description
===========

Module: ``geocompy.tps1200p.tmc``

Definitions for the TPS1200+ Theodolite measurement and calculation
subsystem.

Types
-----

- ``TPS1200PTMC``

"""
from __future__ import annotations

from enum import Enum

from ..data import (
    Angle,
    Coordinate,
    toenum,
    enumparser
)
from ..protocols import (
    GeoComSubsystem,
    GeoComResponse
)


class TPS1200PTMC(GeoComSubsystem):
    """
    Theodolite measurement and calculation subsystem of the TPS1200+
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
    class ONOFF(Enum):
        OFF = 0
        ON = 1

    class INCLINEPRG(Enum):
        MEA = 0  # : Measure inclination.
        AUTO = 1  # : Automatic inclination handling.
        PLANE = 2  # : Model inclination from previous measurements.

    class MEASUREPRG(Enum):
        STOP = 0  # : Stop measurement program.
        DEFDIST = 1  # : Default distance measurement.
        CLEAR = 3  # : Clear current measurement data.
        SIGNAL = 4  # : Signal intensity measurement.
        DOMEASURE = 6  # : Start/Restart measurement.
        RTRKDIST = 8  # : Track distance.
        REDTRKDIST = 10  # : Reflectorless tracking.
        FREQUENCY = 11  # : Frequency measurement.

    class EDMMODE(Enum):
        NOTUSED = 0  # : Initialization mode.
        SINGLE_TAPE = 1  # : IR standard with reflector tape.
        SINGLE_STANDARD = 2  # : IR standard.
        SINGLE_FAST = 3  # : IR fast.
        SINGLE_LRANGE = 4  # : LO standard.
        SINGLE_SRANGE = 5  # : RL standard.
        CONT_STANDARD = 6  # : Continuous standard.
        CONT_DYNAMIC = 7  # : IR tracking.
        CONT_REFLESS = 8  # : RL tracking.
        CONT_FAST = 9  # : Continuous fast.
        AVERAGE_IR = 10  # : IR average.
        AVERAGE_SR = 11  # : RL average.
        AVERAGE_LR = 12  # : LO average.
        PRECISE_IR = 13  #: IR precise (TS30, MS30).
        PRECISE_TAPE = 14  #: IR precise with reflector tape (TS30, MS30).

    class FACEDEF(Enum):
        NORMAL = 0
        TURN = 1

    class FACE(Enum):
        FACE1 = 0
        FACE2 = 1

    def get_coordinate(
        self,
        wait: int = 5000,
        mode: INCLINEPRG | str = INCLINEPRG.AUTO
    ) -> GeoComResponse:
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
        mode : INCLINEPRG | str, optional
            Inclination correction mode, by default INCLINEPRG.AUTO

        Returns
        -------
        GeoComResponse
            - Params:
                - **coord** (`COORDINATE`): Calculated coordinate.
                - **time** (`int`): Time of the coordinate acquisition.
                - **coord_cont** (`COORDINATE`): Continuously calculated
                  coordinate.
                - **time_cont** (`int`): Time of the coordinate
                  acquisition.
            - Warning codes:
                - ``TMC_ACCURACY_GUARANTEE``: Accuracy is not guaranteed,
                  because the measurement contains data with unverified
                  accuracy. Coordinates are available.
                - ``TMC_NO_FULL_CORRECTION``: Results are not corrected by
                  all sensors. Coordinates are available. Run check
                  commands to determine the missing correction.
            - Error codes:
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
        mode : INCLINEPRG | str, optional
            Inclination correction mode, by default INCLINEPRG.AUTO

        Returns
        -------
        GeoComResponse
            - Params:
                - **hz** (`Angle`): Horizontal angle.
                - **v** (`Angle`): Vertical angle.
                - **dist** (`float`): Slope distance.
            - Warning codes:
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
            - Error codes:
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
            - Params:
                - **hz** (`Angle`): Horizontal angle.
                - **v** (`Angle`): Vertical angle.
                - **angleaccuracy** (`Angle`): Angular accuracy.
                - **angletime** (`int`): Time of angle measurement.
                - **crossincline** (`Angle`): Cross inclination.
                - **lengthincline** (`Angle`): Lengthwise inclination.
                - **inclineaccuracy** (`Angle`): Inclination accuracy.
                - **inclinetime** (`int`): Time of inclination measurement.
                - **face** (`FACEDEF`): Instrument face.
            - Warning codes:
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
            - Error codes:
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
                "face": enumparser(self.FACEDEF)
            }
        )

    def get_angle(
        self,
        mode: INCLINEPRG | str = INCLINEPRG.AUTO
    ) -> GeoComResponse:
        """
        RPC 2107, ``TMC_GetAngle5``

        Takes an angular measurement with the selected inclination
        correction mode.

        Parameters
        ----------
        mode : INCLINEPRG | str, optional
            Inclination correction mode, by default INCLINEPRG.AUTO

        Returns
        -------
        GeoComResponse
            - Params:
                - **hz** (`Angle`): Horizontal angle.
                - **v** (`Angle`): Vertical angle.
            - Warning codes:
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
            - Error codes:
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
        """
        RPC 2117, ``TMC_QuickDist``

        Starts an EDM tracking measurement and waits until a distance is
        measured.

        Returns
        -------
        GeoComResponse
            - Params:
                - **hz** (`Angle`): Horizontal angle.
                - **v** (`Angle`): Vertical angle.
                - **dist** (`float`): Slope distance.
            - Warning codes:
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
            - Error codes:
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
        """
        RPC 2167, ``TMC_GetFullMeas``

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
        mode : INCLINEPRG | str, optional
            Inclination correction mode, by default INCLINEPRG.AUTO

        Returns
        -------
        GeoComResponse
            - Params:
                - **hz** (`Angle`): Horizontal angle.
                - **v** (`Angle`): Vertical angle.
                - **angleaccuracy** (`Angle`): Angular accuracy.
                - **crossincline** (`Angle`): Cross inclination.
                - **lengthincline** (`Angle`): Lengthwise inclination.
                - **inclineaccuracy** (`Angle`): Inclination accuracy.
                - **dist** (`float`): Slope distance.
                - **disttime** (`int`): Time of distance measurement.
            - Warning codes:
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
            - Error codes:
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
        """
        RPC 2008, ``TMC_DoMeasure``

        Carries out a distance measurement with the specified measurement
        program and inclination correction mode. The results are not
        returned, but kept in memory until the next measurement command.

        Parameters
        ----------
        command: MEASREPRG | str, optional
            Distance measurement program, by default MEASUREPRG.DEFDIST
        mode : INCLINEPRG | str, optional
            Inclination correction mode, by default INCLINEPRG.AUTO

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
        mode : INCLINEPRG | str, optional
            Inclination correction mode, by default INCLINEPRG.AUTO

        Returns
        -------
        GeoComResponse
            - Warning codes:
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
            - Error codes:
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
        _mode = toenum(self.INCLINEPRG, mode)
        return self._request(
            2019,
            [distance, offset, _mode.value]
        )

    def get_height(self) -> GeoComResponse:
        """
        RPC 2011, ``TMC_GetHeight``

        Gets the current target height.

        Returns
        -------
        GeoComResponse
            - Params:
                - **height** (`float`): Current target height.

        See Also
        --------
        set_height

        """
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
            - Error codes:
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

    def get_atm_corr(self) -> GeoComResponse:
        """
        RPC 2029, ``TMC_GetAtmCorr``

        Gets current parameters of the atmospheric correction.

        Returns
        -------
        GeoComResponse
            - Params:
                - **wavelength** (`float`): EDM transmitter wavelength.
                - **pressure** (`float`): Atmospheric pressure [mbar].
                - **drytemp** (`float`): Dry temperature [°C].
                - **wettemp** (`float`): Wet temperature [°C].

        See Also
        --------
        set_atm_corr

        """
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
    ) -> GeoComResponse:
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
            - Warning codes:
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
            - Error codes:
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

    def get_prism_corr(self) -> GeoComResponse:
        """
        RPC 2023, ``TMC_GetPrismCorr``

        Gets the current prism constant.

        Returns
        -------
        GeoComResponse
            - Params:
                - **const** (`float`): Prism constant.

        See Also
        --------
        set_prism_corr

        """
        return self._request(
            2023,
            parsers={
                "const": float
            }
        )

    def set_prism_corr(
        self,
        const: float
    ) -> GeoComResponse:
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

    def get_refractive_corr(self) -> GeoComResponse:
        """
        RPC 2031, ``TMC_GetRefractiveCorr``

        Gets current refraction correction coefficients.

        Returns
        -------
        GeoComResponse
            - Params:
                - **enabled** (`bool`): Refraction correction enabled.
                - **earthradius** (`float`): Radius of the Earth.
                - **coef** (`float`): Refraction coefficient.

        See Also
        --------
        set_refractive_corr

        """
        return self._request(
            2031,
            parsers={
                "enabled": bool,
                "earthradius": float,
                "coef": float
            }
        )

    def set_refractive_corr(
        self,
        enabled: bool,
        earthradius: float = 6_378_000,
        coef: float = 0.13
    ) -> GeoComResponse:
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

    def get_refractive_method(self) -> GeoComResponse:
        """
        RPC 2091, ``TMC_GetRefractiveMethod``

        Gets the current refraction mode.

        Returns
        -------
        GeoComResponse
            - Params:
                - **method** (`int`): Refraction method.

        See Also
        --------
        set_refractive_method

        """
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

    def get_station(self) -> GeoComResponse:
        """
        RPC 2009, ``TMC_GetStation``

        Gets the current station coordinates and instrument height.

        Returns
        -------
        GeoComResponse
            - Params:
                - **station** (`Coordinate`): Station coordinates.
                - **hi** (`float`): Height of instrument.

        See Also
        --------
        set_station

        """
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
            "station": coord,
            "hi": response.params["hi"]
        }
        return response

    def set_station(
        self,
        station: Coordinate,
        hi: float
    ) -> GeoComResponse:
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
            - Error codes:
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

    def get_atm_ppm(self) -> GeoComResponse:
        """
        RPC 2151, ``TMC_GetAtmPpm``

        Gets the current atmospheric correction factor.

        Returns
        -------
        GeoComResponse
            - Params:
                - **ppm** (`float`): Atmospheric correction factor [ppm].

        See Also
        --------
        set_atm_ppm
        get_geo_ppm
        set_geo_ppm
        get_prism_corr
        set_prism_corr

        """
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
        """
        RPC 2148, ``TMC_SetAtmPpm``

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
        get_atm_ppm
        get_geo_ppm
        set_geo_ppm
        get_prism_corr
        set_prism_corr

        """
        return self._request(
            2148,
            [ppm]
        )

    def get_geo_ppm(self) -> GeoComResponse:
        """
        RPC 2154, ``TMC_GetGeoPpm``

        Gets the current geometric correction factors.

        Returns
        -------
        GeoComResponse
            - Params:
                - **automatic** (`bool`): Autmatically apply geometric
                  corrections.
                - **meridianscale** (`float`): Scale factor on central
                  meridian.
                - **meridianoffset** (`float`): Offset from central
                  meridian.
                - **reduction** (`float`): Length reduction from projection
                  to reference level.
                - **individual** (`float`): Individual correction [ppm].

        See Also
        --------
        get_atm_ppm
        set_atm_ppm
        set_geo_ppm
        get_prism_corr
        set_prism_corr

        """
        return self._request(
            2154,
            parsers={
                "automatic": bool,
                "meridianscale": float,
                "meridianoffset": float,
                "reduction": float,
                "individual": float
            }
        )

    def set_geo_ppm(
        self,
        automatic: bool,
        meridianscale: float,
        meridianoffset: float,
        reduction: float,
        individual: float
    ) -> GeoComResponse:
        """
        RPC 2153, ``TMC_SetGeoPpm``

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
        get_atm_ppm
        set_atm_ppm
        get_geo_ppm
        get_prism_corr
        set_prism_corr

        """
        return self._request(
            2153,
            [
                automatic,
                meridianscale, meridianoffset,
                reduction, individual
            ]
        )

    def get_face(self) -> GeoComResponse:
        """
        RPC 2026, ``TMC_GetFace``

        Gets which face the telescope is corrently positioned in. The face
        information is only valid, if the instrument is in active state.

        Returns
        -------
        GeoComResponse
            - Params:
                - **face** (`FACE`): Current face.

        See Also
        --------
        aut.change_face

        """
        return self._request(
            2026,
            parsers={
                "face": enumparser(self.FACE)
            }
        )

    def get_signal(self) -> GeoComResponse:
        """
        RPC 2022, ``TMC_GetSignal``

        Gets information about the intensity of the EDM signal. The EDM
        most be started in signal measuring mode in advance, and has to
        be cleared afterwards.

        Returns
        -------
        GeoComResponse
            - Params:
                - **intensity** (`float`): Return signal intensity [%].
                - **time** (`int`): Time of the signal measurement.
            - Error codes:
                - ``TMC_SIGNAL_ERROR``: Error in signal measurement.
                - ``ABORT``: Measurement was aborted.
                - ``SHUT_DOWN``: System shutdown.

        See Also
        --------
        do_measure

        """
        return self._request(
            2022,
            parsers={
                "intensity": float,
                "time": int
            }
        )

    def get_angle_switch(self) -> GeoComResponse:
        """
        RPC 2014, ``TMC_GetAngSwitch``

        Gets the current status of the angular corrections.

        Returns
        -------
        GeoComResponse
            - Params:
                - **inclinecorr** (`bool`): Inclination correction.
                - **stdaxiscorr** (`bool`): Standing axis correction.
                - **collimcorr** (`bool`): Collimation error correction.
                - *tiltaxiscorr** (`bool`): Tilting axis correction.

        See Also
        --------
        set_angle_switch

        """
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
        """
        RPC 2007, ``TMC_GetInclineSwitch``

        Gets the current status of the dual axis compensator.

        Returns
        -------
        GeoComResponse
            - Params:
                - **compensator** (`ONOFF`): Compensator status.

        See Also
        --------
        set_incline_switch

        """
        return self._request(
            2007,
            parsers={
                "compensator": enumparser(self.ONOFF)
            }
        )

    def set_incline_switch(
        self,
        compensator: ONOFF | str
    ) -> GeoComResponse:
        """
        RPC 2006, ``TMC_SetInclineSwitch``

        Sets the status of the dual axis compensator.

        Parameters
        ----------
        compensator : ONOFF | str
            Compensator status to set.

        Returns
        -------
        GeoComResponse

        See Also
        --------
        get_incline_switch

        """
        _corr = toenum(self.ONOFF, compensator)
        return self._request(
            2006,
            [_corr.value]
        )

    def get_edm_mode(self) -> GeoComResponse:
        """
        RPC 2021, ``TMC_GetEdmMode``

        Gets the current EDM measurement mode.

        Returns
        -------
        GeoComResponse
            - Params:
                - **mode** (`EDMMODE`): Current EDM mode.

        See Also
        --------
        set_edm_mode

        """
        return self._request(
            2021,
            parsers={
                "mode": enumparser(self.EDMMODE)
            }
        )

    def set_edm_mode(
        self,
        mode: EDMMODE | str
    ) -> GeoComResponse:
        """
        RPC 2020, ``TMC_SetEdmMode``

        Sets the EDM measurement mode.

        Parameters
        ----------
        mode : EDMMODE | str
            EDM mode to activate.

        Returns
        -------
        GeoComResponse

        See Also
        --------
        get_edm_mode

        """
        _mode = toenum(self.EDMMODE, mode)
        return self._request(
            2020,
            [_mode.value]
        )

    def get_simple_coord(
        self,
        wait: int = 5000,
        mode: INCLINEPRG | str = INCLINEPRG.AUTO
    ) -> GeoComResponse:
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
        mode : INCLINEPRG | str, optional
            Inclination correction mode, by default INCLINEPRG.AUTO

        Returns
        -------
        GeoComResponse
            - Params:
                - **coord** (`COORDINATE`): Calculated coordinate.
            - Warning codes:
                - ``TMC_ACCURACY_GUARANTEE``: Accuracy is not guaranteed,
                  because the measurement contains data with unverified
                  accuracy. Coordinates are available.
                - ``TMC_NO_FULL_CORRECTION``: Results are not corrected by
                  all sensors. Coordinates are available. Run check
                  commands to determine the missing correction.
            - Error codes:
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
        _mode = toenum(self.INCLINEPRG, mode)
        return self._request(
            2116,
            [wait, _mode.value],
            parsers={
                "east": float,
                "north": float,
                "height": float
            }
        )

    def if_data_aze_corr_error(self) -> GeoComResponse:
        """
        RPC 2114, ``TMC_IfDataAzeCorrError``

        Gets status of the ATR correction in the last measurement.

        Returns
        -------
        GeoComResponse
            - Params:
                - **atrerror** (`bool`): Last data record was not
                  corrected with ATR deviation.

        See Also
        --------
        if_data_inc_corr_error

        """
        return self._request(
            2114,
            parsers={
                "atrerror": bool
            }
        )

    def if_data_inc_corr_error(self) -> GeoComResponse:
        """
        RPC 2115, ``TMC_IfDataIncCorrError``

        Gets status of the inclination correction in the last measurement.

        Returns
        -------
        GeoComResponse
            - Params:
                - **inclineerror** (`bool`): Last data record was not
                  corrected with inclination correction.

        See Also
        --------
        if_data_inc_corr_error

        """
        return self._request(
            2115,
            parsers={
                "inclineerror": bool
            }
        )

    def set_angle_switch(
        self,
        inclinecorr: bool,
        stdaxiscorr: bool,
        collimcorr: bool,
        tiltaxiscorr: bool
    ) -> GeoComResponse:
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
            - Error codes:
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

    def get_slope_dist_corr(self) -> GeoComResponse:
        """
        RPC 2126, ``TMC_GetSlopDistCorr``

        Gets the total correction (atmospheric + geometric) applied to the
        distance measurements, as well as the current prism constant.

        Returns
        -------
        GeoComResponse
            - Params:
                - **ppmcorr** (`float`): Total corrections [ppm].
                - **prismcorr** (`float`): Prism constant.

        See Also
        --------
        get_prism_corr
        set_prism_corr

        """
        return self._request(
            2126,
            parsers={
                "ppmcorr": float,
                "prismcorr": float
            }
        )
