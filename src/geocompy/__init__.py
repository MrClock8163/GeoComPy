"""
GeoComPy
========

Python wrapper functions for communicating with surveying
instruments over a serial connection.

The implementations use the Leica GeoCom ASCII RPC procotoll
primarily. For older instruments, that do not support it, the
GSI Online commands are used instead.

The package provides
    1. Utility data types for handling instrument responses
    2. Instrument software specific low level commands
    3. Instrument-agnostic higher level functions for instrument types

Documentation
-------------

Public classes and methods are provided with proper docstrings, that can
be viewed in the source code, through introspection tools or editor
utilities. The docstrings follow the NumPy style conventions. In addition
to the in-code documentation, a complete, rendered reference is avaialable
on the `GeoComPy documentation <https://geocompy.readthedocs.io>`_ site.

Some docstrings provide examples. These examples assume that `geocompy`
has been imported as ``gc``:

    >>> import geocompy as gc

Subpackages
-----------

``geocompy.tps1200p``
    Communication with instruments running TPS1200+ software.

``geocompy.vivatps``
    Communication with instruments running Viva(/Nova)TPS software.

``geocompy.dna``
    Communication with DNA digital level instruments.

Submodules
----------

``geocompy.data``
    Utilities for data handling.

``geocompy.communication``
    Communication methods.

"""
from __future__ import annotations

from enum import Enum
from typing import Callable, Any, Iterable, Generic, TypeVar, Literal
from logging import Logger, NullHandler

from .data import Angle, Byte
from .communication import Connection

try:
    from ._version import __version__
except Exception:
    __version__ = "0.0.0"  # Placeholder value for source installs


_T = TypeVar("_T")


class GeoComReturnCode(Enum):
    """Base class for all GeoCom return code enums."""


class GeoComResponse:
    """
    Container class for parsed GeoCom responses.

    """

    def __init__(
        self,
        rpcname: str,
        cmd: str,
        response: str,
        comcode: GeoComReturnCode,
        rpccode: GeoComReturnCode,
        trans: int,
        params: dict[str, Any]
    ):
        """
        Parameters
        ----------
        rpcname : str
            Name of the GeoCom function, that corresponds to the RPC,
            that invoked this response.
        cmd : str
            Full, serialized request, that invoked this response.
        response : str
            Full, received response.
        comcode : GeoComReturnCode
            Parsed COM return code indicating the success/failure of
            communication.
        rpccode : GeoComReturnCode
            Parsed RPC return code indicating the success/failure of
            the command.
        trans : int
            Parsed transaction ID.
        params : dict[str, Any]
            Collection of parsed response parameters. The content
            is dependent on the executed function.
        """
        self.rpcname: str = rpcname
        """Name of the GeoCom function, that correspondes to the RPC,
            that invoked this response."""
        self.cmd: str = cmd
        """Full, serialized request, that invoked this response."""
        self.response: str = response
        """Full, received response."""
        self.comcode: GeoComReturnCode = comcode
        """Parsed COM return code indicating the success/failure of
            communication."""
        self.rpccode: GeoComReturnCode = rpccode
        """Parsed RPC return code indicating the success/failure of
            the command."""
        self.trans: int = trans
        """Parsed transaction ID."""
        self.params: dict[str, Any] = params
        """Collection of parsed response parameters. The content
            is dependent on the executed function."""

    def __str__(self) -> str:
        return (
            f"GeoComResponse({self.rpcname}) com: {self.comcode.name:s}, "
            f"rpc: {self.rpccode.name:s}, "
            f"tr: {self.trans:d}, "
            f"params: {self.params}, "
            f"(cmd: '{self.cmd}', response: '{self.response}')"
        )

    def __bool__(self) -> bool:
        return bool(self.comcode) and bool(self.rpccode)


class GeoComSubsystem:
    """
    Base class for GeoCom subsystems.

    """

    def __init__(self, parent: GeoComProtocol):
        """
        Parameters
        ----------
        parent : GeoComProtocol
            The parent protocol instance of this subsystem.
        """
        self._parent: GeoComProtocol = parent
        """Parent protocol instance"""
        self._request = self._parent.request
        """Shortcut to the `request` method of the parent protocol."""


