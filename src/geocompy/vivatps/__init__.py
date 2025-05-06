"""
Description
===========

Module: ``geocompy.vivatps``

The ``vivatps`` package provides wrapper methods for all GeoCom RPC
functions available on an instrument running the Viva(/Nova)TPS system
software.

Types
-----

- ``VivaTPS``

Submodules
----------

- ``geocompy.vivatps.grc``
- ``geocompy.vivatps.aus``
- ``geocompy.vivatps.aut``
- ``geocompy.vivatps.bap``
- ``geocompy.vivatps.bmm``
- ``geocompy.vivatps.kdm``
- ``geocompy.vivatps.cam``
- ``geocompy.vivatps.com``
- ``geocompy.vivatps.csv``
- ``geocompy.vivatps.edm``
- ``geocompy.vivatps.ftr``
- ``geocompy.vivatps.img``
- ``geocompy.vivatps.mot``
- ``geocompy.vivatps.sup``
- ``geocompy.vivatps.tmc``

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
from .aus import VivaTPSAUS
from .aut import VivaTPSAUT
from .bap import VivaTPSBAP
from .bmm import VivaTPSBMM
from .kdm import VivaTPSKDM
from .cam import VivaTPSCAM
from .com import VivaTPSCOM
from .csv import VivaTPSCSV
from .edm import VivaTPSEDM
from .ftr import VivaTPSFTR
from .img import VivaTPSIMG
from .mot import VivaTPSMOT
from .sup import VivaTPSSUP
from .tmc import VivaTPSTMC
from .grc import VivaTPSGRC, rpcnames


class VivaTPS(GeoComProtocol):
    """
    VivaTPS GeoCom protocol handler.

    The individual commands are available through their respective
    subsystems.

    Examples
    --------

    Opening a simple serial connection:

    >>> from geocompy.communication import open_serial
    >>> from geocompy.vivatps import VivaTPS
    >>>
    >>> with open_serial("COM1") as line:
    ...     tps = VivaTPS(line)
    ...     tps.com.nullprocess()
    ...
    >>>

    Passing a logger:

    >>> from logging import DEBUG
    >>> from geocompy.communication import open_serial, get_logger
    >>> from geocompy.vivatps import VivaTPS
    >>>
    >>> log = get_logger("Viva", "stdout", DEBUG)
    >>> with open_serial("COM1") as line:
    ...     tps = VivaTPS(line, log)
    ...     tps.com.nullprocess()
    ...
    >>>
    GeoComResponse(COM_NullProc) ... # Startup connection test
    GeoComResponse(COM_GetDoublePrecision) ... # Precision sync
    GeoComResponse(COM_NullProc) ... # First executed command

    """
    _RPCNAMES: dict[int, str] = rpcnames
    _CODES: type[GeoComReturnCode] = VivaTPSGRC
    _OK: GeoComReturnCode = VivaTPSGRC.OK
    _FAILED: GeoComReturnCode = VivaTPSGRC.COM_FAILED
    _CANTDECODE: GeoComReturnCode = VivaTPSGRC.COM_CANT_DECODE
    _CANTSEND: GeoComReturnCode = VivaTPSGRC.COM_CANT_SEND
    _TIMEOUT: GeoComReturnCode = VivaTPSGRC.COM_TIMEDOUT
    _UNDEF: GeoComReturnCode = VivaTPSGRC.UNDEFINED

    REF_VERSION = (5, 51)
    """
    Major and minor version of the reference manual, that this
    implementation is based on.
    """
    REF_VERSION_STR = "5.51"
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
        connection : Connection
            Connection to the VivaTPS instrument.
            (usually :class:`~geocompy.communication.SerialConnection`).
        logger : Logger | None, optional
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

        self.aus: VivaTPSAUS = VivaTPSAUS(self)
        """Alt User subsystem."""
        self.aut: VivaTPSAUT = VivaTPSAUT(self)
        """Automation subsystem."""
        self.bap: VivaTPSBAP = VivaTPSBAP(self)
        """Basic applications subsystem."""
        self.bmm: VivaTPSBMM = VivaTPSBMM(self)
        """Basic man-machine interface subsystem."""
        self.kdm: VivaTPSKDM = VivaTPSKDM(self)
        """Keyboard display unit subsystem."""
        self.cam: VivaTPSCAM = VivaTPSCAM(self)
        """Camera subsystem."""
        self.com: VivaTPSCOM = VivaTPSCOM(self)
        """Communications subsystem."""
        self.csv: VivaTPSCSV = VivaTPSCSV(self)
        """Central services subsystem."""
        self.edm: VivaTPSEDM = VivaTPSEDM(self)
        """Electronic distance measurement subsystem."""
        self.ftr: VivaTPSFTR = VivaTPSFTR(self)
        """File transfer subsystem."""
        self.img: VivaTPSIMG = VivaTPSIMG(self)
        """Image processing subsystem."""
        self.mot: VivaTPSMOT = VivaTPSMOT(self)
        """Motorization subsytem."""
        self.sup: VivaTPSSUP = VivaTPSSUP(self)
        """Supervisor subsystem."""
        self.tmc: VivaTPSTMC = VivaTPSTMC(self)
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
