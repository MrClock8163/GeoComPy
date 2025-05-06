"""
Description
===========

Module: ``geocompy.tps1000``

The ``tps1000`` package provides wrapper methods for all GeoCom RPC
functions available on an instrument running the TPS1000 system software.

Types
-----

- ``TPS1000``

Submodules
----------

- ``geocompy.tps1000.rc``
- ``geocompy.tps1000.aut``
- ``geocompy.tps1000.com``
- ``geocompy.tps1000.csv``
- ``geocompy.tps1000.ctl``
- ``geocompy.tps1000.edm``
- ``geocompy.tps1000.mot``
- ``geocompy.tps1000.sup``
- ``geocompy.tps1000.tmc``
- ``geocompy.tps1000.wir``
"""
from __future__ import annotations

import re
import logging
from time import sleep
from typing import TypeVar

from ..communication import Connection
from ..protocols import (
    GeoComReturnCode,
    GeoComProtocol,
    GeoComResponse
)
from .aut import TPS1000AUT
from .bap import TPS1000BAP
from .bmm import TPS1000BMM
from .csv import TPS1000CSV
from .com import TPS1000COM
from .ctl import TPS1000CTL
from .edm import TPS1000EDM
from .mot import TPS1000MOT
from .sup import TPS1000SUP
from .tmc import TPS1000TMC
from .wir import TPS1000WIR
from .rc import TPS1000RC, rpcnames


_T = TypeVar("_T")


class TPS1000(GeoComProtocol):
    """
    TPS1000 GeoCom protocol handler.

    The individual commands are available through their respective
    subsystems.

    Examples
    --------

    Opening a simple serial connection:

    >>> from geocompy.communication import open_serial
    >>> from geocompy.tps1000 import TPS1000
    >>>
    >>> with open_serial("COM1") as line:
    ...     tps = TPS1000(line)
    ...     tps.com.nullprocess()
    ...
    >>>

    Passing a logger:

    >>> from logging import DEBUG
    >>> from geocompy.communication import open_serial, get_logger
    >>> from geocompy.tps1000 import TPS1000
    >>>
    >>> log = get_logger("Viva", "stdout", DEBUG)
    >>> with open_serial("COM1") as line:
    ...     tps = TPS1000(line, log)
    ...     tps.com.nullprocess()
    ...
    >>>
    GeoComResponse(COM_NullProc) ... # Startup connection test
    GeoComResponse(COM_GetDoublePrecision) ... # Precision sync
    GeoComResponse(COM_NullProc) ... # First executed command
    """
    _RESPPAT: re.Pattern = re.compile(
        r"^%R1P,"
        r"(?P<comrc>\d+),"
        r"(?P<tr>\d+):"
        r"(?P<rc>\d+)"
        r"(?:,(?P<params>.*))?$"
    )
    _RPCNAMES: dict[int, str] = rpcnames
    _CODES: type[GeoComReturnCode] = TPS1000RC
    _OK: GeoComReturnCode = TPS1000RC.OK
    _FAILED: GeoComReturnCode = TPS1000RC.COM_FAILED
    _CANTDECODE: GeoComReturnCode = TPS1000RC.COM_CANT_DECODE
    _CANTSEND: GeoComReturnCode = TPS1000RC.COM_CANT_SEND
    _TIMEOUT: GeoComReturnCode = TPS1000RC.COM_TIMEDOUT
    _UNDEF: GeoComReturnCode = TPS1000RC.UNDEFINED

    REF_VERSION = (2, 20)
    """
    Major and minor version of the reference manual, that this
    implementation is based on.
    """
    REF_VERSION_STR = "2.20"
    """
    Version string of the reference manual, that this implementation is
    based on.
    """

    def __init__(
        self,
        connection: Connection,
        logger: logging.Logger | None = None,
        retry: int = 2
    ):
        """
        After the subsystems are initialized, the connection is tested by
        sending an ``LF`` character to clear the receiver buffer, then the
        ``COM_NullProc`` is executed. If the test fails, it is retried with
        one second delay. The test is attempted `retry` number of times.

        Parameters
        ----------
        connection : ~communication.Connection
            Connection to the TPS1200+ instrument.
            (usually :class:`~geocompy.communication.SerialConnection`).
        logger : ~logging.Logger | None, optional
            Logger to log all requests and responses, by default None
        retry : int, optional
            Number of retries at connection validation before giving up.

        Raises
        ------
        ConnectionError
            If the connection could not be verified in the specified
            number of retries.
        """
        super().__init__(connection, logger)
        self.aut: TPS1000AUT = TPS1000AUT(self)
        """Automation subsystem."""
        self.bap: TPS1000BAP = TPS1000BAP(self)
        """Basic applications subsystem."""
        self.bmm: TPS1000BMM = TPS1000BMM(self)
        """Basic man-machine interface subsystem."""
        self.com: TPS1000COM = TPS1000COM(self)
        """Communications subsystem."""
        self.csv: TPS1000CSV = TPS1000CSV(self)
        """Central services subsystem."""
        self.ctl: TPS1000CTL = TPS1000CTL(self)
        """Control task subsystem."""
        self.edm: TPS1000EDM = TPS1000EDM(self)
        """Electronic distance measurement subsystem."""
        self.mot: TPS1000MOT = TPS1000MOT(self)
        """Motorization subsytem."""
        self.sup: TPS1000SUP = TPS1000SUP(self)
        """Supervisor subsystem."""
        self.tmc: TPS1000TMC = TPS1000TMC(self)
        """Theodolite measurement and calculation subsystem."""
        self.wir: TPS1000WIR = TPS1000WIR(self)
        """Word Index registration subsystem."""

        for i in range(retry):
            try:
                self._conn.send("\n")
                if self.com.nullprocess():
                    sleep(1)
                    break
            except Exception:
                self._logger.exception("Exception during connection attempt")

            sleep(1)
        else:
            raise ConnectionError(
                "could not establish connection to instrument"
            )

        resp = self.get_double_precision()
        if resp.params is not None:
            self._precision = resp.params
            self._logger.info(f"Synced double precision: {self._precision}")
        else:
            self._logger.error(
                f"Could not syncronize double precision, "
                f"defaulting to {self._precision:d}"
            )

        self._logger.info("Connection initialized")
        name = self.csv.get_instrument_name().params or "Unknown"
        geocom = self.com.get_geocom_version().params or (0, 0, 0)
        firmware = self.csv.get_firmware_version().params or (0, 0, 0)
        self._logger.info(
            f"Instrument: {name} "
            f"(firmware: v{firmware[0]}.{firmware[1]}.{firmware[2]}, "
            f"geocom: v{geocom[0]}.{geocom[1]}.{geocom[2]})"
        )

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
        return self.request(
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
        response: GeoComResponse[None] = self.request(107, [digits])
        if not response.error:
            self._precision = digits
        return response
