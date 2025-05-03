"""
Description
===========

Module: ``geocompy.tps1100.tmc``

Definitions for the TPS1100 Theodolite measurement and calculation
subsystem.

Types
-----

- ``TPS1100TMC``

"""
from __future__ import annotations

from ..data import (
    toenum,
    enumparser
)
from ..data_geocom import (
    EDMMode,
    EDMModeV2
)
from ..protocols import GeoComResponse
from ..tps1000.tmc import TPS1000TMC


class TPS1100TMC(TPS1000TMC):
    """
    Theodolite measurement and calculation subsystem of the TPS1100
    GeoCom protocol.

    This subsystem is the central module of measurement, calculation and
    geodetic control.

    The module handles:
        - measurement functions
        - measurement control functions
        - data setup functions
        - information functions
        - configuration functions

    Possible return codes:
        System
            General use codes.
        Informative/Warning
            Function terminated with success, but some restrictions may
            apply (e.g.: angle measurement succeded, distance measurement
            failed).
        Error
            Non-successful function termination.

    """

    def get_edm_mode(self) -> GeoComResponse[EDMMode]:
        """
        RPC 2021, ``TMC_GetEdmMode``

        Gets the current EDM measurement mode.

        Returns
        -------
        GeoComResponse
            Params:
                - `EDMMode`: Current EDM mode (EDMModeV2).

        See Also
        --------
        set_edm_mode

        """
        return self._request(
            2021,
            parsers=enumparser(EDMModeV2)
        )

    def set_edm_mode(
        self,
        mode: EDMMode | str
    ) -> GeoComResponse[None]:
        """
        RPC 2020, ``TMC_SetEdmMode``

        Sets the EDM measurement mode.

        Parameters
        ----------
        mode : EDMMode | str
            EDM mode to activate (expects EDMModeV2).

        Returns
        -------
        GeoComResponse

        See Also
        --------
        get_edm_mode

        """
        _mode = toenum(EDMModeV2, mode)
        return self._request(
            2020,
            [_mode.value]
        )

    def get_slope_distance_correction(
        self
    ) -> GeoComResponse[tuple[float, float]]:
        """
        RPC 2126, ``TMC_GetSlopDistCorr``

        Gets the total correction (atmospheric + geometric) applied to the
        distance measurements, as well as the current prism constant.

        Returns
        -------
        GeoComResponse
            Params:
                - `float`: Total corrections [ppm].
                - `float`: Prism constant.

        See Also
        --------
        get_prism_correction
        set_prism_correction

        """
        return self._request(
            2126,
            parsers=(
                float,
                float
            )
        )
