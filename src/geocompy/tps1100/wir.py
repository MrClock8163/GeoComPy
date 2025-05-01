"""
Description
===========

Module: ``geocompy.tps1100.wir``

Definitions for the TPS1100 Word Index registration subsystem.

Types
-----

- ``TPS1100WIR``

"""
from __future__ import annotations

from ..tps1000.wir import TPS1000WIR


class TPS1100WIR(TPS1000WIR):
    """
    Word Index registration subsystem of the TPS1100 GeoCom protocol.
    This subsystem is responsible for the GSI data recording operations.
    """
