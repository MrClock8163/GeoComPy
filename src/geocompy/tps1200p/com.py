"""
``geocompy.tps1200p.com``
=========================

Definitions for the TPS1200+ Communication subsystem.

Types
-----

- ``TPS1200PCOM``

"""
from __future__ import annotations

from enum import Enum

from .. import (
    GeoComSubsystem,
    GeoComResponse
)
from ..data import toenum


class TPS1200PCOM(GeoComSubsystem):
    """
    Communication subsystem of the TPS1200+ GeoCom protocol.

    This subsystem contains functions relevant to the communication
    with the instrument.

    """
    class STOPMODE(Enum):
        SHUTDOWN = 0
        SLEEP = 1

    class STARTUPMODE(Enum):
        LOCAL = 0
        REMOTE = 1

    def get_sw_version(self) -> GeoComResponse:
        """
        RPC 110, ``COM_GetSWVersion``

        Gets the version of the installed GeoCom release.

        Returns
        -------
        GeoComResponse
            - Params:
                - **release** (`int`): Release number.
                - **version** (`int`): Version number.
                - **subversion** (`int`): Subversion number.

        See Also
        --------
        csv.get_sw_version
        """
        return self._request(
            110,
            parsers={
                "release": int,
                "version": int,
                "subversion": int
            }
        )

    def switch_on(
        self,
        onmode: STARTUPMODE | str = STARTUPMODE.REMOTE
    ) -> GeoComResponse:
        """
        RPC 111, ``COM_SwitchOnTPS``

        Switches on the instrument.

        Parameters
        ----------
        onmode : STARTUPMODE | str, optional
            Desired startup mode, by default STARTUPMODE.REMOTE

        Returns
        -------
        GeoComResponse
            - Error codes:
                - ``NOT_IMPL``: Instrument is already on.

        Notes
        -----
        The instrument can be switched on with any command, or even just
        a single character.

        See Also
        --------
        switch_off
        """
        _onmode = toenum(self.STARTUPMODE, onmode)
        return self._request(
            111,
            [_onmode.value]
        )

    def switch_off(
        self,
        offmode: STOPMODE | str = STOPMODE.SHUTDOWN
    ) -> GeoComResponse:
        """
        RPC 112, ``COM_SwitchOffTPS``

        Switches off the instrument.

        Parameters
        ----------
        offmode : STOPMODE | str, optional
            Desired stop mode, by default STOPMODE.SHUTDOWN

        Returns
        -------
        GeoComResponse

        See Also
        --------
        switch_on
        """
        _offmode = toenum(self.STOPMODE, offmode)
        return self._request(
            112,
            [_offmode.value]
        )

    def nullproc(self) -> GeoComResponse:
        """
        RPC 0, ``COM_NullProc``

        Tests connection by executing the null process.

        """
        return self._request(0)

    def get_binary_available(self) -> GeoComResponse:
        """
        RPC 113, ``COM_GetBinaryAvailable``

        Checks if the instrument supports binary communication.

        Returns
        -------
        GeoComResponse
            - Params:
                - **available** (`bool`): Availability of binary mode.

        See Also
        --------
        set_binary_available
        """
        return self._request(
            113,
            parsers={
                "available": bool
            }
        )

    def set_binary_available(
        self,
        enable: bool
    ) -> GeoComResponse:
        """
        RPC 114, ``COM_SetBinaryAvailable``

        Enables or disables binary communication with the instrument.

        Parameters
        ----------
        enable : bool
            Enable or disable binary communication.

        See Also
        --------
        get_binary_available
        """
        return self._request(
            114,
            [enable]
        )
