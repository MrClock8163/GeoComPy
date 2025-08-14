"""
Description
===========

Module: ``geocompy.geo``

The ``geo`` package provides wrapper methods for all GeoCom RPC functions
available on supported instruments running various versions of the TPS
system software, or software based on the TPS system.

Types
-----

- ``GeoCom``

Submodules
----------

- ``geocompy.geo.gcdata``
- ``geocompy.geo.gctypes``
- ``geocompy.geo.aus``
- ``geocompy.geo.aut``
- ``geocompy.geo.bap``
- ``geocompy.geo.bmm``
- ``geocompy.geo.cam``
- ``geocompy.geo.com``
- ``geocompy.geo.csv``
- ``geocompy.geo.ctl``
- ``geocompy.geo.dna``
- ``geocompy.geo.edm``
- ``geocompy.geo.ftr``
- ``geocompy.geo.img``
- ``geocompy.geo.kdm``
- ``geocompy.geo.mot``
- ``geocompy.geo.sup``
- ``geocompy.geo.tmc``
- ``geocompy.geo.wir``
"""
import re
from logging import Logger
from traceback import format_exc
from time import sleep
from typing import Any, Callable, Iterable, overload, TypeVar

from serial import SerialException, SerialTimeoutException

from geocompy.data import Angle, Byte
from geocompy.communication import Connection, DUMMYLOGGER
from .gctypes import (
    GeoComCode,
    GeoComResponse,
    GeoComType,
    rpcnames
)
from .aus import GeoComAUS
from .aut import GeoComAUT
from .bap import GeoComBAP
from .bmm import GeoComBMM
from .cam import GeoComCAM
from .com import GeoComCOM
from .csv import GeoComCSV
from .ctl import GeoComCTL
from .dna import GeoComDNA
from .edm import GeoComEDM
from .ftr import GeoComFTR
from .img import GeoComIMG
from .kdm import GeoComKDM
from .mot import GeoComMOT
from .sup import GeoComSUP
from .tmc import GeoComTMC
from .wir import GeoComWIR


_T = TypeVar("_T")
_MAX_TRANSACTION = 2**15


