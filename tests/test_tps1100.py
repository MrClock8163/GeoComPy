import pytest

from geocompy.communication import Connection
from geocompy.tps1100 import TPS1100

from helpers_geocom import (
    DummyGeoComConnection,
    GeoComTester
)


@pytest.fixture
def tps() -> TPS1100:
    return TPS1100(DummyGeoComConnection())


class TestTPS1100:
    def test_init(self):
        conn_bad = Connection()
        with pytest.raises(ConnectionError):
            TPS1100(conn_bad, retry=1)

        conn_good = DummyGeoComConnection()
        instrument = TPS1100(conn_good)
        assert instrument._precision == 15

    def test_parse_response(self, tps: TPS1100):
        GeoComTester.test_parse_response(tps)

    def test_request(self, tps: TPS1100):
        GeoComTester.test_request(tps)
