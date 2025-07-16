Set Measurement
===============

.. code-block:: shell
    :caption: Invoking the application

    geocom sets -h

.. caution::
    :class: warning

    The Set Measurement application requires
    `Cloup <https://pypi.org/project/cloup/>`_,
    `Click Extra <https://pypi.org/project/click-extra/>`_,
    `jsonschema <https://pypi.org/project/jsonschema/>`_ and
    `jmespath <https://pypi.org/project/jmespath/>`_ to be installed.

    Install them manually, or install GeoComPy with the ``apps`` extra.

    .. code-block:: shell

        pip install geocompy[apps]

The set measurement CLI applications provide a simple way to conduct monitoring
measurements to a set of predefined target points, using a GeoCom capable
total station.

After set measurements are done, the results need to be processed. Thanks
to the easily usable JSON format, this can be done with custom scripts if
needed. For more general use cases, a few processing commands are available
here.

.. note::

    The various subcommands are available as CLI subcommands.

.. toctree::
    :maxdepth: 1

    calc
    merge
    validate
    measure
