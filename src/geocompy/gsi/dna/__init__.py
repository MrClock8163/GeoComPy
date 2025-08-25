"""
Description
===========

Module: ``geocompy.gsi.dna``

The ``dna`` package provides wrapper methods for all GSI Online commands
available on a DNA digital level instrument.

Types
-----

- ``GsiOnlineDNA``

Submodules
----------

- ``geocompy.gsi.dna.settings``
- ``geocompy.gsi.dna.measurements``
"""
from __future__ import annotations

from enum import IntEnum
import re
from typing import Callable, TypeVar
from traceback import format_exc
from logging import Logger
from time import sleep

from ..gsitypes import (
    GsiOnlineType,
    GsiOnlineResponse,
    param_descriptions,
    word_descriptions
)
from ...communication import Connection, DUMMYLOGGER
from ...data import (
    toenum
)
from ..gsiformat import GsiWord
from .settings import GsiOnlineDNASettings
from .measurements import GsiOnlineDNAMeasurements


_T = TypeVar("_T")
_G = TypeVar("_G", bound=GsiWord)
_UNKNOWNERROR = "@E0"


class GsiOnlineDNA(GsiOnlineType):
    """
    DNA GSI Online protocol handler.

    The individual commands are available through their respective
    subsystems.

    Examples
    --------

    Opening a simple serial connection:

    >>> from geocompy.communication import open_serial
    >>> from geocompy.gsi.dna import GsiOnlineDNA
    >>>
    >>> with open_serial("COM1") as line:
    ...     dna = GsiOnlineDNA(line)
    ...     dna.beep('SHORT')
    ...
    >>>

    Passing a logger:

    >>> from sys import stdout
    >>> from logging import getLogger, DEBUG, StreamHandler
    >>>
    >>> from geocompy.communication import open_serial
    >>> from geocompy.gsi.dna import GsiOnlineDNA
    >>>
    >>> logger = getLogger("TPS")
    >>> logger.addHandler(StreamHandler(stdout))
    >>> logger.setLevel(DEBUG)
    >>> with open_serial("COM1") as line:
    ...     dna = GsiOnlineDNA(line, logger)
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

    REF_VERSION = (2008, 3)
    """
    Major and minor version of the reference manual, that this
    implementation is based on.
    """
    REF_VERSION_STR = "2008.03"
    """
    Version string of the reference manual, that this implementation is
    based on.
    """

    class BEEPTYPE(IntEnum):
        SHORT = 0
        LONG = 1
        ALARM = 2

    def __init__(
        self,
        connection: Connection,
        logger: Logger | None = None,
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
        self._conn: Connection = connection
        if logger is None:
            logger = DUMMYLOGGER
        self._logger: Logger = logger
        self._is_client_gsi16 = False

        self.settings: GsiOnlineDNASettings = GsiOnlineDNASettings(self)
        """Instrument settings subsystem."""
        self.measurements: GsiOnlineDNAMeasurements = GsiOnlineDNAMeasurements(
            self)
        """Measurements subsystem."""

        for i in range(retry):
            try:
                reply = self.wakeup()
                if reply.value:
                    break
            except Exception:
                self._logger.exception("Exception during wakeup attempt")

            sleep(1)
        else:
            raise ConnectionError(
                "could not establish connection to instrument"
            )

        self.settings.get_format()  # Sync format setting

        self._logger.info("Connection initialized")

    @property
    def is_client_gsi16(self) -> bool:
        return self._is_client_gsi16

    @is_client_gsi16.setter
    def is_client_gsi16(self, value: bool) -> None:
        self._is_client_gsi16 = value

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
            answer = _UNKNOWNERROR
            comment = "EXCHANGE"
        value = answer == "?"
        if not value:
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

    def confrequest(
        self,
        param: int,
        parser: Callable[[str], _T]
    ) -> GsiOnlineResponse[_T]:
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
            answer = _UNKNOWNERROR
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
        word: GsiWord
    ) -> GsiOnlineResponse[bool]:
        """
        Executes a GSI Online PUT command and returns the success
        of the operation.

        Parameters
        ----------
        word : GsiWord
            GSI word to send.

        Returns
        -------
        GsiOnlineResponse
            Success of the change.
        """
        asterisk = "*" if self.is_client_gsi16 else ""
        cmd = f"PUT/{asterisk}{word.serialize(self.is_client_gsi16):s}"
        comment = ""
        try:
            answer = self._conn.exchange(cmd)
        except Exception:
            self._logger.error(format_exc())
            answer = _UNKNOWNERROR
            comment = "EXCHANGE"
        value = answer == "?"
        if not value:
            comment = "INSTRUMENT"

        response = GsiOnlineResponse(
            word_descriptions.get(word.wi, ""),
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
        wordtype: type[_G]
    ) -> GsiOnlineResponse[_G]:
        """
        Executes a GSI Online GET command and returns the parsed result
        of the GSI word query.

        Parameters
        ----------
        mode : Literal['I', 'M', 'C']
            Request mode. ``I``: internal/instant, ``M``: measure,
            ``C``: continuous.
        wordtype : type[GsiWord]
            GsiWord type to request.

        Returns
        -------
        GsiOnlineResponse
            Parsed value.
        """
        cmd = f"GET/{mode:s}/WI{wordtype.WI():d}"
        comment = ""
        try:
            answer = self._conn.exchange(cmd)
        except Exception:
            self._logger.error(format_exc())
            answer = _UNKNOWNERROR
            comment = "EXCHANGE"

        success = bool(self._GSIPAT.match(answer))
        value: _G | None = None
        if success:
            try:
                value = wordtype.parse(answer.lstrip("*"))
            except Exception:
                comment = "PARSE"
        else:
            comment = "INSTRUMENT"

        response = GsiOnlineResponse(
            word_descriptions.get(wordtype.WI(), ""),
            cmd,
            answer,
            value,
            comment
        )
        self._logger.debug(response)
        return response

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
        """
        comment = ""
        try:
            answer = self._conn.exchange(cmd)
        except Exception:
            self._logger.error(format_exc())
            answer = _UNKNOWNERROR
            comment = "EXCHANGE"

        response = GsiOnlineResponse(
            desc,
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
        response = self.request(cmd, "Beep")
        return response

    def wakeup(self) -> GsiOnlineResponse[bool]:
        """
        Wakes up the instrument.

        Returns
        -------
        GsiOnlineResponse
            Success of the execution.
        """
        response = self.request("a", "Wakeup")
        # It's better to wait one more second for the wakeup to finish,
        # otherwise the instrument may freeze up if the next command is
        # instantly executed.
        sleep(1)
        self._logger.info("Attempting wakeup")
        return response

    def shutdown(self) -> GsiOnlineResponse[bool]:
        """
        Shuts down the instrument.

        Returns
        -------
        GsiOnlineResponse
            Success of the execution.
        """
        # It's better to wait a second after the last command before starting
        # the shutdown. Quick wakeup-cmd-shutdown cycles can freez up the
        # instrument, which can only be solved by physically disconnecting
        # the power.
        sleep(1)
        self._logger.info("Shutting down")
        response = self.request("b", "Shutdown")
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
        response = self.request("c", "Clear")
        return response
