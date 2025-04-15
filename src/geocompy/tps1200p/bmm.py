"""
``geocompy.tps1200p.bmm``
=========================

Definitions for the TPS1200+ Basic man-machine interface subsystem.

Types
-----

- ``TPS1200PBMM``
"""
from __future__ import annotations

from .. import (
    GeoComSubsystem,
    GeoComResponse
)


class TPS1200PBMM(GeoComSubsystem):
    """
    Basic man-machine interface subsystem of the TPS1200+ GeoCom protocol.

    This subsystem contains functions related to the operation of the
    keyboard, character sets and singalling devices.
    """

    def beep_alarm(self) -> GeoComResponse:
        """
        RPC 11804, ``BMM_BeepAlarm``

        Produces a triple beep. Previously started continuous signals will
        be aborted.

        See Also
        --------
        beep_normal
        beep_on
        beep_off
        """
        return self._request(11004)

    def beep_normal(self) -> GeoComResponse:
        """
        RPC 11803, ``BMM_BeepNormal``

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
        intensity: int
    ) -> GeoComResponse:
        """
        RPC 20001, ``IOS_BeepOn``

        Starts a continuous beep signal with the specified intensity.

        Parameters
        ----------
        intensity : int
            Beep signal intensity [0; 100]%.

        See Also
        --------
        beep_off
        beep_alarm
        beep_normal
        """
        return self._request(
            20001,
            [intensity]
        )

    def beep_off(self) -> GeoComResponse:
        """
        RPC 20000, ``IOS_BeepOff``

        Stops continuous beep signals.

        See Also
        --------
        beep_on
        beep_alarm
        beep_normal
        """
        return self._request(20000)
