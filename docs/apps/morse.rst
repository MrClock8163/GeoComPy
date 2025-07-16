Morse
=====

.. code-block:: shell
    :caption: Invoking the application

    geocom morse -h

.. caution::
    :class: warning

    The Morse application requires
    `Click Extra <https://pypi.org/project/click-extra/>`_ to be installed.

    Install it manually, or install GeoComPy with the ``apps`` extra.

    .. code-block:: shell

        pip install geocompy[apps]

The Morse CLI application is a (admittedly not very useful) demo program,
that relays a Morse encoded ASCII message through the speakers of a total
station. The signals are played with the man-machine interface beep signals
of the instrument.

Usage
-----

.. click:: geocompy.apps.morse:cli
    :prog: morse
