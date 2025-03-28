from __future__ import annotations

from enum import Enum

from ..tps1200p.com import TPS1200PCOM


class VivaTPSCOM(TPS1200PCOM):
    class STOPMODE(Enum):
        @classmethod
        def parse(cls, value: str) -> VivaTPSCOM.STOPMODE:
            return cls(int(value))

        SHUTDOWN = 0
        SLEEP = 1
        GUI = 4

    class STARTUPMODE(Enum):
        @classmethod
        def parse(cls, value: str) -> VivaTPSCOM.STARTUPMODE:
            return cls(int(value))

        LOCAL = 0
        REMOTE = 1
        GUI = 2
