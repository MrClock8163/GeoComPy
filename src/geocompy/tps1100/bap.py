"""
Description
===========

Module: ``geocompy.tps1100.bap``

Definitions for the TPS1100 Basic applications subsystem.

Types
-----

- ``TPS1100BAP``

"""
from __future__ import annotations

from ..data import (
    toenum,
    enumparser,
    parsestr,
    EDMPROGRAM,
    TARGET,
    PRISM,
    REFLECTOR
)
from ..protocols import GeoComResponse
from ..tps1000.bap import TPS1000BAP


class TPS1100BAP(TPS1000BAP):
    """
    Basic applications subsystem of the TPS1100 GeoCom protocol.

    This subsystem contains high-level functions that are also accessible
    through the user interface. The commands combine several subcommands
    for ease of operation.

    """

    def get_target_type(self) -> GeoComResponse[TARGET]:
        """
        RPC 17022, ``BAP_GetTargetType``

        .. versionadded:: GeoCom-TPS1100-1.05

        Gets the current EDM target type.

        Returns
        -------
        GeoComResponse
            Params:
                - `TARGET`: Current EMD target type.

        See Also
        --------
        set_target_type
        """
        return self._request(
            17022,
            parsers=enumparser(TARGET)
        )

    def set_target_type(
        self,
        target: TARGET | str
    ) -> GeoComResponse[None]:
        """
        RPC 17021, ``BAP_SetTargetType``

        .. versionadded:: GeoCom-TPS1100-1.05

        Sets the EDM target type. The last target type is remembered for
        all EDM modes.

        Parameters
        ----------
        target : TARGET | str
            New EDM target type to set.

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``IVPARAM``: Target type is not available.

        See Also
        --------
        get_target_type
        set_meas_prg
        """
        _target = toenum(TARGET, target)
        return self._request(
            17021,
            [_target.value]
        )

    def get_prism_type(self) -> GeoComResponse[PRISM]:
        """
        RPC 17009, ``BAP_GetPrismType``

        .. versionadded:: GeoCom-TPS1100-1.05

        Gets the current prism type.

        Returns
        -------
        GeoComResponse
            Params:
                - `PRISM`: Current prism type.
            Error codes:
                - ``IVRESULT``: EDM is set to reflectorless mode.

        See Also
        --------
        set_prism_type
        """
        return self._request(
            17009,
            parsers=enumparser(PRISM)
        )

    def set_prism_type(
        self,
        prism: PRISM | str
    ) -> GeoComResponse[None]:
        """
        RPC 17008, ``BAP_SetPrismType``

        .. versionadded:: GeoCom-TPS1100-1.05

        Sets the prism type. Prism change also overwrites the current
        prism constant.

        Parameters
        ----------
        prism : PRISM | str
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
        _prism = toenum(PRISM, prism)
        return self._request(
            17008,
            [_prism.value]
        )

    def get_prism_def(
        self,
        prism: PRISM | str
    ) -> GeoComResponse[tuple[str, float, REFLECTOR]]:
        """
        RPC 17023, ``BAP_GetPrismDef``

        .. versionadded:: GeoCom-TPS1100-1.05

        Gets the definition of the default prism.

        Parameters
        ----------
        prism : PRISM | str
            Prism type to query.

        Returns
        -------
        GeoComResponse
            Params:
                - `str`: Name of the prism.
                - `float`: Additive prism constant.
                - `REFLECTOR`: Reflector type.
            Error codes:
                - ``IVPARAM``: Invalid prism type.

        """
        _prism = toenum(PRISM, prism)
        return self._request(
            17023,
            [_prism.value],
            (
                parsestr,
                float,
                enumparser(REFLECTOR)
            )
        )

    def set_prism_def(
        self,
        prism: PRISM | str,
        name: str,
        const: float,
        reflector: REFLECTOR | str
    ) -> GeoComResponse[None]:
        """
        RPC 17024, ``BAP_SetPrismDef``

        .. versionadded:: GeoCom-TPS1100-1.05

        Defines a user prism.

        Parameters
        ----------
        prism : PRISM | str
            Type of the new prism. (Can be USER1, 2 and 3.)
        name : str
            Definition name. (Maximum 16 characters. Longer names will be
            truncated.)
        const : float
            Additive prism constant.
        reflector : REFLECTOR | str
            Reflector type.

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``IVPARAM``: Invalid prism type.

        """
        _prism = toenum(PRISM, prism)
        _reflector = toenum(REFLECTOR, reflector)
        name = f"{name:.16s}"
        return self._request(
            17024,
            [
                _prism.value,
                name,
                const,
                _reflector.value
            ]
        )

    def get_meas_prg(self) -> GeoComResponse[EDMPROGRAM]:
        """
        RPC 17018, ``BAP_GetMeasPrg``

        Gets the current measurement program.

        Returns
        -------
        GeoComResponse
            Params:
                - `EDMPROGRAM`: Current measurement program.

        See Also
        --------
        set_meas_prg
        """
        return self._request(
            17018,
            parsers=enumparser(EDMPROGRAM)
        )

    def set_meas_prg(
        self,
        program: EDMPROGRAM | str
    ) -> GeoComResponse[None]:
        """
        RPC 17019, ``BAP_SetMeasPrg``

        Sets a new measurement program.

        Parameters
        ----------
        program : EDMPROGRAM | str
            Measurement program to set.

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``IVPARAM``: Measurement program is not available.

        See Also
        --------
        get_meas_prg
        set_target_type
        """
        _program = toenum(EDMPROGRAM, program)
        return self._request(
            17019,
            [_program.value]
        )

    def search_target(self) -> GeoComResponse[None]:
        """
        RPC 17020, ``BAP_SearchTarget``

        .. versionadded:: GeoCom-TPS1100-1.04

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
        aut.get_user_spiral
        aut.set_user_spiral
        aut.get_search_area
        aut.set_search_area
        """
        return self._request(17020, [0])
