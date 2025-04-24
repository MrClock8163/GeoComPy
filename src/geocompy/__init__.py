"""
GeoComPy
========

Python wrapper functions for communicating with surveying
instruments over a serial connection.

The implementations use the Leica GeoCom ASCII RPC procotol primarily.
For older instruments, that do not support it, the GSI Online commands
are used instead.

The package provides
    1. Utility data types for handling instrument responses
    2. Instrument software specific low level commands

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

``geocompy.protocols``
    Base definitions for command protocols and responses.

"""
from __future__ import annotations

from enum import Enum
from typing import Callable, Any, Iterable
from logging import Logger

from .data import Angle, Byte
from .communication import Connection, get_logger

try:
    from ._version import __version__
except Exception:
    __version__ = "0.0.0"  # Placeholder value for source installs


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
            logger = get_logger("/dev/null")
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
