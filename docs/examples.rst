Examples
========

Below are documented some example programs that were developed for the
package.

Morse
-----

This is a very basic (and not very practical) example of using the man-machine
interface beep signals of a TPS1200+ instrument to encode and relay an ASCII
message in Morse code.

.. code-block:: text

    usage: morse.py [-h] [-b BAUD] [-t TIMEOUT] port intensity message

    positional arguments:
      intensity             beep intensity [1-100]
      message               message to encode

    options:
      -h, --help            show this help message and exit

    communication:
      port                  serial port
      -b BAUD, --baud BAUD  communication speed
      -t TIMEOUT, --timeout TIMEOUT
                            communication timeout

.. seealso::

    `morse.py <https://github.com/MrClock8163/GeoComPy/blob/main/examples/morse.py>`_
        CLI script
