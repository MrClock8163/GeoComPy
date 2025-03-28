from __future__ import annotations

from enum import Enum

from .. import (
    GeoComSubsystem,
    GeoComResponse
)
from ..communication import toenum
from ..data import Angle


class TPS1200PAUT(GeoComSubsystem):
    class POSMODE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PAUT.POSMODE:
            return cls(int(value))

        NORMAL = 0
        PRECISE = 1
        FAST = 2  # TS30 / MS30

    class ADJMODE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PAUT.ADJMODE:
            return cls(int(value))

        NORMAL = 0
        POINT = 1
        DEFINE = 2

    class ATRMODE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PAUT.ATRMODE:
            return cls(int(value))

        POSITION = 0
        TARGET = 1

    class DIRECTION(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PAUT.DIRECTION:
            return cls(int(value))

        CLOCKWISE = 1
        ANTICLOCKWISE = -1

    def read_tol(self) -> GeoComResponse:
        return self._request(
            9008,
            parsers={
                "hz": Angle.parse,
                "v": Angle.parse
            }
        )

    def set_tol(
        self,
        hz: Angle,
        v: Angle
    ) -> GeoComResponse:
        return self._request(9007, [hz, v])

    def read_timeout(self) -> GeoComResponse:
        return self._request(
            9012,
            parsers={
                "hz": float,
                "v": float
            }
        )

    def set_timeout(
        self,
        hz: float,
        v: float
    ) -> GeoComResponse:
        return self._request(
            9011,
            [hz, v]
        )

    def make_positioning(
        self,
        hz: Angle,
        v: Angle,
        posmode: POSMODE | str = POSMODE.NORMAL,
        atrmode: ATRMODE | str = ATRMODE.POSITION
    ) -> GeoComResponse:
        _posmode = toenum(self.POSMODE, posmode)
        _atrmode = toenum(self.ATRMODE, atrmode)
        return self._request(
            9027,
            [hz, v, _posmode.value, _atrmode.value, 0]
        )

    def change_face(
        self,
        posmode: POSMODE | str = POSMODE.NORMAL,
        atrmode: ATRMODE | str = ATRMODE.POSITION
    ) -> GeoComResponse:
        _posmode = toenum(self.POSMODE, posmode)
        _atrmode = toenum(self.ATRMODE, atrmode)
        return self._request(
            9028,
            [_posmode.value, _atrmode.value, 0]
        )

    def fine_adjust(
        self,
        width: Angle,
        height: Angle
    ) -> GeoComResponse:
        return self._request(
            9037,
            [width, height, 0]
        )

    def search(
        self,
        width: Angle,
        height: Angle
    ) -> GeoComResponse:
        return self._request(
            9029,
            [width, height, 0]
        )

    def get_fine_adjust_mode(self) -> GeoComResponse:
        return self._request(
            9030,
            parsers={
                "adjmode": self.ADJMODE.parse
            }
        )

    def set_fine_adjust_mode(
        self,
        adjmode: ADJMODE | str = ADJMODE.NORMAL
    ) -> GeoComResponse:
        _adjmode = toenum(self.ADJMODE, adjmode)
        return self._request(
            9031,
            [_adjmode.value]
        )

    def lock_in(self) -> GeoComResponse:
        return self._request(9013)

    def get_search_area(self) -> GeoComResponse:
        return self._request(
            9042,
            parsers={
                "hz": Angle.parse,
                "v": Angle.parse,
                "width": Angle.parse,
                "height": Angle.parse,
                "enabled": bool
            }
        )

    def set_search_area(
        self,
        hz: Angle,
        v: Angle,
        width: Angle,
        height: Angle,
        enabled: bool = True
    ) -> GeoComResponse:
        return self._request(
            9043,
            [hz, v, width, height, enabled]
        )

    def get_user_spiral(self) -> GeoComResponse:
        return self._request(
            9040,
            parsers={
                "width": Angle.parse,
                "height": Angle.parse
            }
        )

    def set_user_spiral(
        self,
        width: Angle,
        height: Angle
    ) -> GeoComResponse:
        return self._request(
            9041,
            [width, height]
        )

    def ps_enable_range(
        self,
        enable: bool
    ) -> GeoComResponse:
        return self._request(
            9048,
            [enable]
        )

    def ps_set_range(
        self,
        closest: int,
        farthest: int
    ) -> GeoComResponse:
        return self._request(
            9047,
            [closest, farthest]
        )

    def ps_search_window(self) -> GeoComResponse:
        return self._request(9052)

    def ps_search_next(
        self,
        direction: DIRECTION | str,
        swing: bool
    ) -> GeoComResponse:
        _direction = toenum(self.DIRECTION, direction)
        return self._request(
            9051,
            [_direction.value, swing]
        )
