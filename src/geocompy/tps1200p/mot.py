"""
Description
===========

Module: ``geocompy.tps1200p.mot``

Definitions for the TPS1200+ Motorization subsystem.

Types
-----

- ``TPS1200PMOT``

"""
from __future__ import annotations

from ..tps1100.mot import TPS1100MOT


class TPS1200PMOT(TPS1100MOT):
    """
    Motorization subsystem of the TPS1200+ GeoCom protocol.

    This subsystem provides access to motoriztaion parameters and control.

    """
