Morse
=====

.. versionadded:: 0.7.0

.. versionchanged:: 0.8.0
    The CLI is now based on Click and Click Extra

.. code-block:: shell
    :caption: Invoking the application

    python -m geocompy.apps.morse

The Morse CLI application is a (admittedly not very useful) demo program,
that relays a Morse encoded ASCII message through the speakers of a total
station. The signals are played with the man-machine interface beep signals
of the instrument.

Usage
-----

.. click:: geocompy.apps.morse:cli
    :prog: morse
