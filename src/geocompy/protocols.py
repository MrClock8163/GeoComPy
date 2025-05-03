"""
Description
===========

Module: ``geocompy.protocols``

This module contains the base definitions of all command protocol
implementations, including their response types.

Types
-----

- ``GeoComReturnCode``
- ``GeoComResponse``
- ``GeoComProtocol``
- ``GeoComSubsystem``
- ``GsiOnlineResponse``
- ``GsiOnlineProtocol``
- ``GsiOnlineSubsystem``
"""
from __future__ import annotations

from enum import IntEnum
from logging import Logger
from typing import (
    Any, Callable, Iterable, Literal,
    Generic, TypeVar, overload
)

from .communication import Connection, get_logger
from .data import Angle, Byte


_T = TypeVar("_T")
_P = TypeVar("_P", bound=Any)


class GeoComReturnCode(IntEnum):
    """Base class for all GeoCom return code enums."""


class GeoComResponse(Generic[_P]):
    """
    Container class for parsed GeoCom responses.

    The response encapsulates the original command, that was sent, and the
    response received, as well as the codes and parameters extracted from
    the response.

    The `params` usually takes 3 types of values:

    - **None**: the response explicitly returned no values
    - **Scalar**: the response returned a single parameter
    - **Sequence** (usually a `tuple`): the response returned multiple
      parameters

    Warning
    -------
    The `params` will be also `None`, if the parameter parsing failed for
    some reason, to signal the unsuccessful operation. This error case must
    be handled before using the returned values.
    """

    def __init__(
        self,
        rpcname: str,
        cmd: str,
        response: str,
        comcode: GeoComReturnCode,
        rpccode: GeoComReturnCode,
        trans: int,
        params: _P | None = None
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
        params : Any | None, optional
            Collection of parsed response parameters. The content
            is dependent on the executed function. (default: None)
        """
        self.rpcname: str = rpcname
        """Name of the GeoCom function, that correspondes to the RPC,
            that invoked this response."""
        self.cmd: str = cmd
        """Full, serialized request, that invoked this response."""
        self.response: str = response
        """Full, received response."""
        self.code: GeoComReturnCode = (
            comcode
            if comcode.value == 0
            else rpccode
        )
        """Parsed return code indicating the success/failure of the
        request."""
        self.trans: int = trans
        """Parsed transaction ID."""
        self.params: _P | None = params
        """Collection of parsed response parameters. The content
            is dependent on the executed function."""

    def __str__(self) -> str:
        return (
            f"GeoComResponse({self.rpcname}) code: {self.code.name:s}, "
            f"tr: {self.trans:d}, "
            f"params: {self.params}, "
            f"(cmd: '{self.cmd}', response: '{self.response}')"
        )

    def __bool__(self) -> bool:
        return bool(self.code)

    def map_params(
        self,
        transformer: Callable[[_P | None], _T | None]
    ) -> GeoComResponse[_T]:
        """
        Returns a new response object with the metadata maintained, but
        the parameters transformed with the supplied function.

        Parameters
        ----------
        transformer : Callable[[_P  |  None], _T  |  None]
            Function to transform the params to new values.

        Returns
        -------
        GeoComResponse
            Response with transformed parameters.
        """
        try:
            params = transformer(self.params)
        except Exception:
            params = None

        return GeoComResponse(
            self.rpcname,
            self.cmd,
            self.response,
            self.code,
            self.code,
            self.trans,
            params
        )


class GeoComProtocol:
    """
    Base class for GeoCom protocol versions.

    """

    REF_VERSION = (0, 0)
    """
    Major and minor version of the reference manual, that this
    implementation is based on.
    """
    REF_VERSION_STR = "0.00"
    """
    Version string of the reference manual, that this implementation is
    based on.
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
            (usually a serial connection).
        logger : ~logging.Logger | None, optional
            Logger to log all requests and responses, by default None

        """
        self._conn: Connection = connection
        if logger is None:
            logger = get_logger("/dev/null")
        self._logger: Logger = logger

    @overload
    def request(
        self,
        rpc: int,
        params: Iterable[int | float | bool | str | Angle | Byte] = (),
        parsers: Callable[[str], _T] | None = None
    ) -> GeoComResponse[_T]: ...

    @overload
    def request(
        self,
        rpc: int,
        params: Iterable[int | float | bool | str | Angle | Byte] = (),
        parsers: Iterable[Callable[[str], Any]] | None = None
    ) -> GeoComResponse[tuple]: ...

    def request(
        self,
        rpc: int,
        params: Iterable[int | float | bool | str | Angle | Byte] = (),
        parsers: (
            Iterable[Callable[[str], Any]]
            | Callable[[str], Any]
            | None
        ) = None
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
        params : Iterable[int | float | bool | str | Angle | Byte]
            Parameters for the request, by default ()
        parsers : Iterable[Callable[[str], Any]] \
                  | Callable[[str], Any] \
                  | None, optional
            Parser functions for the values in the RPC response,
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

    @overload
    def parse_response(
        cls,
        cmd: str,
        response: str,
        parsers: Callable[[str], _T] | None = None
    ) -> GeoComResponse[_T]: ...

    @overload
    def parse_response(
        cls,
        cmd: str,
        response: str,
        parsers: Iterable[Callable[[str], Any]] | None = None
    ) -> GeoComResponse[tuple]: ...

    def parse_response(
        cls,
        cmd: str,
        response: str,
        parsers: (
            Iterable[Callable[[str], Any]]
            | Callable[[str], Any]
            | None
        ) = None
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
        parsers : Iterable[Callable[[str], Any]] \
                  | Callable[[str], Any] \
                  | None, optional
            Parser functions for the values in the RPC response,
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


class GsiOnlineResponse(Generic[_T]):
    """Container class for parsed GSI Online responses."""

    def __init__(
        self,
        desc: str,
        cmd: str,
        response: str,
        value: _T | None,
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
        self.value: _T | None = value
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


class GsiOnlineProtocol:
    """
    Base class for GSI Online protocol versions.
    """

    REF_VERSION = (0, 0)
    """
    Major and minor version of the reference manual, that this
    implementation is based on.
    """
    REF_VERSION_STR = "0000.00"
    """
    Version string of the reference manual, that this implementation is
    based on.
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
            (usually a serial connection).
        logger : ~logging.Logger | None, optional
            Logger to log all requests and responses, by default None
        """
        self._conn: Connection = connection
        if logger is None:
            logger = get_logger("/dev/null")
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
