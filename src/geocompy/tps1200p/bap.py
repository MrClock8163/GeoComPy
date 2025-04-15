"""
``geocompy.tps1200p.bap``
=========================

Definitions for the TPS1200+ Basic applications subsystem.

Types
-----

- ``TPS1200PBAP``

"""
from __future__ import annotations

from enum import Enum

from .. import (
    GeoComSubsystem,
    GeoComResponse
)
from ..data import (
    Angle,
    toenum,
    enumparser,
    parsestr
)


class TPS1200PBAP(GeoComSubsystem):
    """
    Basic applications subsystem of the TPS1200+ GeoCom protocol.

    This subsystem contains high-level functions that are also accessible
    through the user interface. The commands combine several subcommands
    for ease of operation.

    """
    class MEASUREPRG(Enum):
        NOMEAS = 0  # : No measurement, take last value.
        NODIST = 1  # : No distance measurement, angles only.
        DEFDIST = 2  # : Default distance measurement.
        CLEARDIST = 5  # : Clear distances.
        STOPTRK = 6  # : Stop tracking.

    class USERMEASPRG(Enum):
        SINGLE_REF_STANDARD = 0  # : IR standard.
        SINGLE_REF_FAST = 1  # : IR fast.
        SINGLE_REF_VISIBLE = 2  # : LO standard.
        SINGLE_RLESS_VISIBLE = 3  # : RL standard.
        CONT_REF_STANDARD = 4  # : IR tracking.
        CONT_REF_FAST = 5
        CONT_RLESS_VISIBLE = 6  # : RL fast tracking.
        AVG_REF_STANDARD = 7  # : IR average.
        AVG_REF_VISIBLE = 8  # : LO average.
        AVG_RLESS_VISIBLE = 9  # : RL average.
        CONT_REF_SYNCHRO = 10  # : IR synchro tracking.
        SINGLE_REF_PRECISE = 11  # : IR precise (TS30, MS30)

    class PRISMTYPE(Enum):
        ROUND = 0  # : Leica Circular Prism
        MINI = 1  # : Leica Mini Prism
        TAPE = 2  # : Leica Reflector Tape
        THREESIXTY = 3  # : Leica 360° Prism.
        USER1 = 4
        USER2 = 5
        USER3 = 6
        MINI360 = 7  # : Leica Mini 360° Prism.
        MINIZERO = 8  # : Leica Mini Zero Prism.
        USER = 9  # : User defined prism.
        NDSTAPE = 10  # : Leica HDS Target.
        GRZ121 = 11  # : Leica GRZ121 360° Prism.
        MAMPR122 = 12  # : Leica MPR122 360° Prism.

    class REFLTYPE(Enum):
        UNDEF = 0  # : Reflector not defined.
        PRISM = 1  # : Reflector prism.
        TAPE = 2  # : Reflector tape.

    class TARGETTYPE(Enum):
        REFL_USE = 0  # : Reflector.
        REFL_LESS = 1  # : Not reflector.

    class ATRSETTING(Enum):
        NORMAL = 0  # : Normal mode.
        LOWVISON = 1  # : Low visibility on.
        LOWVISAON = 2  # : Low visibility always on.
        SRANGEON = 3  # : High reflectivity on.
        SRANGEAON = 4  # : Hight reflectivity always on.

    class ONOFF(Enum):
        OFF = 0
        ON = 1

    def get_target_type(self) -> GeoComResponse:
        """
        RPC 17022, ``BAP_GetTargetType``

        Gets the current EDM target type.

        Returns
        -------
        GeoComResponse
            - Params:
                - **targettype** (`TARGETTYPE`): Current EMD target type.

        See Also
        --------
        set_target_type
        set_meas_prg
        """
        return self._request(
            17022,
            parsers={
                "targettype": enumparser(self.TARGETTYPE)
            }
        )

    def set_target_type(
        self,
        targettype: TARGETTYPE | str
    ) -> GeoComResponse:
        """
        RPC 17021, ``BAP_SetTargetType``

        Sets the EDM target type. The last target type is remembered for
        all EDM modes.

        Parameters
        ----------
        targettype : TARGETTYPE | str
            New EDM target type to set.

        Returns
        -------
        GeoComResponse
            - Error codes:
                - ``IVPARAM``: Target type is not available.

        See Also
        --------
        get_target_type
        set_meas_prg
        """
        _targettype = toenum(self.TARGETTYPE, targettype)
        return self._request(
            17021,
            [_targettype.value]
        )

    def get_prism_type(self) -> GeoComResponse:
        """
        RPC 17009, ``BAP_GetPrismType``

        Gets the current prism type.

        Returns
        -------
        GeoComResponse
            - Params:
                - **prismtype** (`PRISMTYPE`): Current prism type.
            - Error codes:
                - ``IVRESULT``: EDM is set to reflectorless mode.

        See Also
        --------
        set_prism_type
        """
        return self._request(
            17009,
            parsers={
                "prismtype": enumparser(self.PRISMTYPE)
            }
        )

    def set_prism_type(
        self,
        prismtype: PRISMTYPE | str
    ) -> GeoComResponse:
        """
        RPC 17008, ``BAP_SetPrismType``

        Sets the prism type. Prism change also overwrites the current
        prism constant.

        Parameters
        ----------
        prismtype : PRISMTYPE | str
            New prism type to set.

        Returns
        -------
        GeoComResponse
            - Error codes:
                - ``IVPARAM``: Prism type is not available.

        See Also
        --------
        get_prism_type2
        tmc.set_prism_corr
        """
        _prismtype = toenum(self.PRISMTYPE, prismtype)
        return self._request(
            17008,
            [_prismtype.value]
        )

    def get_prism_type2(self) -> GeoComResponse:
        """
        RPC 17031, ``BAP_GetPrismType2``

        Gets the current prism type and name.

        Returns
        -------
        GeoComResponse
            - Params:
                - **prismtype** (`PRISMTYPE`): Current prism type.
                - **name** (`str`): Prism type name.

        See Also
        --------
        set_prism_type
        set_prism_type2
        """
        return self._request(
            17031,
            parsers={
                "prismtype": enumparser(self.PRISMTYPE),
                "name": parsestr
            }
        )

    def set_prism_type2(
        self,
        prismtype: PRISMTYPE | str,
        name: str
    ) -> GeoComResponse:
        """
        RPC 17030, ``BAP_SetPrismType2``

        Sets the prism type and name.

        Parameters
        ----------
        prismtype : PRISMTYPE | str
            Prism type to set.
        name : str
            Name of the prism type.

        Returns
        -------
        GeoComResponse
            - Error codes:
                - ``IVPARAM``: Prism type is not available, a user prism
                  is not defined.

        See Also
        --------
        get_prism_type2
        tmc.set_prism_corr
        """
        _prismtype = toenum(self.PRISMTYPE, prismtype)
        return self._request(
            17030,
            [_prismtype.value, name]
        )

    def get_prism_def(
        self,
        prismtype: PRISMTYPE | str
    ) -> GeoComResponse:
        """
        RPC 17023, ``BAP_GetPrismDef``

        Gets the definition of the default prism.

        Parameters
        ----------
        prismtype : PRISMTYPE | str
            Prism type to query.

        Returns
        -------
        GeoComResponse
            - Params:
                - **name** (`str`): Name of the prism.
                - **const** (`float`): Additive prism constant.
                - **refltype** (`REFLTYPE`): Reflector type.
            - Error codes:
                - ``IVPARAM``: Invalid prism type.

        See Also
        --------
        set_user_prism_def
        """
        _prismtype = toenum(self.PRISMTYPE, prismtype)
        return self._request(
            17023,
            [_prismtype.value],
            {
                "name": parsestr,
                "const": float,
                "refltype": enumparser(self.REFLTYPE)
            }
        )

    def get_user_prism_def(
        self,
        name: str
    ) -> GeoComResponse:
        """
        RPC 17033, ``BAP_GetUserPrismDef``

        Gets the definition of a user defined prism.

        Parameters
        ----------
        name : str
            Name of the prism.

        Returns
        -------
        GeoComResponse
            - Params:
                - **name** (`str`): Name of the prism.
                - **const** (`float`): Additive prism constant.
                - **refltype** (`REFLTYPE`): Reflector type.
            - Error codes:
                - ``IVPARAM``: Invalid prism definition.

        See Also
        --------
        get_prism_type
        get_prism_type2
        get_prism_def
        set_user_prism_def
        """
        return self._request(
            17033,
            [name],
            {
                "const": float,
                "refltype": enumparser(self.REFLTYPE),
                "creator": parsestr
            }
        )

    def set_user_prism_def(
        self,
        name: str,
        const: float,
        refltype: REFLTYPE | str,
        creator: str
    ) -> GeoComResponse:
        """
        RPC 17032, ``BAP_SetUserPrismDef``

        Defines a new user defined prism.

        Parameters
        ----------
        name : str
            Name of the prism.
        const : float
            Additive prism constant.
        refltype: REFLTYPE | str
            Reflector type.
        creator : str
            Name of the creator.

        Returns
        -------
        GeoComResponse
            - Error codes:
                - ``IVPARAM``: Invalid prism definition.
                - ``IVRESULT``: Prism definition is not set.

        See Also
        --------
        set_prism_type
        get_prism_def
        set_user_prism_def
        """
        _refltype = toenum(self.REFLTYPE, refltype)
        return self._request(
            17032,
            [name, const, _refltype.value, creator]
        )

    def get_meas_prg(self) -> GeoComResponse:
        """
        RPC 17018, ``BAP_GetMeasPrg``

        Gets the current measurement program.

        Returns
        -------
        GeoComResponse
            - Params:
                - **measprg** (`MEASUREPRG`): Current measurement program.

        See Also
        --------
        set_meas_prg
        """
        return self._request(
            17018,
            parsers={
                "measprg": enumparser(self.MEASUREPRG)
            }
        )

    def set_meas_prg(
        self,
        measprg: MEASUREPRG | str
    ) -> GeoComResponse:
        """
        RPC 17019, ``BAP_SetMeasPrg``

        Sets a new measurement program.

        Parameters
        ----------
        measprg : MEASUREPRG | str
            Measurement program to set.

        Returns
        -------
        GeoComResponse
            - Error codes:
                - ``IVPARAM``: Measurement program is not available.

        See Also
        --------
        get_meas_prg
        set_target_type
        """
        _measprg = toenum(self.MEASUREPRG, measprg)
        return self._request(
            17019,
            [_measprg.value]
        )

    def meas_distance_angle(
        self,
        distmode: MEASUREPRG | str = MEASUREPRG.DEFDIST
    ) -> GeoComResponse:
        """
        RPC 17017, ``BAP_MeasDistanceAngle``

        Take an angle and distance measuremnt depending on the distance
        mode.

        Parameters
        ----------
        distmode : MEASUREPRG | str, optional
            Distance measurement mode to use, by default MEASUREPRG:DEFDIST

        Returns
        -------
        GeoComResponse
            - Params:
                - **hz** (`Angle`): Horizontal angle.
                - **v** (`Angle`): Vertical angle.
                - **dist** (`float`): Slope distance.
                - **distmode** (`MEASUREPRG`): Actual distance mode.
            - Info codes:
                - ``TMC_ACCURACY_GUARANTEE``: Accuracy cannot be guaranteed.
                - ``TMC_ANGLE_ACCURACY_GUARANTEE``: Only angle measurement
                  valid, accuracy cannot be guaranteed.
            - Warning codes:
                - ``TMC_ANGLE_NO_FULL_CORRECTION``: Only angle measurement
                  valid, accuracy cannot be guaranteed.
                - ``TMC_ANGLE_OK``: Only angle measurement valid.
                - ``TMC_NO_FULL_CORRECTION``: Measurement without full
                  correction.
            - Error codes:
                - ``AUT_ANGLE_ERROR``: Angle measurement error.
                - ``AUT_BAD_ENVIRONMENT``: Bad environmental conditions.
                - ``AUT_CALACC``: ATR calibration failed.
                - ``AUT_DETECTOR_ERROR``: Error in target acquisition.
                - ``AUT_DEV_ERROR``: Error in angle deviation calculation.
                - ``AUT_INCACC``: Position not exactly reached.
                - ``AUT_MOTOR_ERROR``: Motorization error.
                - ``AUT_MULTIPLE_TARGETS``: Multiple targets detected.
                - ``AUT_NO_TARGET``: No target detected.
                - ``AUT_TIMEOUT``: Position not reached.
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
        _distmode = toenum(self.MEASUREPRG, distmode)
        return self._request(
            17017,
            [_distmode.value],
            {
                "hz": Angle.parse,
                "v": Angle.parse,
                "dist": float,
                "distmode": enumparser(self.MEASUREPRG)
            }
        )

    def search_target(self) -> GeoComResponse:
        """
        RPC 17020, ``BAP_SearchTarget``

        Executes target search in the predefined PowerSearch window.

        Returns
        -------
        GeoComResponse
            - Error codes:
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
        aut.get_user_spiral
        aut.set_user_spiral
        get_atr_setting
        set_atr_setting
        get_red_atr_fov
        set_red_atr_fov
        """
        return self._request(17020, [0])

    def get_atr_setting(self) -> GeoComResponse:
        """
        RPC 17034, ``BAP_GetATRSetting``

        Gets the current ATR setting.

        Returns
        -------
        GeoComResponse
            - Params:
                - **atrsetting** (`ATRSETTING`): Current ATR setting.

        See Also
        --------
        set_atr_setting
        """
        return self._request(
            17034,
            parsers={
                "atrsetting": enumparser(self.ATRSETTING)
            }
        )

    def set_atr_setting(
        self,
        atrsetting: ATRSETTING | str
    ) -> GeoComResponse:
        """
        RPC 17035, ``BAP_SetATRSetting``

        Sets the ATR setting.

        Parameters
        ----------
        atrsetting : ATRSETTING | str
            ATR setting to activate.

        See Also
        --------
        get_atr_setting
        """
        _atrsetting = toenum(self.ATRSETTING, atrsetting)
        return self._request(
            17035,
            [_atrsetting.value]
        )

    def get_red_atr_fov(self) -> GeoComResponse:
        """
        RPC 17036, ``BAP_GetRedATRFov``

        Gets the state of the reduced ATR field of view mode.

        Returns
        -------
        GeoComResponse
            - Params:
                - **redfov** (`ONOFF`): State of the reduced FOV mode.

        See Also
        --------
        set_red_atr_fov
        """
        return self._request(
            17036,
            parsers={
                "redfov": enumparser(self.ONOFF)
            }
        )

    def set_red_atr_fov(
        self,
        redfov: ONOFF | str
    ) -> GeoComResponse:
        """
        RPC 17037, ``BAP_SetRedATRFov``

        Sets the state of the reduced ATR field of view mode.

        Parameters
        ----------
        redfov : ONOFF | str
            New state of the reduced ATR FOV mode.

        See Also
        --------
        get_red_atr_fov
        """
        _redfov = toenum(self.ONOFF, redfov)
        return self._request(
            17037,
            [_redfov.value]
        )
