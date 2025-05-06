"""
Description
===========

Module: ``geocompy.communication``

Implementations of connection methods.

Functions
---------

- ``get_logger``
- ``open_serial``

Types
-----

- ``Connection``
- ``SerialConnection``
"""
from __future__ import annotations

import logging
from types import TracebackType
from typing import Literal

from serial import (
    Serial,
    SerialException,
    SerialTimeoutException,
    PARITY_NONE
)


def get_logger(
    name: str,
    target: Literal['null', 'file', 'stdout'] = 'null',
    level: int = logging.NOTSET,
    file: str = ""
) -> logging.Logger:
    """
    Utility function that creates a logger instance with standard
    formatting, logging to the specified target.

    Parameters
    ----------
    name : str
        Name of the logger.
    target : Literal['null', 'file', 'stdout'], optional
        Logging target, by default 'null'
    level : int, optional
        Logging level, by default logging.NOTSET
    file : str, optional
        Path to target log file (**must not be** ``""`` when target is
        'file'), by default ""

    Returns
    -------
    logging.Logger

    Note
    ----
    If a logger with the specified name already exists, it will be
    overwritten with the newly created handlers.
    """
    log = logging.getLogger(name)
    log.handlers.clear()
    log.setLevel(level)
    fmt = logging.Formatter(
        "%(asctime)s <%(name)s> [%(levelname)s] %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )
    match target:
        case "null":
            log.addHandler(logging.NullHandler())
        case "file" if file != "":
            fhandler = logging.FileHandler(
                file,
                encoding="utf8"
            )
            fhandler.setFormatter(fmt)
            log.addHandler(fhandler)
        case "stdout":
            shandler = logging.StreamHandler()
            shandler.setFormatter(fmt)
            log.addHandler(shandler)

    return log


class Connection:
    """
    Base class for all connection types. It specifies the required
    methods of all connection implementations, to serve as a generic
    interface.

    """

    def is_open(self) -> bool:
        """
        Checks if the communication channel is currently open.

        Returns
        -------
        bool
            State of the channel.

        Raises
        ------
        NotImplementedError
            If the method is not implemented on the child class.

        """
        raise NotImplementedError("interface does not implement 'is_open'")

    def send(self, message: str) -> None:
        """
        Sends a single serialized message through the connection.

        Parameters
        ----------
        message : str
            Message to send.

        Raises
        ------
        NotImplementedError
            If the method is not implemented on the child class.

        """
        raise NotImplementedError("interface does not implement 'send'")

    def receive(self) -> str:
        """
        Receives a single serialized message from the connection.

        Returns
        -------
        str
            Received message.

        Raises
        ------
        NotImplementedError
            If the method is not implemented on the child class.

        """
        raise NotImplementedError("interface does not implement 'receive'")

    def exchange(self, cmd: str) -> str:
        """
        Sends a message through the connection, and receives the
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
        NotImplementedError
            If the method is not implemented on the child class.

        """
        raise NotImplementedError("interface does not implement 'exchange1'")


def open_serial(
    port: str,
    *,
    speed: int = 9600,
    databits: int = 8,
    stopbits: int = 1,
    parity: str = PARITY_NONE,
    timeout: int = 15,
    eom: str = "\r\n",
    eoa: str = "\r\n"
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

    Returns
    -------
    SerialConnection

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
    serialport = Serial(port, speed, databits, parity, stopbits, timeout)
    wrapper = SerialConnection(serialport, eom=eom, eoa=eoa)
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
        eoa: str = "\r\n"
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

        Notes
        -----
        If the serial port is not already open, the opening will be
        attempted. This might raise an exception if the port cannot
        be opened.

        """

        self._port: Serial = port
        self.eom: str = eom  # end of message
        self.eoa: str = eoa  # end of answer

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
        self._port.close()

    def close(self) -> None:
        """
        Closes the serial port.
        """
        self._port.close()

    def is_open(self) -> bool:
        """
        Checks if the serial port is currently open.

        Returns
        -------
        bool
            State of the port.

        """
        return self._port.is_open

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
        if not self._port.is_open:
            raise SerialException(
                "serial port is not open"
            )

        if not message.endswith(self.eom):
            message += self.eom

        payload = message.encode('ascii', 'ignore')
        self._port.write(payload)

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
        if not self._port.is_open:
            raise SerialException(
                "serial port is not open"
            )

        eoabytes = self.eoa.encode("ascii")
        answer = self._port.read_until(eoabytes)
        if not answer.endswith(eoabytes):
            raise SerialTimeoutException(
                "serial connection timed out on 'receive'"
            )

        return answer.decode("ascii").removesuffix(self.eoa)

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
        self.send(cmd)
        return self.receive()
