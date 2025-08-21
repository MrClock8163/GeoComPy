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

    from geocompy import GeoCom, open_serial


    with open_serial("COM1", timeout=10) as com:
        tps = GeoCom(com)

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

    from geocompy import GsiOnlineDNA, open_serial


    with open_serial("COM1", timeout=10) as com:
        level = GsiOnlineDNA(com)

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

All GSI Online commands return a
:class:`~geocompy.gsi.gsitypes.GsiOnlineResponse` object, that encapsulates
command metadata and the result of the request.

.. tip::

    The complete list of available commands and their documentations are
    available in their respective API documentation categories.

Logging
-------

For debugging purposes it might be very useful to have a log of certain events,
errors and debug information. To support this, the instrument classes all take
an optional :class:`~logging.Logger` object, that they use to log specific
events.

.. code-block:: python
    :caption: Passing a console logger
    :linenos:

    from sys import stdout
    from logging import getLogger, DEBUG, StreamHandler

    from geocompy import GsiOnlineDNA, open_serial


    logger = getLogger("TPS")
    logger.addHandler(StreamHandler(stdout))
    logger.setLevel(DEBUG)
    with open_serial("COM1", timeout=15) as com:
        level = GsiOnlineDNA(com, logger)

Some examples of the information logged on various levels:

- connection start
- instrument wake up
- instrument shutdown
- all unexpected exceptions
- all command responses

Error handling and development
------------------------------

As described in the previous sections, under normal conditions, all commands
return response wrapper objects. If an error occured it is indicated by the
error code in the response object and/or the lack of parsed parameters. These
errors have to be explicitly handled in the application.

.. caution::
    :class: warning

    The error codes have descriptive names, that usually give some clue
    about the nature of the issue. One caveat is, that the response parser
    returns the ``UNDEFINED`` code not just when that was actually received,
    but also when an unknown error code was received. One example of this is
    error code ``30``, which can be seen in the wild, but is not documented
    anywhere. The response wrapper will contain ``UNDEFINED`` in cases like
    this.

The simplest solution is to check if the error code is simply ``OK``:

.. code-block:: python

    response = tps.ftr.setup_listing()
    if response.error != GeoComCode.OK:
        # handle error

When static type checkers are involved, it might be necessary to check for both
the error code and the existence of the parsed parameters.

.. code-block:: python

    response = tps.ftr.setup_listing()
    if response.error != GeoComCode.OK or response.params is not None:
        # handle error

Different commands return different errors signaling the various issues.
Some errors might be recoverable, others might not be.

.. code-block:: python

    response = tps.aut.fine_adjust(1, 1)
    if response.error == GeoComCode.AUT_NOT_ENABLED:
        response = tps.aus.switch_user_atr(True)
        if response.error == GeoComCode.OK:
            reponse = tps.aut.fine_adjust(1, 1)
        else:
            print("Cannot activate ATR")
            exit(1)
    
    if response.error == GeoComCode.AUT_NO_TARGET:
        response_ps = tps.aut.powersearch_next('CLOCKWISE', True)
        if response_ps.error != GeoComCode.OK:
            print("Could not find target")
            exit(1)
        else:
            response = tps.aut.fine_adjust(1, 1)

    if response.error != GeoComCode.OK:
        print("ATR fine adjustment failed, and could not reackquire target")
        exit(1)

.. note::

    The command line programs implemented in the
    `Instrumentman <https://github.com/MrClock8163/Instrumentman>`_ package can
    be used as reference examples for development.
