from __future__ import annotations

from types import TracebackType
from enum import Enum

from serial import Serial, SerialException, SerialTimeoutException


def parsestr(value: str) -> str:
    return value[1:-1]


def parsebyte(value: str) -> int:
    return int(value[1:-1], base=16)


def tostr(value: str) -> str:
    return f"\"{value:s}\""


def tobyte(value: int) -> str:
    return f"'{value:02X}'"


def toenum[T: type[Enum], R: Enum](typ: T, value: R | str):
    if isinstance(value, str):
        return typ._member_map_[value]

    return value


class Connection:
    def __init__(self, name: str = ""):
        self.name: str = name

    def is_open(self) -> bool:
        raise NotImplementedError("interface does not implement 'is_open'")

    def send(self, message: str):
        raise NotImplementedError("interface does not implement 'send'")

    def receive(self) -> str:
        raise NotImplementedError("interface does not implement 'receive'")

    def exchange(self, cmds: list[str]) -> list[str]:
        raise NotImplementedError("interface does not implement 'exchange'")

    def exchange1(self, cmd: str) -> str:
        raise NotImplementedError("interface does not implement 'exchange1'")


class SerialConnection(Connection):
    def __init__(
        self,
        port: Serial,
        *,
        eom: str = "\r\n",
        eoa: str = "\r\n"
    ):
        super().__init__("")

        self._port: Serial = port
        self.eom: str = eom  # end of message
        self.eoa: str = eoa  # end of answer

        if not self._port.is_open:
            self._port.open()

    def __del__(self):
        self._port.close()

    def __enter__(self) -> SerialConnection:
        return self

    def __exit__(
        self,
        exc_type: BaseException,
        exc_value: BaseException,
        exc_tb: TracebackType
    ):
        self._port.close()

    def close(self):
        self._port.close()

    def is_open(self):
        return self._port.is_open

    def send(self, message: str):
        if not self._port.is_open:
            raise SerialException(
                "serial port is not open"
            )

        if not message.endswith(self.eom):
            message += self.eom

        payload = message.encode('ascii', 'ignore')
        self._port.write(payload)

    def receive(self) -> str:
        if not self._port.is_open:
            raise SerialException(
                "serial port is not open"
            )

        eoabytes = self.eoa.encode("ascii")
        answer = self._port.read_until(eoabytes)
        if not answer.endswith(eoabytes):
            raise SerialTimeoutException("serial connection timed out on 'receive'")

        return answer.decode("ascii").removesuffix(self.eoa)

    def exchange(self, cmds: list[str]) -> list[str]:
        answers: list[str] = []
        for item in cmds:
            self.send(item)
            answers.append(self.receive())

        return answers

    def exchange1(self, cmd: str) -> str:
        self.send(cmd)
        return self.receive()