class GeoCom(GeoComType):
    """
    GeoCom protocol handler.

    The individual commands are available through their respective
    subsystems.

    Examples
    --------

    Opening a simple serial connection:

    >>> from geocompy.communication import open_serial
    >>> from geocompy.geo import GeoCom
    >>>
    >>> with open_serial("COM1") as line:
    ...     tps = GeoCom(line)
    ...     tps.com.nullprocess()
    ...
    >>>

    Passing a logger:

    >>> from sys import stdout
    >>> from logging import getLogger, DEBUG, StreamHandler
    >>>
    >>> from geocompy.communication import open_serial
    >>> from geocompy.geo import GeoCom
    >>>
    >>> logger = getLogger("TPS")
    >>> logger.addHandler(StreamHandler(stdout))
    >>> logger.setLevel(DEBUG)
    >>> with open_serial("COM1") as line:
    ...     tps = GeoCom(line, logger)
    ...     tps.com.nullprocess()
    ...
    >>>
    GeoComResponse(COM_NullProc) ... # Startup connection test
    GeoComResponse(COM_GetDoublePrecision) ... # Precision sync
    GeoComResponse(COM_NullProc) ... # First executed command
    """
    _R1P: re.Pattern[str] = re.compile(
        r"^%R1P,"
        r"(?P<comrc>\d+),"
        r"(?P<tr>\d+):"
        r"(?P<rc>\d+)"
        r"(?:,(?P<params>.*))?$"
    )

    def __init__(
        self,
        connection: Connection,
        logger: Logger | None = None,
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
            Connection to use for communication
            (usually a serial connection).
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
        self.transaction_counter = 0
        """Number of command transactions started during the current
        session."""
        self._conn: Connection = connection
        if logger is None:
            logger = DUMMYLOGGER
        self._logger: Logger = logger
        self.precision = 15

        self.aus: GeoComAUS = GeoComAUS(self)
        """
        Alt User subsystem.

        .. versionadded:: GeoCom-TPS1100-1.04
        """
        self.aut: GeoComAUT = GeoComAUT(self)
        """Automation subsystem."""
        self.bap: GeoComBAP = GeoComBAP(self)
        """Basic applications subsystem."""
        self.bmm: GeoComBMM = GeoComBMM(self)
        """Basic man-machine interface subsystem."""
        self.cam: GeoComCAM = GeoComCAM(self)
        """
        Camera subsystem.

        .. versionadded:: GeoCom-VivaTPS
        """
        self.com: GeoComCOM = GeoComCOM(self)
        """Communications subsystem."""
        self.csv: GeoComCSV = GeoComCSV(self)
        """Central services subsystem."""
        self.ctl: GeoComCTL = GeoComCTL(self)
        """
        Control task subsystem.

        .. versionremoved:: GeoCom-TPS1200
        """
        self.dna: GeoComDNA = GeoComDNA(self)
        """
        Digital level subsystem.

        .. versionadded:: GeoCom-LS
        """
        self.edm: GeoComEDM = GeoComEDM(self)
        """Electronic distance measurement subsystem."""
        self.ftr: GeoComFTR = GeoComFTR(self)
        """
        File transfer subsystem.

        .. versionadded:: GeoCom-TPS1200
        """
        self.img: GeoComIMG = GeoComIMG(self)
        """
        Image processing subsystem.

        .. versionadded:: GeoCom-TPS1200
        """
        self.kdm: GeoComKDM = GeoComKDM(self)
        """
        Keyboard display unit subsystem.

        .. versionadded:: GeoCom-VivaTPS
        """
        self.mot: GeoComMOT = GeoComMOT(self)
        """Motorization subsytem."""
        self.sup: GeoComSUP = GeoComSUP(self)
        """Supervisor subsystem."""
        self.tmc: GeoComTMC = GeoComTMC(self)
        """Theodolite measurement and calculation subsystem."""
        self.wir: GeoComWIR = GeoComWIR(self)
        """
        Word Index registration subsystem.

        .. versionremoved:: GeoCom-TPS1200
        """

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

        resp = self.com.get_double_precision()
        if resp.params is not None:
            self.precision = resp.params
            self._logger.info(f"Synced double precision: {self.precision}")
        else:
            self._logger.error(
                f"Could not syncronize double precision, "
                f"defaulting to {self.precision:d}"
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

    @property
    def precision(self) -> int:
        """Decimal precision in serial communication."""
        return self._precision

    @precision.setter
    def precision(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"Precision must be a number not '{type(value)}'")

        self._precision = value

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
    ) -> GeoComResponse[tuple[Any, ...]]: ...

    def request(
        self,
        rpc: int,
        params: Iterable[int | float | bool | str | Angle | Byte] = (),
        parsers: (
            Iterable[Callable[[str], Any]]
            | Callable[[str], Any]
            | None
        ) = None
    ) -> GeoComResponse[Any]:
        """
        Executes an RPC request and returns the parsed GeoCom response.

        Constructs a request(from the given RPC code and parameters),
        writes it to the serial line, then reads the response. The
        response is then parsed using the provided parser functions.

        Parameters
        ----------
        rpc: int
            Number of the RPC to execute.
        params: Iterable[int | float | bool | str | Angle | Byte]
            Parameters for the request, by default()
        parsers: Iterable[Callable[[str], Any]] \
                  | Callable[[str], Any] \
                  | None, optional
            Parser functions for the values in the RPC response,
            by default None

        Returns
        -------
        GeoComResponse
            Parsed return codes and parameters from the RPC response.

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

        trid = self.transaction_counter % _MAX_TRANSACTION
        self.transaction_counter += 1
        cmd = f"%R1Q,{rpc},{trid}:{','.join(strparams)}"
        try:
            answer = self._conn.exchange(cmd)
        except SerialTimeoutException:
            self._logger.error(format_exc())
            answer = (
                f"%R1P,{GeoComCode.COM_TIMEDOUT:d},"
                f"{trid}:{GeoComCode.OK:d}"
            )
        except SerialException:
            self._logger.error(format_exc())
            answer = (
                f"%R1P,{GeoComCode.COM_CANT_SEND:d},"
                f"{trid}:{GeoComCode.OK:d}"
            )
        except Exception:
            self._logger.error(format_exc())
            answer = (
                f"%R1P,{GeoComCode.COM_FAILED:d},"
                f"{trid}:{GeoComCode.OK:d}"
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
    ) -> GeoComResponse[tuple[Any, ...]]: ...

    def parse_response(
        self,
        cmd: str,
        response: str,
        parsers: (
            Iterable[Callable[[str], Any]]
            | Callable[[str], Any]
            | None
        ) = None
    ) -> GeoComResponse[Any]:
        """
        Parses RPC response and constructs `GeoComResponse` instance.

        Parameters
        ----------
        cmd: str
            Full, serialized request, that invoked the response.
        response: str
            Full, received response.
        parsers: Iterable[Callable[[str], Any]] \
                  | Callable[[str], Any] \
                  | None, optional
            Parser functions for the values in the RPC response,
            by default None

        Returns
        -------
        GeoComResponse
            Parsed return codes and parameters from the RPC response.

        """
        m = self._R1P.match(response)
        rpc = int(cmd.split(":")[0].split(",")[1])
        trid_expected = int(cmd.split(":")[0].split(",")[2])
        rpcname = rpcnames.get(rpc, str(rpc))
        if not m:
            return GeoComResponse(
                rpcname,
                cmd,
                response,
                GeoComCode.COM_CANT_DECODE,
                GeoComCode.OK,
                0
            )

        groups = m.groupdict()
        trid = int(groups.get("tr", "-1"))
        if trid != trid_expected:
            return GeoComResponse(
                rpcname,
                cmd,
                response,
                GeoComCode.COM_TR_ID_MISMATCH,
                GeoComCode.OK,
                trid
            )

        try:
            comrc = GeoComCode(int(groups["comrc"]))
        except Exception:
            comrc = GeoComCode.UNDEFINED

        try:
            rc = GeoComCode(int(groups["rc"]))
        except Exception:
            rc = GeoComCode.UNDEFINED

        values = groups.get("params", "")
        if values is None:
            values = ""

        if values == "":
            return GeoComResponse(
                rpcname,
                cmd,
                response,
                comrc,
                rc,
                trid
            )

        if parsers is None:
            parsers = ()
        elif not isinstance(parsers, Iterable):
            parsers = (parsers,)

        params: list[Any] = []
        try:
            for func, value in zip(parsers, values.split(",")):
                params.append(func(value))
        except Exception:
            return GeoComResponse(
                rpcname,
                cmd,
                response,
                GeoComCode.COM_CANT_DECODE,
                GeoComCode.OK,
                0
            )

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

    def abort(self) -> GeoComResponse[None]:
        """
        Aborts the current motorized function.

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``UNDEFINED``: The command was accepted, but the response
                  indicated failed execution. Possibly nothing to abort.
                - ``COM_FAILED``: The abort command could not be sent due
                  to a communication issue.

        Note
        ----
        The abort command does not actually use the GeoCom syntax, but the
        function returns a `GeoComResponse` anyway, in order to maintain
        the uniformity with the rest of the commands.
        """
        cmd = "c"
        try:
            ans = self._conn.exchange(cmd)
            rpccode = GeoComCode.OK if ans == "?" else GeoComCode.UNDEFINED
            comcode = GeoComCode.OK
        except Exception:
            ans = ""
            rpccode = GeoComCode.OK
            comcode = GeoComCode.COM_FAILED

        return GeoComResponse(
            "Abort",
            cmd,
            ans,
            comcode,
            rpccode,
            0
        )
