"""
``geocompy.vivatps.img``
=========================

Definitions for the VivaTPS Imaging subsystem.

Types
-----

- ``VivaTPSIMG``

"""
from __future__ import annotations

from enum import Enum

from .. import GeoComResponse
from ..tps1200p.img import TPS1200PIMG


class VivaTPSIMG(TPS1200PIMG):
    """
    Imaging subsystem of the VivaTPS GeoCom protocol.

    This subsystem provides access to the telescoping camera functions
    for instruments that possess such functionality.

    """
    class MEMTYPE(Enum):
        INTERNAL = 0x0
        PCCARD = 0x1
        SDCARD = 0x2

    def set_tcc_exposure_time(
        self,
        time: int
    ) -> GeoComResponse:
        """
        RPC 23403, ``IMG_SetTCCExposureTime``

        Sets the exposure time for the telescopic camera.

        Parameters
        ----------
        time : int
            Exposure time [ms].

        Returns
        -------
        GeoComResponse

        """
        return self._request(
            23403,
            [time]
        )
