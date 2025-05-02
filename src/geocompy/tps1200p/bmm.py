"""
Description
===========

Module: ``geocompy.tps1200p.bmm``

Definitions for the TPS1200+ Basic man-machine interface subsystem.

Types
-----

- ``TPS1200PBMM``
"""
from __future__ import annotations

from ..tps1100.bmm import TPS1100BMM


class TPS1200PBMM(TPS1100BMM):
    """
    Basic man-machine interface subsystem of the TPS1200+ GeoCom protocol.

    This subsystem contains functions related to the operation of the
    keyboard, character sets and singalling devices.
    """
