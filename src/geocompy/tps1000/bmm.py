"""
Description
===========

Module: ``geocompy.tps1000.bmm``

Definitions for the TPS1000 Basic man-machine interface subsystem.

Types
-----

- ``TPS1000BMM``
"""
from __future__ import annotations

from ..protocols import (
    GeoComSubsystem,
    GeoComResponse
)


class TPS1000BMM(GeoComSubsystem):
    """
    Basic man-machine interface subsystem of the TPS1000 GeoCom protocol.

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

        Stops continuous beep signals.

        See Also
        --------
        beep_on
        beep_alarm
        beep_normal
        """
        return self._request(11002)
