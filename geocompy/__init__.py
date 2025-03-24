from __future__ import annotations

from enum import Enum
from typing import Callable, Any

from .communication import Connection


class GeoComReturnCode(Enum):
    pass


class GeoComResponse:
    def __init__(
        self,
        cmd: str,
        response: str,
        comcode: GeoComReturnCode,
        rpccode: GeoComReturnCode,
        trans: int,
        params: dict
    ):
        self.cmd: str = cmd
        self.response: str = response
        self.comcode: GeoComReturnCode = comcode
        self.rpccode: GeoComReturnCode = rpccode
        self.trans: int = trans
        self.params: dict = params

    def __str__(self) -> str:
        return (
            f"GeoComResponse com: {self.comcode.name:s}, "
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


class GeoComProtocol:
    def __init__(self, connection: Connection):
        self._conn: Connection = connection

    def exec1(
        self,
        cmd: str,
        args: dict[str, Callable[[str], Any]] | None = None
    ) -> GeoComResponse:
        raise NotImplementedError()

    def parse_reply(
        cls,
        cmd: str,
        response: str,
        args: dict[str, Callable[[str], Any]]
    ) -> GeoComResponse:
        raise NotImplementedError()
