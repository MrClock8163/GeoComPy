"""
Description
===========

Module: ``geocompy.geo.bap``

Definitions for the GeoCOM Basic applications subsystem.

Types
-----

- ``GeoComBAP``

"""
from __future__ import annotations

from ..data import (
    Angle,
    get_enum,
    get_enum_parser,
    parse_string,
    parse_bool
)
from .gcdata import (
    Program,
    Prism,
    Reflector,
    Target,
    UserProgram,
    ATRMode
)
from .gctypes import (
    GeoComSubsystem,
    GeoComResponse
)


class GeoComBAP(GeoComSubsystem):
    """
    Basic applications subsystem of the GeoCOM protocol.

    This subsystem contains high-level functions that are also accessible
    through the user interface. The commands combine several subcommands
    for ease of operation.

    """

    def get_last_displayed_error(self) -> GeoComResponse[tuple[int, int]]:
        """
        RPC 17003, ``BAP_GetLastDisplayedError``

        .. versionremoved:: GeoCOM-TPS1200

        Retrieves the number of the last displayed system error.

        Returns
        -------
        GeoComResponse
            Params:
                - `int`: Last error, warning or info number.
                - `int`: Corresponding GSI error number.

            Error codes:
                - ``IVRESULT``: No error was displayed since last call.

        Note
        ----
        The error code will be reset once command is executed. A repeated
        call will be unsuccessful.
        """
        return self._request(
            17003,
            parsers=(
                int,
                int
            )
        )

    def measure_distance_angle(
        self,
        mode: Program | str = Program.DISTANCE
    ) -> GeoComResponse[tuple[Angle, Angle, float, Program]]:
        """
        RPC 17017, ``BAP_MeasDistanceAngle``

        Take an angle and distance measuremnt depending on the distance
        mode.

        Parameters
        ----------
        mode : Program | str, optional
            Distance measurement mode to use, by default
            Program.DISTANCE

        Returns
        -------
        GeoComResponse
            Params:
                - `Angle`: Horizontal angle.
                - `Angle`: Vertical angle.
                - `float`: Slope distance.
                - `MEASUREPRG`: Actual distance mode.
            Info codes:
                - ``TMC_ACCURACY_GUARANTEE``: Accuracy cannot be guaranteed.
                - ``TMC_ANGLE_ACCURACY_GUARANTEE``: Only angle measurement
                  valid, accuracy cannot be guaranteed.
            Warning codes:
                - ``TMC_ANGLE_NO_FULL_CORRECTION``: Only angle measurement
                  valid, accuracy cannot be guaranteed.
                - ``TMC_ANGLE_OK``: Only angle measurement valid.
                - ``TMC_NO_FULL_CORRECTION``: Measurement without full
                  correction.
            Error codes:
                - ``AUT_ANGLE_ERROR``: Angle measurement error.
                - ``AUT_BAD_ENVIRONMENT``: Bad environmental conditions.
                - ``AUT_CALACC``: ATR calibration failed.
                - ``AUT_DETECTOR_ERROR``: Error in target acquisition.
                - ``AUT_DETENT_ERROR``: Positioning not possible.
                - ``AUT_DEV_ERROR``: Error in angle deviation calculation.
                - ``AUT_INCACC``: Position not exactly reached.
                - ``AUT_MOTOR_ERROR``: Motorization error.
                - ``AUT_MULTIPLE_TARGETS``: Multiple targets detected.
                - ``AUT_NO_TARGET``: No target detected.
                - ``AUT_TIMEOUT``: Position not reached.
                - ``BAP_CHANGE_ALL_TO_DIST``: Prism not detected, changed
                  command to ALL.
                - ``TMC_ANGLE_ERROR``: No valid angle measurement.
                - ``TMC_BUSY``: TMC submodule already in use by another
                  subsystem, command not processed.
                - ``TMC_DIST_ERROR``: An error occurred during distance
                  measurement.
                - ``TMC_DIST_PPM``: Wrong PPM setting.
                - ``TMC_SIGNAL_ERROR``: No signal on EDM (only in signal
                  mode).
                - ``ABORT``: Measurement aborted.
                - ``COM_TIMEDOUT``: Communication timeout.
                - ``IVPARAM``: Invalid distance mode.
                - ``SHUT_DOWN``: System stopped.

        """
        _mode = get_enum(Program, mode)
        return self._request(
            17017,
            [_mode],
            (
                Angle.parse,
                Angle.parse,
                float,
                get_enum_parser(Program)
            )
        )

    def get_target_type(self) -> GeoComResponse[Target]:
        """
        RPC 17022, ``BAP_GetTargetType``

        .. versionadded:: GeoCOM-TPS1100-1.05

        Gets the current EDM target type.

        Returns
        -------
        GeoComResponse
            Params:
                - `Target`: Current EMD target type.

        See Also
        --------
        set_target_type
        """
        return self._request(
            17022,
            parsers=get_enum_parser(Target)
        )

    def set_target_type(
        self,
        target: Target | str
    ) -> GeoComResponse[None]:
        """
        RPC 17021, ``BAP_SetTargetType``

        .. versionadded:: GeoCOM-TPS1100-1.05

        Sets the EDM target type. The last target type is remembered for
        all EDM modes.

        Parameters
        ----------
        target : Target | str
            New EDM target type to set.

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``IVPARAM``: Target type is not available.

        See Also
        --------
        get_target_type
        set_measurement_program
        """
        _target = get_enum(Target, target)
        return self._request(
            17021,
            [_target]
        )

    def get_prism_type(self) -> GeoComResponse[Prism]:
        """
        RPC 17009, ``BAP_GetPrismType``

        .. versionadded:: GeoCOM-TPS1100-1.05

        Gets the current prism type.

        Returns
        -------
        GeoComResponse
            Params:
                - `Prism`: Current prism type.

            Error codes:
                - ``IVRESULT``: EDM is set to reflectorless mode.

        See Also
        --------
        set_prism_type
        """
        return self._request(
            17009,
            parsers=get_enum_parser(Prism)
        )

    def set_prism_type(
        self,
        prism: Prism | str
    ) -> GeoComResponse[None]:
        """
        RPC 17008, ``BAP_SetPrismType``

        .. versionadded:: GeoCOM-TPS1100-1.05

        Sets the prism type. Prism change also overwrites the current
        prism constant.

        Parameters
        ----------
        prism : Prism | str
            New prism type to set.

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``IVPARAM``: Prism type is not available.

        See Also
        --------
        get_prism_type
        """
        _prism = get_enum(Prism, prism)
        return self._request(
            17008,
            [_prism]
        )

    def get_prism_definition(
        self,
        prism: Prism | str
    ) -> GeoComResponse[tuple[str, float, Reflector]]:
        """
        RPC 17023, ``BAP_GetPrismDef``

        .. versionadded:: GeoCOM-TPS1100-1.05

        Gets the definition of the default prism.

        Parameters
        ----------
        prism : Prism | str
            Prism type to query.

        Returns
        -------
        GeoComResponse
            Params:
                - `str`: Name of the prism.
                - `float`: Additive prism constant.
                - `Reflector`: Reflector type.

            Error codes:
                - ``IVPARAM``: Invalid prism type.

        """
        _prism = get_enum(Prism, prism)
        return self._request(
            17023,
            [_prism],
            (
                parse_string,
                float,
                get_enum_parser(Reflector)
            )
        )

    def set_prism_definition(
        self,
        prism: Prism | str,
        name: str,
        const: float,
        reflector: Reflector | str
    ) -> GeoComResponse[None]:
        """
        RPC 17024, ``BAP_SetPrismDef``

        .. versionadded:: GeoCOM-TPS1100-1.05

        .. versionremoved:: GeoCOM-TPS1200

        Defines a user prism.

        Parameters
        ----------
        prism : Prism | str
            Type of the new prism. (Can be USER1, 2 and 3.)
        name : str
            Definition name. (Maximum 16 characters. Longer names will be
            truncated.)
        const : float
            Additive prism constant.
        reflector : Reflector | str
            Reflector type.

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``IVPARAM``: Invalid prism type.

        """
        _prism = get_enum(Prism, prism)
        _reflector = get_enum(Reflector, reflector)
        name = f"{name:.16s}"
        return self._request(
            17024,
            [
                _prism,
                name,
                const,
                _reflector
            ]
        )

    def get_measurement_program(self) -> GeoComResponse[UserProgram]:
        """
        RPC 17018, ``BAP_GetMeasPrg``

        Gets the current measurement program.

        Returns
        -------
        GeoComResponse
            Params:
                - `UserProgram`: Current measurement program.

        See Also
        --------
        set_measurement_program
        """
        return self._request(
            17018,
            parsers=get_enum_parser(UserProgram)
        )

    def set_measurement_program(
        self,
        program: UserProgram | str
    ) -> GeoComResponse[None]:
        """
        RPC 17019, ``BAP_SetMeasPrg``

        Sets a new measurement program.

        Parameters
        ----------
        program : UserProgram | str
            Measurement program to set.

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``IVPARAM``: Measurement program is not available.

        See Also
        --------
        get_measurement_program
        set_target_type
        """
        _program = get_enum(UserProgram, program)
        return self._request(
            17019,
            [_program]
        )

    def search_target(self) -> GeoComResponse[None]:
        """
        RPC 17020, ``BAP_SearchTarget``

        .. versionadded:: GeoCOM-TPS1100-1.04

        Executes target search in the predefined window.

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``AUT_BAD_ENVIRONMENT``: Bad environmental conditions.
                - ``AUT_DEV_ERROR``: Error in angle deviation calculation.
                - ``AUT_ANGLE_ACCURACY``: Position not exactly reached.
                - ``AUT_MOTOR_ERROR``: Motorization error.
                - ``AUT_MULTIPLE_TARGETS``: Multiple targets detected.
                - ``AUT_NO_TARGET``: No target detected.
                - ``AUT_TIMEOUT``: Position not reached.
                - ``ABORT``: Measurement aborted.
                - ``FATAL``: Fatal error.

        See Also
        --------
        aut.get_spiral
        aut.set_spiral
        aut.get_search_area
        aut.set_search_area
        """
        return self._request(17020, [0])

    def get_prism_type_name(self) -> GeoComResponse[tuple[Prism, str]]:
        """
        RPC 17031, ``BAP_GetPrismType2``

        .. versionadded:: GeoCOM-TPS1200

        Gets the current prism type and name.

        Returns
        -------
        GeoComResponse
            Params:
                - `Prism`: Current prism type.
                - `str`: Prism type name.

        See Also
        --------
        set_prism_type
        set_prism_type_name
        """
        return self._request(
            17031,
            parsers=(get_enum_parser(Prism), parse_string)
        )

    def set_prism_type_name(
        self,
        prism: Prism | str,
        name: str
    ) -> GeoComResponse[None]:
        """
        RPC 17030, ``BAP_SetPrismType2``

        .. versionadded:: GeoCOM-TPS1200

        Sets the prism type and name.

        Parameters
        ----------
        prism : Prism | str
            Prism type to set.
        name : str
            Name of the prism type.

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``IVPARAM``: Prism type is not available, a user prism
                  is not defined.

        See Also
        --------
        get_prism_type_name
        tmc.set_prism_correction
        """
        _prism = get_enum(Prism, prism)
        return self._request(
            17030,
            [_prism, name]
        )

    def get_user_prism_definition(
        self,
        name: str
    ) -> GeoComResponse[tuple[float, Reflector, str]]:
        """
        RPC 17033, ``BAP_GetUserPrismDef``

        .. versionadded:: GeoCOM-TPS1200

        Gets the definition of a user defined prism.

        Parameters
        ----------
        name : str
            Name of the prism.

        Returns
        -------
        GeoComResponse
            Params:
                - `float`: Additive prism constant.
                - `Reflector`: Reflector type.
                - `str`: Creator of the prism definition.

            Error codes:
                - ``IVPARAM``: Invalid prism definition.

        See Also
        --------
        get_prism_type
        get_prism_type_name
        get_prism_definition
        set_user_prism_definition
        """
        return self._request(
            17033,
            [name],
            (
                float,
                get_enum_parser(Reflector),
                parse_string
            )
        )

    def set_user_prism_definition(
        self,
        name: str,
        const: float,
        reflector: Reflector | str,
        creator: str
    ) -> GeoComResponse[None]:
        """
        RPC 17032, ``BAP_SetUserPrismDef``

        .. versionadded:: GeoCOM-TPS1200

        Defines a new user defined prism.

        Parameters
        ----------
        name : str
            Name of the prism.
        const : float
            Additive prism constant.
        reflector: Reflector | str
            Reflector type.
        creator : str
            Name of the creator.

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``IVPARAM``: Invalid prism definition.
                - ``IVRESULT``: Prism definition is not set.

        See Also
        --------
        set_prism_type
        get_prism_definition
        set_user_prism_definition
        """
        _reflector = get_enum(Reflector, reflector)
        return self._request(
            17032,
            [name, const, _reflector, creator]
        )

    def get_atr_setting(self) -> GeoComResponse[ATRMode]:
        """
        RPC 17034, ``BAP_GetATRSetting``

        .. versionadded:: GeoCOM-TPS1200

        Gets the current ATR setting.

        Returns
        -------
        GeoComResponse
            Params:
                - `ATRMode`: Current ATR setting.

        See Also
        --------
        set_atr_setting
        """
        return self._request(
            17034,
            parsers=get_enum_parser(ATRMode)
        )

    def set_atr_setting(
        self,
        mode: ATRMode | str
    ) -> GeoComResponse[None]:
        """
        RPC 17035, ``BAP_SetATRSetting``

        .. versionadded:: GeoCOM-TPS1200

        Sets the ATR setting.

        Parameters
        ----------
        mode : ATRMode | str
            ATR setting to activate.

        See Also
        --------
        get_atr_setting
        """
        _mode = get_enum(ATRMode, mode)
        return self._request(
            17035,
            [_mode]
        )

    def get_reduced_atr_fov_status(self) -> GeoComResponse[bool]:
        """
        RPC 17036, ``BAP_GetRedATRFov``

        .. versionadded:: GeoCOM-TPS1200

        Gets the state of the reduced ATR field of view mode.

        Returns
        -------
        GeoComResponse
            Params:
                - `bool`: Reduced field of view ATR is enabled.

        See Also
        --------
        switch_reduced_atr_fov
        """
        return self._request(
            17036,
            parsers=parse_bool
        )

    def switch_reduced_atr_fov(
        self,
        enabled: bool
    ) -> GeoComResponse[None]:
        """
        RPC 17037, ``BAP_SetRedATRFov``

        .. versionadded:: GeoCOM-TPS1200

        Sets the state of the reduced ATR field of view mode.

        Parameters
        ----------
        enabled : bool
            Reduced field of view ATR is enabled.

        See Also
        --------
        get_reduced_atr_fov_status
        """
        return self._request(
            17037,
            [enabled]
        )

    def get_precise_atr_status(self) -> GeoComResponse[bool]:
        """
        RPC 17039, ``BAP_GetATRPrecise``

        .. versionadded:: GeoCOM-VivaTPS

        Gets the current state of the precise ATR mode.

        Returns
        -------
        GeoComResponse
            Params:
                - `bool`: Precise ATR mode is enabled.

        See Also
        --------
        switch_precise_atr
        """
        return self._request(
            17039,
            parsers=parse_bool
        )

    def switch_precise_atr(
        self,
        enabled: bool
    ) -> GeoComResponse[None]:
        """
        RPC 17040, ``BAP_SetATRPrecise``

        .. versionadded:: GeoCOM-VivaTPS

        Sets the state of the precise ATR mode.

        Parameters
        ----------
        enabled : bool
            Precise ATR mode is enabled.

        Returns
        -------
        GeoComResponse

        See Also
        --------
        get_precise_atr_status
        """
        return self._request(
            17040,
            [enabled]
        )
