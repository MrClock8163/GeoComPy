from typing import Callable, Any, Iterable
import re

from geocompy.protocols import GeoComProtocol
from geocompy.communication import Connection
from geocompy.data import (
    Byte
)

from helpers import faulty_parser


class DummyGeoComConnection(Connection):
    _RESP = re.compile(
        r"^%R1P,"
        r"(?P<comrc>\d+),"
        r"(?P<tr>\d+):"
        r"(?P<rc>\d+)"
        r"(?:,(?P<params>.*))?$"
    )

    _CMD = re.compile(
        r"^%R1Q,"
        r"(?P<rpc>\d+):"
        r"(?:(?P<params>.*))?$"
    )

    def send(self, message: str) -> None:
        return

    def exchange(self, cmd: str) -> str:
        if not self._CMD.match(cmd):
            return "%R1P,0,0:2"

        if cmd == "%R1Q,5008:":
            return "%R1P,0,0:0,1996,'07','19','10','13','2f'"

        return "%R1P,0,0:0"


class GeoComTester:
    @staticmethod
    def test_parse_response(instrument: GeoComProtocol) -> None:
        cmd = "%R1Q,5008:"
        answer = "%R1P,0,0:0,1996,'07','19','10','13','2f'"
        parsers: Iterable[Callable[[str], Any]] = (
            int,
            Byte.parse,
            Byte.parse,
            Byte.parse,
            Byte.parse,
            Byte.parse
        )
        response = instrument.parse_response(
            cmd,
            answer,
            parsers
        )
        assert response.params is not None
        assert response.params[0] == 1996

        response = instrument.parse_response(
            cmd,
            "%R1P,1,0:",
            parsers
        )
        assert response.params is None

        parsers_faulty = (
            faulty_parser,
            Byte.parse,
            Byte.parse,
            Byte.parse,
            Byte.parse,
            Byte.parse
        )
        response = instrument.parse_response(
            cmd,
            answer,
            parsers_faulty
        )
        assert response.params is None

    @staticmethod
    def test_request(instrument: GeoComProtocol) -> None:
        response = instrument.request(
            5008,
            parsers=(
                int,
                Byte.parse,
                Byte.parse,
                Byte.parse,
                Byte.parse,
                Byte.parse
            )
        )
        assert response.params is not None
        assert response.params[0] == 1996

        response = instrument.request(
            1,
            (1, 2.0)
        )
        assert response.cmd == "%R1Q,1:1,2.0"
        assert response.response == "%R1P,0,0:0"
