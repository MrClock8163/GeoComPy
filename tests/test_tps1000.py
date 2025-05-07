import pytest

from geocompy.communication import Connection
from geocompy.tps1000 import TPS1000

from helpers_geocom import (
    DummyGeoComConnection,
    GeoComTester
)


@pytest.fixture
def tps() -> TPS1000:
    return TPS1000(DummyGeoComConnection())


class TestTPS1000:
    def test_init(self) -> None:
        conn_bad = Connection()
        with pytest.raises(ConnectionError):
            TPS1000(conn_bad, retry=1)

        conn_good = DummyGeoComConnection()
        instrument = TPS1000(conn_good)
        assert instrument._precision == 15

    def test_parse_response(self, tps: TPS1000) -> None:
        GeoComTester.test_parse_response(tps)

    def test_request(self, tps: TPS1000) -> None:
        GeoComTester.test_request(tps)
