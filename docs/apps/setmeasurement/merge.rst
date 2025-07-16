Merge
=====

.. code-block:: shell
    :caption: Invoking the application

    geocom sets merge -h

.. caution::
    :class: warning

    The set measurement merging command requires
    `Click Extra <https://pypi.org/project/click-extra/>`_,
    `jsonschema <https://pypi.org/project/jsonschema/>`_ and
    `jmespath <https://pypi.org/project/jmespath/>`_ to be installed.

    Install them manually, or install GeoComPy with the ``apps`` extra.

    .. code-block:: shell

        pip install geocompy[apps]

Usage
-----

.. click:: geocompy.apps.setmeasurement.process:cli_merge
    :prog: merge