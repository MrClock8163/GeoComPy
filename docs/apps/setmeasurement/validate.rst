Validate
========

.. code-block:: shell
    :caption: Invoking the application

    geocom sets validate -h

.. caution::
    :class: warning

    The set measurement validate command requires
    `Click Extra <https://pypi.org/project/click-extra/>`_,
    `jsonschema <https://pypi.org/project/jsonschema/>`_ and
    `jmespath <https://pypi.org/project/jmespath/>`_ to be installed.

    Install them manually, or install GeoComPy with the ``apps`` extra.

    .. code-block:: shell

        pip install geocompy[apps]

Usage
-----

.. click:: geocompy.apps.setmeasurement.process:cli_validate
    :prog: validate