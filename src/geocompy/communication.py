"""
``geocompy.communication``
==========================

Implementations of connection methods.

Types
-----

- ``Connection`` (generic base class)
- ``SerialConnection``

"""
from __future__ import annotations

from types import TracebackType
from typing import Iterable

from serial import Serial, SerialException, SerialTimeoutException


class Connection:
    """
    Base class for all connection types. It specifies the required
    methods of all connection implementations, to serve as a generic
    interface.

    """

    def __init__(self, name: str = ""):
        """
        Parameters
        ----------
        name : str, optional
            Descriptive name, by default ""

        """
        self.name: str = name

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

    def send(self, message: str):
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

    def exchange(self, cmds: Iterable[str]) -> list[str]:
        """
        Sends an arbitrary number of messages through the connection,
        and receives the corresponding responses.

        Parameters
        ----------
        cmds : Iterable[str]
            Collection of messages to send.

        Returns
        -------
        list[str]
            Responses to the sent messages.

        Raises
        ------
        NotImplementedError
            If the method is not implemented on the child class.

        """
        raise NotImplementedError("interface does not implement 'exchange'")

    def exchange1(self, cmd: str) -> str:
        """
        Sends a single message through the connection, and receives the
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
        port : ~serial.Serial
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
        super().__init__("")

        self._port: Serial = port
        self.eom: str = eom  # end of message
        self.eoa: str = eoa  # end of answer

        if not self._port.is_open:
            self._port.open()

    def __del__(self):
        self._port.close()

    def __enter__(self) -> SerialConnection:
        return self

    def __exit__(
        self,
        exc_type: BaseException,
        exc_value: BaseException,
        exc_tb: TracebackType
    ):
        self._port.close()

    def close(self):
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

    def send(self, message: str):
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
            raise SerialTimeoutException("serial connection timed out on 'receive'")

        return answer.decode("ascii").removesuffix(self.eoa)

    def exchange(self, cmds: Iterable[str]) -> list[str]:
        """
        Writes an arbitrary number of messages to the serial line,
        and receives the corresponding responses, one pair at a time.

        Parameters
        ----------
        cmds : Iterable[str]
            Collection of messages to send.

        Returns
        -------
        list[str]
            Responses to the sent messages.

        Raises
        ------
        ~serial.SerialException
            If the serial port is not open.
        ~serial.SerialTimeoutException
            If the connection timed out before receiving the
            EndOfAnswer sequence for one of the responses.

        """
        answers: list[str] = []
        for item in cmds:
            self.send(item)
            answers.append(self.receive())

        return answers

    def exchange1(self, cmd: str) -> str:
        """
        Writes a single message to the serial line, and receives the
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
