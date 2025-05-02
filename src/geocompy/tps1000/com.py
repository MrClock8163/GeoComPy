"""
Description
===========

Module: ``geocompy.tps1000.com``

Definitions for the TPS1000 Communication subsystem.

Types
-----

- ``TPS1000COM``

"""
from __future__ import annotations

from ..data import (
    toenum,
    parsebool
)
from ..data_geocom import (
    Shutdown,
    Startup
)
from ..protocols import (
    GeoComSubsystem,
    GeoComResponse
)


class TPS1000COM(GeoComSubsystem):
    """
    Communication subsystem of the TPS1000 GeoCom protocol.

    This subsystem contains functions relevant to the communication
    with the instrument.

    """

    def get_geocom_version(self) -> GeoComResponse[tuple[int, int, int]]:
        """
        RPC 110, ``COM_GetSWVersion``

        Gets the version of the installed GeoCom release.

        Returns
        -------
        GeoComResponse
            Params:
                - `int`: Release number.
                - `int`: Version number.
                - `int`: Subversion number.

        See Also
        --------
        csv.get_sw_version
        """
        return self._request(
            110,
            parsers=(int, int, int)
        )

    def set_send_delay(
        self,
        delay: int
    ) -> GeoComResponse[None]:
        """
        RPC 109, ``COM_SetSendDelay``

        Sets response delay on the instrument.

        Parameters
        ----------
        delay : int
            Response delay [s].

        Returns
        -------
        GeoComResponse
        """
        return self._request(109, [delay])

    def switch_to_local(self) -> GeoComResponse[None]:
        """
        RPC 1, ``COM_Local``

        Switches instrument to local mode, exiting the online mode.

        Returns
        -------
        GeoComResponse

        Warning
        -------
        Once the instrument is switched to local mode, all further RPCs
        will be ignored, until the online mode is manually activated again.
        """
        return self._request(1)

    def switch_on(
        self,
        mode: Startup | str = Startup.REMOTE
    ) -> GeoComResponse[None]:
        """
        RPC 111, ``COM_SwitchOnTPS``

        Switches on the instrument.

        Parameters
        ----------
        mode : Startup | str, optional
            Desired startup mode, by default Startup.REMOTE

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``NOT_IMPL``: Instrument is already on.

        Notes
        -----
        The instrument can be switched on with any command, or even just
        a single character.

        See Also
        --------
        switch_off
        """
        _mode = toenum(Startup, mode)
        return self._request(
            111,
            [_mode.value]
        )

    def switch_off(
        self,
        mode: Shutdown | str = Shutdown.SHUTDOWN
    ) -> GeoComResponse[None]:
        """
        RPC 112, ``COM_SwitchOffTPS``

        Switches off the instrument.

        Parameters
        ----------
        mode : Shutdown | str, optional
            Desired stop mode, by default Shutdown.SHUTDOWN

        Returns
        -------
        GeoComResponse

        See Also
        --------
        switch_on
        """
        _mode = toenum(Shutdown, mode)
        return self._request(
            112,
            [_mode.value]
        )

    def nullproc(self) -> GeoComResponse[None]:
        """
        RPC 0, ``COM_NullProc``

        Tests connection by executing the null process.

        """
        return self._request(0)

    def enable_signoff(
        self,
        enable: bool
    ) -> GeoComResponse[None]:
        """
        RPC 115, ``COM_EnableSignOff``

        Enables or disables the signoff message upon operation mode
        changes.

        Parameters
        ----------
        enable : bool

        Returns
        -------
        GeoComResponse

        Note
        ----
        This setting is not persistent between sessions.
        """
        return self._request(115, [enable])

    def get_binary_available(self) -> GeoComResponse[bool]:
        """
        RPC 113, ``COM_GetBinaryAvailable``

        Checks if the instrument supports binary communication.

        Returns
        -------
        GeoComResponse
            Params:
                - `bool`: Availability of binary mode.

        See Also
        --------
        set_binary_available
        """
        return self._request(
            113,
            parsers=parsebool
        )

    def set_binary_available(
        self,
        enable: bool
    ) -> GeoComResponse[None]:
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
