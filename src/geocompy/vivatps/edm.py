"""
Description
===========

Module: ``geocompy.vivatps.edm``

Definitions for the VivaTPS EDM subsystem.

Types
-----

- ``VivaTPSEDM``

"""
from __future__ import annotations

from ..data import (
    toenum,
    parsebool
)
from ..data_geocom import MeasurementType
from ..protocols import GeoComResponse
from ..tps1200p.edm import TPS1200PEDM


class VivaTPSEDM(TPS1200PEDM):
    """
    Electronic distance measurement subsystem of the VivaTPS GeoCom
    protocol.

    This subsystem provides access to control some of the EDM module
    functions.

    """

    def is_continuous_measurement(
        self,
        mode: MeasurementType | str
    ) -> GeoComResponse[bool]:
        """
        RPC 1070, ``EDM_IsContMeasActive``

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
        _mode = toenum(MeasurementType, mode)
        return self._request(
            1070,
            [_mode.value],
            parsebool
        )

    def set_boomerang_filter_new(
        self,
        enable: bool
    ) -> GeoComResponse[None]:
        """
        RPC 1061, ``EDM_SetBoomerangFilter``

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
