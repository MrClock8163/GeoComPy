from typing import Callable, Any
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

    def send(self, message: str):
        return

    def exchange(self, cmd: str) -> str:
        if not self._CMD.match(cmd):
            return "%R1P,0,0:2"

        if cmd == "%R1Q,5008:":
            return "%R1P,0,0:0,1996,'07','19','10','13','2f'"

        return "%R1P,0,0:0"


class GeoComTester:
    @staticmethod
    def test_parse_response(instrument: GeoComProtocol):
        cmd = "%R1Q,5008:"
        answer = "%R1P,0,0:0,1996,'07','19','10','13','2f'"
        parsers: dict[str, Callable[[str], Any]] = {
            "year": int,
            "month": Byte.parse,
            "day": Byte.parse,
            "hour": Byte.parse,
            "minute": Byte.parse,
            "second": Byte.parse
        }
        response = instrument.parse_response(
            cmd,
            answer,
            parsers
        )
        assert response.params["year"] == 1996

        response = instrument.parse_response(
            cmd,
            "%R1P,1,0:",
            parsers
        )
        assert len(response.params) == 0

        parsers_faulty = parsers.copy()
        parsers_faulty["year"] = faulty_parser
        response = instrument.parse_response(
            cmd,
            answer,
            parsers_faulty
        )
        assert len(response.params) == 0

    @staticmethod
    def test_request(instrument: GeoComProtocol):
        response = instrument.request(
            5008,
            parsers={
                "year": int,
                "month": Byte.parse,
                "day": Byte.parse,
                "hour": Byte.parse,
                "minute": Byte.parse,
                "second": Byte.parse
            }
        )
        assert response.params["year"] == 1996

        response = instrument.request(
            1,
            (1, 2.0)
        )
        assert response.cmd == "%R1Q,1:1,2.0"
        assert response.response == "%R1P,0,0:0"
