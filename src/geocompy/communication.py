"""
Description
===========

Module: ``geocompy.communication``

Implementations of connection methods.

Functions
---------

- ``get_dummy_logger``
- ``open_serial``
- ``crc16_bitwise``
- ``crc16_bytewise``

Constants
---------

- ``DUMMYLOGGER``

Types
-----

- ``Connection``
- ``SerialConnection``
"""
from __future__ import annotations

import logging
from types import TracebackType
from typing import Self, Literal
from collections.abc import Generator
from contextlib import contextmanager
from abc import ABC, abstractmethod
from time import sleep
from socket import (
    socket,
    SHUT_RDWR,
    AF_BLUETOOTH,
    AF_INET,
    SOCK_STREAM,
    BTPROTO_RFCOMM,
    IPPROTO_TCP
)

from serial import (
    Serial,
    SerialException,
    SerialTimeoutException,
    PARITY_NONE
)


def get_dummy_logger(name: str = "geocompy.dummy") -> logging.Logger:
    """
    Utility function that sets up a dummy logger instance, that does not
    propagate records, and logs to the nulldevice.

    Parameters
    ----------
    name : str
        Logger name.

    Returns
    -------
    logging.Logger
        Dummy logger.
    """
    logger = logging.getLogger(name)
    if len(logger.handlers) == 0:
        logger.addHandler(logging.NullHandler())

    logger.propagate = False
    return logger


DUMMYLOGGER = get_dummy_logger()
"""Dummy logger instance to use when no logger is actually needed."""


class Connection(ABC):
    """
    Interface definition for connection implementations.
    """

    @abstractmethod
    def is_open(self) -> bool: ...

    @abstractmethod
    def send_binary(self, data: bytes) -> None: ...

    @abstractmethod
    def send(self, message: str) -> None: ...

    @abstractmethod
    def receive_binary(self) -> bytes: ...

    @abstractmethod
    def receive(self) -> str: ...

    @abstractmethod
    def exchange_binary(self, data: bytes) -> bytes: ...

    @abstractmethod
    def exchange(self, cmd: str) -> str: ...

    @abstractmethod
    def close(self) -> None: ...

    @abstractmethod
    def reset(self) -> None: ...


def open_serial(
    port: str,
    *,
    speed: int = 9600,
    databits: int = 8,
    stopbits: int = 1,
    parity: str = PARITY_NONE,
    timeout: int = 15,
    eom: str = "\r\n",
    eoa: str = "\r\n",
    sync_after_timeout: bool = False,
    attempts: int = 1,
    logger: logging.Logger | None = None
) -> SerialConnection:
    """
    Constructs a SerialConnection with the given communication
    parameters.

    Parameters
    ----------
    port : str
        Name of the port to use (e.g. ``COM1`` or ``/dev/ttyUSB0``).
    speed : int, optional
        Communication speed (baud), by default 9600
    databits : int, optional
        Number of data bits, by default 8
    stopbits : int, optional
        Number of stop bits, by default 1
    parity : str, optional
        Parity bit behavior, by default PARITY_NONE
    timeout : int, optional
        Communication timeout threshold, by default 15
    eom : str, optional
        EndOfMessage sequence, by default ``"\\r\\n"``
    eoa : str, optional
        EndOfAnswer sequence, by default ``"\\r\\n"``
    sync_after_timeout : bool, optional
        Attempt to re-sync the message-response que, if a timeout
        occured in the previous exchange, by default False
    attempts : int, optional
        Number of attempts at opening the connection, by default 1
    logger : logging.Logger | None, optional
        Logger instance to use to log connection related events. Defaults
        to a dummy logger when not specified, by default None

    Returns
    -------
    SerialConnection

    Warning
    -------

    The syncing feature should be used with caution! See `SerialConnection`
    for more information!

    Examples
    --------

    Opening a serial connection similar to a file:

    >>> conn = open_serial("COM1", speed=19200, timeout=5)
    >>> # do operations
    >>> conn.close()

    Using as a context manager:

    >>> with open_serial("COM1", timeout=20) as conn:
    ...     conn.send("test")

    """
    logger = logger or DUMMYLOGGER
    logger.info(f"Opening connection on {port}")
    logger.debug(
        f"Connection parameters: "
        f"baud={speed:d}, timeout={timeout:d}, "
        f"sync_after_timeout={str(sync_after_timeout)}, "
        f"attempts={attempts:d}, "
        f"databits={databits:d}, stopbits={stopbits:d}, parity={parity}, "
        f"eom={eom.encode('ascii')!r}, eoa={eoa.encode('ascii')!r}"
    )
    exc: Exception = Exception()
    for i in range(max(attempts, 1)):
        try:
            serialport = Serial(
                port, speed, databits, parity, stopbits, timeout
            )
            break
        except Exception as e:
            logger.error(
                f"Failed to open connection, {attempts-i} trie(s) remains..."
            )
            exc = e

        sleep(5)
    else:
        raise exc

    wrapper = SerialConnection(
        serialport,
        eom=eom,
        eoa=eoa,
        sync_after_timeout=sync_after_timeout,
        logger=logger
    )
    return wrapper


