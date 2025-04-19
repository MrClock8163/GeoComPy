import re

from geocompy.communication import Connection
from geocompy.data import gsiword
from geocompy.dna import DNA
from geocompy.dna.meta import DNAErrors

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

    def __init__(self, gsi16=False):
        super().__init__("")
        self._gsi16 = gsi16

    def exchange1(self, cmd: str) -> str:
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


class GsiOnlineTester:
    @staticmethod
    def test_request(dna: DNA):
        response = dna.request("d")
        assert not response.value
        response = dna.request("a")
        assert response.value == "1"

    @staticmethod
    def test_setrequest(dna: DNA):
        response = dna.setrequest(0, 0)
        assert not response.value
        assert response.comment == "INSTRUMENT"
        assert response.response == DNAErrors.W_INVCMD

        response = dna.setrequest(1, 1)
        assert response.value

    @staticmethod
    def test_confrequest(dna: DNA):
        response = dna.confrequest(0, int)
        assert not response.value
        assert response.comment == "INSTRUMENT"
        assert response.response == DNAErrors.W_INVCMD

        response = dna.confrequest(1, faulty_parser)
        assert response.value is None
        assert response.comment == "PARSE"

        response = dna.confrequest(1, int)
        assert response.comment == ""
        assert response.response == "0001/0000"
        assert response.value == 0

    @staticmethod
    def test_putrequest(dna: DNA):
        response = dna.putrequest(0, "0.....+00000000 ")
        assert not response.value
        assert response.comment == "INSTRUMENT"
        assert response.response == DNAErrors.W_INVCMD

        response = dna.putrequest(1, "1.....+00000001 ")
        assert response.value

    @staticmethod
    def test_getrequest(dna: DNA):
        response = dna.getrequest("I", 0, int)
        assert response.value is None
        assert response.response == DNAErrors.W_INVCMD

        response = dna.getrequest("I", 1, faulty_parser)
        assert response.value is None
        assert response.comment == "PARSE"

        response = dna.getrequest("I", 1, gsiparser)
        assert response.value == 1