class GeoComProtocol:
    """
    Base class for GeoCom protocol versions.

    """

    def __init__(
        self,
        connection: Connection,
        logger: Logger | None = None
    ):
        """
        Parameters
        ----------
        connection : Connection
            Connection to use for communication
            (usually :class:`~communication.SerialConnection`).
        logger : ~logging.Logger | None, optional
            Logger to log all requests and responses, by default None

        """
        self._conn: Connection = connection
        if logger is None:
            logger = Logger("/dev/null")
            logger.addHandler(NullHandler())
        self._logger: Logger = logger

    def request(
        self,
        rpc: int,
        params: Iterable[int | float | bool | str | Angle | Byte] = [],
        parsers: dict[str, Callable[[str], Any]] | None = None
    ) -> GeoComResponse:
        """
        Executes an RPC request and returns the parsed GeoCom response.

        Constructs a request (from the given RPC code and parameters),
        writes it to the serial line, then reads the response. The
        response is then parsed using the provided parser functions.

        Parameters
        ----------
        rpc : int
            Number of the RPC to execute.
        params : Iterable[int | float | bool | str | Angle | Byte], optional
            Parameters for the request, by default []
        parsers : dict[str, Callable[[str], Any]] | None, optional
            Parser functions for the values in the RPC response
            (Maps the parser functions to the names of the parameters),
            by default None

        Returns
        -------
        GeoComResponse
            Parsed return codes and parameters from the RPC response.

        Raises
        ------
        NotImplementedError
            If the method is not implemented on the class.

        """
        raise NotImplementedError()

    def parse_response(
        cls,
        cmd: str,
        response: str,
        parsers: dict[str, Callable[[str], Any]]
    ) -> GeoComResponse:
        """
        Parses RPC response and constructs :class:`GeoComResponse`
        instance.

        Parameters
        ----------
        cmd : str
            Full, serialized request, that invoked the response.
        response : str
            Full, received response.
        parsers : dict[str, Callable[[str], Any]]
            Parser functions for the values in the RPC response.
            (Maps the parser functions to the names of the parameters.)

        Returns
        -------
        GeoComResponse
            Parsed return codes and parameters from the RPC response.

        Raises
        ------
        NotImplementedError
            If the method is not implemented on the class.

        """
        raise NotImplementedError()


class GsiOnlineResponse(Generic[_T]):
    """Container class for parsed GSI Online responses."""

    def __init__(
        self,
        desc: str,
        cmd: str,
        response: str,
        value: _T,
        comment: str = ""
    ):
        """
        Parameters
        ----------
        desc : str
            Description of the GSI Online command, that invoked this
            response.
        cmd : str
            Full, serialized command, that invoked this response.
        response : str
            Full, received response.
        value
            Parsed response value. The content is dependent on the
            executed command.
        comment : str
            Additional comment (e.g. explanation of an error).
        """
        self.desc: str = desc
        """Description of the GSI Online command, that invoked this
        response."""
        self.cmd: str = cmd
        """Full, serialized command, that invoked this response."""
        self.response: str = response
        """Full, received response."""
        self.value: _T = value
        """Parsed response value. The content is dependent on the
        executed command."""
        self.comment: str = comment
        """Additional comment (e.g. explanation of an error)."""

    def __str__(self) -> str:
        success = (
            "success"
            if self.value is not None
            else f"fail ({self.comment})"
        )
        return (
            f"GsiOnlineResponse({self.desc}) "
            f"{success}, "
            f"value: {self.value}, "
            f"(cmd: '{self.cmd}', response: '{self.response}')"
        )

    def __bool__(self) -> bool:
        return self.value is not None


