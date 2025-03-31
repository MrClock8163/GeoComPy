"""
``geocompy.vivatps.com``
=========================

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
        @classmethod
        def parse(cls, value: str) -> VivaTPSCOM.STOPMODE:
            """
            Parses enum member from serialized enum value.

            Parameters
            ----------
            value : str
                Serialized enum value.

            Returns
            -------
            ~VivaTPSCOM.STOPMODE
                Parsed enum member.
            """
            return cls(int(value))

        SHUTDOWN = 0
        SLEEP = 1
        GUI = 4

    class STARTUPMODE(Enum):
        @classmethod
        def parse(cls, value: str) -> VivaTPSCOM.STARTUPMODE:
            """
            Parses enum member from serialized enum value.

            Parameters
            ----------
            value : str
                Serialized enum value.

            Returns
            -------
            ~VivaTPSCOM.STARTUPMODE
                Parsed enum member.
            """
            return cls(int(value))

        LOCAL = 0
        REMOTE = 1
        GUI = 2
