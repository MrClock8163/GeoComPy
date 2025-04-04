Overview
========


Requirements
------------

- Python 3.10 or newer
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

    pip install geocompy

From source
^^^^^^^^^^^

Download the release archive from
`PyPI <https://pypi.org/project/geocompy/>`_, or from 
`GitHub releases <https://github.com/MrClock8163/GeoComPy/releases>`_.
Unpack the archive to a suitable place, and enter the ``geocompy-x.y.z``
directory. Build and install the package with the following command:

.. code-block:: shell

    python -m build
