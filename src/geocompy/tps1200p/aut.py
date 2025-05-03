"""
Description
===========

Module: ``geocompy.tps1200p.aut``

Definitions for the TPS1200+ Automation subsystem.

Types
-----

- ``TPS1200PAUT``

"""
from __future__ import annotations

from typing import Never
from typing_extensions import deprecated

from ..data import toenum
from ..data_geocom import Turn
from ..protocols import GeoComResponse
from ..tps1100.aut import TPS1100AUT


class TPS1200PAUT(TPS1100AUT):
    """
    Automation subsystem of the TPS1200+ GeoCom protocol.

    This subsystem controls most of the motorized functions of
    a total station, such as positioning of the axes, target search,
    target lock, etc.

    """

    @deprecated("This command was removed for TPS1200 instruments")
    def get_atr_status(self) -> Never:
        """
        RPC 9019, ``AUT_GetATRStatus``

        .. versionremoved:: GeoCom-TPS1200

        Raises
        ------
        AttributeError
        """
        raise AttributeError()

    @deprecated("This command was removed for TPS1200 instruments")
    def switch_atr(
        self,
        *args
    ) -> Never:
        """
        RPC 9018, ``AUT_SetATRStatus``

        .. versionremoved:: GeoCom-TPS1200

        Raises
        ------
        AttributeError
        """
        raise AttributeError()

    @deprecated("This command was removed for TPS1200 instruments")
    def get_lock_status(self) -> Never:
        """
        RPC 9021, ``AUT_GetLockStatus``

        .. versionremoved:: GeoCom-TPS1200

        Raises
        ------
        AttributeError
        """
        raise AttributeError()

    @deprecated("This command was removed for TPS1200 instruments")
    def switch_lock(
        self,
        *args
    ) -> Never:
        """
        RPC 9020, ``AUT_SetLockStatus``

        .. versionremoved:: GeoCom-TPS1200

        Raises
        ------
        AttributeError
        """
        raise AttributeError()

    def switch_powersearch_range(
        self,
        enable: bool
    ) -> GeoComResponse[None]:
        """
        RPC 9048, ``AUT_PS_EnableRange``

        Enables or disables the PowerSearch window and range limit.

        Parameters
        ----------
        enable : bool
            Enable predefined PowerSearch window and range limits.
            Defaults to [0; 400] range when disabled.

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``NA``: GeoCom Robotic license not found.

        See Also
        --------
        set_powersearch_range
        set_search_area
        """
        return self._request(
            9048,
            [enable]
        )

    def set_powersearch_range(
        self,
        closest: int,
        farthest: int
    ) -> GeoComResponse[None]:
        """
        RPC 9044, ``AUT_PS_SetRange``

        Sets the PowerSearch range limits.

        Parameters
        ----------
        closest : int
            Minimum distance to prism [0; ...].
        farthest : int
            Maxmimum distance to prism [closest + 10; 400].

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``NA``: GeoCom Robotic license not found.
                - ``IVPARAM``: Invalid parameters.

        See Also
        --------
        switch_powersearch_range
        powersearch_window
        set_search_area
        """
        return self._request(
            9047,
            [closest, farthest]
        )

    def powersearch_window(self) -> GeoComResponse[None]:
        """
        RPC 9052, ``AUT_PS_SearchWindow``

        Executes PowerSearch in the predefined search window.

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``NA``: GeoCom Robotic license not found.
                - ``AUT_NO_WORKING_AREA``: Search window is not defined.
                - ``AUT_NO_TARGET``: Target was not found.

        See Also
        --------
        switch_powersearch_range
        set_powersearch_range
        powersearch_next
        set_search_area
        """
        return self._request(9052)

    def powersearch_next(
        self,
        direction: Turn | str,
        swing: bool
    ) -> GeoComResponse[None]:
        """
        RPC 9051, ``AUT_PS_SearchNext``

        Executes 360° default PowerSearch to find the next target.

        Parameters
        ----------
        direction : Turn | str
            Turning direction during PowerSearch.
        swing : bool
            Search starts -10 GON to the given turn direction.

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``NA``: GeoCom Robotic license not found.
                - ``AUT_NO_TARGET``: Target was not found.
                - ``IVPARAM``: Invalid parameters.

        See Also
        --------
        switch_powersearch_range
        powersearch_window
        """
        _direction = toenum(Turn, direction)
        return self._request(
            9051,
            [_direction.value, swing]
        )
