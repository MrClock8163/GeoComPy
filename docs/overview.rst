Overview
========

This package provides "low-level" (i.e. the primary implementations do not
process data, only facilitate access to the raw commands) Python wrapper
functions for controlling various surveying instruments. GeoComPy is
primarily based on and uses the GeoCom ASCII command system (and
occasionally the GSI Online commands) of Leica products. Communication is
typically through a serial port.

Features
--------

- Pure Python implementation
- Serial communication handler
- Universal data types for communication
- Automatic serialization and deserialization of parameters
- Commands implemented from reference manuals

  .. only:: html

    - :si-icon:`protocol_gsionline` DNA
    - :si-icon:`protocol_gsionline` :si-icon:`protocol_geocom` LS
    - :si-icon:`protocol_geocom` TPS1000
    - :si-icon:`protocol_geocom` TPS1100
    - :si-icon:`protocol_geocom` TPS1200(+)
    - :si-icon:`protocol_geocom` VivaTPS

  .. only:: latex

    - DNA
    - LS
    - TPS1000
    - TPS1100
    - TPS1200(+)
    - VivaTPS

- Command line applications

Requirements
------------

- Python 3.11 or newer
- `pySerial <https://pyserial.readthedocs.io/>`_ package

Installation
------------

The installed package and subpackages can be imported from the
``geocompy`` root package.

.. code-block:: python
    :caption: Import example

    from geocompy.tps1200p import TPS1200P

As with any Python package, it might be advisable to install GeoComPy
in an isolated enviroment, like a virtual enviroment for more complex
projects.

From PyPI
^^^^^^^^^

GeoComPy is hosted on PyPI, therefore it can be installed with ``pip``.
Package dependencies are automatically handled.

.. code-block:: shell
    :caption: Installing from PyPI

    pip install geocompy

The dependencies of the CLI applications are not installed by default.
These either have to be installed manually, or GeoComPy has to be
installed with the ``apps`` extra.

.. code-block:: shell
    :caption: Installing from PyPI with CLI app dependencies included

    pip install geocompy[apps]

From source
^^^^^^^^^^^

Download the release archive from
`PyPI <https://pypi.org/project/geocompy/>`_, or from 
`GitHub releases <https://github.com/MrClock8163/GeoComPy/releases>`_.
Unpack the archive to a suitable place, and enter the ``geocompy-x.y.z``
directory. Build and install the package with the following command:

.. code-block:: shell
    :caption: Building and installing locally

    python -m pip install .
