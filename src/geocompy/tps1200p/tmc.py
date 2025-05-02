"""
Description
===========

Module: ``geocompy.tps1200p.tmc``

Definitions for the TPS1200+ Theodolite measurement and calculation
subsystem.

Types
-----

- ``TPS1200PTMC``

"""
from __future__ import annotations

from ..data import parsebool
from ..protocols import GeoComResponse
from ..tps1100.tmc import TPS1100TMC


class TPS1200PTMC(TPS1100TMC):
    """
    Theodolite measurement and calculation subsystem of the TPS1200+
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

    def get_atm_ppm(self) -> GeoComResponse[float]:
        """
        RPC 2151, ``TMC_GetAtmPpm``

        Gets the current atmospheric correction factor.

        Returns
        -------
        GeoComResponse
            Params:
                - `float`: Atmospheric correction factor [ppm].

        See Also
        --------
        set_atm_ppm
        get_geo_ppm
        set_geo_ppm
        get_prism_corr
        set_prism_corr

        """
        return self._request(
            2151,
            parsers=float
        )

    def set_atm_ppm(
        self,
        ppm: float
    ) -> GeoComResponse[None]:
        """
        RPC 2148, ``TMC_SetAtmPpm``

        Sets the atmospheric correction factor.

        Parameters
        ----------
        ppm : float
            Atmospheric correction factor [ppm].

        Returns
        -------
        GeoComResponse

        See Also
        --------
        get_atm_ppm
        get_geo_ppm
        set_geo_ppm
        get_prism_corr
        set_prism_corr

        """
        return self._request(
            2148,
            [ppm]
        )

    def get_geo_ppm(
        self
    ) -> GeoComResponse[tuple[bool, float, float, float, float]]:
        """
        RPC 2154, ``TMC_GetGeoPpm``

        Gets the current geometric correction factors.

        Returns
        -------
        GeoComResponse
            Params:
                - `bool`: Autmatically apply geometric
                  corrections.
                - `float`: Scale factor on central
                  meridian.
                - `float`: Offset from central
                  meridian.
                - `float`: Length reduction from projection
                  to reference level.
                - `float`: Individual correction [ppm].

        See Also
        --------
        get_atm_ppm
        set_atm_ppm
        set_geo_ppm
        get_prism_corr
        set_prism_corr

        """
        return self._request(
            2154,
            parsers=(
                parsebool,
                float,
                float,
                float,
                float
            )
        )

    def set_geo_ppm(
        self,
        automatic: bool,
        meridianscale: float,
        meridianoffset: float,
        reduction: float,
        individual: float
    ) -> GeoComResponse[None]:
        """
        RPC 2153, ``TMC_SetGeoPpm``

        Sets the geometric correction factors.

        Parameters
        ----------
        automatic : bool
            Automatically apply geometric corrections.
        meridianscale : float
            Scale factor on central meridian.
        meridianoffset : float
            Offset from central meridian.
        reduction : float
            Length reduction from projection to reference level [ppm].
        individual : float
            Individual correction [ppm].

        Returns
        -------
        GeoComResponse

        See Also
        --------
        get_atm_ppm
        set_atm_ppm
        get_geo_ppm
        get_prism_corr
        set_prism_corr

        """
        return self._request(
            2153,
            [
                automatic,
                meridianscale, meridianoffset,
                reduction, individual
            ]
        )
