"""
Description
===========

Module: ``geocompy.tps1100.sup``

Definitions for the TPS1100 Supervisor subsystem.

Types
-----

- ``TPS1100SUP``

"""
from __future__ import annotations

from ..tps1000.sup import TPS1000SUP


class TPS1100SUP(TPS1000SUP):
    """
    Supervisor subsystem of the TPS1100 GeoCom protocol.

    This subsystem controls the continuous operation of the system, and it
    allows to automatically display status information.

    """
