GeoCom Test
===========

.. versionadded:: 0.8.0

.. code-block:: shell
    :caption: Invoking the application

    python -m geocompy.apps.geocomtest

Simple application, that runs rudimentary tests to see what GeoCom functions
are available on an instrument. The tests are conducted by attempting to
execute related GeoCom commands.

.. warning::
    :class: warning

    Some instrument settings might be changed during the tests. Make sure
    to check and correct the settings, before using the instrument again!

Usage
-----

.. argparse::
    :module: geocompy.apps.geocomtest
    :func: cli
