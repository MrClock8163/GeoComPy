"""
Description
===========

Module: ``geocompy.tps1100.ctl``

Definitions for the TPS1100 Control task subsystem.

Types
-----

- ``TPS1100CTL``

"""
from __future__ import annotations

from ..tps1000.ctl import TPS1000CTL


class TPS1100CTL(TPS1000CTL):
    """
    Control task subsystem of the TPS1100 GeoCom protocol.
    """
