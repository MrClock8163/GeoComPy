from geocompy.communication import Connection


def faulty_parser(value: str) -> int:
    raise Exception()


class FaultyConnection(Connection):
    def send_binary(self, data: bytes) -> None:
        pass

    def send(self, value: str) -> None:
        pass

    def receive_binary(self) -> bytes:
        return b""

    def receive(self) -> str:
        return ""

    def exchange_binary(self, data: bytes) -> bytes:
        return b""

    def exchange(self, value: str) -> str:
        return ""

    def reset(self) -> None:
        return

    def close(self) -> None:
        pass

    def is_open(self) -> bool:
        return True
