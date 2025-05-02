"""
Description
===========

Module: ``geocompy.tps1200p.csv``

Definitions for the TPS1200+ Central services subsystem.

Types
-----

- ``TPS1200PCSV``

"""
from __future__ import annotations

from typing import Never
from typing_extensions import deprecated

from datetime import datetime

from ..data import enumparser
from ..data_geocom import Reflectorless
from ..protocols import GeoComResponse
from ..tps1100.csv import TPS1100CSV


class TPS1200PCSV(TPS1100CSV):
    """
    Central services subsystem of the TPS1200+ GeoCom protocol.

    This subsystem contains functions to maintain centralised data
    and configuration of the instruments.

    """

    @deprecated("This command was removed for TPS1200 instruments")
    def get_voltage_battery(self) -> Never:
        """
        RPC 5009, ``CSV_GetVBat``

        .. versionremoved:: GeoCom-TPS1200

        Raises
        ------
        AttributeError
        """
        raise AttributeError()

    @deprecated("This command was removed for TPS1200 instruments")
    def get_voltage_memory(self) -> Never:
        """
        RPC 5009, ``CSV_GetVMem``

        .. versionremoved:: GeoCom-TPS1200

        Raises
        ------
        AttributeError
        """
        raise AttributeError()

    def get_reflectorless_class(self) -> GeoComResponse[Reflectorless]:
        """
        RPC 5100, ``CSV_GetReflectorlessClass``

        Gets the class of the reflectorless EDM module, if the instrument
        is equipped with one.

        Returns
        -------
        GeoComResponse
            Params:
                - `Reflectorless`: Class of the reflectorless EDM module.

        """
        return self._request(
            5100,
            parsers=enumparser(Reflectorless)
        )

    def get_datetime_precise(self) -> GeoComResponse[datetime]:
        """
        RPC 5117, ``CSV_GetDateTimeCentiSec``

        Gets the current date and time set on the instrument in
        centiseconds resolution.

        Returns
        -------
        GeoComResponse
            Params:
                - `datetime`: Current date and time.

        See Also
        --------
        get_datetime
        set_datetime

        """
        def make_datetime(
            params: tuple[int, int, int, int, int, int, int] | None
        ) -> datetime | None:
            if params is None:
                return None

            return datetime(
                params[0],
                int(params[1]),
                int(params[2]),
                int(params[3]),
                int(params[4]),
                int(params[5]),
                int(params[5]) * 10000
            )

        response = self._request(
            5117,
            parsers=(
                int,
                int,
                int,
                int,
                int,
                int,
                int
            )
        )
        return response.map_params(make_datetime)
