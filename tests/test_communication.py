from os import environ
import pytest
from serial import Serial
from geocompy.communication import (
    get_dummy_logger,
    open_serial,
    SerialConnection,
    crc16_bitwise,
    crc16_bytewise
)


portname = environ.get("GEOCOMPY_TEST_PORT_CLIENT", "")
if portname == "":  # pragma: no coverage
    raise ValueError(
        "Echo server serial port name must be set in "
        "'GEOCOMPY_TEST_PORT_CLIENT' environment variable"
    )

faultyportname = environ.get("GEOCOMPY_TEST_PORT_FAULTY", "")
if faultyportname == "":  # pragma: no coverage
    raise ValueError(
        "Echo server serial port name must be set in "
        "'GEOCOMPY_TEST_PORT_FAULTY' environment variable"
    )


class TestDummyLogger:
    def test_get_dummy_logger(self) -> None:
        log = get_dummy_logger()
        assert log.name == "geocompy.dummy"
        assert len(log.handlers) == 1


class TestSerialConnection:
    def test_init(self) -> None:
        port = Serial(portname)
        with SerialConnection(port) as com:
            assert com.is_open()

        port = Serial()
        port.port = portname
        with SerialConnection(port) as com:
            assert com.is_open()

    def test_open_serial(self) -> None:
        with open_serial(portname) as com:
            assert com.is_open()

        with pytest.raises(Exception):
            open_serial(faultyportname, timeout=1)

    def test_messaging(self) -> None:
        with open_serial(portname) as com:
            request = "Test"
            assert com.exchange(request) == request

            com.send("ascii")
            assert com.receive() == "ascii"

            assert com.exchange_binary(b"00\r\n") == b"00"

            com.reset()

        with pytest.raises(ConnectionError):
            com.send("closed")

        with pytest.raises(ConnectionError):
            com.receive()

        with open_serial(
            portname,
            sync_after_timeout=True
        ) as com:
            com.send("msg1")
            com.send("msg2")
            com.send("msg3")
            com._timeout_counter = 3
            assert com.exchange("recovered") == "recovered"

            with com.timeout_override(1):
                with pytest.raises(TimeoutError):
                    com.receive()

                assert com._timeout_counter == 1

                with pytest.raises(TimeoutError):
                    com.receive()

                assert com._timeout_counter == 2


class TestCrc:
    def test_crc(self) -> None:
        # Verify CRC-16/ARC check value of "123456789" string
        assert crc16_bitwise("") == 0
        assert crc16_bitwise(b"") == 0
        assert crc16_bitwise("123456789") == 0xbb3d
        assert crc16_bitwise("123456789".encode("ascii")) == 0xbb3d
        assert crc16_bytewise("") == 0
        assert crc16_bytewise(b"") == 0
        assert crc16_bytewise("123456789") == 0xbb3d
        assert crc16_bytewise("123456789".encode("ascii")) == 0xbb3d
