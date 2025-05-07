"""
Description
===========

Module: ``geocompy.tps1200p``

The ``tps1200p`` package provides wrapper methods for all GeoCom RPC
functions available on an instrument running the TPS1200(+) system software.

Types
-----

- ``TPS1200P``

Submodules
----------

- ``geocompy.tps1200p.grc``
- ``geocompy.tps1200p.aus``
- ``geocompy.tps1200p.aut``
- ``geocompy.tps1200p.bap``
- ``geocompy.tps1200p.bmm``
- ``geocompy.tps1200p.com``
- ``geocompy.tps1200p.csv``
- ``geocompy.tps1200p.edm``
- ``geocompy.tps1200p.ftr``
- ``geocompy.tps1200p.img``
- ``geocompy.tps1200p.mot``
- ``geocompy.tps1200p.sup``
- ``geocompy.tps1200p.tmc``
"""
from __future__ import annotations

import logging
from time import sleep

from ..communication import Connection
from ..protocols import (
    GeoComReturnCode,
    GeoComProtocol,
    GeoComResponse
)
from .aus import TPS1200PAUS
from .aut import TPS1200PAUT
from .bap import TPS1200PBAP
from .bmm import TPS1200PBMM
from .com import TPS1200PCOM
from .csv import TPS1200PCSV
from .edm import TPS1200PEDM
from .ftr import TPS1200PFTR
from .img import TPS1200PIMG
from .mot import TPS1200PMOT
from .sup import TPS1200PSUP
from .tmc import TPS1200PTMC
from .grc import TPS1200PGRC, rpcnames


class TPS1200P(GeoComProtocol):
    """
    TPS1200+ GeoCom protocol handler.

    The individual commands are available through their respective
    subsystems.

    Examples
    --------

    Opening a simple serial connection:

    >>> from geocompy.communication import open_serial
    >>> from geocompy.tps1200p import TPS1200P
    >>>
    >>> with open_serial("COM1") as line:
    ...     tps = TPS1200P(line)
    ...     tps.com.nullprocess()
    ...
    >>>

    Passing a logger:

    >>> from logging import DEBUG
    >>> from geocompy.communication import open_serial, get_logger
    >>> from geocompy.tps1200p import TPS1200P
    >>>
    >>> log = get_logger("Viva", "stdout", DEBUG)
    >>> with open_serial("COM1") as line:
    ...     tps = TPS1200P(line, log)
    ...     tps.com.nullprocess()
    ...
    >>>
    GeoComResponse(COM_NullProc) ... # Startup connection test
    GeoComResponse(COM_GetDoublePrecision) ... # Precision sync
    GeoComResponse(COM_NullProc) ... # First executed command
    """
    _RPCNAMES: dict[int, str] = rpcnames
    _CODES: type[GeoComReturnCode] = TPS1200PGRC
    _OK: GeoComReturnCode = TPS1200PGRC.OK
    _FAILED: GeoComReturnCode = TPS1200PGRC.COM_FAILED
    _CANTDECODE: GeoComReturnCode = TPS1200PGRC.COM_CANT_DECODE
    _CANTSEND: GeoComReturnCode = TPS1200PGRC.COM_CANT_SEND
    _TIMEOUT: GeoComReturnCode = TPS1200PGRC.COM_TIMEDOUT
    _UNDEF: GeoComReturnCode = TPS1200PGRC.UNDEFINED

    REF_VERSION = (1, 50)
    """
    Major and minor version of the reference manual, that this
    implementation is based on.
    """
    REF_VERSION_STR = "1.50"
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
        self.aus: TPS1200PAUS = TPS1200PAUS(self)
        """Alt User subsystem."""
        self.aut: TPS1200PAUT = TPS1200PAUT(self)
        """Automation subsystem."""
        self.bap: TPS1200PBAP = TPS1200PBAP(self)
        """Basic applications subsystem."""
        self.bmm: TPS1200PBMM = TPS1200PBMM(self)
        """Basic man-machine interface subsystem."""
        self.com: TPS1200PCOM = TPS1200PCOM(self)
        """Communications subsystem."""
        self.csv: TPS1200PCSV = TPS1200PCSV(self)
        """Central services subsystem."""
        self.edm: TPS1200PEDM = TPS1200PEDM(self)
        """Electronic distance measurement subsystem."""
        self.ftr: TPS1200PFTR = TPS1200PFTR(self)
        """File transfer subsystem."""
        self.img: TPS1200PIMG = TPS1200PIMG(self)
        """Image processing subsystem."""
        self.mot: TPS1200PMOT = TPS1200PMOT(self)
        """Motorization subsytem."""
        self.sup: TPS1200PSUP = TPS1200PSUP(self)
        """Supervisor subsystem."""
        self.tmc: TPS1200PTMC = TPS1200PTMC(self)
        """Theodolite measurement and calculation subsystem."""

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

        self._precision = 15
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
        digits : int
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
