"""
Description
===========

Module: ``geocompy.geo.edm``

Definitions for the GeoCom EDM subsystem.

Types
-----

- ``GeoComEDM``

"""
from __future__ import annotations

from ..data import (
    get_enum,
    get_enum_parser,
    parse_bool
)
from .gcdata import (
    Tracklight,
    Guidelight,
    MeasurementType
)
from .gctypes import (
    GeoComSubsystem,
    GeoComResponse
)


class GeoComEDM(GeoComSubsystem):
    """
    Electronic distance measurement subsystem of the GeoCom
    protocol.

    This subsystem provides access to control some of the EDM module
    functions.

    """

    def switch_laserpointer(
        self,
        activate: bool
    ) -> GeoComResponse[None]:
        """
        RPC 1004, ``EDM_Laserpointer``

        Enables or disables the laser pointer.

        Parameters
        ----------
        activate : bool
            Activate laser pointer

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``NOT_IMPL``: Instrument has no
                  switch_laserpointer.
                - ``EDM_HWFAILURE``: Hardware error.
                - ``EDM_COMERR``: Error communicating with EDM.
                - ``TIMEDOUT``: Process timed out.
                - ``ABORT``: Function was interrupted.
                - ``SYSBUSY``: EDM is already busy.
                - ``IVPARAM``: Invalid parameter.
                - ``UNDEFINED``: Instrument name could not be read.

        """
        return self._request(
            1004,
            [activate]
        )

    def switch_edm(
        self,
        activate: bool
    ) -> GeoComResponse[None]:
        """
        RPC 1010, ``EDM_On``

        .. versionremoved:: GeoCom-TPS1100

        Activates or deactivates the EDM module.

        Parameters
        ----------
        activate : bool
            Activate EDM module.

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``SYSBUSY``: EDM is already busy.
                - ``EDM_COMERR``: Error communicating with EDM.
                - ``EDM_ERR12``: Supply voltage below minimum.
                - ``EDM_HWFAILURE``: Hardware error.
                - ``TIMEDOUT``: Process timed out.
                - ``ABORT``: Function was interrupted.
                - ``UNDEFINED``: Instrument name could not be read.
        """
        return self._request(
            1010,
            [activate]
        )

    def get_boomerang_filter_status(self) -> GeoComResponse[bool]:
        """
        RPC 1044, ``EDM_GetBumerang``

        .. versionremoved:: GeoCom-TPS1100

        Gets the current status of the boomerang filter.

        Returns
        -------
        GeoComResponse
            Params:
                - `bool`: Boomerang filtering is enabled.

            Error codes:
                - ``IVRESULT``: Wrong result due to error.
                - ``SYSBUSY``: EDM is already busy.
                - ``NOT_IMPL``: Boomerang filter is not available.
                - ``EDM_COMERR``: Error communicating with EDM.
                - ``EDM_HWFAILURE``: Hardware error.
                - ``TIMEDOUT``: Process timed out.
                - ``ABORT``: Function was interrupted.
                - ``UNDEFINED``: Instrument name could not be read.
                - ``EDM_ERR12``: Supply voltage below minimum.
        """
        return self._request(
            1044,
            parsers=parse_bool
        )

    def switch_boomerang_filter(
        self,
        enabled: bool
    ) -> GeoComResponse[None]:
        """
        RPC 1007, ``EDM_SetBumerang``

        .. versionremoved:: GeoCom-TPS1100

        Sets the status of the boomerang filter.

        Parameters
        ----------
        enabled : bool
            Boomerant filter status to set.

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``IVRESULT``: Wrong result due to error.
                - ``SYSBUSY``: EDM is already busy.
                - ``NOT_IMPL``: Boomerang filter is not available.
                - ``EDM_COMERR``: Error communicating with EDM.
                - ``EDM_HWFAILURE``: Hardware error.
                - ``TIMEDOUT``: Process timed out.
                - ``ABORT``: Function was interrupted.
                - ``UNDEFINED``: Instrument name could not be read.
                - ``EDM_ERR12``: Supply voltage below minimum.
        """
        return self._request(
            1007,
            [enabled]
        )

    def get_tracklight_brightness(self) -> GeoComResponse[Tracklight]:
        """
        RPC 1041, ``EDM_GetTrkLightBrightness``

        .. versionremoved:: GeoCom-TPS1100

        Gets the brightness of the tracklight.

        Returns
        -------
        GeoComResponse
            Params:
                - `Tracklight`: Tracklight brightness.

            Error codes:
                - ``NOT_IMPL``: Tracklight is not available.
        """
        return self._request(
            1041,
            parsers=get_enum_parser(Tracklight)
        )

    def set_tracklight_brightness(
        self,
        intensity: Tracklight | str
    ) -> GeoComResponse[None]:
        """
        RPC 1032, ``EDM_SetTrkLightBrightness``

        .. versionremoved:: GeoCom-TPS1100

        Sets the brightness of the tracklight.

        Parameters
        ----------
        intensity : Tracklight | str
            Tracklight intensity to set.

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``NOT_IMPL``: Tracklight is not available.
        """
        _intensity = get_enum(Tracklight, intensity)
        return self._request(
            1032,
            [_intensity.value]
        )

    def get_tracklight_status(self) -> GeoComResponse[bool]:
        """
        RPC 1040, ``EDM_GetTrkLightSwitch``

        .. versionremoved:: GeoCom-TPS1100

        Gets if the track light is currently active.

        Returns
        -------
        GeoComResponse
            Params:
                - `bool`: Tracklight is on.

            Error codes:
                - ``NOT_IMPL``: Tracklight is not available.
        """
        return self._request(
            1040,
            parsers=parse_bool
        )

    def switch_tracklight(
        self,
        activate: bool
    ) -> GeoComResponse[None]:
        """
        RPC 1031, ``EDM_SetTrkLightSwitch``

        .. versionremoved:: GeoCom-TPS1100

        Sets the status of the tracklight.

        Parameters
        ----------
        activate : bool
            Activate track light.

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``IVRESULT``: Wrong result due to error.
                - ``SYSBUSY``: EDM is already busy.
                - ``NOT_IMPL``: Tracklight is not available.
        """
        return self._request(
            1031,
            [activate]
        )

    def get_guidelight_intensity(self) -> GeoComResponse[Guidelight]:
        """
        RPC 1058, ``EDM_GetEglIntensity``

        .. versionadded:: GeoCom-TPS1100

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
            parsers=get_enum_parser(Guidelight)
        )

    def set_guidelight_intensity(
        self,
        intensity: Guidelight | str
    ) -> GeoComResponse[None]:
        """
        RPC 1059, ``EDM_SetEglIntensity``

        .. versionadded:: GeoCom-TPS1100

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
        _intesity = get_enum(Guidelight, intensity)
        return self._request(
            1059,
            [_intesity.value]
        )

    def is_continuous_measurement(
        self,
        mode: MeasurementType | str
    ) -> GeoComResponse[bool]:
        """
        RPC 1070, ``EDM_IsContMeasActive``

        .. versionadded:: GeoCom-VivaTPS

        Checks if the continuous measurement is active in the specified
        mode.

        Parameters
        ----------
        mode : MeasurementType | str
            Measurement mode.

        Returns
        -------
        GeoComResponse
            Params:
                - `bool`: Continuous measurement is active.

        """
        _mode = get_enum(MeasurementType, mode)
        return self._request(
            1070,
            [_mode.value],
            parse_bool
        )

    def switch_boomerang_filter_new(
        self,
        enable: bool
    ) -> GeoComResponse[None]:
        """
        RPC 1061, ``EDM_SetBoomerangFilter``

        .. versionadded:: GeoCom-VivaTPS

        Enables or disables the boomerang filter.

        Parameters
        ----------
        enable : bool
            Enable boomerang filter.

        Returns
        -------
        GeoComResponse
        """
        return self._request(
            1061,
            [enable]
        )
