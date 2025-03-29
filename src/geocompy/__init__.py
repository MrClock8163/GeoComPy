from __future__ import annotations

from enum import Enum
from typing import Callable, Any, Iterable
from logging import Logger, NullHandler

from ._version import __version__
from .data import Angle, Byte
from .communication import Connection


class GeoComReturnCode(Enum):
    pass


class GeoComResponse:
    def __init__(
        self,
        rpcname: str,
        cmd: str,
        response: str,
        comcode: GeoComReturnCode,
        rpccode: GeoComReturnCode,
        trans: int,
        params: dict[str, Any]
    ):
        self.rpcname: str = rpcname
        self.cmd: str = cmd
        self.response: str = response
        self.comcode: GeoComReturnCode = comcode
        self.rpccode: GeoComReturnCode = rpccode
        self.trans: int = trans
        self.params: dict[str, Any] = params

    def __str__(self) -> str:
        return (
            f"GeoComResponse({self.rpcname}) com: {self.comcode.name:s}, "
            f"rpc: {self.rpccode.name:s}, "
            f"tr: {self.trans:d}, "
            f"params: {self.params}, "
            f"(cmd: '{self.cmd}', response: '{self.response}')"
        )

    def __bool__(self) -> bool:
        return bool(self.comcode) and bool(self.rpccode)


class GeoComSubsystem:
    def __init__(self, parent: GeoComProtocol):
        self._parent: GeoComProtocol = parent
        self._request = self._parent.request


class GeoComProtocol:
    def __init__(
        self,
        connection: Connection,
        logger: Logger | None = None
    ):
        self._conn: Connection = connection
        if logger is None:
            logger = Logger("/dev/null")
            logger.addHandler(NullHandler())
        self.logger: Logger = logger

    def request(
        self,
        rpc: int,
        params: Iterable[int | float | bool | str | Angle | Byte] = [],
        parsers: dict[str, Callable[[str], Any]] | None = None
    ) -> GeoComResponse:
        raise NotImplementedError()

    def parse_response(
        cls,
        cmd: str,
        response: str,
        args: dict[str, Callable[[str], Any]]
    ) -> GeoComResponse:
        raise NotImplementedError()


class GsiOnlineProtocol:
    def __init__(
        self,
        connection: Connection,
        logger: Logger | None = None
    ):
        self._conn: Connection = connection
        if logger is None:
            logger = Logger("/dev/null")
            logger.addHandler(NullHandler())
        self.logger: Logger = logger
    
    def set(
        self,
        spec: int,
        param: int
    ):  
        cmd = f"SET/{spec:d}/{param:d}"
        self._conn.exchange1(cmd)

    def conf(
        self,
        spec: int
    ):
        cmd = f"CONF/{spec:d}"
        response = self._conn.exchange1(cmd)
