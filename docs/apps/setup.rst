Targets
=======

.. code-block:: shell
    :caption: Invoking the application

    geocom targets -h

.. caution::
    :class: warning

    The Setup application requires
    `Click Extra <https://pypi.org/project/click-extra/>`_ to be installed.

    Install it manually, or install GeoComPy with the ``apps`` extra.

    .. code-block:: shell

        pip install geocompy[apps]

Automated measurement tasks need a target list definition. The Setup
application can be used to create this target list. Targets can be either
measured in an interactive program, or imported as coordinates from existing
files.

.. note::

    A station setup and orientation must be in the same system as the
    targets. If there is no predefined coordinate system, an arbitrary
    local, station centered setup can be used as well.

Usage
-----

.. click:: geocompy.apps.setup:cli
    :prog: targets

.. click:: geocompy.apps.setup:cli_import
    :prog: import

.. click:: geocompy.apps.setup:cli_measure
    :prog: measure
