from enum import Enum

import pytest
from pytest import approx

from geocompy.data import (
    toenum,
    enumparser,
    parsestr,
    Angle,
    AngleUnit,
    Byte,
    Coordinate
)


class A(Enum):
    MEMBER = 1


class TestFunctions:
    def test_toenum(self):
        assert toenum(A, "MEMBER") is A.MEMBER
        assert toenum(A, A.MEMBER) is A.MEMBER

    def test_enumparser(self):
        assert callable(enumparser(A))
        assert enumparser(A)("1") is A.MEMBER

    def test_parsestr(self):
        assert parsestr("value") == "value"
        assert parsestr("\"value") == "\"value"
        assert parsestr("value\"") == "value\""
        assert parsestr("\"value\"") == "value"


class TestAngle:
    def test_init(self):
        assert float(Angle(1)) == approx(float(Angle(1, AngleUnit.RAD)))

        units = AngleUnit._member_names_.copy()
        units.remove("DMS")

        for name in units:
            unit = AngleUnit[name]
            assert (
                float(Angle(1, name))  # type: ignore
                == approx(float(Angle(1, unit)))
            )

    def test_asunit(self):
        value = Angle(180, 'DEG')
        assert value.asunit('DEG') == approx(180)
        assert value.asunit() == value.asunit('RAD')

    def test_normalize(self):
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

    def test_arithmetic(self):
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
    def test_init(self):
        with pytest.raises(ValueError):
            Byte(-1)

        with pytest.raises(ValueError):
            Byte(256)

    def test_str(self):
        value = Byte(12)
        assert int(value) == 12
        assert str(value) == "'0C'"


class TestCoordinate:
    def test_init(self):
        value = Coordinate(1, 2, 3)
        assert value.x == 1
        assert value.y == 2
        assert value.z == 3
        assert value[0] == value.x
        x, _, _ = value
        assert x == value.x

    def test_arithmetic(self):
        c1 = Coordinate(1, 1, 1)
        c2 = Coordinate(1, 2, 3)

        assert c1 + c2 == Coordinate(2, 3, 4)
        assert c1 - c2 == Coordinate(0, -1, -2)
        assert type(+c1) is Coordinate
        c3 = +c1
        assert c3 is not c1
