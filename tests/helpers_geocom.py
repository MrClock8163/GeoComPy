import re

from geocompy import GeoComProtocol
from geocompy.communication import Connection
from geocompy.data import (
    Byte
)


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
        r"(?:,(?P<params>.*))?$"
    )

    def send(self, message: str):
        return

    def exchange1(self, cmd: str) -> str:
        print(cmd)

        if not self._CMD.match(cmd):
            return "%R1P,0,2:"

        if cmd == "%R1Q,0:":
            return "%R1P,0,0:0"

        return ""


class GeoComTester:
    @staticmethod
    def test_parse_response(instrument: GeoComProtocol):
        response = instrument.parse_response(
            "%R1Q,5008:",
            "%R1P,0,0:0,1996,'07','19','10','13','2f'",
            {
                "year": int,
                "month": Byte.parse,
                "day": Byte.parse,
                "hour": Byte.parse,
                "minute": Byte.parse,
                "second": Byte.parse
            }
        )
        assert response.params["year"] == 1996
