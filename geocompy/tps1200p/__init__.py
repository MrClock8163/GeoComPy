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
from .grc import TPS1200PGRC


class TPS1200P(GeoComProtocol):
    RESPPAT: re.Pattern = re.compile(
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
        super().__init__(connection, logger)
        self.aus = TPS1200PAUS(self)
        self.aut = TPS1200PAUT(self)
        self.bap = TPS1200PBAP(self)
        self.bmm = TPS1200PBMM(self)
        self.com = TPS1200PCOM(self)
        self.csv = TPS1200PCSV(self)
        self.edm = TPS1200PEDM(self)
        self.ftr = TPS1200PFTR(self)
        self.img = TPS1200PIMG(self)
        self.mot = TPS1200PMOT(self)
        self.sup = TPS1200PSUP(self)
        self.tmc = TPS1200PTMC(self)

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
        return self.request(
            108,
            parsers={"digits": int}
        )

    def set_double_precision(
        self,
        digits: int
    ) -> GeoComResponse:
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

        cmd = f"%R1Q,{rpc}:{",".join(strparams)}"
        try:
            answer = self._conn.exchange1(cmd)
        except SerialTimeoutException as e:
            self.logger.error(format_exc())
            answer = (
                f"%R1P,{TPS1200PGRC.COM_TIMEOUT.value:d},"
                f"0:{TPS1200PGRC.FATAL.value:d}"
            )
        except SerialException as e:
            self.logger.error(format_exc())
            answer = (
                f"%R1P,{TPS1200PGRC.COM_CANT_SEND.value:d},"
                f"0:{TPS1200PGRC.FATAL.value:d}"
            )
        except Exception as e:
            self.logger.error(format_exc())
            answer = (
                f"%R1P,{TPS1200PGRC.FATAL.value:d},"
                f"0:{TPS1200PGRC.FATAL.value:d}"
            )

        response = self.parse_response(
            cmd,
            answer,
            parsers if parsers is not None else {}
        )
        self.logger.debug(response)
        return response

    def parse_response(
        self,
        cmd: str,
        reply: str,
        args: dict[str, Callable[[str], Any]]
    ) -> GeoComResponse:
        m = self.RESPPAT.match(reply)
        if not m:
            return GeoComResponse(
                cmd,
                reply,
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
            for (name, func), value in zip(args.items(), values.split(",")):
                params[name] = func(value)
        except:
            return GeoComResponse(
                cmd,
                reply,
                TPS1200PGRC.COM_CANT_DECODE,
                TPS1200PGRC.UNDEFINED,
                0,
                {}
            )

        comrc = TPS1200PGRC(int(groups["comrc"]))
        rc = TPS1200PGRC(int(groups["rc"]))
        return GeoComResponse(
            cmd,
            reply,
            comrc,
            rc,
            int(groups["tr"]),
            params
        )
