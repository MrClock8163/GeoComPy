"""
Description
===========

Module: ``geocompy.tps1200p.edm``

Definitions for the TPS1200+ EDM subsystem.

Types
-----

- ``TPS1200PEDM``

"""
from __future__ import annotations

from ..tps1100.edm import TPS1100EDM


class TPS1200PEDM(TPS1100EDM):
    """
    Electronic distance measurement subsystem of the TPS1200+ GeoCom
    protocol.

    This subsystem provides access to control some of the EDM module
    functions.

    """
