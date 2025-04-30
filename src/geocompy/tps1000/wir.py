"""
Description
===========

Module: ``geocompy.tps1000.wir``

Definitions for the TPS1000 Word Index registration subsystem.

Types
-----

- ``TPS1000WIR``

"""
from __future__ import annotations

from enum import IntEnum

from ..data import enumparser, toenum
from ..protocols import (
    GeoComSubsystem,
    GeoComResponse
)


class TPS1000WIR(GeoComSubsystem):
    """
    Word Index registration subsystem of the TPS1000 GeoCom protocol.
    This subsystem is responsible for the GSI data recording operations.
    """

    class FORMAT(IntEnum):
        GSI8 = 0
        GSI16 = 1

    def get_rec_format(self) -> GeoComResponse[FORMAT]:
        """
        RPC 8011, ``WIR_GetRecFormat``

        Retrieves the current data recording format.

        Returns
        -------
        GeoComResponse
            Params:
                - `FORMAT`: GSI version used in data recording.

        """
        return self._request(
            8011,
            parsers=enumparser(self.FORMAT)
        )

    def set_rec_format(
        self,
        format: FORMAT | str
    ) -> GeoComResponse[None]:
        """
        RPC 8012, ``WIR_SetRecFormat``

        Sets the data recording format.

        Parameters
        ----------
        format : FORMAT | str
            GSI format to use in data recording.

        Returns
        -------
        GeoComResponse

        """
        _format = toenum(self.FORMAT, format)
        return self._request(
            8012,
            [_format.value]
        )
