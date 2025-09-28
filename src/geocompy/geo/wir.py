"""
Description
===========

Module: ``geocompy.geo.wir``

Definitions for the GeoCOM Word Index registration subsystem.

Types
-----

- ``GeoComWIR``

"""
from __future__ import annotations

from ..data import (
    get_enum_parser,
    get_enum
)
from .gcdata import Format
from .gctypes import (
    GeoComSubsystem,
    GeoComResponse
)


class GeoComWIR(GeoComSubsystem):
    """
    Word Index registration subsystem of the GeoCOM protocol.
    This subsystem is responsible for the GSI data recording operations.

    .. versionremoved:: GeoCOM-TPS1200
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
            parsers=get_enum_parser(Format)
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
        _format = get_enum(Format, format)
        return self._request(
            8012,
            [_format]
        )
