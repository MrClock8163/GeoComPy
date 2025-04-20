import pytest

from geocompy.tps1200p import TPS1200P

from helpers_geocom import (
    DummyGeoComConnection,
    GeoComTester
)


@pytest.fixture
def tps() -> TPS1200P:
    return TPS1200P(DummyGeoComConnection())


class TestTPS1200P:
    def test_parse_response(self, tps: TPS1200P):
        GeoComTester.test_parse_response(tps)
