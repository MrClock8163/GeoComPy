from typing import Any
from collections.abc import Callable, Iterable
import re

import pytest

from geocompy.geo import GeoCom
from geocompy.communication import Connection
from geocompy.data import Byte

from helpers import faulty_parser, FaultyConnection


@pytest.fixture
def instrument() -> GeoCom:
    return GeoCom(DummyGeoComConnection())


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
        r"(?P<rpc>\d+)"
        r"(?P<trid>,\d+)?:"
        r"(?:(?P<params>.*))?$"
    )

    def send(self, message: str) -> None:
        return

    def receive(self) -> str:
        return ""

    def exchange(self, cmd: str) -> str:
        if not self._CMD.match(cmd):
            return "%R1P,0,0:2"

        head, _ = cmd.split(":")
        match head.split(","):
            case [_, _, trid_str]:
                pass
            case _:
                trid_str = "0"

        trid = int(trid_str)

        if re.match(r"%R1Q,5008,\d+:", cmd):
            return f"%R1P,0,{trid}:0,1996,'07','19','10','13','2f'"

        return f"%R1P,0,{trid}:0"

    def close(self) -> None:
        pass

    def reset(self) -> None:
        pass

    def is_open(self) -> bool:
        return True


class TestGeoCom:
    def test_init(self) -> None:
        conn_bad = FaultyConnection()
        with pytest.raises(ConnectionError):
            GeoCom(conn_bad, retry=1)

        conn_good = DummyGeoComConnection()
        instrument = GeoCom(conn_good)
        assert instrument.precision == 15

    def test_parse_response(self, instrument: GeoCom) -> None:
        cmd = "%R1Q,5008,0:"
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

    def test_request(self, instrument: GeoCom) -> None:
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
        assert re.match(r"%R1Q,1,\d+:1,2.0", response.cmd)
        assert re.match(r"%R1P,0,\d+:0", response.response)
