from geocompy.communication import Connection


def faulty_parser(value: str) -> int:
    raise Exception()


class FaultyConnection(Connection):
    def send(self, value: str) -> None:
        pass

    def receive(self) -> str:
        return ""

    def exchange(self, value: str) -> str:
        return ""

    def reset(self) -> None:
        return

    def close(self) -> None:
        pass

    def is_open(self) -> bool:
        return True
