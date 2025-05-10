"""
Description
===========

Module: ``geocompy.geo.wir``

Definitions for the GeoCom Word Index registration subsystem.

Types
-----

- ``GeoComWIR``

"""
from __future__ import annotations

from ..data import (
    enumparser,
    toenum
)
from .gcdata import Format
from .gctypes import (
    GeoComSubsystem,
    GeoComResponse
)


class GeoComWIR(GeoComSubsystem):
    """
    Word Index registration subsystem of the GeoCom protocol.
    This subsystem is responsible for the GSI data recording operations.
    """

    def get_recording_format(self) -> GeoComResponse[Format]:
        """
        RPC 8011, ``WIR_GetRecFormat``

        Retrieves the current data recording format.

        Returns
        -------
        GeoComResponse
            Params:
                - `Format`: GSI version used in data recording.

        """
        return self._request(
            8011,
            parsers=enumparser(Format)
        )

    def set_recording_format(
        self,
        format: Format | str
    ) -> GeoComResponse[None]:
        """
        RPC 8012, ``WIR_SetRecFormat``

        Sets the data recording format.

        Parameters
        ----------
        format : Format | str
            GSI format to use in data recording.

        Returns
        -------
        GeoComResponse

        """
        _format = toenum(Format, format)
        return self._request(
            8012,
            [_format.value]
        )
