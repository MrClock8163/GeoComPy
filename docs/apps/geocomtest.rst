GeoCom Test
===========

.. code-block:: shell
    :caption: Invoking the application

    geocom test -h

Simple application, that runs rudimentary tests to see what GeoCom functions
are available on an instrument. The tests are conducted by attempting to
execute related GeoCom commands.

.. warning::
    :class: warning

    Some instrument settings might be changed during the tests. Make sure
    to check and correct the settings, before using the instrument again!

Usage
-----

.. click:: geocompy.apps.geocomtest:cli
    :prog: test