def open_socket(
    address: str,
    port: int,
    protocol: Literal['rfcomm', 'tcp'],
    *,
    timeout: int = 15,
    eom: str = "\r\n",
    eoa: str = "\r\n",
    sync_after_timeout: bool = False,
    attempts: int = 1,
    logger: logging.Logger | None = None
) -> SocketConnection:
    logger = logger or DUMMYLOGGER
    logger.info(
        f"Opening socket connection to {address} on channel/port {port}"
    )
    logger.debug(
        f"Connection parameters: "
        f"timeout={timeout:d}, "
        f"sync_after_timeout={str(sync_after_timeout)}, "
        f"attempts={attempts:d}, "
        f"eom={eom.encode('ascii')!r}, eoa={eoa.encode('ascii')!r}"
    )
    match protocol:
        case "rfcomm":
            sock = socket(
                AF_BLUETOOTH,
                SOCK_STREAM,
                BTPROTO_RFCOMM
            )
        case "tcp":
            sock = socket(
                AF_INET,
                SOCK_STREAM,
                IPPROTO_TCP
            )
        case _:
            raise ValueError(f"Unknown protocol '{protocol}'")

    sock.settimeout(timeout)
    for i in range(max(attempts, 1)):
        try:
            sock.connect((address, port))
            break
        except Exception:
            logger.exception(
                f"Failed to open connection, {attempts - i} attempts remain"
            )
        sleep(2)
    else:
        raise ConnectionError("Could not open connection")

    return SocketConnection(
        sock,
        eom=eom,
        eoa=eoa,
        sync_after_timeout=sync_after_timeout,
        logger=logger
    )


