Interactive Terminal
====================

.. code-block:: shell
    :caption: Invoking the application

    geocom terminal

.. caution::
    :class: warning

    The Interactive Terminal requires
    `Textual <https://pypi.org/project/textual/>`_ and
    `RapidFuzz <https://pypi.org/project/RapidFuzz/>`_ to be installed.

    Install them manually, or install GeoComPy with the ``apps`` extra.

    .. code-block:: shell

        pip install geocompy[apps]

The interactive terminal is a TUI application for testing and
experimentation purposes. It allows to connect to an instrument, and
issue any of the available commands. The responses are displayed in a log
format.

.. only:: html

    .. image:: terminal_screenshot.svg
