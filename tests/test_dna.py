import pytest

from geocompy.gsi.dna import GsiOnlineDNA

from helpers_gsionline import (
    DummyGsiOnlineConnection,
    GsiOnlineTester
)

from helpers import FaultyConnection


@pytest.fixture
def dna() -> GsiOnlineDNA:
    return GsiOnlineDNA(DummyGsiOnlineConnection())


class TestDNA:
    def test_init(self) -> None:
        conn_bad = FaultyConnection()
        with pytest.raises(ConnectionRefusedError):
            GsiOnlineDNA(conn_bad, attempts=1)

        conn_good = DummyGsiOnlineConnection(True)
        dna = GsiOnlineDNA(conn_good)
        assert dna.is_client_gsi16

    def test_request(self, dna: GsiOnlineDNA) -> None:
        GsiOnlineTester.test_request(dna)

    def test_setrequest(self, dna: GsiOnlineDNA) -> None:
        GsiOnlineTester.test_setrequest(dna)

    def test_confrequest(self, dna: GsiOnlineDNA) -> None:
        GsiOnlineTester.test_confrequest(dna)

    def test_putrequest(self, dna: GsiOnlineDNA) -> None:
        GsiOnlineTester.test_putrequest(dna)

    def test_getrequest(self, dna: GsiOnlineDNA) -> None:
        GsiOnlineTester.test_getrequest(dna)
