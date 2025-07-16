Calculate
=========

.. code-block:: shell
    :caption: Invoking the application

    geocom sets calc -h

.. caution::
    :class: warning

    The set measurement calculation command requires
    `Click Extra <https://pypi.org/project/click-extra/>`_,
    `jsonschema <https://pypi.org/project/jsonschema/>`_ and
    `jmespath <https://pypi.org/project/jmespath/>`_ to be installed.

    Install them manually, or install GeoComPy with the ``apps`` extra.

    .. code-block:: shell

        pip install geocompy[apps]

Usage
-----

.. click:: geocompy.apps.setmeasurement.process:cli_calc
    :prog: calc
