import pytest

from geocompy.communication import Connection
from geocompy.dna import DNA

from helpers_gsionline import (
    DummyGsiOnlineConnection,
    GsiOnlineTester
)


@pytest.fixture
def dna() -> DNA:
    return DNA(DummyGsiOnlineConnection())


class TestDNA:
    def test_init(self):
        conn_bad = Connection()
        with pytest.raises(ConnectionError):
            DNA(conn_bad, retry=1)

        conn_good = DummyGsiOnlineConnection(True)
        dna = DNA(conn_good)
        assert dna._gsi16

    def test_request(self, dna: DNA):
        GsiOnlineTester.test_request(dna)

    def test_setrequest(self, dna: DNA):
        GsiOnlineTester.test_setrequest(dna)

    def test_confrequest(self, dna: DNA):
        GsiOnlineTester.test_confrequest(dna)

    def test_putrequest(self, dna: DNA):
        GsiOnlineTester.test_putrequest(dna)

    def test_getrequest(self, dna: DNA):
        GsiOnlineTester.test_getrequest(dna)
