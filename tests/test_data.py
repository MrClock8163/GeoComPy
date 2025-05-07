import math
from enum import Enum

import pytest
from pytest import approx

from geocompy.data import (
    toenum,
    enumparser,
    parsestr,
    gsiword,
    Angle,
    AngleUnit,
    Byte,
    Coordinate
)


class A(Enum):
    MEMBER = 1


class TestFunctions:
    def test_toenum(self) -> None:
        assert toenum(A, "MEMBER") is A.MEMBER
        assert toenum(A, A.MEMBER) is A.MEMBER

    def test_enumparser(self) -> None:
        assert callable(enumparser(A))
        assert enumparser(A)("1") is A.MEMBER

    def test_parsestr(self) -> None:
        assert parsestr("value") == "value"
        assert parsestr("\"value") == "\"value"
        assert parsestr("value\"") == "value\""
        assert parsestr("\"value\"") == "value"

    def test_gsiword(self) -> None:
        assert gsiword(11, "1") == "11....+00000001 "
        assert gsiword(11, "1", gsi16=True) == "*11....+0000000000000001 "
        assert gsiword(
            330,
            "123",
            negative=True,
            info="08"
        ) == "330.08-00000123 "


class TestAngle:
    def test_init(self) -> None:
        assert float(Angle(1)) == approx(float(Angle(1, AngleUnit.RAD)))

        units = AngleUnit._member_names_.copy()
        units.remove("DMS")

        for name in units:
            unit = AngleUnit[name]
            assert (
                float(Angle(1, name))  # type: ignore
                == approx(float(Angle(1, unit)))
            )

    def test_asunit(self) -> None:
        value = Angle(180, 'DEG')
        assert value.asunit('DEG') == approx(180)
        assert value.asunit() == value.asunit('RAD')

    def test_normalize(self) -> None:
        assert (
            Angle(
                370,
                'DEG',
                normalize=True,
                positive=True
            ).asunit('DEG')
            == approx(10)
        )
        assert (
            Angle(
                -10,
                'DEG',
                normalize=True,
                positive=True
            ).asunit('DEG')
            == approx(350)
        )
        assert (
            Angle(
                -370,
                'DEG',
                normalize=True,
                positive=True
            ).asunit('DEG')
            == approx(350)
        )
        assert (
            Angle(370, 'DEG', normalize=True).asunit('DEG')
            == approx(Angle(370, 'DEG').normalized().asunit('DEG'))
        )

    def test_arithmetic(self) -> None:
        a1 = Angle(90, 'DEG')
        a2 = Angle(90, 'DEG')
        assert (
            float(a1 + a2)
            == approx(float(Angle(180, 'DEG')))
        )
        assert (
            float(a1 - a2)
            == approx(float(Angle(0, 'DEG')))
        )
        assert (
            float(a1 * 2)
            == approx(float(Angle(180, 'DEG')))
        )
        assert (
            float(a1 / 2)
            == approx(float(Angle(45, 'DEG')))
        )
        with pytest.raises(TypeError):
            a1 * "str"  # type: ignore

        with pytest.raises(TypeError):
            a1 / "str"  # type: ignore


class TestByte:
    def test_init(self) -> None:
        with pytest.raises(ValueError):
            Byte(-1)

        with pytest.raises(ValueError):
            Byte(256)

    def test_str(self) -> None:
        value = Byte(12)
        assert int(value) == 12
        assert str(value) == "'0C'"


class TestCoordinate:
    def test_init(self) -> None:
        value = Coordinate(1, 2, 3)
        assert value.x == 1
        assert value.y == 2
        assert value.z == 3
        assert value[0] == value.x
        x, _, _ = value
        assert x == value.x

    def test_arithmetic(self) -> None:
        c1 = Coordinate(1, 1, 1)
        c2 = Coordinate(1, 2, 3)

        assert c1 + c2 == Coordinate(2, 3, 4)
        assert c1 - c2 == Coordinate(0, -1, -2)
        assert type(+c1) is Coordinate
        c3 = +c1
        assert c3 is not c1

    def test_polar(self) -> None:
        c1 = Coordinate(-1, -1, -1)
        p1 = c1.to_polar()

        assert float(p1[0]) == approx(math.radians(225))
        assert float(p1[1]) == approx(math.radians(125.2643897))
        assert p1[2] == approx(math.sqrt(3))

        c2 = Coordinate.from_polar(*p1)

        assert c1.x == approx(c2.x)
        assert c1.y == approx(c2.y)
        assert c1.z == approx(c2.z)
