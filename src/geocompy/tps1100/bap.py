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
    parsestr
)
from ..data_geocom import (
    Prism,
    Reflector,
    Target,
    UserProgram
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

    def get_target_type(self) -> GeoComResponse[Target]:
        """
        RPC 17022, ``BAP_GetTargetType``

        .. versionadded:: GeoCom-TPS1100-1.05

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
            parsers=enumparser(Target)
        )

    def set_target_type(
        self,
        target: Target | str
    ) -> GeoComResponse[None]:
        """
        RPC 17021, ``BAP_SetTargetType``

        .. versionadded:: GeoCom-TPS1100-1.05

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
        set_meas_prg
        """
        _target = toenum(Target, target)
        return self._request(
            17021,
            [_target.value]
        )

    def get_prism_type(self) -> GeoComResponse[Prism]:
        """
        RPC 17009, ``BAP_GetPrismType``

        .. versionadded:: GeoCom-TPS1100-1.05

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
            parsers=enumparser(Prism)
        )

    def set_prism_type(
        self,
        prism: Prism | str
    ) -> GeoComResponse[None]:
        """
        RPC 17008, ``BAP_SetPrismType``

        .. versionadded:: GeoCom-TPS1100-1.05

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
        _prism = toenum(Prism, prism)
        return self._request(
            17008,
            [_prism.value]
        )

    def get_prism_def(
        self,
        prism: Prism | str
    ) -> GeoComResponse[tuple[str, float, Reflector]]:
        """
        RPC 17023, ``BAP_GetPrismDef``

        .. versionadded:: GeoCom-TPS1100-1.05

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
        _prism = toenum(Prism, prism)
        return self._request(
            17023,
            [_prism.value],
            (
                parsestr,
                float,
                enumparser(Reflector)
            )
        )

    def set_prism_def(
        self,
        prism: Prism | str,
        name: str,
        const: float,
        reflector: Reflector | str
    ) -> GeoComResponse[None]:
        """
        RPC 17024, ``BAP_SetPrismDef``

        .. versionadded:: GeoCom-TPS1100-1.05

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
        _prism = toenum(Prism, prism)
        _reflector = toenum(Reflector, reflector)
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

    def get_meas_prg(self) -> GeoComResponse[UserProgram]:
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
        set_meas_prg
        """
        return self._request(
            17018,
            parsers=enumparser(UserProgram)
        )

    def set_meas_prg(
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
        get_meas_prg
        set_target_type
        """
        _program = toenum(UserProgram, program)
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
        aut.get_spiral
        aut.set_spiral
        aut.get_search_area
        aut.set_search_area
        """
        return self._request(17020, [0])
