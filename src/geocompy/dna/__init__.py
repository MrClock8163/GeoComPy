"""
``geocompy.dna``
=====================

The ``dna`` package provides wrapper methods for all GSI Online commands
available on a DNA digital level instrument.

Types
-----

- ``DNA``

Submodules
----------

- ``geocompy.dna.meta``
- ``geocompy.dna.settings``
- ``geocompy.dna.measurements``
"""
from __future__ import annotations

from enum import IntEnum
import re
from typing import Callable, TypeVar
from traceback import format_exc
import logging
from time import sleep

from .. import (
    GsiOnlineProtocol,
    GsiOnlineResponse
)
from ..communication import Connection
from ..data import (
    toenum
)
from .meta import (
    param_descriptions,
    word_descriptions,
    DNAErrors
)
from .settings import DNASettings
from .measurements import DNAMeasurements


_T = TypeVar("_T")


class DNA(GsiOnlineProtocol):
    """
    DNA GSI Online protocol handler.

    The individual commands are available through their respective
    subsystems.

    Examples
    --------

    Opening a simple serial connection:

    >>> from serial import Serial
    >>> from geocompy.communication import SerialConnection
    >>> from geocompy.dna import DNA
    >>>
    >>> port = Serial("COM4", timeout=15)
    >>> with SerialConnection(port) as line:
    ...     dna = DNA(line)
    ...     dna.beep('SHORT')
    ...
    >>>

    Passing a logger:

    >>> from logging import Logger, StreamHandler, DEBUG
    >>> from serial import Serial
    >>> from geocompy.communication import SerialConnection
    >>> from geocompy.dna import DNA
    >>>
    >>> log = Logger("stdout", DEBUG)
    >>> log.addHandler(StreamHandler())
    >>> port = Serial("COM4", timeout=15)
    >>> with SerialConnection(port) as line:
    ...     dna = DNA(line, log)
    ...     dna.beep('SHORT')
    ...
    >>>
    GsiOnlineResponse(GSI Type) ... # Startup GSI format sync
    GsiOnlineResponse(Beep) ... # First executed command
    """
    _CONFPAT = re.compile(
        r"^(?:\d{4})/"
        r"(?:\d{4})$"
    )
    _GSIPAT = re.compile(
        r"^\*?"
        r"(?:[0-9\.]{6})"
        r"(?:\+|\-)"
        r"(?:[a-zA-Z0-9]{8}|[a-zA-Z0-9]{16}) $"
    )

    class BEEPTYPE(IntEnum):
        SHORT = 0
        LONG = 1
        ALARM = 2

    def __init__(
        self,
        connection: Connection,
        logger: logging.Logger | None = None,
        retry: int = 2
    ):
        """
        After all subsystems are initialized, the connection is tested /
        initiated with a wake up command (this means the instruments does
        not have to be turned on manually before initiating the
        connection). If the test fails, it is retried with one second
        delay. The test / wakeup is attempted `retry` amount of times.

        Parameters
        ----------
        connection : Connection
            Connection to the DNA instrument (usually a serial connection).
        logger : logging.Logger | None, optional
            Logger to log all requests and responses, by default None
        retry : int, optional
            Number of retries at connection validation before giving up,
            by default 2

        Raises
        ------
        ConnectionError
            If the connection could not be verified in the specified
            number of retries.
        """
        super().__init__(connection, logger)
        self.settings: DNASettings = DNASettings(self)
        """Instrument settings subsystem."""
        self.measurements: DNAMeasurements = DNAMeasurements(self)
        """Measurements subsystem."""

        for i in range(retry):
            try:
                reply = self._conn.exchange("a")
                if reply == "?":
                    break
            except Exception:
                pass

            sleep(1)
        else:
            raise ConnectionError(
                "could not establish connection to instrument"
            )

        self.settings.get_format()  # Sync format setting

    def setrequest(
        self,
        param: int,
        value: int
    ) -> GsiOnlineResponse[bool]:
        """
        Executes a GSI Online SET command and returns the success
        of the operation.

        Parameters
        ----------
        param : int
            Index of the parameter to set.
        value : int
            Value to set the parameter to.

        Returns
        -------
        GsiOnlineResponse
            Success of the parameter change.
        """
        cmd = f"SET/{param:d}/{value:d}"
        comment = ""
        try:
            answer = self._conn.exchange(cmd)
        except Exception:
            self._logger.error(format_exc())
            answer = DNAErrors.E_UNKNOWN.value
            comment = "EXCHANGE"
        value = answer == "?"
        if not value:
            comment = "INSTRUMENT"

        return GsiOnlineResponse(
            param_descriptions.get(param, ""),
            cmd,
            answer,
            value,
            comment
        )

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
        """
        cmd = f"CONF/{param:d}"
        comment = ""
        try:
            answer = self._conn.exchange(cmd)
        except Exception:
            self._logger.error(format_exc())
            answer = DNAErrors.E_UNKNOWN.value
            comment = "EXCHANGE"

        success = bool(self._CONFPAT.match(answer))
        value = None
        if success:
            try:
                value = parser(answer.split("/")[1])
            except Exception:
                comment = "PARSE"
        else:
            comment = "INSTRUMENT"

        response = GsiOnlineResponse(
            param_descriptions.get(param, ""),
            cmd,
            answer,
            value,
            comment
        )
        self._logger.debug(response)
        return response

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
            Success of the change.
        """
        cmd = f"PUT/{word:s}"
        comment = ""
        try:
            answer = self._conn.exchange(cmd)
        except Exception:
            self._logger.error(format_exc())
            answer = DNAErrors.E_UNKNOWN.value
            comment = "EXCHANGE"
        value = answer == "?"
        if not value:
            comment = "INSTRUMENT"

        response = GsiOnlineResponse(
            word_descriptions.get(wordindex, ""),
            cmd,
            answer,
            value,
            comment
        )
        self._logger.debug(response)
        return response

    def getrequest(
        self,
        mode: str,
        wordindex: int,
        parser: Callable[[str], _T]
    ) -> GsiOnlineResponse[_T | None]:
        """
        Executes a GSI Online GET command and returns the parsed result
        of the GSI word query.

        Parameters
        ----------
        mode : Literal['I', 'M', 'C']
            Request mode. ``I``: internal/instant, ``M``: measure,
            ``C``: continuous.
        wordindex : int
            Index of the GSI word to get.
        parser
            Parser function to process the result of the query.

        Returns
        -------
        GsiOnlineResponse
            Parsed value.
        """
        cmd = f"GET/{mode:s}/WI{wordindex:d}"
        comment = ""
        try:
            answer = self._conn.exchange(cmd)
        except Exception:
            self._logger.error(format_exc())
            answer = DNAErrors.E_UNKNOWN.value
            comment = "EXCHANGE"

        success = bool(self._GSIPAT.match(answer))
        value = None
        if success:
            try:
                value = parser(answer)
            except Exception:
                comment = "PARSE"
        else:
            comment = "INSTRUMENT"

        response = GsiOnlineResponse(
            word_descriptions.get(wordindex, ""),
            cmd,
            answer,
            value,
            comment
        )
        self._logger.debug(response)
        return response

    def request(
        self,
        cmd: str
    ) -> GsiOnlineResponse[bool]:
        """
        Executes a low level GSI Online command and returns the success
        of the execution.

        Parameters
        ----------
        cmd : str
            Command string to send to instrument.

        Returns
        -------
        GsiOnlineResponse
            Success of the execution.
        """
        comment = ""
        try:
            answer = self._conn.exchange(cmd)
        except Exception:
            self._logger.error(format_exc())
            answer = DNAErrors.E_UNKNOWN.value
            comment = "EXCHANGE"

        response = GsiOnlineResponse(
            "",
            cmd,
            answer,
            answer == "?",
            comment
        )
        self._logger.debug(response)
        return response

    def beep(
        self,
        beeptype: BEEPTYPE | str
    ) -> GsiOnlineResponse[bool]:
        """
        Gives a beep signal command to the instrument.

        Parameters
        ----------
        beeptype : BEEPTYPE | str
            Type of the beep signal to give off.

        Returns
        -------
        GsiOnlineResponse
            Success of the execution.
        """
        _beeptype = toenum(self.BEEPTYPE, beeptype)
        cmd = f"BEEP/{_beeptype.value:d}"
        response = self.request(cmd)
        response.desc = "Beep"
        return response

    def wakeup(self) -> GsiOnlineResponse[bool]:
        """
        Wakes up the instrument.

        Returns
        -------
        GsiOnlineResponse
            Success of the execution.
        """
        response = self.request("a")
        response.desc = "Wakeup"
        return response

    def shutdown(self) -> GsiOnlineResponse[bool]:
        """
        Shuts down the instrument.

        Returns
        -------
        GsiOnlineResponse
            Success of the execution.
        """
        response = self.request("b")
        response.desc = "Shutdown"
        return response

    def clear(self) -> GsiOnlineResponse[bool]:
        """
        Clears the command receiver buffer and aborts any running
        continuous measurement.

        Returns
        -------
        GsiOnlineResponse
            Success of the execution.
        """
        response = self.request("c")
        response.desc = "Clear"
        return response
