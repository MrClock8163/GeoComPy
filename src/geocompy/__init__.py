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

Reexports
---------

``geocompy.data.Angle``
    Angle value primitive.

``geocompy.data.AngleUnit``
    Angle unit enum.

``geocompy.data.Vector``
    3D vector primitive.

``geocompy.data.Coordinate``
    3D coordinate primitive.

``geocompy.communication.open_serial``
    Serial connection context manager function.

``geocompy.communication.get_logger``
    Utility function to create logger objects.

``geocompy.protocols.GeoComResponse``
    GeoCom protocol response container.

``geocompy.protocols.GsiOnlineResponse``
    GSI Online protocol response container.

``geocompy.dna.DNA``
    DNA instrument implementation.

``geocompy.tps1000.TPS1000``
    TPS1000 instrument implementation.

``geocompy.tps1000.rc.TPS1000RC``
    TPS1000 GeoCom return codes.

``geocompy.tps1100.TPS1100``
    TPS1100 instrument implementation.

``geocompy.tps1100.rc.TPS1100RC``
    TPS1100 GeoCom return codes.

``geocompy.tps1200p.TPS1200P``
    TPS1200+ instrument implementation.

``geocompy.tps1200p.grc.TPS1200PGRC``
    TPS1200+ GeoCom return codes.

``geocompy.vivatps.VivaTPS``
    VivaTPS instrument implementation.

``geocompy.vivatps.grc.VivaTPSGRC``
    VivaTPS GeoCom return codes.

"""
try:
    from ._version import __version__
except Exception:
    __version__ = "0.0.0"  # Placeholder value for source installs

from .data import (  # noqa: F401
    Angle as Angle,
    AngleUnit as AngleUnit,
    Vector as Vector,
    Coordinate as Coordinate
)

from .communication import (  # noqa: F401
    open_serial as open_serial,
    get_logger as get_logger
)

from .protocols import (  # noqa: F401
    GeoComResponse as GeoComResponse,
    GsiOnlineResponse as GsiOnlineResponse
)

from .dna import DNA as DNA  # noqa: F401

from .tps1000 import TPS1000 as TPS1000  # noqa: F401
from .tps1000.rc import TPS1000RC as TPS1000RC  # noqa: F401
from .tps1100 import TPS1100 as TPS1100  # noqa: F401
from .tps1100.rc import TPS1100RC as TPS1100RC  # noqa: F401
from .tps1200p import TPS1200P as TPS1200P  # noqa: F401
from .tps1200p.grc import TPS1200PGRC as TPS1200PGRC  # noqa: F401
from .vivatps import VivaTPS as VivaTPS  # noqa: F401
from .vivatps.grc import VivaTPSGRC as VivaTPSGRC  # noqa: F401
