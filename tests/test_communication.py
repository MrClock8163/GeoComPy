from os import environ
import socket

import pytest
from serial import Serial
from geocompy.communication import (
    get_dummy_logger,
    open_serial,
    open_socket,
    SerialConnection,
    SocketConnection,
    crc16_bitwise,
    crc16_bytewise
)


@pytest.fixture
def sock() -> socket.socket:
    return socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_TCP
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

tcpport = environ.get("GEOCOMPY_TEST_TCPPORT_SERVER", "")
if faultyportname == "":  # pragma: no coverage
    raise ValueError(
        "Echo server tcp port must be set in "
        "'GEOCOMPY_TEST_TCPPORT_SERVER' environment variable"
    )


class TestDummyLogger:
    def test_get_dummy_logger(self) -> None:
        log = get_dummy_logger()
        assert log.name == "geocompy.dummy"
        assert len(log.handlers) == 1


class TestSocketConnection:
    def test_init(self, sock: socket.socket) -> None:
        sock.connect(("127.0.0.1", int(tcpport)))
        with SocketConnection(sock) as client:
            assert client.is_open()

        client.close()
        assert not client.is_open()

    def test_open_socket(self) -> None:
        with open_socket("127.0.0.1", int(tcpport), "tcp") as soc:
            assert soc.is_open()

        with pytest.raises(Exception):
            open_socket("127.0.0.1", int(tcpport), "rfcomm", timeout=1)

        with pytest.raises(ValueError):
            open_socket(
                "127.0.0.1",
                int(tcpport),
                "mistake",  # type: ignore[arg-type]
                timeout=1
            )

    def test_messaging(self) -> None:
        with open_socket(
            "127.0.0.1",
            int(tcpport),
            "tcp"
        ) as soc:
            soc.is_open()
            request = "Test"
            assert soc.exchange(request) == request

            soc.send("ascii")
            assert soc.receive() == "ascii"

            assert soc.exchange_binary(b"00\r\n") == b"00"

            soc.reset()

        with pytest.raises(ConnectionError):
            soc.send("closed")

        with pytest.raises(ConnectionError):
            soc.receive()

        with open_socket(
            "127.0.0.1",
            int(tcpport),
            "tcp",
            sync_after_timeout=True
        ) as soc:
            soc.send("msg1")
            soc.send("msg2")
            soc.send("msg3")
            soc._timeout_counter = 3
            assert soc.exchange("recovered") == "recovered"

            with soc.timeout_override(1):
                with pytest.raises(TimeoutError):
                    soc.receive()

                assert soc._timeout_counter == 1

                with pytest.raises(TimeoutError):
                    soc.receive()

                assert soc._timeout_counter == 2

        with pytest.raises(ConnectionError):
            soc.receive()


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
