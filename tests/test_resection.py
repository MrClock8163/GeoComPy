from random import randint

from pytest import approx

from geocompy.data import Angle, Coordinate
from geocompy.apps.resection import (
    calculate_preliminary_station
)


class TestFunctions:
    def test_intersection(self) -> None:
        p1 = Coordinate(
            randint(-5000, 5000) * 1e-3,
            randint(-5000, 5000) * 1e-3,
            randint(-5000, 5000) * 1e-3
        )
        p2 = Coordinate(
            randint(-5000, 5000) * 1e-3,
            randint(-5000, 5000) * 1e-3,
            randint(-5000, 5000) * 1e-3
        )
        p3 = Coordinate(
            randint(-5000, 5000) * 1e-3,
            randint(-5000, 5000) * 1e-3,
            randint(-5000, 5000) * 1e-3
        )
        s = Coordinate(
            randint(-5000, 5000) * 1e-3,
            randint(-5000, 5000) * 1e-3,
            randint(-5000, 5000) * 1e-3
        )

        print()
        print("p1", p1)
        print("p2", p2)
        print("p3", p3)
        print("s", s)

        dp1 = (p1 - s).to_polar()
        dp2 = (p2 - s).to_polar()
        dp3 = (p3 - s).to_polar()

        for a in range(0, 360, 10):
            o = Angle(a, 'deg')

            obs = [
                (abs(dp1[0] - o), dp1[1], dp1[2]),
                (abs(dp2[0] - o), dp2[1], dp2[2]),
                (abs(dp3[0] - o), dp3[1], dp3[2])
            ]

            st = calculate_preliminary_station(
                obs,
                [
                    p1,
                    p2,
                    p3
                ]
            )

            assert s.x == approx(st.x)
            assert s.y == approx(st.y)
            assert s.z == approx(st.z)
