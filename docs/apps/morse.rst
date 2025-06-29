Morse
=====

.. versionadded:: 0.7.0

.. code-block:: shell
    :caption: Invoking the application

    python -m geocompy.apps.morse

The Morse CLI application is a (admittedly not very useful) demo program,
that relays a Morse encoded ASCII message through the speakers of a total
station. The signals are played with the man-machine interface beep signals
of the instrument.

Usage
-----

.. argparse::
    :module: geocompy.apps.morse
    :func: cli
