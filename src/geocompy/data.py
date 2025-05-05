"""
Description
===========

Module: ``geocompy.data``

The data module provides utility functions and classes for serializing
and deserializing data in the serial communication.

Functions
---------

- ``parsestr``
- ``parsebool``
- ``toenum``
- ``enumparser``
- ``gsiword``

Types
-----

- ``AngleUnit``
- ``Angle``
- ``Byte``
- ``Vector``
- ``Coordinate``
"""
from __future__ import annotations

import re
import math
from enum import Enum
from typing import (
    TypeAlias,
    Literal,
    Callable,
    TypeVar,
    Self
)


RO = 180 * 60 * 60 / math.pi
"""RAD-SEC conversion coefficient"""

PI2 = 2 * math.pi
"""Full angle in RAD"""

_E = TypeVar("_E", bound=Enum)


def parsestr(value: str) -> str:
    """
    Returns a string value with the enclosing quote marks (``"..."``)
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
    if value[0] == value[-1] == "\"":
        return value[1:-1]

    return value


def parsebool(value: str) -> bool:
    """
    Utility function to parse a serialized boolean value.

    Parameters
    ----------
    value : str
        Serialized value.

    Returns
    -------
    bool
        Parsed boolean.
    """
    return bool(int(value))


def toenum(e: type[_E], value: _E | str) -> _E:
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


def enumparser(e: type[_E]) -> Callable[[str], _E]:
    """
    Returns a parser function that can parse the target enum from the
    serialized enum value.

    Parameters
    ----------
    e: Enum
        Target enum type.

    Returns
    -------
    Callable
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
    def parseenum(value: str) -> _E:
        return e(int(value))

    return parseenum


def gsiword(
    wi: int,
    data: str,
    *,
    info: str = "",
    negative: bool = False,
    gsi16: bool = False
) -> str:
    """
    Constructs a GSI data word from the given parameters.

    Parameters
    ----------
    wi : int
        GSI word index.
    data : str
        Data, max 8 characters (or 16 for GSI16).
    info : str, optional
        Data information, max 4 characters (or 3 if ``wi`` is 3), by default ""
    negative : bool, optional
        Negative numerical data, by default False
    gsi16 : bool, optional
        Construct GSI16 instead of GSI8, by default False

    Returns
    -------
    str
        Constructed GSI word.

    Examples
    --------

    Simple point ID word:

    >>> gsiword(
    ...     11,
    ...     "A1"
    ... )
    11....+000000A1

    GSI16 inverted staff reading word:

    >>> gsiword(
    ...     330,
    ...     "123456",
    ...     info="08",
    ...     negative=True,
    ...     gsi16=True
    ... )
    *330.08-0000000000123456

    """
    if gsi16:
        data = f"{data.zfill(16):.16s}"
    else:
        data = f"{data.zfill(8):.8s}"

    sign = "-" if negative else "+"
    info = f"{info:.4s}"
    if len(info) < 4:
        idx = f"{str(wi):.3s}"
    else:
        idx = f"{str(wi):.2s}"
    padding = "." * (6 - len(idx) - len(info))
    mark = "*" if gsi16 else ""
    return f"{mark}{idx}{padding}{info}{sign}{data} "


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
        norm = angle % PI2

        if not positive and angle < 0:
            norm -= PI2

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
                raise ValueError(
                    f"unknown source unit and value type pair: "
                    f"{unit} - {type(value).__name__}"
                )

        if normalize:
            self._value = self.normalize_rad(self._value, positive)

    def __str__(self) -> str:
        return f"{self.asunit(AngleUnit.DEG):.4f} DEG"

    def __repr__(self) -> str:
        return f"{type(self).__name__:s}({self.asunit(AngleUnit.DMS):s})"

    def __eq__(self, other: object) -> bool:
        if type(other) is not Angle:
            return False

        return math.isclose(self._value, other._value)

    def __pos__(self) -> Angle:
        return Angle(self._value)

    def __neg__(self) -> Angle:
        return Angle(-self._value)

    def __add__(self, other: Angle) -> Angle:
        if type(other) is not Angle:
            raise TypeError(
                f"unsupported operand type(s) for +: 'Angle' and "
                f"'{type(other).__name__}'"
            )

        return Angle(self._value + other._value)

    def __sub__(self, other: Angle) -> Angle:
        if type(other) is not Angle:
            raise TypeError(
                f"unsupported operand type(s) for -: 'Angle' and "
                f"'{type(other).__name__}'"
            )

        return Angle(self._value - other._value)

    def __mul__(self, other: int | float) -> Angle:
        if type(other) not in (int, float):
            raise TypeError(
                f"unsupported operand type(s) for *: 'Angle' and "
                f"'{type(other).__name__}'"
            )

        return Angle(self._value * other)

    def __truediv__(self, other: int | float) -> Angle:
        if type(other) not in (int, float):
            raise TypeError(
                f"unsupported operand type(s) for /: 'Angle' and "
                f"'{type(other).__name__}'"
            )

        return Angle(self._value / other)

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


