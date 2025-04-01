"""
``geocompy.data``
=================

The data module provides utility functions and classes for serializing
and deserializing data in the serial communication.

Functions
---------

- ``parsestr``
- ``toenum``

Types
-----

- ``AngleUnit``
- ``Angle``
- ``Byte``
- ``Coordinate``

"""
from __future__ import annotations

import re
import math
from enum import Enum
from typing import (
    TypeAlias,
    Literal,
    Callable
)


_RO = 180 * 60 * 60 / math.pi
"""RAD-SEC conversion coefficient"""

_PI2 = 2 * math.pi
"""Full angle in RAD"""


def parsestr(value: str) -> str:
    """
    Returns a string value with the inclosing quote marks (``"..."``)
    removed.

    Parameters
    ----------
    value : str
        A string value read from the communication with
        an instrument.

    Returns
    -------
    str
        String suitable for further processing.

    Notes
    -----
    When a string value is read from an instrument connection, the
    string is enclosed quotes to indicated the data type. This is a
    simple convenience function to strip them.
    """
    return value[1:-1]


def toenum[T: Enum](e: type[T], value: T | str) -> T:
    """
    Returns the member of an :class:`~enum.Enum` with the given name.

    If the passed value is already a member instance, the function
    returns it without modification.

    Parameters
    ----------
    e : ~enum.Enum
        Enum type to search for member.
    value : ~enum.Enum | str
        The member or the name of the member to return.

    Returns
    -------
    ~enum.Enum
        Enum member instance.

    Examples
    --------
    >>> from enum import Enum
    >>> 
    >>> class MyEnum(Enum):
    ...     ONE = 1
    ...     TWO = 2
    >>>
    >>> gc.data.toenum(MyEnum, 'ONE')
    <MyEnum.ONE: 1>
    >>> gc.data.toenum(MyEnum, MyEnum.TWO)
    <MyEnum.TWO: 2>
    """
    if isinstance(value, str):
        return e[value]
    
    if value not in e:
        raise ValueError(
            f"given member ({value}) is not a member "
            f"of the target enum: {e}"
        )
    
    return value


def enumparser[T: Enum](e: type[T]) -> Callable[[str], T]:
    """
    Returns a parser function that can parse the target enum from the
    serialized enum value.

    Parameters
    ----------
    e: ~enum.Enum
        Target enum type.
    
    Returns
    -------
    Callable[[str], ~enum.Enum]
        Parser function, that takes a string as input, and returns an
        enum member.
    
    Examples
    --------

    >>> from enum import Enum
    >>> 
    >>> class MyEnum(Enum):
    ...     ONE = 1
    ...     TWO = 2
    >>>
    >>> parser = gc.data.enumparser(MyEnum)
    >>> parser('1')
    <MyEnum.ONE: 1>

    """
    def parseenum(value: str) -> T:
        return e(int(value))
    
    return parseenum


class AngleUnit(Enum):
    """
    Angle measurement units to indicate the unit of an :class:`Angle`
    instance.

    See Also
    --------
    Angle

    """
    RAD = 1
    """Radians"""

    DEG = 2
    """Degrees"""

    PDEG = 3
    """Pseudo-degrees (DDD.MMSS)"""

    GON = 4
    """Gradians"""

    MIL = 5
    """NATO milliradians (6400 mils per circle)"""

    SEC = 6
    """Arcseconds"""

    DMS = 7
    """DDD-MM-SS"""

    NMEA = 8
    """NMEA degrees (DDDMM.NNNNNN)"""


_AngleUnitLike: TypeAlias = (
    AngleUnit
    | Literal['RAD', 'DEG', 'PDEG', 'GON', 'MIL', 'SEC', 'DMS', 'NMEA']
)


