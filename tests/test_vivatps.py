import pytest

from geocompy.communication import Connection
from geocompy.vivatps import VivaTPS

from helpers_geocom import (
    DummyGeoComConnection,
    GeoComTester
)


@pytest.fixture
def tps() -> VivaTPS:
    return VivaTPS(DummyGeoComConnection())


class TestVivaTPS:
    def test_init(self) -> None:
        conn_bad = Connection()
        with pytest.raises(ConnectionError):
            VivaTPS(conn_bad, retry=1)

        conn_good = DummyGeoComConnection()
        instrument = VivaTPS(conn_good)
        assert instrument._precision == 15

    def test_parse_response(self, tps: VivaTPS) -> None:
        GeoComTester.test_parse_response(tps)

    def test_request(self, tps: VivaTPS) -> None:
        GeoComTester.test_request(tps)
