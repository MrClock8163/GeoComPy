"""
``geocompy.vivatps.mot``
=========================

Definitions for the VivaTPS Motorization subsystem.

Types
-----

- ``VivaTPSMOT``

"""
from __future__ import annotations

from ..tps1200p.mot import TPS1200PMOT


class VivaTPSMOT(TPS1200PMOT):
    """
    Motorization subsystem of the VivaTPS GeoCom protocol.

    This subsystem provides access to motoriztaion parameters and control.

    """
