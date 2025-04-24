"""
``geocompy.protocols``
======================

This module contains the base definitions of all command protocol
implementations, including their response types.

Types
-----

- ``GsiOnlineResponse``
- ``GsiOnlineProtocol``
- ``GsiOnlineSubsystem``
"""
from logging import Logger
from typing import Callable, Literal, Generic, TypeVar

from geocompy.communication import Connection, get_logger


_T = TypeVar("_T")


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
