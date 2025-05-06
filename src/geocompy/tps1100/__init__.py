"""
Description
===========

Module: ``geocompy.tps1100``

The ``tps1100`` package provides wrapper methods for all GeoCom RPC
functions available on an instrument running the TPS1100 system software.

Types
-----

- ``TPS1100``

Submodules
----------

- ``geocompy.tps1100.rc``
- ``geocompy.tps1100.aus``
- ``geocompy.tps1100.aut``
- ``geocompy.tps1100.bap``
- ``geocompy.tps1100.bmm``
- ``geocompy.tps1100.com``
- ``geocompy.tps1100.csv``
- ``geocompy.tps1100.ctl``
- ``geocompy.tps1100.edm``
- ``geocompy.tps1100.mot``
- ``geocompy.tps1100.sup``
- ``geocompy.tps1100.tmc``
- ``geocompy.tps1100.wir``
"""
from __future__ import annotations

import logging
from time import sleep
from typing import TypeVar

from ..communication import Connection
from ..protocols import (
    GeoComReturnCode,
    GeoComProtocol,
    GeoComResponse
)
from .aus import TPS1100AUS
from .aut import TPS1100AUT
from .bap import TPS1100BAP
from .bmm import TPS1100BMM
from .com import TPS1100COM
from .csv import TPS1100CSV
from .ctl import TPS1100CTL
from .edm import TPS1100EDM
from .mot import TPS1100MOT
from .sup import TPS1100SUP
from .tmc import TPS1100TMC
from .wir import TPS1100WIR
from .rc import TPS1100RC, rpcnames


_T = TypeVar("_T")


class TPS1100(GeoComProtocol):
    """
    TPS1100 GeoCom protocol handler.

    The individual commands are available through their respective
    subsystems.

    Examples
    --------

    Opening a simple serial connection:

    >>> from geocompy.communication import open_serial
    >>> from geocompy.tps1100 import TPS1100
    >>>
    >>> with open_serial("COM1") as line:
    ...     tps = TPS1100(line)
    ...     tps.com.nullprocess()
    ...
    >>>

    Passing a logger:

    >>> from logging import DEBUG
    >>> from geocompy.communication import open_serial, get_logger
    >>> from geocompy.tps1100 import TPS1100
    >>>
    >>> log = get_logger("Viva", "stdout", DEBUG)
    >>> with open_serial("COM1") as line:
    ...     tps = TPS1100(line, log)
    ...     tps.com.nullprocess()
    ...
    >>>
    GeoComResponse(COM_NullProc) ... # Startup connection test
    GeoComResponse(COM_GetDoublePrecision) ... # Precision sync
    GeoComResponse(COM_NullProc) ... # First executed command
    """
    _RPCNAMES: dict[int, str] = rpcnames
    _CODES: type[GeoComReturnCode] = TPS1100RC
    _OK: GeoComReturnCode = TPS1100RC.OK
    _FAILED: GeoComReturnCode = TPS1100RC.COM_FAILED
    _CANTDECODE: GeoComReturnCode = TPS1100RC.COM_CANT_DECODE
    _CANTSEND: GeoComReturnCode = TPS1100RC.COM_CANT_SEND
    _TIMEOUT: GeoComReturnCode = TPS1100RC.COM_TIMEDOUT
    _UNDEF: GeoComReturnCode = TPS1100RC.UNDEFINED

    REF_VERSION = (1, 5)
    """
    Major and minor version of the reference manual, that this
    implementation is based on.
    """
    REF_VERSION_STR = "1.05"
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
        self.aus: TPS1100AUS = TPS1100AUS(self)
        """Alt User subsystem."""
        self.aut: TPS1100AUT = TPS1100AUT(self)
        """Automation subsystem."""
        self.bap: TPS1100BAP = TPS1100BAP(self)
        """Basic applications subsystem."""
        self.bmm: TPS1100BMM = TPS1100BMM(self)
        """Basic man-machine interface subsystem."""
        self.com: TPS1100COM = TPS1100COM(self)
        """Communications subsystem."""
        self.csv: TPS1100CSV = TPS1100CSV(self)
        """Central services subsystem."""
        self.ctl: TPS1100CTL = TPS1100CTL(self)
        """Control task subsystem."""
        self.edm: TPS1100EDM = TPS1100EDM(self)
        """Electronic distance measurement subsystem."""
        self.mot: TPS1100MOT = TPS1100MOT(self)
        """Motorization subsytem."""
        self.sup: TPS1100SUP = TPS1100SUP(self)
        """Supervisor subsystem."""
        self.tmc: TPS1100TMC = TPS1100TMC(self)
        """Theodolite measurement and calculation subsystem."""
        self.wir: TPS1100WIR = TPS1100WIR(self)
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
