"""
Description
===========

Module: ``geocompy.communication``

Implementations of connection methods.

Functions
---------

- ``get_dummy_logger``
- ``open_serial``

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
from collections.abc import Generator
from contextlib import contextmanager
from abc import ABC, abstractmethod
from time import sleep

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
    def send(self, message: str) -> None: ...

    @abstractmethod
    def receive(self) -> str: ...

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
    retry: int = 1,
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
    retry : int, optional
        Number of retry attempts if the connection opening fails, by
        default 1
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
        f"sync_after_timeout={str(sync_after_timeout)}, tries={retry:d}, "
        f"databits={databits:d}, stopbits={stopbits:d}, parity={parity}, "
        f"eom={eom.encode('ascii')!r}, eoa={eoa.encode('ascii')!r}"
    )
    exc: Exception = Exception()
    for i in range(retry):
        try:
            serialport = Serial(
                port, speed, databits, parity, stopbits, timeout
            )
            break
        except Exception as e:
            logger.error(
                f"Failed to open connection, {retry-i} trie(s) remains..."
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

    def __enter__(self) -> SerialConnection:
        return self

    def __exit__(
        self,
        exc_type: BaseException,
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
