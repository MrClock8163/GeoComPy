"""
``geocompy.vivatps.edm``
=========================

Definitions for the VivaTPS EDM subsystem.

Types
-----

- ``VivaTPSEDM``

"""
from __future__ import annotations

from enum import Enum

from .. import GeoComResponse
from ..data import toenum
from ..tps1200p.edm import TPS1200PEDM


class VivaTPSEDM(TPS1200PEDM):
    """
    Electronic distance measurement subsystem of the VivaTPS GeoCom
    protocol.

    This subsystem provides access to control some of the EDM module
    functions.

    """
    class ONOFF(Enum):
        @classmethod
        def parse(cls, value: str) -> VivaTPSEDM.ONOFF:
            """
            Parses enum member from serialized enum value.

            Parameters
            ----------
            value : str
                Serialized enum value.

            Returns
            -------
            ~VivaTPSEDM.ONOFF
                Parsed enum member.
            """
            return cls(int(value))

        OFF = 0
        ON = 1
    
    class MEASUREMENTTYPE(Enum):
        @classmethod
        def parse(cls, value: str) -> VivaTPSEDM.MEASUREMENTTYPE:
            """
            Parses enum member from serialized enum value.

            Parameters
            ----------
            value : str
                Serialized enum value.

            Returns
            -------
            ~VivaTPSEDM.MEASUREMENTTYPE
                Parsed enum member.
            """
            return cls(int(value))
    
        SIGNAL = 1
        FREQ = 2
        DIST = 3
        ANY = 4

    def is_cont_meas_active(
        self,
        mode: MEASUREMENTTYPE | str
    ) -> GeoComResponse:
        """
        RPC 1070, ``EDM_IsContMeasActive``

        Checks if the continuous measurement is active in the specified
        mode.

        Parameters
        ----------
        mode : MEASUREMENTTYPE | str
            Measurement mode.

        Returns
        -------
        GeoComResponse
            - Params:
                - **active** (`bool`): Continuous measurement is active.

        """
        _mode = toenum(self.MEASUREMENTTYPE, mode)
        return self._request(
            1070,
            [_mode.value],
            {
                "active": bool
            }
        )
    
    def set_boomerang_filter(
        self,
        state: ONOFF | str
    ) -> GeoComResponse:
        """
        RPC 1061, ``EDM_SetBoomerangFilter``

        Enables or disables the boomerang filter.

        Parameters
        ----------
        state : ONOFF | str
            New state to set the boomerang filter to.

        Returns
        -------
        GeoComResponse
        """
        _state = toenum(self.ONOFF, state)
        return self._request(
            1061,
            [_state.value]
        )
