from __future__ import annotations

from enum import Enum

from .. import (
    GeoComSubsystem,
    GeoComResponse
)
from ..communication import toenum


class TPS1200PMOT(GeoComSubsystem):
    class LOCKSTATUS(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PMOT.LOCKSTATUS:
            return cls(int(value))

        LOCKEDOUT = 0
        LOCKEDIN = 1
        PREDICTION = 2

    class STOPMODE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PMOT.STOPMODE:
            return cls(int(value))

        NORMAL = 0
        SHUTDOWN = 1

    class MODE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PMOT.MODE:
            return cls(int(value))

        POSIT = 0
        OCONST = 1
        MANUPOS = 2
        LOCK = 3
        BREAK = 4
        # 5, 6 do not use (why?)
        TERM = 7

    def read_lock_status(self) -> GeoComResponse:
        return self._request(
            6021,
            parsers={
                "status": self.LOCKSTATUS.parse
            }
        )

    def start_controller(
        self,
        mode: MODE | str = MODE.MANUPOS
    ) -> GeoComResponse:
        _mode = toenum(self.MODE, mode)
        return self._request(
            6001,
            [_mode.value]
        )

    def stop_controller(
        self,
        mode: STOPMODE | str = STOPMODE.NORMAL
    ) -> GeoComResponse:
        _mode = toenum(TPS1200PMOT.STOPMODE, mode)
        return self._request(
            6002,
            [_mode.value]
        )

    def set_velocity(
        self,
        horizontal: float,
        vertical: float
    ) -> GeoComResponse:
        horizontal = min(0.79, max(-0.79, horizontal))
        vertical = min(0.79, max(-0.79, vertical))
        return self._request(
            6004,
            [horizontal, vertical]
        )
