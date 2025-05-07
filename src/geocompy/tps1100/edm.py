"""
Description
===========

Module: ``geocompy.tps1100.edm``

Definitions for the TPS1100 EDM subsystem.

Types
-----

- ``TPS1100EDM``

"""
from __future__ import annotations

from typing import Never, Any
from typing_extensions import deprecated

from ..data import (
    toenum,
    enumparser
)
from ..data_geocom import Guidelight
from ..protocols import GeoComResponse
from ..tps1000.edm import TPS1000EDM


class TPS1100EDM(TPS1000EDM):
    """
    Electronic distance measurement subsystem of the TPS1100 GeoCom
    protocol.

    This subsystem provides access to control some of the EDM module
    functions.

    """

    def get_guidelight_intensity(self) -> GeoComResponse[Guidelight]:
        """
        RPC 1058, ``EDM_GetEglIntensity``

        Gets the current intensity setting of the electronic guide light.

        Returns
        -------
        GeoComResponse
            Params:
                - `Guidelight`: Current intensity mode.
            Error codes:
                - ``EDM_DEV_NOT_INSTALLED``: Instrument has no
                  EGL.

        """
        return self._request(
            1058,
            parsers=enumparser(Guidelight)
        )

    def set_guidelight_intensity(
        self,
        intensity: Guidelight | str
    ) -> GeoComResponse[None]:
        """
        RPC 1059, ``EDM_SetEglIntensity``

        Sets the intensity setting of the electronic guide light.

        Parameters
        ----------
        intensity : GUIDELIGHT | str
            Intensity setting to switch_edm.

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``EDM_DEV_NOT_INSTALLED``: Instrument has no
                  EGL.

        """
        _intesity = toenum(Guidelight, intensity)
        return self._request(
            1059,
            [_intesity.value]
        )

    @deprecated("This command was removed for TPS1100 instruments")
    def switch_edm(
        self,
        *args: Any,
        **kwargs: Any
    ) -> Never:
        """
        RPC 1010, ``EDM_On``

        .. versionremoved:: GeoCom-TPS1100-1.00

        Raises
        ------
        AttributeError
        """
        raise AttributeError()

    @deprecated("This command was removed for TPS1100 instruments")
    def get_boomerang_filter_status(self) -> Never:
        """
        RPC 1044, ``EDM_GetBumerang``

        .. versionremoved:: GeoCom-TPS1100-1.00

        Raises
        ------
        AttributeError
        """
        raise AttributeError()

    @deprecated("This command was removed for TPS1100 instruments")
    def switch_boomerang_filter(
        self,
        *args: Any,
        **kwargs: Any
    ) -> Never:
        """
        RPC 1007, ``EDM_SetBumerang``

        .. versionremoved:: GeoCom-TPS1100-1.00

        Raises
        ------
        AttributeError
        """
        raise AttributeError()

    @deprecated("This command was removed for TPS1100 instruments")
    def get_tracklight_brightness(self) -> Never:
        """
        RPC 1041, ``EDM_GetTrkLightBrightness``

        .. versionremoved:: GeoCom-TPS1100-1.00
            Use `get_guidelight_intensity` instead.

        Raises
        ------
        AttributeError
        """
        raise AttributeError()

    @deprecated("This command was removed for TPS1100 instruments")
    def set_tracklight_brightness(
        self,
        *args: Any,
        **kwargs: Any
    ) -> Never:
        """
        RPC 1032, ``EDM_SetTrkLightBrightness``

        .. versionremoved:: GeoCom-TPS1100-1.00
            Use `set_guidelight_intensity` instead.

        Raises
        ------
        AttributeError
        """
        raise AttributeError()

    @deprecated("This command was removed for TPS1100 instruments")
    def get_tracklight_status(self) -> Never:
        """
        RPC 1040, ``EDM_GetTrkLightSwitch``

        .. versionremoved:: GeoCom-TPS1100-1.00
            Use `get_guidelight_intensity` instead.

        Raises
        ------
        AttributeError
        """
        raise AttributeError()

    @deprecated("This command was removed for TPS1100 instruments")
    def switch_tracklight(
        self,
        *args: Any,
        **kwargs: Any
    ) -> Never:
        """
        RPC 1031, ``EDM_SetTrkLightSwitch``

        .. versionremoved:: GeoCom-TPS1100-1.00
            Use `set_guidelight_intensity` instead.

        Raises
        ------
        AttributeError
        """
        raise AttributeError()
