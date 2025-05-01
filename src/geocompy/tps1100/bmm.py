"""
Description
===========

Module: ``geocompy.tps1100.bmm``

Definitions for the TPS1100 Basic man-machine interface subsystem.

Types
-----

- ``TPS1100BMM``
"""
from __future__ import annotations

from ..protocols import GeoComResponse
from ..tps1000.bmm import TPS1000BMM


class TPS1100BMM(TPS1000BMM):
    """
    Basic man-machine interface subsystem of the TPS1100 GeoCom protocol.

    This subsystem contains functions related to the operation of the
    keyboard, character sets and singalling devices.
    """

    def beep_on(
        self,
        volume: int = 100,
        deprecated: int = 0
    ) -> GeoComResponse[None]:
        """
        RPC 20001, ``IOS_BeepOn``

        .. versionchanged:: GeoCom-TPS1100
            The ``BMM_BeepOn`` command was replaced by ``IOS_BeepOn``.
            Frequency setting was deprecated.

        Starts a continuous beep signal with the specified intensity.

        Parameters
        ----------
        volume : int, optional
            Beep signal intensity [0; 100]%, by default 100
        deprecated : int, optional
            Unused, maintained for compatibility, by default 0

        See Also
        --------
        beep_off
        beep_alarm
        beep_normal
        """
        return self._request(
            20001,
            [volume]
        )

    def beep_off(self) -> GeoComResponse[None]:
        """
        RPC 20000, ``IOS_BeepOff``

        .. versionchanged:: GeoCom-TPS1100
            The ``BMM_BeepOff`` command was replaced by ``IOS_BeepOff``.

        Stops continuous beep signals.

        See Also
        --------
        beep_on
        beep_alarm
        beep_normal
        """
        return self._request(20000)