class GsiOnlineSubsystem:
    """
    Base class for GSI Online subsystems.
    """

    def __init__(self, parent: GsiOnlineProtocol):
        """
        Parameters
        ----------
        parent : GsiOnlineProtocol
            The parent protocol instance of this subsystem.
        """
        self._parent: GsiOnlineProtocol = parent
        """Parent protocol instance"""
        self._setrequest = self._parent.setrequest
        """Shortcut to the `setrequest` method of the parent protocol."""
        self._confrequest = self._parent.confrequest
        """Shortcut to the `confrequest` method of the parent protocol."""
        self._putrequest = self._parent.putrequest
        """Shortcut to the `putrequest` method of the parent protocol."""
        self._getrequest = self._parent.getrequest
        """Shortcut to the `getrequest` method of the parent protocol."""


class GsiOnlineProtocol:
    """
    Base class for GSI Online protocol versions.
    """

    def __init__(
        self,
        connection: Connection,
        logger: Logger | None = None
    ):
        """
        Parameters
        ----------
        connection : Connection
            Connection to use for communication
            (usually :class:`~communication.SerialConnection`).
        logger : ~logging.Logger | None, optional
            Logger to log all requests and responses, by default None
        """
        self._conn: Connection = connection
        if logger is None:
            logger = Logger("/dev/null")
            logger.addHandler(NullHandler())
        self._logger: Logger = logger
        self._gsi16 = False

    def setrequest(
        self,
        param: int,
        value: int
    ) -> GsiOnlineResponse[bool]:
        """
        Executes a GSI Online SET command and returns the success
        of the operation in a GSI Online response.

        Parameters
        ----------
        param : int
            Index of the parameter to set.
        value : int
            Value to set the parameter to.

        Returns
        -------
        GsiOnlineResponse
            Response information.

        Raises
        ------
        NotImplementedError
            If the method is not implemented on the class.
        """
        raise NotImplementedError()

    def confrequest(
        self,
        param: int,
        parser: Callable[[str], _T]
    ) -> GsiOnlineResponse[_T | None]:
        """
        Executes a GSI Online CONF command and returns the result
        of the parameter query.

        Parameters
        ----------
        param : int
            Index of the parameter to query.
        parser
            Parser function to process the result of the query.

        Returns
        -------
        GsiOnlineResponse
            Parsed parameter value.

        Raises
        ------
        NotImplementedError
            If the method is not implemented on the class.
        """
        raise NotImplementedError()

    def putrequest(
        self,
        wordindex: int,
        word: str
    ) -> GsiOnlineResponse[bool]:
        """
        Executes a GSI Online PUT command and returns the success
        of the operation.

        Parameters
        ----------
        wordindex : int
            Index of the GSI word to set.
        word : str
            Complete GSI word to set.

        Returns
        -------
        GsiOnlineResponse
            Response information.

        Raises
        ------
        NotImplementedError
            If the method is not implemented on the class.
        """
        raise NotImplementedError()

    def getrequest(
        self,
        mode: Literal['I', 'M', 'C'],
        wordindex: int,
        parser: Callable[[str], _T]
    ) -> GsiOnlineResponse[_T | None]:
        """
        Executes a GSI Online GET command and returns the result
        of the GSI word query.

        Parameters
        ----------
        mode : Literal['I', 'M', 'C']
            Request mode. ``I``: internal/instant, ``M``: measure,
            ``C``: continuous.
        wordindex : int
            Index of the GSI word to get.
        parser : Callable[[str], _T]
            Parser function to process the result of the query.

        Returns
        -------
        GsiOnlineResponse
            Parsed value.

        Raises
        ------
        NotImplementedError
            If the method is not implemented on the class.
        """
        raise NotImplementedError()

    def request(
        self,
        cmd: str,
        desc: str = ""
    ) -> GsiOnlineResponse[bool]:
        """
        Executes a low level GSI Online command and returns the success
        of the execution.

        Parameters
        ----------
        cmd : str
            Command string to send to instrument.
        desc : str
            Command description to show in response.

        Returns
        -------
        GsiOnlineResponse
            Success of the execution.

        Raises
        ------
        NotImplementedError
            If the method is not implemented on the class.
        """
        raise NotImplementedError()
