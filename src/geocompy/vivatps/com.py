"""
Description
===========

Module: ``geocompy.vivatps.com``

Definitions for the VivaTPS Communication subsystem.

Types
-----

- ``VivaTPSCOM``

"""
from __future__ import annotations

from ..tps1200p.com import TPS1200PCOM


class VivaTPSCOM(TPS1200PCOM):
    """
    Communication subsystem of the VivaTPS GeoCom protocol.

    This subsystem contains functions relevant to the communication
    with the instrument.

    """
