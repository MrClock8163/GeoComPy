import pytest

from geocompy.communication import Connection
from geocompy.tps1200p import TPS1200P

from helpers_geocom import (
    DummyGeoComConnection,
    GeoComTester
)


@pytest.fixture
def tps() -> TPS1200P:
    return TPS1200P(DummyGeoComConnection())


class TestTPS1200P:
    def test_init(self) -> None:
        conn_bad = Connection()
        with pytest.raises(ConnectionError):
            TPS1200P(conn_bad, retry=1)

        conn_good = DummyGeoComConnection()
        instrument = TPS1200P(conn_good)
        assert instrument._precision == 15

    def test_parse_response(self, tps: TPS1200P) -> None:
        GeoComTester.test_parse_response(tps)

    def test_request(self, tps: TPS1200P) -> None:
        GeoComTester.test_request(tps)
