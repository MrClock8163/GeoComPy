"""
``geocompy.tps1200p``
=====================

The ``tps1200p`` package provides wrapper methods for all GeoCom RPC
functions available on an instrument running the TPS1200+ system software.

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

import re
import logging
from time import sleep
from traceback import format_exc
from typing import Callable, Iterable, Any

from serial import SerialException, SerialTimeoutException

from .. import (
    GeoComProtocol,
    GeoComResponse
)
from ..data import (
    Angle,
    Byte
)
from ..communication import Connection
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

    >>> from serial import Serial
    >>> from geocompy.communication import SerialConnection
    >>> from geocompy.tps1200p import TPS1200P
    >>>
    >>> port = Serial("COM4", timeout=15)
    >>> with SerialConnection(port) as line:
    ...     tps = TPS1200P(line)
    ...     tps.com.nullproc()
    ...
    >>>

    Passing a logger:

    >>> from logging import Logger, StreamHandler, DEBUG
    >>> from serial import Serial
    >>> from geocompy.communication import SerialConnection
    >>> from geocompy.tps1200p import TPS1200P
    >>>
    >>> log = Logger("stdout", DEBUG)
    >>> log.addHandler(StreamHandler())
    >>> port = Serial("COM4", timeout=15)
    >>> with SerialConnection(port) as line:
    ...     tps = TPS1200P(line, log)
    ...     tps.com.nullproc()
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
            self._conn.send("\n")
            response = self.com.nullproc()
            if response.comcode and response.rpccode:
                break

            sleep(1)
        else:
            raise ConnectionError(
                "could not establish connection to instrument"
            )

        self._precision = 15
        resp = self.get_double_precision()
        if resp.comcode and resp.rpccode:
            self._precision = resp.params["digits"]

    def get_double_precision(self) -> GeoComResponse:
        """
        RPC 108, ``COM_GetDoublePrecision``

        Gets the current ASCII communication floating point precision of
        the instrument.

        Returns
        -------
        GeoComResponse
            - Params:
                - **digits** (`int`): Floating point decimal places.

        See Also
        --------
        set_double_precision
        """
        return self.request(
            108,
            parsers={"digits": int}
        )

    def set_double_precision(
        self,
        digits: int
    ) -> GeoComResponse:
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
        response = self.request(107, [digits])
        if response.comcode and response.rpccode:
            self._precision = digits
        return response

    def request(
        self,
        rpc: int,
        params: Iterable[int | float | bool | str | Angle | Byte] = [],
        parsers: dict[str, Callable[[str], Any]] | None = None
    ) -> GeoComResponse:
        """
        Executes a TPS1200+ RPC request and returns the parsed GeoCom
        response.

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
        TypeError
            If the passed parameters contained an unexpected type.

        Notes
        -----
        If a :class:`~serial.SerialTimeoutException` occurs during the
        request, a response with :attr:`~grc.TPS1200PGRC.COM_TIMEDOUT`
        and :attr:`~grc.TPS1200PGRC.FATAL` codes is returned.

        If a :class:`~serial.SerialException` occurs during the requrest,
        a response with :attr:`~grc.TPS1200PGRC.COM_CANT_SEND` and
        :attr:`~grc.TPS1200PGRC.FATAL` codes is returned.

        If an unknown :class:`Exception` occurs during the request, a
        response with :attr:`~grc.TPS1200PGRC.FATAL` and
        :attr:`~grc.TPS1200PGRC.FATAL` codes is returned.

        Examples
        --------

        Executing a command without input or output parameters:

        >>> ts # Instantiated TPS1200P
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
            answer = self._conn.exchange1(cmd)
        except SerialTimeoutException:
            self._logger.error(format_exc())
            answer = (
                f"%R1P,{TPS1200PGRC.COM_TIMEDOUT.value:d},"
                f"0:{TPS1200PGRC.FATAL.value:d}"
            )
        except SerialException:
            self._logger.error(format_exc())
            answer = (
                f"%R1P,{TPS1200PGRC.COM_CANT_SEND.value:d},"
                f"0:{TPS1200PGRC.FATAL.value:d}"
            )
        except Exception:
            self._logger.error(format_exc())
            answer = (
                f"%R1P,{TPS1200PGRC.FATAL.value:d},"
                f"0:{TPS1200PGRC.FATAL.value:d}"
            )

        response = self.parse_response(
            cmd,
            answer,
            parsers if parsers is not None else {}
        )
        self._logger.debug(response)
        return response

    def parse_response(
        self,
        cmd: str,
        response: str,
        parsers: dict[str, Callable[[str], Any]]
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
        parsers : dict[str, Callable[[str], Any]]
            Parser functions for the values in the RPC response.
            (Maps the parser functions to the names of the parameters.)

        Returns
        -------
        GeoComResponse
            Parsed return codes and parameters from the RPC response.

        Notes
        -----
        If the response does not match the expected pattern, or an
        :class:`Exception` occurs during parsing, a response with
        :attr:`~grc.TPS1200PGRC.COM_CANT_DECODE` and
        :attr:`~grc.TPS1200PGRC.UNDEFINED` codes is returned.
        """
        m = self._RESPPAT.match(response)
        rpc = int(cmd.split(":")[0].split(",")[1])
        rpcname = rpcnames.get(rpc, str(rpc))
        if not m:
            return GeoComResponse(
                rpcname,
                cmd,
                response,
                TPS1200PGRC.COM_CANT_DECODE,
                TPS1200PGRC.UNDEFINED,
                0,
                {}
            )

        groups = m.groupdict()
        values = groups.get("params", "")
        if values is None:
            values = ""
        params: dict = {}
        try:
            for (name, func), value in zip(parsers.items(), values.split(",")):
                params[name] = func(value)
        except Exception:
            return GeoComResponse(
                rpcname,
                cmd,
                response,
                TPS1200PGRC.COM_CANT_DECODE,
                TPS1200PGRC.UNDEFINED,
                0,
                {}
            )

        comrc = TPS1200PGRC(int(groups["comrc"]))
        rc = TPS1200PGRC(int(groups["rc"]))
        return GeoComResponse(
            rpcname,
            cmd,
            response,
            comrc,
            rc,
            int(groups["tr"]),
            params
        )
