"""
Description
===========

Module: ``geocompy.tps1200p.bap``

Definitions for the TPS1200+ Basic applications subsystem.

Types
-----

- ``TPS1200PBAP``

"""
from __future__ import annotations

from typing import Never
from typing_extensions import deprecated

from ..data import (
    toenum,
    enumparser,
    parsestr,
    parsebool
)
from ..data_geocom import (
    ATRMode,
    Prism,
    Reflector
)
from ..protocols import GeoComResponse
from ..tps1100.bap import TPS1100BAP


class TPS1200PBAP(TPS1100BAP):
    """
    Basic applications subsystem of the TPS1200+ GeoCom protocol.

    This subsystem contains high-level functions that are also accessible
    through the user interface. The commands combine several subcommands
    for ease of operation.

    """

    @deprecated("This command was removed for TPS1200 instruments")
    def get_last_displayed_error(self) -> Never:
        """
        RPC 17003, ``BAP_GetLastDisplayedError``

        .. versionremoved:: GeoCom-TPS1200

        Raises
        ------
        AttributeError
        """
        raise AttributeError()

    @deprecated("This command was removed for TPS1200 instruments")
    def set_prism_definition(
        self,
        *args
    ) -> Never:
        """
        RPC 17024, ``BAP_SetPrismDef``

        .. versionremoved:: GeoCom-TPS1200

        Raises
        ------
        AttributeError
        """
        raise AttributeError()

    def get_prism_type_name(self) -> GeoComResponse[tuple[Prism, str]]:
        """
        RPC 17031, ``BAP_GetPrismType2``

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
            parsers=(enumparser(Prism), parsestr)
        )

    def set_prism_type_name(
        self,
        prism: Prism | str,
        name: str
    ) -> GeoComResponse[None]:
        """
        RPC 17030, ``BAP_SetPrismType2``

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
        _prism = toenum(Prism, prism)
        return self._request(
            17030,
            [_prism.value, name]
        )

    def get_user_prism_definition(
        self,
        name: str
    ) -> GeoComResponse[tuple[str, float, Reflector]]:
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
            Params:
                - `str`: Name of the prism.
                - `float`: Additive prism constant.
                - `Reflector`: Reflector type.
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
                parsestr,
                float,
                enumparser(Reflector)
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
        _reflector = toenum(Reflector, reflector)
        return self._request(
            17032,
            [name, const, _reflector.value, creator]
        )

    def get_atr_setting(self) -> GeoComResponse[ATRMode]:
        """
        RPC 17034, ``BAP_GetATRSetting``

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
            parsers=enumparser(ATRMode)
        )

    def set_atr_setting(
        self,
        mode: ATRMode | str
    ) -> GeoComResponse[None]:
        """
        RPC 17035, ``BAP_SetATRSetting``

        Sets the ATR setting.

        Parameters
        ----------
        mode : ATRMode | str
            ATR setting to activate.

        See Also
        --------
        get_atr_setting
        """
        _mode = toenum(ATRMode, mode)
        return self._request(
            17035,
            [_mode.value]
        )

    def get_reduced_atr_fov(self) -> GeoComResponse[bool]:
        """
        RPC 17036, ``BAP_GetRedATRFov``

        Gets the state of the reduced ATR field of view mode.

        Returns
        -------
        GeoComResponse
            Params:
                - `bool`: Reduced field of view ATR is enabled.

        See Also
        --------
        set_reduced_atr_fov
        """
        return self._request(
            17036,
            parsers=parsebool
        )

    def set_reduced_atr_fov(
        self,
        enabled: bool
    ) -> GeoComResponse[None]:
        """
        RPC 17037, ``BAP_SetRedATRFov``

        Sets the state of the reduced ATR field of view mode.

        Parameters
        ----------
        enabled : bool
            Reduced field of view ATR is enabled.

        See Also
        --------
        get_reduced_atr_fov
        """
        return self._request(
            17037,
            [enabled]
        )
