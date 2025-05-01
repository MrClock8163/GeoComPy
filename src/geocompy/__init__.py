"""
GeoComPy
========

Python wrapper functions for communicating with surveying
instruments over a serial connection.

The implementations use the Leica GeoCom ASCII RPC procotol primarily.
For older instruments, that do not support it, the GSI Online commands
are used instead.

The package provides
    1. Utility data types for handling instrument responses
    2. Instrument software specific low level commands

Documentation
-------------

Public classes and methods are provided with proper docstrings, that can
be viewed in the source code, through introspection tools or editor
utilities. The docstrings follow the NumPy style conventions. In addition
to the in-code documentation, a complete, rendered reference is avaialable
on the `GeoComPy documentation <https://geocompy.readthedocs.io>`_ site.

Some docstrings provide examples. These examples assume that `geocompy`
has been imported as ``gc``:

    >>> import geocompy as gc

Subpackages
-----------

``geocompy.tps1000``
    Communication with instruments running TPS1000 software.

``geocompy.tps1100``
    Communication with instruments running TPS1100 software.

``geocompy.tps1200p``
    Communication with instruments running TPS1200(+) software.

``geocompy.vivatps``
    Communication with instruments running Viva(/Nova)TPS software.

``geocompy.dna``
    Communication with DNA digital level instruments.

Submodules
----------

``geocompy.data``
    Utilities for data handling.

``geocompy.communication``
    Communication methods.

``geocompy.protocols``
    Base definitions for command protocols and responses.

"""
try:
    from ._version import __version__
except Exception:
    __version__ = "0.0.0"  # Placeholder value for source installs