class Angle:
    """
    Utility type to represent an angular value.

    Supported arithmetic operations:
        - \\+ `Angle`
        - \\- `Angle`
        - `Angle` + `Angle`
        - `Angle` - `Angle`
        - `Angle` * number (:class:`int` | :class:`float`)
        - `Angle` / number (:class:`int` | :class:`float`)

    Notes
    -----
    An `Angle` can be instantiated from a number of units,
    and can be converted to any other unit, but internally it is always
    represented in radians.

    See Also
    --------
    AngleUnit

    """

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
        return angle / _RO

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
        return angle * _RO

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
        secs = round(abs(angle) * _RO)
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
        secs = round(angle * _RO)
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
    def normalize_rad(angle: float, positive: bool = False) -> float:
        """Normalizes angle to [+2PI; -2PI] range.

        Parameters
        ----------
        angle : float
            Angular value in radians unit.
        positive : bool, optional
            Normalize to [0; +2PI] range, by default False

        Returns
        -------
        float
            Normalized angular value.
        """
        norm = angle % _PI2

        if not positive and angle < 0:
            norm -= _PI2

        return norm

    @classmethod
    def parse(cls, string: str) -> Angle:
        """Parses string value to float and creates new `Angle`.

        Parameters
        ----------
        string : str
            Floating point number to parse.

        Returns
        -------
        Angle

        """
        return Angle(float(string))

    def __init__(
        self,
        value: float | str,
        unit: _AngleUnitLike = AngleUnit.RAD,
        /,
        normalize: bool = False,
        positive: bool = False
    ):
        """
        Parameters
        ----------
        value : float | str
            Angular value to represent.
        unit : AngleUnit | str, optional
            Unit of the source value, by default AngleUnit.RAD
        normalize : bool, optional
            Normalize angle to +/- full angle, by default False
        positive : bool, optional
            Normalize angle only to positive, by default False

        Raises
        ------
        ValueError
            If an unknown `unit` was passed.
        """
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
        """
        Returns the represented angle in the target unit.

        Parameters
        ----------
        unit : AngleUnit | str, optional
            Target unit, by default AngleUnit.RAD

        Returns
        -------
        float | str
            Angular value.

        Raises
        ------
        ValueError
            If an unknown `unit` was passed
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
        """
        Returns a copy of the angle normalized to full angle.

        Parameters
        ----------
        positive : bool, optional
            Normalize to [0; +2PI] range, by default True

        Returns
        -------
        Angle
            New `Angle` with normalized value.
        """
        return Angle(self._value, AngleUnit.RAD, True, positive)


class Byte:
    """
    Utility type to represent a single byte value.

    The main purpose of this class is to help the parsing and formatting
    of byte values during the handling of serial communication.

    Examples
    --------

    Creating, then "serializing" a `Byte`:

    >>> b = gc.data.Byte(17)
    >>> print(b)
    '11'

    Parsing a `Byte` from the serialized representation:

    >>> value = "'11'"
    >>> b = gc.data.Byte.parse(value)

    """

    def __init__(self, value: int):
        """
        Parameters
        ----------
        value : int
            Number to represent.

        Raises
        ------
        ValueError
            If the passed value is outside the [0; 255] range.

        """
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
        """
        Parses `Byte` from string representation.

        Parameters
        ----------
        string : str
            Byte value represented as 2 digit hexadecimal string
            in single quotes (').

        Returns
        -------
        Byte

        Examples
        --------

        >>> value = "'1A'" # value read from serial line
        >>> b = gc.data.Byte.parse(value)

        """
        if string[0] == string[-1] == "'":
            string = string[1:-1]

        value = int(string, base=16)
        return cls(value)


class Coordinate:
    """
    Utility type to represent a position with 3D cartesian coordinates.

    Examples
    --------

    Creating new coordinate and accessing components:

    >>> c = gc.data.Coordinate(1, 2, 3)
    >>> print(c)
    Coordinate(1.0, 2.0, 3.0)
    >>> c.x
    1.0
    >>> c[1]
    2.0
    >>> x, y, z = c
    >>> z
    3.0

    """

    def __init__(self, x: float, y: float, z: float):
        """
        Parameters
        ----------
        x : float
            X component (often easting)
        y : float
            Y component (often northing)
        z : float
            Z component (often height/up)

        """
        self.x: float = x
        self.y: float = y
        self.z: float = z

    def __str__(self) -> str:
        return f"Coordinate({self.x:f}, {self.y:f}, {self.z:f})"

    def __repr__(self) -> str:
        return str(self)

    def __iter__(self):
        return iter([self.x, self.y, self.z])

    def __getitem__(self, idx: int) -> float:
        if idx < 0 or idx > 2:
            raise ValueError(f"index out of valid 0-2 range, got: {idx}")

        coords = (self.x, self.y, self.z)
        return coords[idx]
