"""
Description
===========

Module: ``geocompy.tps1000.edm``

Definitions for the TPS1000 EDM subsystem.

Types
-----

- ``TPS1000EDM``

"""
from __future__ import annotations

from ..data import (
    toenum,
    enumparser,
    parsebool
)
from ..data_geocom import Tracklight
from ..protocols import (
    GeoComSubsystem,
    GeoComResponse
)


class TPS1000EDM(GeoComSubsystem):
    """
    Electronic distance measurement subsystem of the TPS1000 GeoCom
    protocol.

    This subsystem provides access to control some of the EDM module
    functions.

    """

    def laserpointer(
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
                  laserpointer.
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

    def on(
        self,
        activate: bool
    ) -> GeoComResponse[None]:
        """
        RPC 1010, ``EDM_On``

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

    def get_bumerang(self) -> GeoComResponse[bool]:
        """
        RPC 1044, ``EDM_GetBumerang``

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
            parsers=parsebool
        )

    def set_bumerang(
        self,
        enabled: bool
    ) -> GeoComResponse[None]:
        """
        RPC 1007, ``EDM_SetBumerang``

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

    def get_trk_light_brightness(self) -> GeoComResponse[Tracklight]:
        """
        RPC 1041, ``EDM_GetTrkLightBrightness``

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
            parsers=enumparser(Tracklight)
        )

    def set_trk_light_brightness(
        self,
        intensity: Tracklight | str
    ) -> GeoComResponse[None]:
        """
        RPC 1032, ``EDM_SetTrkLightBrightness``

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
        _intensity = toenum(Tracklight, intensity)
        return self._request(
            1032,
            [_intensity.value]
        )

    def get_trk_light_switch(self) -> GeoComResponse[bool]:
        """
        RPC 1040, ``EDM_GetTrkLightSwitch``

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
            parsers=parsebool
        )

    def set_trk_light_switch(
        self,
        activate: bool
    ) -> GeoComResponse[None]:
        """
        RPC 1031, ``EDM_SetTrkLightSwitch``

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