class Vector:
    """
    Utility type to represent a position with 3D cartesian coordinates.

    Supported arithmetic operations:
        - \\+ `Vector`
        - \\- `Vector`
        - `Vector` + `Vector`
        - `Vector` - `Vector`
        - `Vector` * number (`int` | `float`)
        - `Vector` / number (`int` | `float`)

    Examples
    --------

    Creating new vector and accessing components:

    >>> c = gc.data.Vector(1, 2, 3)
    >>> print(c)
    Vector(1.0, 2.0, 3.0)
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
            X component
        y : float
            Y component
        z : float
            Z component

        """
        self.x: float = x
        self.y: float = y
        self.z: float = z

    def __str__(self) -> str:
        return f"{type(self).__name__}({self.x:f}, {self.y:f}, {self.z:f})"

    def __repr__(self) -> str:
        return str(self)

    def __iter__(self):
        return iter([self.x, self.y, self.z])

    def __getitem__(self, idx: int) -> float:
        if idx < 0 or idx > 2:
            raise ValueError(f"index out of valid 0-2 range, got: {idx}")

        coords = (self.x, self.y, self.z)
        return coords[idx]

    def __eq__(self, other) -> bool:
        if type(other) is not type(self):
            return False

        return (
            math.isclose(self.x, other.x)
            and math.isclose(self.y, other.y)
            and math.isclose(self.z, other.z)
        )

    def __pos__(self) -> Self:
        return type(self)(
            self.x,
            self.y,
            self.z
        )

    def __neg__(self) -> Self:
        return type(self)(
            -self.x,
            -self.y,
            -self.z
        )

    def __add__(self, other: Self) -> Self:
        if type(other) is not type(self):
            raise TypeError(
                f"unsupported operand type(s) for +: "
                f"'{type(self).__name__}' and "
                f"'{type(other).__name__}'"
            )

        return type(self)(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )

    def __sub__(self, other: Self) -> Self:
        if type(other) is not type(self):
            raise TypeError(
                f"unsupported operand type(s) for -: "
                f"'{type(self).__name__}' and "
                f"'{type(other).__name__}'"
            )

        return type(self)(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        )

    def __mul__(self, other: int | float) -> Self:
        if type(other) not in (int, float):
            raise TypeError(
                f"unsupported operand type(s) for *: "
                f"'{type(self).__name__}' and "
                f"'{type(other).__name__}'"
            )

        return type(self)(
            self.x * other,
            self.y * other,
            self.z * other
        )

    def __truediv__(self, other: int | float) -> Self:
        if type(other) not in (int, float):
            raise TypeError(
                f"unsupported operand type(s) for /: "
                f"'{type(self).__name__}' and "
                f"'{type(other).__name__}'"
            )

        return type(self)(
            self.x / other,
            self.y / other,
            self.z / other
        )

    def length(self) -> float:
        """
        Calculates the length of the vector.

        Returns
        -------
        float
            Length of the vector.
        """
        return math.sqrt(
            math.fsum(
                (
                    self.x**2,
                    self.y**2,
                    self.z**2
                )
            )
        )

    def normalized(self) -> Self:
        """
        Returns a copy of the vector, normalized to unit length.

        Returns
        -------
        Self
            Normalized vector.
        """
        length = self.length()
        if length == 0:
            return +self

        return self / length


class Coordinate(Vector):
    """
    Utility type to represent a position with 3D cartesian coordinates.

    Supported arithmetic operations:
        - \\+ `Coordinate`
        - \\- `Coordinate`
        - `Coordinate` + `Coordinate`
        - `Coordinate` - `Coordinate`
        - `Coordinate` * number (`int` | `float`)
        - `Coordinate` / number (`int` | `float`)

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

    @classmethod
    def from_polar(
        cls,
        hz: Angle,
        v: Angle,
        dist: float
    ) -> Self:
        """
        Constructs 3D cartesian coordinate from polar coordinate.

        Parameters
        ----------
        hz : Angle
            Horizontal angle.
        v : Angle
            Vertical angle.
        dist : float
            Slope distance.

        Returns
        -------
        Coordinate
        """
        dist2d = math.sin(v) * dist
        x = math.sin(hz) * dist2d
        y = math.cos(hz) * dist2d
        z = math.cos(v) * dist

        return cls(x, y, z)

    def to_polar(self) -> tuple[Angle, Angle, float]:
        """
        Converts 3D cartesian coordinates to polar coordinates.

        Returns
        -------
        tuple
            Horizontal and vertical angles and slope distance.
        """
        dist2d = math.sqrt(self.x**2 + self.y**2)
        dist = math.sqrt(dist2d**2 + self.z**2)
        hz = math.atan2(self.x, self.y)
        v = math.atan2(dist2d, self.z)
        return (
            Angle(hz, normalize=True, positive=True),
            Angle(v, normalize=True, positive=True),
            dist
        )
