import pytest

from geocompy.communication import Connection
from geocompy.gsi.dna import GsiOnlineDNA

from helpers_gsionline import (
    DummyGsiOnlineConnection,
    GsiOnlineTester
)


@pytest.fixture
def dna() -> GsiOnlineDNA:
    return GsiOnlineDNA(DummyGsiOnlineConnection())


class TestDNA:
    def test_init(self) -> None:
        conn_bad = Connection()
        with pytest.raises(ConnectionError):
            GsiOnlineDNA(conn_bad, retry=1)

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
