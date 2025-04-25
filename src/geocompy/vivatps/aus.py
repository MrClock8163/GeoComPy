"""
Description
===========

Module: ``geocompy.vivatps.aus``

Definitions for the VivaTPS Alt user subsystem.

Types
-----

- ``VivaTPSAUS``

"""
from __future__ import annotations

from ..tps1200p.aus import TPS1200PAUS


class VivaTPSAUS(TPS1200PAUS):
    """
    Alt user subsystem of the VivaTPS GeoCom protocol.

    This subsystem can be used to set and query the ATR and LOCK
    automation modes.

    """
