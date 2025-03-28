from __future__ import annotations

import re
import logging
from time import sleep
from traceback import format_exc
from typing import Callable, Iterable, Any

from serial import SerialException, SerialTimeoutException

from ..communication import Connection
from .. import (
    GeoComProtocol,
    GeoComResponse
)
from ..data import (
    Angle,
    Byte
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
    RESPPAT: re.Pattern = re.compile(
        r"^%R1P,"
        r"(?P<comrc>\d+),"
        r"(?P<tr>\d+)"
        r"(?:,(?P<chk>\d+))?:"
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
        
        self.aus = VivaTPSAUS(self)
        self.aut = VivaTPSAUT(self)
        self.bap = VivaTPSBAP(self)
        self.bmm = VivaTPSBMM(self)
        self.kdm = VivaTPSKDM(self)
        self.cam = VivaTPSCAM(self)
        self.com = VivaTPSCOM(self)
        self.csv = VivaTPSCSV(self)
        self.edm = VivaTPSEDM(self)
        self.ftr = VivaTPSFTR(self)
        self.img = VivaTPSIMG(self)
        self.mot = VivaTPSMOT(self)
        self.sup = VivaTPSSUP(self)
        self.tmc = VivaTPSTMC(self)
        
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
                f"%R1P,{VivaTPSGRC.COM_TIMEDOUT.value:d},"
                f"0:{VivaTPSGRC.FATAL.value:d}"
            )
        except SerialException as e:
            self.logger.error(format_exc())
            answer = (
                f"%R1P,{VivaTPSGRC.COM_CANT_SEND.value:d},"
                f"0:{VivaTPSGRC.FATAL.value:d}"
            )
        except Exception as e:
            self.logger.error(format_exc())
            answer = (
                f"%R1P,{VivaTPSGRC.FATAL.value:d},"
                f"0:{VivaTPSGRC.FATAL.value:d}"
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
        rpc = int(cmd.split(":")[0].split(",")[1])
        rpcname = rpcnames.get(rpc, str(rpc))
        if not m:
            return GeoComResponse(
                rpcname,
                cmd,
                reply,
                VivaTPSGRC.COM_CANT_DECODE,
                VivaTPSGRC.UNDEFINED,
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
                rpcname,
                cmd,
                reply,
                VivaTPSGRC.COM_CANT_DECODE,
                VivaTPSGRC.UNDEFINED,
                0,
                {}
            )

        comrc = VivaTPSGRC(int(groups["comrc"]))
        rc = VivaTPSGRC(int(groups["rc"]))
        return GeoComResponse(
            rpcname,
            cmd,
            reply,
            comrc,
            rc,
            int(groups["tr"]),
            params
        )
