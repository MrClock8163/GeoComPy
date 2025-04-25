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

from enum import Enum

from ..tps1200p.com import TPS1200PCOM


class VivaTPSCOM(TPS1200PCOM):
    """
    Communication subsystem of the VivaTPS GeoCom protocol.

    This subsystem contains functions relevant to the communication
    with the instrument.

    """
    class STOPMODE(Enum):
        SHUTDOWN = 0
        SLEEP = 1
        GUI = 4

    class STARTUPMODE(Enum):
        LOCAL = 0
        REMOTE = 1
        GUI = 2
