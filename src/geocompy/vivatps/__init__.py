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

import re
import logging
from time import sleep
from traceback import format_exc
from typing import Callable, Iterable, Any, overload, TypeVar

from serial import SerialException, SerialTimeoutException

from ..data import (
    Angle,
    Byte
)
from ..communication import Connection
from ..protocols import (
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


_T = TypeVar("_T")


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
    _RESPPAT: re.Pattern = re.compile(
        r"^%R1P,"
        r"(?P<comrc>\d+),"
        r"(?P<tr>\d+)"
        r"(?:,(?P<chk>\d+))?:"
        r"(?P<rc>\d+)"
        r"(?:,(?P<params>.*))?$"
    )

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
        else:
            self._logger.error(
                f"Could not syncronize double precision, "
                f"defaulting to {self._precision:d}"
            )

        self._logger.info("Connection initialized")

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
        params: Iterable[int | float | bool | str | Angle | Byte] = [],
        parsers: (
            Iterable[Callable[[str], Any]]
            | Callable[[str], Any]
            | None
        ) = None
    ) -> GeoComResponse:
        """
        Executes a VivaTPS RPC request and returns the parsed GeoCom
        response.

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
        TypeError
            If the passed parameters contained an unexpected type.

        Notes
        -----
        If a :class:`~serial.SerialTimeoutException` occurs during the
        request, a response with :attr:`~grc.VivaTPSGRC.COM_TIMEDOUT`
        and :attr:`~grc.VivaTPSGRC.FATAL` codes is returned.

        If a :class:`~serial.SerialException` occurs during the requrest,
        a response with :attr:`~grc.VivaTPSGRC.COM_CANT_SEND` and
        :attr:`~grc.VivaTPSGRC.FATAL` codes is returned.

        If an unknown :class:`Exception` occurs during the request, a
        response with :attr:`~grc.VivaTPSGRC.FATAL` and
        :attr:`~grc.VivaTPSGRC.FATAL` codes is returned.

        Examples
        --------

        Executing a command without input or output parameters:

        >>> ts # Instantiated VivaTPS
        >>> ts.request(9013) # AUT_LockIn

        Query command with output:

        >>> ts.request(
        ...     9030, # AUT_GetFineAdjustMode
        ...     parsers={
        ...         "adjmode": ts.aut.ADJMODE.parse
        ...     }
        ... )

        Execute command with both input and output parameters:

        >>> ts.request(
        ...     2108, # TMC_GetSimpleMea
        ...     [5000, ts.tmc.INCLINEPRG.AUTO.value],
        ...     {
        ...         "hz": Angle.parse,
        ...         "v": Angle.parse,
        ...         "dist": float
        ...     }
        ... )

        """
        strparams: list[str] = []
        for item in params:
            match item:
                case Angle():
                    value = f"{round(float(item), self._precision):f}"
                    value = value.rstrip("0")
                    if value[-1] == ".":
                        value += "0"
                case Byte():
                    value = str(item)
                case float():
                    value = f"{round(item, self._precision):f}".rstrip("0")
                    if value[-1] == ".":
                        value += "0"
                case int():
                    value = f"{item:d}"
                case str():
                    value = f"\"{item}\""
                case _:
                    raise TypeError(f"unexpected parameter type: {type(item)}")

            strparams.append(value)

        cmd = f"%R1Q,{rpc}:{','.join(strparams)}"
        try:
            answer = self._conn.exchange(cmd)
        except SerialTimeoutException:
            self._logger.error(format_exc())
            answer = (
                f"%R1P,{VivaTPSGRC.COM_TIMEDOUT:d},"
                f"0:{VivaTPSGRC.OK:d}"
            )
        except SerialException:
            self._logger.error(format_exc())
            answer = (
                f"%R1P,{VivaTPSGRC.COM_CANT_SEND:d},"
                f"0:{VivaTPSGRC.OK:d}"
            )
        except Exception:
            self._logger.error(format_exc())
            answer = (
                f"%R1P,{VivaTPSGRC.COM_FAILED:d},"
                f"0:{VivaTPSGRC.OK:d}"
            )

        response = self.parse_response(
            cmd,
            answer,
            parsers
        )
        self._logger.debug(response)
        return response

    @overload
    def parse_response(
        self,
        cmd: str,
        response: str,
        parsers: Callable[[str], _T] | None = None
    ) -> GeoComResponse[_T]: ...

    @overload
    def parse_response(
        self,
        cmd: str,
        response: str,
        parsers: Iterable[Callable[[str], Any]] | None = None
    ) -> GeoComResponse[tuple]: ...

    def parse_response(
        self,
        cmd: str,
        response: str,
        parsers: (
            Iterable[Callable[[str], Any]]
            | Callable[[str], Any]
            | None
        ) = None
    ) -> GeoComResponse:
        """
        Parses RPC response and constructs GeoComResponse
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

        Notes
        -----
        If the response does not match the expected pattern, or an
        :class:`Exception` occurs during parsing, a response with
        :attr:`~grc.VivaTPSGRC.COM_CANT_DECODE` and
        :attr:`~grc.VivaTPSGRC.UNDEFINED` codes is returned.

        """
        m = self._RESPPAT.match(response)
        rpc = int(cmd.split(":")[0].split(",")[1])
        rpcname = rpcnames.get(rpc, str(rpc))
        if not m:
            return GeoComResponse(
                rpcname,
                cmd,
                response,
                VivaTPSGRC.COM_CANT_DECODE,
                VivaTPSGRC.OK,
                0
            )

        groups = m.groupdict()
        values = groups.get("params", "")
        if values is None:
            values = ""

        if parsers is None:
            parsers = ()
        elif not isinstance(parsers, Iterable):
            parsers = (parsers,)

        params: list = []
        try:
            for func, value in zip(parsers, values.split(",")):
                params.append(func(value))
        except Exception:
            return GeoComResponse(
                rpcname,
                cmd,
                response,
                VivaTPSGRC.COM_CANT_DECODE,
                VivaTPSGRC.OK,
                0
            )

        comrc = VivaTPSGRC(int(groups["comrc"]))
        rc = VivaTPSGRC(int(groups["rc"]))
        match len(params):
            case 0:
                params_final = None
            case 1:
                params_final = params[0]
            case _:
                params_final = tuple(params)

        return GeoComResponse(
            rpcname,
            cmd,
            response,
            comrc,
            rc,
            int(groups["tr"]),
            params_final
        )
