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

from enum import Enum

from ..data import (
    toenum,
    enumparser
)
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
    class ONOFF(Enum):
        OFF = 0
        ON = 1

    class TRKLIGHTBRIGHTNESS(Enum):
        LOW = 0
        MID = 1
        HIGH = 2

    def laserpointer(
        self,
        laser: ONOFF | str
    ) -> GeoComResponse[None]:
        """
        RPC 1004, ``EDM_Laserpointer``

        Enables or disables the laser pointer.

        Parameters
        ----------
        laser : ONOFF | str
            Activation state to set.

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
        _laser = toenum(self.ONOFF, laser)
        return self._request(
            1004,
            [_laser.value]
        )

    def on(
        self,
        state: ONOFF | str
    ) -> GeoComResponse[None]:
        """
        RPC 1010, ``EDM_On``

        Activates or deactivates the EDM module.

        Parameters
        ----------
        state : ONOFF | str
            EDM state to change to.

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
        _state = toenum(self.ONOFF, state)
        return self._request(
            1010,
            [_state.value]
        )

    def get_bumerang(self) -> GeoComResponse[ONOFF]:
        """
        RPC 1044, ``EDM_GetBumerang``

        Gets the current status of the boomerang filter.

        Returns
        -------
        GeoComResponse
            Params:
                - `ONOFF`: State of the boomerang filter.
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
            parsers=enumparser(self.ONOFF)
        )

    def set_bumerang(
        self,
        status: ONOFF | str
    ) -> GeoComResponse[None]:
        """
        RPC 1007, ``EDM_SetBumerang``

        Sets the status of the boomerang filter.

        Parameters
        ----------
        status : ONOFF | str
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
        _status = toenum(self.ONOFF, status)
        return self._request(
            1007,
            [_status.value]
        )

    def get_trk_light_brightness(self) -> GeoComResponse[TRKLIGHTBRIGHTNESS]:
        """
        RPC 1041, ``EDM_GetTrkLightBrightness``

        Gets the brightness of the tracklight.

        Returns
        -------
        GeoComResponse
            Params:
                - `TRKLIGHTBRIGHTNESS`: Tracklight brightness.
            Error codes:
                - ``NOT_IMPL``: Tracklight is not available.
        """
        return self._request(
            1041,
            parsers=enumparser(self.TRKLIGHTBRIGHTNESS)
        )

    def set_trk_light_brightness(
        self,
        intensity: TRKLIGHTBRIGHTNESS | str
    ) -> GeoComResponse[None]:
        """
        RPC 1032, ``EDM_SetTrkLightBrightness``

        Sets the brightness of the tracklight.

        Parameters
        ----------
        intensity : TRKLIGHTBRIGHTNESS | str
            Tracklight intensity to set.

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``NOT_IMPL``: Tracklight is not available.
        """
        _intensity = toenum(self.TRKLIGHTBRIGHTNESS, intensity)
        return self._request(
            1032,
            [_intensity.value]
        )

    def get_trk_light_switch(self) -> GeoComResponse[ONOFF]:
        """
        RPC 1040, ``EDM_GetTrkLightSwitch``

        Gets the current activity state of the tracklight.

        Returns
        -------
        GeoComResponse
            Params:
                - `ONOFF`: Tracklight state.
            Error codes:
                - ``NOT_IMPL``: Tracklight is not available.
        """
        return self._request(
            1040,
            parsers=enumparser(self.ONOFF)
        )

    def set_trk_light_switch(
        self,
        state: ONOFF | str
    ) -> GeoComResponse[None]:
        """
        RPC 1031, ``EDM_SetTrkLightSwitch``

        Sets the status of the tracklight.

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``IVRESULT``: Wrong result due to error.
                - ``SYSBUSY``: EDM is already busy.
                - ``NOT_IMPL``: Tracklight is not available.
        """
        _state = toenum(self.ONOFF, state)
        return self._request(
            1031,
            [_state.value]
        )
