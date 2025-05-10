Introduction
============

This section aims to introduce the basic usage, and general concepts of the
package.

Communication
-------------

The primary way of communication with surveying instruments is through
a direct serial connection (RS232). This is available on almost all products.
Newer equipment might also come with built-in, or attachable bluetooth
connection capabilities.

Communication related definitions can be found in the
:mod:`~geocompy.communication` module.

A utility function can be used to open the serial connection, that works
similarly to the :func:`open` function of the standard library.

.. code-block:: python
    :caption: Creating connection with the utility function
    :linenos:

    from geocompy.communication import open_serial


    with open_serial("COM1", timeout=15) as com:
        com.send("some message")

.. seealso::

    Communication methods are discussed in more detail in
    :ref:`page_connections`.

Protocols
---------

The GeoComPy package (as the name suggests) primarily built around the
GeoCom command protocol. This was developed by Leica and is available on
a wide range of their products. For some older instrument types, that do
not support GeoCom, older systems (like GSI Online) might be implemented
instead. All serial communication based protocols are fundamentally
synchronous systems, consisting of request-response pairs.

.. note::

    Leica stopped selling GeoCom robotic licenses for their TPS1200 series
    instruments in 2019. Newer instruments have a more complicated
    licensing scheme.

The primary goal is to provide methods to call all known GeoCom commands on the
supported instruments. These "low-level" commands can then be used to build
more complex applications.

GeoCom
^^^^^^

GeoCom enabled instruments can communicate with the ASCII version of the
protocol through a stable connection. Each command is a serialized RPC
(Remote Procedure Call) request, that specifies the code of the procedure
to run, and supplies the necessary arguments. The reply is a serialized
RPC response message, containing the return parameters.

.. code-block::
    :caption: GeoCom exchange example

    %R1Q,9029:1,1,0 # RPC 9029, prism search in window
    %R1P,0,0:0      # Standard OK response

All the supported instruments follow a similar API structure. The instrument
object implements the generic request functions. The actual GeoCom commands
are available through their respective subsystems.

The connection to an instrument can be easily set up through a serial
connection. The connection is tested during the initialization, and some
communication parameters are syncronized.

.. code-block:: python
    :caption: Initializing instrument connection with GeoCom
    :linenos:

    from geocompy.communication import open_serial
    from geocompy.tps1200p import TPS1200P


    with open_serial("COM1", timeout=10) as conn:
        tps = TPS1200P(conn)

.. note::

    If the instrument is not turned on when the connection is initiated,
    the process will try to wake it up. Since some instruments must be
    manually put into GeoCom mode, the initialization might not be successful
    from a completely shutdown state.

Once the connection is verified, the commands can be executed through the
various subsystems.

.. code-block:: python
    :caption: Querying the system software version through Central Services
    :linenos:

    resp = tps.csv.get_firmware_version()
    print(resp)  # GeoComResponse(CSV_GetSWVersion) com: OK, rpc: OK...

All GeoCom commands return a :class:`~geocompy.geo.gctypes.GeoComResponse`
object, that encapsulates the return codes, as well as the optional
returned paramters.

.. tip::

    The complete list of available commands and their documentations are
    available in their respective API documentation categories.

GSI Online
^^^^^^^^^^

The GSI Online protocol is a command system that is older than GeoCom. Many
older instruments only support this system. Some support both (e.g. 
TPS1100 series).

The commands fall into two groups:

- instrument settings (CONF and SET commands)
- measurements (GET and PUT commands)

Instrument settings are set and queried with the ``SET`` and ``CONF`` commands.
The values are communicated with simple enumerations of the valid settings.

.. code-block::
    :caption: GSI Online settings exchange example

    CONF/30   # Query command
    0030/0001 # Response

    SET/30/2  # Setting beeping to loud
    ?         # Success confirmation

Measurement related ``PUT`` and ``GET`` commands on the other hand use GSI data
words to exchange the necessary information.

.. code-block::
    :caption: GSI Online measurements exchange example

    GET/M/WI11                # Query current point ID
    11....+000000A1           # Response if format is GSI8
    *11....+00000000000000A1  # Response if format is GSI16

    PUT/11....+000000A2       # Setting new point ID
    ?                         # Success confirmation

The GSI Online based implementations mainly consist of 3 parts. The instrument
object implements the basic request functions. The ``settings`` and the
``measurements`` subsystems provide the individual commands.

The connection to an instrument is identical to the GeoCom versions. The
connection is tested during the initialization, and some communication
parameters are syncronized.

.. code-block:: python
    :caption: Initializing instrument connection with GSI Online
    :linenos:

    from geocompy.communication import open_serial
    from geocompy.dna import DNA


    with open_serial("COM1", timeout=10) as conn:
        level = DNA(conn)

.. note::

    If the instrument is not turned on when the connection is initiated,
    the process will try to wake it up.

Once the connection is live, the commands can be executed.

.. code-block:: python
    :caption: Turning off beeping and getting a staff reading
    :linenos:

    level.settings.set_beep(level.settings.BEEPINTENSITY.OFF)
    resp = level.measurements.get_reading()
    print(resp)  # GsiOnlineResponse(Reading) success, value: ...

All GSI Online commands return a :class:`~geocompy.protocols.GsiOnlineResponse`
object, that encapsulates command metadata and the result of the request.

.. tip::

    The complete list of available commands and their documentations are
    available in their respective API documentation categories.

Logging
-------

For debugging purposes it might be very useful to have a log of certain events,
errors and debug information. To support this, the instrument classes all take
an optional :class:`~logging.Logger` object, that they use to log specific
events. The :func:`~geocompy.communication.get_logger` utility function can be
used to create a simple logger.

.. code-block:: python
    :caption: Passing a console logger
    :linenos:

    from logging import DEBUG

    from geocompy.communication import open_serial, get_logger
    from geocompy.dna import DNA


    log = get_logger("DNA", "stdout", DEBUG)
    with open_serial("COM1", timeout=15) as conn:
        level = DNA(conn, log)

Some examples of the information logged on various levels:

- connection start
- instrument wake up
- instrument shutdown
- all unexpected exceptions
- all command responses
