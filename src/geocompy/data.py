from __future__ import annotations

import re
import math
from enum import Enum, auto
from typing import TypeAlias, Literal


RO = 180 * 60 * 60 / math.pi
"""RAD-SEC conversion coefficient"""

PI2 = 2 * math.pi
"""Full angle in RAD"""


class AngleUnit(Enum):
    RAD = auto()
    """Radians"""

    DEG = auto()
    """Degrees"""

    PDEG = auto()
    """Pseudo-degrees (DDD.MMSS)"""

    GON = auto()
    """Gradians"""

    MIL = auto()
    """NATO milliradians (6400 mils per circle)"""

    SEC = auto()
    """Arcseconds"""

    DMS = auto()
    """DDD-MM-SS"""

    NMEA = auto()
    """NMEA degrees (DDDMM.NNNNNN)"""


_AngleUnitLike: TypeAlias = (
    AngleUnit
    | Literal['RAD', 'DEG', 'PDEG', 'GON', 'MIL', 'SEC', 'DMS', 'NMEA']
)


class Angle:
    @staticmethod
    def deg2rad(angle: float) -> float:
        """Converts degrees to radians.
        """
        return math.radians(angle)

    @staticmethod
    def gon2rad(angle: float) -> float:
        """Converts gradians to radians.
        """
        return angle / 200 * math.pi

    @staticmethod
    def dms2rad(dms: str) -> float:
        """Converts DDD-MM-SS to radians.
        """
        if not re.search(r"^[0-9]{1,3}(-[0-9]{1,2}){0,2}$", dms):
            raise ValueError("Angle invalid argument", dms)

        items = [float(item) for item in dms.split("-")]
        div = 1
        a = 0.0
        for val in items:
            a += val / div
            div *= 60

        return math.radians(a)

    @staticmethod
    def dm2rad(angle: float) -> float:
        """Converts DDDMM.NNNNNN NMEA angle to radians.
        """
        w = angle / 100
        d = int(w)
        return math.radians(d + (w - d) * 100 / 60)

    @staticmethod
    def pdeg2rad(angle: float) -> float:
        """Converts DDD.MMSS to radians.
        """
        d = math.floor(angle)
        angle = round((angle - d) * 100, 10)
        m = math.floor(angle)
        s = round((angle - m) * 100, 10)
        return math.radians(d + m / 60 + s / 3600)

    @staticmethod
    def sec2rad(angle: float) -> float:
        """Converts arcseconds to radians.
        """
        return angle / RO

    @staticmethod
    def mil2rad(angle: float) -> float:
        """Converts NATO mils to radians.
        """
        return angle / 6400 * 2 * math.pi

    @staticmethod
    def rad2gon(angle: float) -> float:
        """Converts radians to gradians.
        """
        return angle / math.pi * 200

    @staticmethod
    def rad2sec(angle: float) -> float:
        """Converts radians to arcseconds.
        """
        return angle * RO

    @staticmethod
    def rad2deg(angle: float) -> float:
        """Converts radians to degrees.
        """
        return math.degrees(angle)

    @staticmethod
    def rad2dms(angle: float) -> str:
        """Converts radians to DDD-MM-SS.
        """
        signum = "-" if angle < 0 else ""
        secs = round(abs(angle) * RO)
        mi, sec = divmod(secs, 60)
        deg, mi = divmod(mi, 60)
        deg = int(deg)
        return f"{signum:s}{deg:d}-{mi:02d}-{sec:02d}"

    @staticmethod
    def rad2dm(angle: float) -> float:
        """Converts radians to NMEA DDDMM.NNNNNNN.
        """
        w = angle / math.pi * 180.0
        d = int(w)
        return d * 100 + (w - d) * 60

    @staticmethod
    def rad2pdeg(angle: float) -> float:
        """Converts radians to DDD.MMSS.
        """
        secs = round(angle * RO)
        mi, sec = divmod(secs, 60)
        deg, mi = divmod(mi, 60)
        deg = int(deg)
        return deg + mi / 100 + sec / 10000

    @staticmethod
    def rad2mil(angle: float) -> float:
        """Converts radian to NATO mils.
        """
        return angle / math.pi / 2 * 6400

    @staticmethod
    def normalize_rad(angle: float, positive: float = False) -> float:
        """Normalizes angle to [+2PI; -2PI] range.
        """
        norm = angle % PI2

        if not positive and angle < 0:
            norm -= PI2

        return norm

    @classmethod
    def parse(cls, string: str) -> Angle:
        return Angle(float(string))

    def __init__(
        self,
        value: float | str,
        unit: _AngleUnitLike = AngleUnit.RAD,
        /,
        normalize: bool = False,
        positive: bool = False
    ):
        self._value: float = 0

        match unit, value:
            case AngleUnit.RAD | 'RAD', float() | int():
                self._value = value
            case AngleUnit.DEG | 'DEG', float() | int():
                self._value = self.deg2rad(value)
            case AngleUnit.PDEG | 'PDEG', float() | int():
                self._value = self.pdeg2rad(value)
            case AngleUnit.GON | 'GON', float() | int():
                self._value = self.gon2rad(value)
            case AngleUnit.MIL | 'MIL', float() | int():
                self._value = self.mil2rad(value)
            case AngleUnit.SEC | 'SEC', float() | int():
                self._value = self.sec2rad(value)
            case AngleUnit.DMS | 'DMS', str():
                self._value = self.dms2rad(value)
            case AngleUnit.NMEA | 'NMEA', float() | int():
                self._value = self.dm2rad(value)
            case _:
                raise ValueError(f"unknown source unit and value type pair: {unit} - {type(value).__name__}")

        if normalize:
            self._value = self.normalize_rad(self._value, positive)

    def __str__(self) -> str:
        return f"{self.asunit(AngleUnit.DEG):.4f} DEG"

    def __repr__(self) -> str:
        return f"{type(self).__name__:s}({self.asunit(AngleUnit.DMS):s})"

    def __pos__(self) -> Angle:
        return Angle(self._value)

    def __neg__(self) -> Angle:
        return Angle(-self._value)

    def __add__(self, other: Angle) -> Angle:
        if type(other) is not Angle:
            raise TypeError(f"unsupported operand type(s) for +: 'Angle' and '{type(other).__name__}'")

        return Angle(self._value + other._value)

    def __iadd__(self, other: Angle) -> Angle:
        if type(other) is not Angle:
            raise TypeError(f"unsupported operand type(s) for +=: 'Angle' and '{type(other).__name__}'")

        self._value += other._value
        return self

    def __sub__(self, other: Angle) -> Angle:
        if type(other) is not Angle:
            raise TypeError(f"unsupported operand type(s) for -: 'Angle' and '{type(other).__name__}'")

        return Angle(self._value - other._value)

    def __isub__(self, other: Angle) -> Angle:
        if type(other) is not Angle:
            raise TypeError(f"unsupported operand type(s) for -=: 'Angle' and '{type(other).__name__}'")

        self._value -= other._value
        return self

    def __mul__(self, other: int | float) -> Angle:
        if type(other) not in (int, float):
            raise TypeError(f"unsupported operand type(s) for *: 'Angle' and '{type(other).__name__}'")

        return Angle(self._value * other)

    def __imul__(self, other: int | float) -> Angle:
        if type(other) not in (int, float):
            raise TypeError(f"unsupported operand type(s) for *=: 'Angle' and '{type(other).__name__}'")

        self._value *= other
        return self

    def __truediv__(self, other: int | float) -> Angle:
        if type(other) not in (int, float):
            raise TypeError(f"unsupported operand type(s) for /: 'Angle' and '{type(other).__name__}'")

        return Angle(self._value / other)

    def __itruediv__(self, other: int | float) -> Angle:
        if type(other) not in (int, float):
            raise TypeError(f"unsupported operand type(s) for /=: 'Angle' and '{type(other).__name__}'")

        self._value /= other
        return self

    def __abs__(self) -> Angle:
        return self.normalized()

    def __float__(self) -> float:
        return float(self._value)

    def asunit(self, unit: _AngleUnitLike = AngleUnit.RAD) -> float | str:
        """Returns the value of the angle in the target unit.
        """
        match unit:
            case AngleUnit.RAD | 'RAD':
                return self._value
            case AngleUnit.DEG | 'DEG':
                return self.rad2deg(self._value)
            case AngleUnit.PDEG | 'PDEG':
                return self.rad2pdeg(self._value)
            case AngleUnit.GON | 'GON':
                return self.rad2gon(self._value)
            case AngleUnit.MIL | 'MIL':
                return self.rad2mil(self._value)
            case AngleUnit.SEC | 'SEC':
                return self.rad2sec(self._value)
            case AngleUnit.DMS | 'DMS':
                return self.rad2dms(self._value)
            case AngleUnit.NMEA | 'NMEA':
                return self.rad2dm(self._value)
            case _:
                raise ValueError(f"unknown target unit: {unit}")

    def normalized(self, positive: bool = True) -> Angle:
        """Returns a copy of the angle normalized to full angle.
        """
        return Angle(self._value, AngleUnit.RAD, True, positive)


class Byte:
    def __init__(self, value: int):
        if not (0 <= value <= 255):
            raise ValueError(
                f"bytes must fall in the 0-255 range, got: {value}"
            )

        self._value: int = value

    def __str__(self) -> str:
        return f"'{format(self._value, '02X')[-2:]}'"

    def __repr__(self) -> str:
        return str(self)

    def __int__(self) -> int:
        return self._value

    @classmethod
    def parse(cls, string: str) -> Byte:
        if string[0] == string[-1] == "'":
            string = string[1:-1]

        value = int(string, base=16)
        return cls(value)


class Coordinate:
    def __init__(self, x: float, y: float, z: float):
        self.x: float = x
        self.y: float = y
        self.z: float = z

    def __str__(self) -> str:
        return f"Coordinate({self.x}, {self.y}, {self.z})"

    def __repr__(self) -> str:
        return str(self)

    def __iter__(self):
        return iter([self.x, self.y, self.z])

    def __getitem__(self, idx: int) -> float:
        if idx < 0 or idx > 2:
            raise ValueError(f"index out of valid 0-2 range, got: {idx}")

        coords = (self.x, self.y, self.z)
        return coords[idx]
