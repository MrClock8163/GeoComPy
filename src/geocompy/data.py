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
    Literal,
    Callable,
    Iterator,
    TypeVar,
    Self,
    Any,
    SupportsFloat
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


_AngleUnit = Literal['deg', 'rad', 'gon']


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
        if not re.search(r"^-?[0-9]{1,3}(-[0-9]{1,2}){0,2}(\.\d+)?$", dms):
            raise ValueError("Angle invalid argument", dms)

        if dms.startswith("-"):
            sign = -1
            dms = dms[1:]
        else:
            sign = 1

        items = [float(item) for item in dms.split("-")]
        div = 1
        a = 0.0
        for val in items:
            a += val / div
            div *= 60

        return math.radians(a) * sign

    @staticmethod
    def rad2gon(angle: float) -> float:
        """Converts radians to gradians.
        """
        return angle / math.pi * 200

    @staticmethod
    def rad2deg(angle: float) -> float:
        """Converts radians to degrees.
        """
        return math.degrees(angle)

    @staticmethod
    def rad2dms(angle: float, precision: int = 0) -> str:
        """Converts radians to DDD-MM-SS.
        """
        signum = "-" if angle < 0 else ""
        secs = round(abs(angle) * RO, precision)
        mi, sec = divmod(secs, 60)
        deg, mi = divmod(int(mi), 60)
        secstr = f"{{:.{precision}f}}".format(sec).zfill(
            precision + 3
            if precision > 0
            else 2
        )
        return f"{signum:s}{deg:d}-{mi:02d}-{secstr}"

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
    def parse(cls, string: str, unit: _AngleUnit = 'rad') -> Angle:
        """Parses string value to float and creates new `Angle`.

        Parameters
        ----------
        string : str
            Floating point number to parse.
        unit : Literal['deg', 'rad', 'gon'], optional
            Unit of the value to parse, by default 'rad'

        Returns
        -------
        Angle

        """
        return Angle(float(string), unit)

    def __init__(
        self,
        value: float,
        unit: _AngleUnit = 'rad',
        /,
        normalize: bool = False,
        positive: bool = False
    ):
        """
        Parameters
        ----------
        value : float
            Angular value to represent.
        unit : Literal['deg', 'rad', 'gon'], optional
            Unit of the source value, by default 'rad'
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

        match unit:
            case 'deg':
                self._value = self.deg2rad(value)
            case 'rad':
                self._value = float(value)
            case 'gon':
                self._value = self.gon2rad(value)
            case _:
                raise ValueError(f"unknown source unit: '{unit}'")

        if normalize:
            self._value = self.normalize_rad(self._value, positive)

    @classmethod
    def from_dms(cls, value: str) -> Angle:
        """
        Parses angle from DMS notation.

        Parameters
        ----------
        value : str
            DMS angle to parse.

        Returns
        -------
        Angle
        """
        return Angle(cls.dms2rad(value))

    def __float__(self) -> float:
        return self._value

    def __str__(self) -> str:
        return f"{self.asunit('deg'):.4f} DEG"

    def __repr__(self) -> str:
        return f"{type(self).__name__:s}({self.to_dms():s})"

    def __format__(self, format_spec: str) -> str:
        return format(self._value, format_spec)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, SupportsFloat):
            return False

        return self._value == float(other)

    def __gt__(self, other: SupportsFloat) -> bool:
        if not isinstance(other, SupportsFloat):
            return NotImplemented

        return float(self) > float(other)

    def __lt__(self, other: SupportsFloat) -> bool:
        if not isinstance(other, SupportsFloat):
            return NotImplemented

        return float(self) < float(other)

    def __ge__(self, other: SupportsFloat) -> bool:
        if not isinstance(other, SupportsFloat):
            return NotImplemented

        return float(self) >= float(other)

    def __le__(self, other: SupportsFloat) -> bool:
        if not isinstance(other, SupportsFloat):
            return NotImplemented

        return float(self) <= float(other)

    def __pos__(self) -> Self:
        return type(self)(self._value)

    def __neg__(self) -> Self:
        return type(self)(-self._value)

    def __add__(self, other: SupportsFloat) -> Self:
        if not isinstance(other, SupportsFloat):
            return NotImplemented

        return type(self)(self._value + float(other))

    def __radd__(self, other: SupportsFloat) -> Self:
        return self + other

    def __iadd__(self, other: SupportsFloat) -> Self:
        return self + other

    def __sub__(self, other: SupportsFloat) -> Self:
        if not isinstance(other, SupportsFloat):
            return NotImplemented

        return type(self)(self._value - float(other))

    def __rsub__(self, other: SupportsFloat) -> Self:
        if not isinstance(other, SupportsFloat):
            return NotImplemented

        return type(self)(float(other) - self._value)

    def __isub__(self, other: SupportsFloat) -> Self:
        return self - other

    def __mul__(self, other: SupportsFloat) -> Self:
        if not isinstance(other, SupportsFloat):
            return NotImplemented

        return type(self)(self._value * float(other))

    def __rmul__(self, other: SupportsFloat) -> Self:
        return self * other

    def __imul__(self, other: SupportsFloat) -> Self:
        return self * other

    def __truediv__(self, other: SupportsFloat) -> Self:
        if not isinstance(other, SupportsFloat):
            return NotImplemented

        return type(self)(self._value / float(other))

    def __rtruediv__(self, other: SupportsFloat) -> Self:
        if not isinstance(other, SupportsFloat):
            return NotImplemented

        return type(self)(float(other) / self._value)

    def __itruediv__(self, other: SupportsFloat) -> Self:
        return self / other

    def __floordiv__(self, other: SupportsFloat) -> Self:
        if not isinstance(other, SupportsFloat):
            return NotImplemented

        return type(self)(self._value // float(other))

    def __rfloordiv__(self, other: SupportsFloat) -> Self:
        if not isinstance(other, SupportsFloat):
            return NotImplemented

        return type(self)(float(other) // self._value)

    def __ifloordiv__(self, other: SupportsFloat) -> Self:
        return self // other

    def __abs__(self) -> Angle:
        return self.normalized()

    def to_dms(self, precision: int = 0) -> str:
        """
        Returns the represented angle as a formatted DDD-MM-SS string.

        Returns
        -------
        str
            Angle in DMS notation.
        """
        return self.rad2dms(self._value, precision)

    def asunit(self, unit: _AngleUnit = 'rad') -> float:
        """
        Returns the represented angle in the target unit.

        Parameters
        ----------
        unit : Literal['deg', 'rad', 'gon'], optional
            Target unit, by default 'rad'

        Returns
        -------
        float
            Angular value.

        Raises
        ------
        ValueError
            If an unknown `unit` was passed
        """
        match unit:
            case 'deg':
                return self.rad2deg(self._value)
            case 'rad':
                return self._value
            case 'gon':
                return self.rad2gon(self._value)
            case _:
                raise ValueError(f"unknown target unit: '{unit}'")

    def normalized(self, positive: bool = True) -> Self:
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
        return type(self)(self._value, 'rad', True, positive)

    def relative_to(self, other: SupportsFloat) -> Self:
        """
        Returns an angle relative to a reference angle in the [-180;+180] deg
        range.

        The calculated relative angle is positive in the clockwise, and
        negative in the counter clockwise-direction. Value is always between
        -180 degrees and +180 degrees.

        Parameters
        ----------
        other : SupportsFloat
            Reference angle.

        Returns
        -------
        Angle
            Relative angle.
        """

        diff = float(self) - float(other)
        if diff > math.pi:
            return type(self)(diff - PI2)
        elif diff < -math.pi:
            return type(self)(diff + PI2)

        return type(self)(diff)


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

    def __iter__(self) -> Iterator[float]:
        return iter([self.x, self.y, self.z])

    def __getitem__(self, idx: int) -> float:
        if idx < 0 or idx > 2:
            raise ValueError(f"index out of valid 0-2 range, got: {idx}")

        coords = (self.x, self.y, self.z)
        return coords[idx]

    def __eq__(self, other: Any) -> bool:
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

    def __add__(self, other: Vector) -> Self:
        if not isinstance(other, Vector):
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

    def __sub__(self, other: Vector) -> Self:
        if not isinstance(other, Vector):
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

    def dot(self, other: Vector) -> float:
        """
        Calculate the dot product of 2 vectors.

        Parameters
        ----------
        other : Vector
            Second operand.

        Returns
        -------
        float

        Raises
        ------
        TypeError
            If other operand was not compatible.
        """
        if not isinstance(other, Vector):
            raise TypeError(
                "unsupported types for dot product: "
                f"'{type(self).__name__}' and '{type(other).__name__}'"
            )

        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: Vector) -> Self:
        """
        Calculate the cross product of 2 vectors.

        Parameters
        ----------
        other : Vector
            Second operand.

        Returns
        -------
        Self

        Raises
        ------
        TypeError
            If other operand was not compatible.
        """
        if not isinstance(other, Vector):
            raise TypeError(
                "unsupported types for cross product: "
                f"'{type(self).__name__}' and '{type(other).__name__}'"
            )

        return type(self)(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def _swizzle_component(
        self,
        component: Literal['x', 'y', 'z', '0'],
        flip: bool = False
    ) -> float:
        """
        Get a swizzled component.

        Parameters
        ----------
        component : Literal['x', 'y', 'z', '0']
            Swizzle component to get.
        flip : bool, optional
            Flip component sign, by default False

        Returns
        -------
        float
            Resulting swizzled component.

        Raises
        ------
        ValueError
            If an invalid component name was given.
        """
        match component.lower():
            case '0':
                comp = 0.0
            case 'x':
                comp = self.x
            case 'y':
                comp = self.y
            case 'z':
                comp = self.z
            case _:
                raise ValueError(f"Unknown swizzle component: '{component}'")

        return comp if not flip else -1 * comp

    def swizzle(
        self,
        x: Literal['x', 'y', 'z', '0'],
        y: Literal['x', 'y', 'z', '0'],
        z: Literal['x', 'y', 'z', '0'],
        *,
        flip_x: bool = False,
        flip_y: bool = False,
        flip_z: bool = False
    ) -> Self:
        """
        Returns a copy of the vector, with the components rearranged
        according to the swizzle spec.

        Parameters
        ----------
        x : Literal['x', 'y', 'z', '0']
            Component to use as X component.
        y : Literal['x', 'y', 'z', '0']
            Component to use as Y component.
        z : Literal['x', 'y', 'z', '0']
            Component to use as Z component.
        flip_x : bool, optional
            Negate X component, by default False
        flip_y : bool, optional
            Negate Y component, by default False
        flip_z : bool, optional
            Negate Z component, by default False

        Returns
        -------
        Self
            Vector with swizzled components.

        Example
        -------

        >>> v = Vector(1.0, 2.0, 3.0)
        >>> v.swizzle('y', 'x', 'z')
        Vector(2.0, 1.0, 3.0)
        >>> v.swizzle('x', 'y', '0', flip_x=True)
        Vector(-1.0, 2.0, 0.0)

        """
        return type(self)(
            self._swizzle_component(x, flip_x),
            self._swizzle_component(y, flip_y),
            self._swizzle_component(z, flip_z)
        )


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

    @property
    def e(self) -> float:
        """Easting (alias of x)"""
        return self.x

    @e.setter
    def e(self, value: float) -> None:
        self.x = value

    @property
    def n(self) -> float:
        """Northing (alias of y)"""
        return self.y

    @n.setter
    def n(self, value: float) -> None:
        self.y = value

    @property
    def h(self) -> float:
        """Height (alias of z)"""
        return self.z

    @h.setter
    def h(self, value: float) -> None:
        self.z = value

    @classmethod
    def from_polar(
        cls,
        hz: Angle,
        v: Angle,
        dist: float
    ) -> Self:
        """
        Constructs 3D cartesian coordinate from polar survey coordinates.

        Parameters
        ----------
        hz : Angle
            Whole circle bearing.
        v : Angle
            Zenith angle.
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
        Converts 3D cartesian coordinates to polar survey coordinates.

        Returns
        -------
        tuple
            Whole circle bearing, zenith angle and slope distance.
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

    def to_2d(self) -> Self:
        """
        Returns a copy of the coordinate with the vertical component set
        to zero.

        Returns
        -------
        Coordinate
            New coordinate with 0 vertical component.
        """
        return type(self)(
            self.x,
            self.y,
            0
        )
