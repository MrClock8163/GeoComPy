Interactive Terminal
====================

.. caution::
    :class: warning

    The Interactive Terminal requires
    `Textual <https://pypi.org/project/textual/>`_ and
    `RapidFuzz <https://pypi.org/project/RapidFuzz/>`_ to be installed.

    Install them manually, or install GeoComPy with the ``terminal`` extra.

    .. code-block:: shell

        pip install geocompy[terminal]

The interactive terminal is a TUI application for testing and
experimentation purposes. It allows to connect to an instrument, and
issue any of the available commands. The responses are displayed in a log
format.

.. only:: html

    .. image:: terminal_screenshot.svg

Usage
-----

.. code-block:: shell
    
    python -m geocompy.apps.terminal
