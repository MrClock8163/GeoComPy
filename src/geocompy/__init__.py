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

``geocompy.geo``
    Communication through GeoCom protocol.

``geocompy.gsi``
    Communication through GSI Online protocol.

Submodules
----------

``geocompy.data``
    Utilities for data handling.

``geocompy.communication``
    Communication methods.

Reexports
---------

``geocompy.data.Angle``
    Angle value primitive.

``geocompy.data.Vector``
    3D vector primitive.

``geocompy.data.Coordinate``
    3D coordinate primitive.

``geocompy.communication.open_serial``
    Serial connection context manager function.

``geocompy.gsi.dna.GsiOnlineDNA``
    DNA instrument implementation.

``geocompy.gsi.gsitypes.GsiOnlineResponse``
    GSI Online protocol response container.

``geocompy.geo.GeoCom``
    GeoCom protocol handler.

``geocompy.geo.gctypes.GeoComCode``
    GeoCom return codes.

``geocompy.geo.gctypes.GeoComResponse``
    GeoCom protocol response container.
"""
try:
    from ._version import __version__ as __version__
except Exception:  # pragma: no coverage
    __version__ = "0.0.0"  # Placeholder value for source installs

from .data import (  # noqa: F401
    Angle as Angle,
    Vector as Vector,
    Coordinate as Coordinate
)

from .communication import open_serial as open_serial  # noqa: F401

from .gsi.gsitypes import GsiOnlineResponse as GsiOnlineResponse  # noqa: F401
from .gsi.dna import GsiOnlineDNA as GsiOnlineDNA  # noqa: F401

from .geo.gctypes import GeoComResponse as GeoComResponse  # noqa: F401
from .geo.gctypes import GeoComCode as GeoComCode  # noqa: F401
from .geo import GeoCom as GeoCom  # noqa: F401
