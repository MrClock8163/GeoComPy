"""
Description
===========

Module: ``geocompy.geo.bmm``

Definitions for the GeoCOM Basic man-machine interface subsystem.

Types
-----

- ``GeoComBMM``
"""
from __future__ import annotations

from .gctypes import (
    GeoComSubsystem,
    GeoComResponse
)


class GeoComBMM(GeoComSubsystem):
    """
    Basic man-machine interface subsystem of the GeoCOM protocol.

    This subsystem contains functions related to the operation of the
    keyboard, character sets and singalling devices.
    """

    def beep_alarm(self) -> GeoComResponse[None]:
        """
        RPC 11004, ``BMM_BeepAlarm``

        Produces a triple beep. Previously started continuous signals will
        be aborted.

        See Also
        --------
        beep_normal
        beep_on
        beep_off
        """
        return self._request(11004)

    def beep_normal(self) -> GeoComResponse[None]:
        """
        RPC 11003, ``BMM_BeepNormal``

        Produces a single beep. Previously started continuous signals will
        be aborted.

        See Also
        --------
        beep_alarm
        beep_on
        beep_off
        """
        return self._request(11003)

    def beep_on(
        self,
        volume: int = 100,
        frequency: int = 3900
    ) -> GeoComResponse[None]:
        """
        RPC 11001, ``BMM_BeepOn``

        .. versionremoved:: GeoCOM-TPS1100

        Starts a continuous beep signal with the specified volume and
        frequency.

        Parameters
        ----------
        volume : int
            Beep signal volume [0; 100]%.
        frequency : int
            Beep signal frequency [500; 5000] [Hz].

        See Also
        --------
        beep_off
        beep_alarm
        beep_normal
        """
        return self._request(
            11001,
            [volume, frequency]
        )

    def beep_off(self) -> GeoComResponse[None]:
        """
        RPC 11002, ``BMM_BeepOff``

        .. versionremoved:: GeoCOM-TPS1100

        Stops continuous beep signals.

        See Also
        --------
        beep_on
        beep_alarm
        beep_normal
        """
        return self._request(11002)

    def beep_start(
        self,
        volume: int = 100
    ) -> GeoComResponse[None]:
        """
        RPC 20001, ``IOS_BeepOn``

        .. versionadded:: GeoCOM-TPS1100
            Replaces the `beep_on` command.

        Starts a continuous beep signal with the specified intensity.

        Parameters
        ----------
        volume : int, optional
            Beep signal intensity [0; 100]%, by default 100

        See Also
        --------
        beep_stop
        beep_alarm
        beep_normal
        """
        return self._request(
            20001,
            [volume]
        )

    def beep_stop(self) -> GeoComResponse[None]:
        """
        RPC 20000, ``IOS_BeepOff``

        .. versionadded:: GeoCOM-TPS1100
            Replaces the `beep_off` command.

        Stops continuous beep signals.

        See Also
        --------
        beep_start
        beep_alarm
        beep_normal
        """
        return self._request(20000)

    def switch_display(
        self,
        enable: bool
    ) -> GeoComResponse[None]:
        """
        RPC 11009, (unknown)

        Activates or deactivates the display of the instrument.

        Parameters
        ----------
        enable : bool
            Enable the backlit display.

        Returns
        -------
        GeoComResponse

        Note
        ----
        This command was not found in the reference manuals, but discovered
        by accident while testing. Version or the corresponding GeoCOM
        function name is not known. Use with caution!
        """
        return self._request(
            11009,
            [enable]
        )