class SocketConnection(Connection):
    def __init__(
        self,
        sock: socket,
        *,
        eom: str = "\r\n",
        eoa: str = "\r\n",
        sync_after_timeout: bool = False,
        logger: logging.Logger | None = None
    ):
        self.socket = sock
        self.eom: str = eom  # end of message
        self.eombytes: bytes = eom.encode("ascii")
        self.eoa: str = eoa  # end of answer
        self.eoabytes: bytes = eoa.encode("ascii")
        self._attempt_sync: bool = sync_after_timeout
        self._timeout_counter: int = 0
        self._logger: logging.Logger = logger or DUMMYLOGGER

        self._receiver_buffer: bytes = b""
        self._chunk = 1024

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: TracebackType
    ) -> None:
        self.close()

    def is_open(self) -> bool:
        try:
            sent = self.socket.send(self.eombytes)
            return sent == len(self.eombytes)
        except Exception:
            return False

    def send_binary(self, data: bytes) -> None:
        if not data.endswith(self.eombytes):
            data += self.eombytes

        try:
            self.socket.send(data)
        except Exception as e:
            raise ConnectionError(
                "Cannot send data, socket most likely disconnected"
            ) from e

    def send(self, message: str) -> None:
        self.send_binary(message.encode("ascii", "ignore"))

    def _receive_chunked(self) -> bytes:
        while self.eoabytes not in self._receiver_buffer:
            data = self.socket.recv(self._chunk)
            self._receiver_buffer += data

        end = self._receiver_buffer.index(self.eoabytes)
        data = self._receiver_buffer[:end]
        self._receiver_buffer = self._receiver_buffer[
            end + len(self.eoabytes):
        ]
        return data

    def receive_binary(self) -> bytes:
        if self._attempt_sync and self._timeout_counter > 0:
            for _ in range(self._timeout_counter):
                try:
                    self._receive_chunked()
                except TimeoutError as e:
                    self._timeout_counter += 1
                    raise TimeoutError(
                        "Socket connection timed out while recovering from a "
                        "previous timeout"
                    ) from e

        try:
            return self._receive_chunked()
        except TimeoutError as e:
            self._timeout_counter += 1
            raise TimeoutError("Socket connection timed out") from e

    def receive(self) -> str:
        return self.receive_binary().decode("ascii")

    def exchange_binary(self, data: bytes) -> bytes:
        self.send_binary(data)
        return self.receive_binary()

    def exchange(self, cmd: str) -> str:
        return self.exchange_binary(
            cmd.encode("ascii", "ignore")
        ).decode("ascii")

    def close(self) -> None:
        address: str
        port: int
        address, port = self.socket.getpeername()
        self.socket.shutdown(SHUT_RDWR)
        self.socket.close()
        self._logger.info(
            f"Closed connection to {address} on channel/port {port}"
        )

    def reset(self) -> None:
        address = self.socket.getpeername()
        newsoc = socket(
            self.socket.family,
            self.socket.type,
            self.socket.proto
        )
        newsoc.settimeout(self.socket.timeout)
        self.socket.close()
        self.socket = newsoc
        self.socket.connect(address)
        self._receiver_buffer = b""
        self._timeout_counter = 0
        self._logger.debug("Reset connection")

    @contextmanager
    def timeout_override(
        self,
        timeout: int | None
    ) -> Generator[None, None, None]:
        saved_timeout = self.socket.gettimeout()

        try:
            self.socket.settimeout(timeout)
            self._logger.debug(f"Temporary timeout override to {timeout}")
            yield
        finally:
            self.socket.settimeout(saved_timeout)
            self._logger.debug(f"Restored timeout to {saved_timeout}")


