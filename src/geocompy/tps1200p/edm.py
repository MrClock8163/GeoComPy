"""
``geocompy.tps1200p.edm``
=========================

Definitions for the TPS1200+ EDM subsystem.

Types
-----

- ``TPS1200PEDM``

"""
from __future__ import annotations

from enum import Enum

from .. import (
    GeoComSubsystem,
    GeoComResponse
)
from ..data import toenum


class TPS1200PEDM(GeoComSubsystem):
    """
    Electronic distance measurement subsystem of the TPS1200+ GeoCom
    protocol.

    This subsystem provides access to control some of the EDM module
    functions.

    """
    class ONOFF(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PEDM.ONOFF:
            """
            Parses enum member from serialized enum value.

            Parameters
            ----------
            value : str
                Serialized enum value.

            Returns
            -------
            ~TPS1200PEDM.ONOFF
                Parsed enum member.
            """
            return cls(int(value))

        OFF = 0
        ON = 1

    class EGLINTENSITYTYPE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PEDM.EGLINTENSITYTYPE:
            """
            Parses enum member from serialized enum value.

            Parameters
            ----------
            value : str
                Serialized enum value.

            Returns
            -------
            ~TPS1200PEDM.EGLINTENSITYTYPE
                Parsed enum member.
            """
            return cls(int(value))

        OFF = 0
        LOW = 1
        MID = 2
        HIGH = 3

    def laserpointer(
        self,
        laser: ONOFF | str
    ) -> GeoComResponse:
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
            - Error codes:
                - ``EDM_DEV_NOT_INSTALLED``: Instrument has no
                  laserpointer.

        """
        _laser = toenum(self.ONOFF, laser)
        return self._request(
            1004,
            [_laser.value]
        )

    def get_egl_intensity(self) -> GeoComResponse:
        """
        RPC 1058, ``EDM_GetEglIntensity``

        Gets the current intensity setting of the electronic guide light.

        Returns
        -------
        GeoComResponse
            - Params:
                - **intensity** (`EGLINTENSITYTYPE`): Current intensity
                  mode.
            - Error codes:
                - ``EDM_DEV_NOT_INSTALLED``: Instrument has no
                  EGL.

        """
        return self._request(
            1058,
            parsers={
                "intensity": self.EGLINTENSITYTYPE.parse
            }
        )

    def set_egl_intensity(
        self,
        intensity: EGLINTENSITYTYPE | str
    ) -> GeoComResponse:
        """
        RPC 1059, ``EDM_SetEglIntensity``

        Sets the intensity setting of the electronic guide light.

        Parameters
        ----------
        intensity : EGLINTENSITYTYPE | str
            Intensity setting to activate.

        Returns
        -------
        GeoComResponse
            - Error codes:
                - ``EDM_DEV_NOT_INSTALLED``: Instrument has no
                  EGL.

        """
        _intesity = toenum(self.EGLINTENSITYTYPE, intensity)
        return self._request(
            1059,
            [_intesity.value]
        )
