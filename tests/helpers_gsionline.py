import re

from geocompy.communication import Connection
from geocompy.data import gsiword
from geocompy.gsi.gsitypes import GsiOnlineType

from helpers import faulty_parser


def gsiparser(value: str) -> int:
    value = value.strip("* ")
    return int(value[6:])


class DummyGsiOnlineConnection(Connection):
    _CONF = re.compile(r"^CONF/\d+$")
    _SET = re.compile(r"^SET/\d+/\d+$")
    _GET = re.compile(r"^GET/[M,I,C]/WI\d+$")
    _PUT = re.compile(
        r"^PUT/"
        r"\*?"
        r"(?:[0-9\.]{6})"
        r"(?:\+|\-)"
        r"(?:[a-zA-Z0-9]{8}|[a-zA-Z0-9]{16}) $"
    )

    def __init__(self, gsi16: bool = False):
        self._gsi16 = gsi16

    def send(self, value: str) -> None:
        pass

    def receive(self) -> str:
        return ""

    def exchange(self, cmd: str) -> str:
        if self._CONF.match(cmd) and cmd != "CONF/0":
            if cmd == "CONF/137":
                return f"0137/{self._gsi16:04d}"
            return f"{cmd.split('/')[1].zfill(4)}/0000"
        elif self._SET.match(cmd) and cmd != "SET/0/0":
            return "?"
        elif self._GET.match(cmd) and cmd != "GET/I/WI0":
            wi = int(cmd.split("/")[-1].removeprefix("WI"))
            word = gsiword(
                wi,
                "1",
                gsi16=self._gsi16
            )

            return word
        elif self._PUT.match(cmd) and cmd != "PUT/0.....+00000000 ":
            return "?"
        elif cmd in ("a", "b", "c", "BEEP/0", "BEEP/1", "BEEP/2"):
            return "?"

        return "@W427"

    def reset(self) -> None:
        pass

    def close(self) -> None:
        pass

    def is_open(self) -> bool:
        return True


class GsiOnlineTester:
    @staticmethod
    def test_request(instrument: GsiOnlineType) -> None:
        response = instrument.request("d")
        assert not response.value
        response = instrument.request("a")
        assert response.value

    @staticmethod
    def test_setrequest(instrument: GsiOnlineType) -> None:
        response = instrument.setrequest(0, 0)
        assert not response.value
        assert response.comment == "INSTRUMENT"
        assert response.response == "@W427"

        response = instrument.setrequest(1, 1)
        assert response.value

    @staticmethod
    def test_confrequest(instrument: GsiOnlineType) -> None:
        response = instrument.confrequest(0, int)
        assert not response.value
        assert response.comment == "INSTRUMENT"
        assert response.response == "@W427"

        response = instrument.confrequest(1, faulty_parser)
        assert response.value is None
        assert response.comment == "PARSE"

        response = instrument.confrequest(1, int)
        assert response.comment == ""
        assert response.response == "0001/0000"
        assert response.value == 0

    @staticmethod
    def test_putrequest(instrument: GsiOnlineType) -> None:
        response = instrument.putrequest(0, "0.....+00000000 ")
        assert not response.value
        assert response.comment == "INSTRUMENT"
        assert response.response == "@W427"

        response = instrument.putrequest(1, "1.....+00000001 ")
        assert response.value

    @staticmethod
    def test_getrequest(instrument: GsiOnlineType) -> None:
        response = instrument.getrequest("I", 0, int)
        assert response.value is None
        assert response.response == "@W427"

        response = instrument.getrequest("I", 1, faulty_parser)
        assert response.value is None
        assert response.comment == "PARSE"

        response = instrument.getrequest("I", 1, gsiparser)
        assert response.value == 1
