.. _page_connections:

Connections
===========

Total stations and digital levels usually support a serial connection
with RS232. Some instruments come with additional connection methods, like
bluetooth as well.

Serial Line
-----------

The RS232 serial line is the main method of connection. The main primitive
is the :class:`~geocompy.communication.SerialConnection` class, that acts as a
wrapper around a :class:`~serial.Serial` object that implements the actual
low level serial communication.

.. code-block:: python
    :caption: Simple serial connection
    :linenos:

    from serial import Serial
    from geocompy.communication import SerialConnection


    port = Serial("COM1", timeout=15)
    com = SerialConnection(port)
    com.send("some message")
    com.close()  # Closes the wrapped serial port

.. caution::
    :class: warning

    It is strongly recommended to set a ``timeout`` on the connection. Without
    a ``timeout`` set, the connection may end up in a perpetual waiting state
    if the instrument becomes unresponsive. A too small value however might
    result in premature timeout issues when using slow commands (e.g.
    motorized functions, measurements).

The :class:`~geocompy.communication.SerialConnection` can also be used as a
context manager, that automatically closes the serial port when the context
is left.

.. code-block:: python
    :caption: Serial connection as context manager
    :linenos:

    from serial import Serial
    from geocompy.communication import SerialConnection


    port = Serial("COM1", timeout=15)
    with SerialConnection(port) as com:
        com.send("some message")

To make the connection creation simpler, a utility function is also included
that can be used similarly to the :func:`open` function of the standard
library.

.. code-block:: python
    :caption: Creating connection with the utility function
    :linenos:

    from geocompy.communication import open_serial


    with open_serial("COM1", timeout=15) as com:
        com.send("some message")

If a time consuming request has to be executed, that might exceed the normal
connection timeout, it is possible to run it with a temporary override.

.. code-block:: python
    :caption: Timeout override for slow requests
    :linenos:

    from geocompy.communication import open_serial


    with open_serial("COM1", timeout=5) as com:
        ans = com.exchage("message")
        # normal operation

        # request that might time out
        with com.timeout_override(20):
            ans = com.exchange("blocking message")
        
        # resumed normal operation

Bluetooth
---------

Newer instruments (particularly robotic total stations) might come with
built-in or attachable bluetooth connection capabilities (e.g. Leica TS15
with radio handle). These instruments communicate over Serial Port Profile
Bluetooth Classic, that emulates a direct line serial connection.

To initiate a connection like this, the instrument first has to be paired
to the controlling computer, and the bluetooth address of the instrument
must be bound to an RFCOMM port as well.

On windows machines this can be done manually through the Devices and
Printers in the Control Panel. These RFCOMM devices will typically get one
of the higher numbered ports, like ``COM9``.

Linux systems will typically use something like
`bluetoothctl <https://documentation.ubuntu.com/core/explanation/system-snaps/bluetooth/pairing/index.html>`_
to handle the pairing process, and then ``rfcomm`` command to bind a device
to an RFCOMM port.

Once the pairing and binding is complete, the connection over bluetooth can
be opened just like a normal serial line.

.. code-block:: python
    :caption: Opening connection through an RFCOMM port
    :linenos:

    from geocompy.communication import open_serial


    with open_serial("COM9") as com:
        com.send("some message")

.. note::

    In case of Leica instruments and GeoCom, the GeoCom interface on the
    instrument has to be manually switched to the bluetooth device,
    before initiating a connection. Make sure to sync the port parameters
    (e.g. speed, parity) between the instrument and the computer!

.. seealso::

    https://youtu.be/6Z4PXct8Rg0?si=db53q6F6NRi2M4BF
        Video explaining the pairing process between a Raspberry PI and
        a windows PC. It shows how to properly add an RFCOMM device in
        the Control Panel.