class SerialConnection(Connection):
    """
    Connection wrapping an open serial port.

    The passed serial port should be configured and opened in advance.
    Take care to set the approriate speed (baud), data bits, timeout etc.
    For most instruments a 9600 speed setting, 8 data + 1 stop bits is
    correct. A suitable timeout for total stations might be 15 seconds.
    (A too short timeout may result in unexpected errors when waiting for
    a slower, motorized function.)

    Examples
    --------

    Setting up a basic serial connection:

    >>> from serial import Serial
    >>> port = Serial("COM4", timeout=15)
    >>> conn = gc.communication.SerialConnection(port)
    >>> # message exchanges
    >>> conn.close()

    Using as a context manager:

    >>> from serial import Serial
    >>> port = Serial("COM4", timeout=15)
    >>> with gc.communication.SerialConnection(port) as conn:
    ...     # message exchanges
    >>>
    >>> port.is_open
    False
    >>> # port is automatically closed when the context is exited

    """

    def __init__(
        self,
        port: Serial,
        *,
        eom: str = "\r\n",
        eoa: str = "\r\n",
        sync_after_timeout: bool = False,
        logger: logging.Logger | None = None
    ):
        """
        Parameters
        ----------
        port : Serial
            Serial port to communicate on.
        eom : str, optional
            EndOfMessage sequence, by default ``"\\r\\n"``
        eoa : str, optional
            EndOfAnswer sequence, by default ``"\\r\\n"``
        sync_after_timeout : bool, optional
            Attempt to re-sync the message-response que, if a timeout
            occured in the previous exchange, by default False
        logger : logging.Logger | None, optional
            Logger instance to use to log connection related events. Defaults
            to a dummy logger when not specified, by default None

        Notes
        -----
        If the serial port is not already open, the opening will be
        attempted. This might raise an exception if the port cannot
        be opened.

        Warning
        -------

        The que syncing is attempted by repeatedly reading from the
        receiving buffer, as many times as a timeout was previously
        detected. This can only solve issues, if the connection target
        was just slow, and not completely unresponsive. If the target
        became truly unresponsive, but came back online later, the sync
        attempt can cause further problems. Use with caution!

        (Timeouts should be avoided when possible, use a temporary override
        on exchanges that are expected to finish in a longer time.)

        """

        self._port: Serial = port
        self.eom: str = eom  # end of message
        self.eombytes: bytes = eom.encode("ascii")
        self.eoa: str = eoa  # end of answer
        self.eoabytes: bytes = eoa.encode("ascii")
        self._attempt_sync: bool = sync_after_timeout
        self._timeout_counter: int = 0
        self._logger: logging.Logger = logger or DUMMYLOGGER

        if not self._port.is_open:
            self._port.open()

    def __del__(self) -> None:
        self._port.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: TracebackType
    ) -> None:
        self.close()

    def close(self) -> None:
        """
        Closes the serial port.
        """
        self._port.close()
        self._logger.info(f"Closed connection on {self._port.port}")

    def is_open(self) -> bool:
        """
        Checks if the serial port is currently open.

        Returns
        -------
        bool
            State of the port.

        """
        return self._port.is_open

    def send_binary(self, data: bytes) -> None:
        """
        Writes a single message to the serial line.

        Parameters
        ----------
        data : bytes
            Data to send.

        Raises
        ------
        ~serial.SerialException
            If the serial port is not open.

        """
        if not self._port.is_open:
            raise SerialException(
                "serial port is not open"
            )

        if not data.endswith(self.eombytes):
            data += self.eombytes

        self._port.write(data)

    def send(self, message: str) -> None:
        """
        Writes a single message to the serial line.

        Parameters
        ----------
        message : str
            Message to send.

        Raises
        ------
        ~serial.SerialException
            If the serial port is not open.

        """
        self.send_binary(message.encode("ascii", "ignore"))

    def receive_binary(self) -> bytes:
        """
        Reads a single binary data block from the serial line.

        Returns
        -------
        bytes
            Received data.

        Raises
        ------
        ~serial.SerialException
            If the serial port is not open.
        ~serial.SerialTimeoutException
            If the connection timed out before receiving the
            EndOfAnswer sequence.

        """
        if not self._port.is_open:
            raise SerialException(
                "serial port is not open"
            )

        eoabytes = self.eoa.encode("ascii")
        if self._attempt_sync and self._timeout_counter > 0:
            for i in range(self._timeout_counter):
                excess = self._port.read_until(eoabytes)
                if not excess.endswith(eoabytes):
                    self._timeout_counter += 1
                    raise SerialTimeoutException(
                        "Serial connection timed out on 'receive_binary' "
                        "during an attempt to recover from a previous timeout"
                    )
            else:
                self._timeout_counter = 0

        answer = self._port.read_until(eoabytes)
        if not answer.endswith(eoabytes):
            self._timeout_counter += 1
            raise SerialTimeoutException(
                "serial connection timed out on 'receive_binary'"
            )

        return answer.removesuffix(eoabytes)

    def receive(self) -> str:
        """
        Reads a single message from the serial line.

        Returns
        -------
        str
            Received message.

        Raises
        ------
        ~serial.SerialException
            If the serial port is not open.
        ~serial.SerialTimeoutException
            If the connection timed out before receiving the
            EndOfAnswer sequence.

        """

        return self.receive_binary().decode("ascii")

    def exchange_binary(self, data: bytes) -> bytes:
        """
        Writes a block of data to the serial line, and receives the
        corresponding response.

        Parameters
        ----------
        data : bytes
            Message to send.

        Returns
        -------
        bytes
            Response to the sent data

        Raises
        ------
        ~serial.SerialException
            If the serial port is not open.
        ~serial.SerialTimeoutException
            If the connection timed out before receiving the
            EndOfAnswer sequence for one of the responses.

        """
        self.send_binary(data)
        return self.receive_binary()

    def exchange(self, cmd: str) -> str:
        """
        Writes a message to the serial line, and receives the
        corresponding response.

        Parameters
        ----------
        cmd : str
            Message to send.

        Returns
        -------
        str
            Response to the sent message

        Raises
        ------
        ~serial.SerialException
            If the serial port is not open.
        ~serial.SerialTimeoutException
            If the connection timed out before receiving the
            EndOfAnswer sequence for one of the responses.

        """
        return self.exchange_binary(
            cmd.encode("ascii", "ignore")
        ).decode("ascii")

    def reset(self) -> None:
        """
        Resets the connection by clearing the incoming and outgoing
        buffers, and resetting the internal state. This could be used
        to recover from a desync (possibly caused by a timeout).

        Warning
        -------

        Trying to recover after repeated timeouts with a hard reset can
        cause further issues, if the reset is attempted while responses
        were finally being received. It is recommended to wait some time
        after the last command was sent, before resetting.
        """
        self._port.reset_input_buffer()
        self._port.reset_output_buffer()
        self._timeout_counter = 0
        self._logger.debug("Reset connection")

    @contextmanager
    def timeout_override(
        self,
        timeout: int | None
    ) -> Generator[None, None, None]:
        """
        Context manager that temporarily overrides connection parameters.

        Parameters
        ----------
        timeout : int | None
            Temporary timeout in seconds. Set to None to wait indefinitely.

        Returns
        -------
        Generator
            Context manager generator object.

        Warning
        -------
        An indefinite timeout might leave the connection in a perpetual
        waiting state, if the instrument became unresponsive in the
        mean time (e.g. it powered off due to low battery charge).

        Example
        -------

        >>> from serial import Serial
        >>> from geocompy.communication import SerialConnection
        >>>
        >>> port = Serial("COM1", timeout=5)
        >>> with SerialConnection(port) as com:
        ...     # normal operation
        ...
        ...     # potentially long operation
        ...     with com.timeout_override(20):
        ...         answer = com.exchange("message")
        ...
        ...     # continue normal operation
        ...
        """
        saved_timeout = self._port.timeout

        try:
            self._port.timeout = timeout
            self._logger.debug(f"Temporary timeout override to {timeout}")
            yield
        finally:
            self._port.timeout = saved_timeout
            self._logger.debug(f"Restored timeout to {saved_timeout}")


