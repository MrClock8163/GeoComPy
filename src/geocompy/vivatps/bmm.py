"""
``geocompy.vivatps.bmm``
=========================

Definitions for the VivaTPS Basic man-machine interface subsystem.

Types
-----

- ``VivaTPSBMM``

"""
from __future__ import annotations

from ..tps1200p.bmm import TPS1200PBMM


class VivaTPSBMM(TPS1200PBMM):
    """
    Basic man-machine interface subsystem of the VivaTPS GeoCom protocol.

    This subsystem contains functions related to the operation of the
    keyboard, character sets and singalling devices.

    """
