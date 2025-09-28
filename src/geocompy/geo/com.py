"""
Description
===========

Module: ``geocompy.geo.com``

Definitions for the GeoCOM Communication subsystem.

Types
-----

- ``GeoComCOM``

"""
from __future__ import annotations

from ..data import (
    get_enum,
    parse_bool
)
from .gcdata import (
    Shutdown,
    Startup
)
from .gctypes import (
    GeoComSubsystem,
    GeoComResponse
)


class GeoComCOM(GeoComSubsystem):
    """
    Communication subsystem of the GeoCOM protocol.

    This subsystem contains functions relevant to the communication
    with the instrument.

    """

    def get_double_precision(self) -> GeoComResponse[int]:
        """
        RPC 108, ``COM_GetDoublePrecision``

        Gets the current ASCII communication floating point precision of
        the instrument.

        Returns
        -------
        GeoComResponse
            Params:
                - `int`: Floating point decimal places.

        See Also
        --------
        set_double_precision
        """
        return self._request(
            108,
            parsers=int
        )

    def set_double_precision(
        self,
        digits: int
    ) -> GeoComResponse[None]:
        """
        RPC 107, ``COM_SetDoublePrecision``

        Sets the ASCII communication floating point precision of the
        instrument.

        Parameters
        ----------
        digits: int
            Floating points decimal places.

        Returns
        -------
        GeoComResponse

        See Also
        --------
        get_double_precision
        """
        response: GeoComResponse[None] = self._request(107, [digits])
        if not response.error:
            self._parent.precision = digits
        return response

    def get_geocom_version(self) -> GeoComResponse[tuple[int, int, int]]:
        """
        RPC 110, ``COM_GetSWVersion``

        Gets the version of the installed GeoCOM release.

        Returns
        -------
        GeoComResponse
            Params:
                - `int`: Release number.
                - `int`: Version number.
                - `int`: Subversion number.

        See Also
        --------
        csv.get_firmware_version
        """
        return self._request(
            110,
            parsers=(int, int, int)
        )

    def set_send_delay(
        self,
        delay: float
    ) -> GeoComResponse[None]:
        """
        RPC 109, ``COM_SetSendDelay``

        .. versionremoved:: GeoCOM-TPS1200

        Sets response delay on the instrument.

        Parameters
        ----------
        delay : float
            Response delay [s].

        Returns
        -------
        GeoComResponse
        """
        return self._request(109, [int(delay * 1000)])

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
        _mode = get_enum(Startup, mode)
        return self._request(
            111,
            [_mode]
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
        _mode = get_enum(Shutdown, mode)
        return self._request(
            112,
            [_mode]
        )

    def nullprocess(self) -> GeoComResponse[None]:
        """
        RPC 0, ``COM_NullProc``

        Tests connection by executing the null process.

        """
        return self._request(0)

    def switch_signoff(
        self,
        enable: bool
    ) -> GeoComResponse[None]:
        """
        RPC 115, ``COM_EnableSignOff``

        .. versionremoved:: GeoCOM-TPS1200

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
            parsers=parse_bool
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