# The GeoCOM protocol supports CRC-16 checksums in message exchanges.
# From testing it appears it uses the ARC/IBM parameter set.
#
# Parameters and other info on various CRC versions:
# https://reveng.sourceforge.io/crc-catalogue/16.htm#disclaimer
#
# Good reference article and calculator:
# https://www.sunshine2k.de/articles/coding/crc/understanding_crc.html
# https://www.sunshine2k.de/coding/javascript/crc/crc_js.html
#
# The implementations below are for this specific variant of CRC-16, not
# general solutions. The methods were modified to take into account the
# input and output reflection.
def crc16_bitwise(value: str | bytes) -> int:
    """
    Bitwise CRC-16/ARC calculation method.

    Adapted from: https://stackoverflow.com/a/68095008

    Parameters
    ----------
    value : str | bytes
        Data to digest.

    Returns
    -------
    int
        CRC-16 checksum
    """
    crc = 0

    if len(value) == 0:
        return crc

    if isinstance(value, bytes):
        data = value
    else:
        data = value.encode("ascii")

    for char in data:
        crc ^= char

        for _ in range(8):
            crc = (crc >> 1) ^ 0xa001 if (crc & 1) else (crc >> 1)

    return crc


_crc16_table_reflected: list[int] = [
    0x0000, 0xc0c1, 0xc181, 0x0140, 0xc301, 0x03c0, 0x0280, 0xc241,
    0xc601, 0x06c0, 0x0780, 0xc741, 0x0500, 0xc5c1, 0xc481, 0x0440,
    0xcc01, 0x0cc0, 0x0d80, 0xcd41, 0x0f00, 0xcfc1, 0xce81, 0x0e40,
    0x0a00, 0xcac1, 0xcb81, 0x0b40, 0xc901, 0x09c0, 0x0880, 0xc841,
    0xd801, 0x18c0, 0x1980, 0xd941, 0x1b00, 0xdbc1, 0xda81, 0x1a40,
    0x1e00, 0xdec1, 0xdf81, 0x1f40, 0xdd01, 0x1dc0, 0x1c80, 0xdc41,
    0x1400, 0xd4c1, 0xd581, 0x1540, 0xd701, 0x17c0, 0x1680, 0xd641,
    0xd201, 0x12c0, 0x1380, 0xd341, 0x1100, 0xd1c1, 0xd081, 0x1040,
    0xf001, 0x30c0, 0x3180, 0xf141, 0x3300, 0xf3c1, 0xf281, 0x3240,
    0x3600, 0xf6c1, 0xf781, 0x3740, 0xf501, 0x35c0, 0x3480, 0xf441,
    0x3c00, 0xfcc1, 0xfd81, 0x3d40, 0xff01, 0x3fc0, 0x3e80, 0xfe41,
    0xfa01, 0x3ac0, 0x3b80, 0xfb41, 0x3900, 0xf9c1, 0xf881, 0x3840,
    0x2800, 0xe8c1, 0xe981, 0x2940, 0xeb01, 0x2bc0, 0x2a80, 0xea41,
    0xee01, 0x2ec0, 0x2f80, 0xef41, 0x2d00, 0xedc1, 0xec81, 0x2c40,
    0xe401, 0x24c0, 0x2580, 0xe541, 0x2700, 0xe7c1, 0xe681, 0x2640,
    0x2200, 0xe2c1, 0xe381, 0x2340, 0xe101, 0x21c0, 0x2080, 0xe041,
    0xa001, 0x60c0, 0x6180, 0xa141, 0x6300, 0xa3c1, 0xa281, 0x6240,
    0x6600, 0xa6c1, 0xa781, 0x6740, 0xa501, 0x65c0, 0x6480, 0xa441,
    0x6c00, 0xacc1, 0xad81, 0x6d40, 0xaf01, 0x6fc0, 0x6e80, 0xae41,
    0xaa01, 0x6ac0, 0x6b80, 0xab41, 0x6900, 0xa9c1, 0xa881, 0x6840,
    0x7800, 0xb8c1, 0xb981, 0x7940, 0xbb01, 0x7bc0, 0x7a80, 0xba41,
    0xbe01, 0x7ec0, 0x7f80, 0xbf41, 0x7d00, 0xbdc1, 0xbc81, 0x7c40,
    0xb401, 0x74c0, 0x7580, 0xb541, 0x7700, 0xb7c1, 0xb681, 0x7640,
    0x7200, 0xb2c1, 0xb381, 0x7340, 0xb101, 0x71c0, 0x7080, 0xb041,
    0x5000, 0x90c1, 0x9181, 0x5140, 0x9301, 0x53c0, 0x5280, 0x9241,
    0x9601, 0x56c0, 0x5780, 0x9741, 0x5500, 0x95c1, 0x9481, 0x5440,
    0x9c01, 0x5cc0, 0x5d80, 0x9d41, 0x5f00, 0x9fc1, 0x9e81, 0x5e40,
    0x5a00, 0x9ac1, 0x9b81, 0x5b40, 0x9901, 0x59c0, 0x5880, 0x9841,
    0x8801, 0x48c0, 0x4980, 0x8941, 0x4b00, 0x8bc1, 0x8a81, 0x4a40,
    0x4e00, 0x8ec1, 0x8f81, 0x4f40, 0x8d01, 0x4dc0, 0x4c80, 0x8c41,
    0x4400, 0x84c1, 0x8581, 0x4540, 0x8701, 0x47c0, 0x4680, 0x8641,
    0x8201, 0x42c0, 0x4380, 0x8341, 0x4100, 0x81c1, 0x8081, 0x4040
]
"""
Reflected CRC-16/ARC lookup table for bytewise computation.

https://www.sunshine2k.de/coding/javascript/crc/crc_js.html
"""


def crc16_bytewise(value: str | bytes) -> int:
    """
    Bytewise CRC-16/ARC calculation method.

    The method uses a precomputed lookup table to reduce the number of
    required operations to calculate a checksum.

    Parameters
    ----------
    value : str | bytes
        Data to digest.

    Returns
    -------
    int
        CRC-16 checksum
    """
    crc = 0

    if len(value) == 0:
        return crc

    if isinstance(value, bytes):
        data: bytes = value
    else:
        data = value.encode("ascii")

    for char in data:
        # Due to the arbirarily sized integers in Python, the index must be
        # masked to 8 bit
        idx = (char ^ (crc)) & 0xff
        crc = _crc16_table_reflected[idx] ^ (crc >> 8)

    return crc
