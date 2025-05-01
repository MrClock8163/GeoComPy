"""
Description
===========

Module: ``geocompy.tps1100.com``

Definitions for the TPS1100 Communication subsystem.

Types
-----

- ``TPS1100COM``

"""
from __future__ import annotations

from ..tps1000.com import TPS1000COM


class TPS1100COM(TPS1000COM):
    """
    Communication subsystem of the TPS1100 GeoCom protocol.

    This subsystem contains functions relevant to the communication
    with the instrument.

    """
