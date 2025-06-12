import math
from typing import Sequence

import numpy as np

from ..data import Angle, Coordinate


def calculate_preliminary_station(
    measurements: Sequence[tuple[Angle, Angle, float]],
    targets: Sequence[Coordinate]
) -> Coordinate:
    t1 = targets[0].to_2d()
    t2 = targets[1].to_2d()
    t1_3d = targets[0]

    hz12, _, d12 = (t2 - t1).to_polar()
    hzs1, vs1, ds1 = measurements[0]
    _, vs2, ds2 = measurements[1]

    r1 = math.sin(vs1) * ds1
    r2 = math.sin(vs2) * ds2

    alpha = Angle(math.acos((r1**2 + d12**2 - r2**2) / (2 * r1 * d12)))

    station1 = t1_3d + Coordinate.from_polar(
        hz12 - alpha,
        Angle(180, "deg") - vs1,
        ds1
    )
    station2 = t1_3d + Coordinate.from_polar(
        hz12 + alpha,
        Angle(180, "deg") - vs1,
        ds1
    )

    orient, _, _ = (t1 - station1).to_polar()
    hzs2, _, _ = (t2 - station1).to_polar()
    if ((orient + hzs1) - hzs2).normalized() > Angle.from_dms("0-01-00"):
        return station2

    return station1


def stdev_to_weights(
    hz: Angle,
    v: Angle,
    d: float
) -> tuple[float, float, float]:
    return 1 / float(hz)**2, 1 / float(v)**2, 1 / d**2


def _build_matrices(
    measurements: list[tuple[Angle, Angle, float]],
    targets: list[Coordinate],
    station: Coordinate,
    orientation: Angle
) -> tuple[list[list[float]], list[float]]:
    design_matrix: list[list[float]] = []
    observation_vector: list[float] = []

    for (hz, v, d), coord in zip(measurements, targets):
        dr0 = coord - station
        dx0, dy0, dz0 = dr0
        hz0, v0, d0 = dr0.to_polar()
        design_matrix.append(
            [
                -1,
                -dx0 / d0**2,
                dy0 / d0**2,
                0
            ]
        )
        design_matrix.append(
            [
                0,
                -dx0 * dz0 / (math.sqrt(dx0**2 + dy0**2) * d0**2),
                -dx0 * dz0 / (math.sqrt(dx0**2 + dy0**2) * d0**2),
                math.sqrt(dx0**2 + dy0**2) / d0**2
            ]
        )
        design_matrix.append(
            [
                0,
                -dx0 / d0,
                -dy0 / d0,
                -dz0 / d0
            ]
        )
        observation_vector.extend(
            [
                float(hz0 - hz - orientation),
                float(-v + v0),
                d0 - d
            ]
        )

    return design_matrix, observation_vector


def adjust_resection(
    measurements: list[tuple[Angle, Angle, float]],
    targets: list[Coordinate],
    preliminary_station: Coordinate,
    *,
    coordinate_tolerance: Coordinate = Coordinate(1e-4, 1e-4, 1e-4),
    orientation_tolerance: Angle = Angle(1 / 3600, "deg"),
    max_iterations: int = 50,
    weight_hz: float = 1,
    weight_v: float = 1,
    weight_d: float = 1
) -> tuple[Angle, Angle, Coordinate, Coordinate]:
    if len(measurements) != len(targets) or len(targets) < 2:
        raise ValueError("Cannot calculate resection with less than 2 targets")

    station = preliminary_station
    orientation = Angle(0)
    weights = np.diag(
        [weight_hz, weight_v, weight_d] * len(measurements)
    )
    defect = len(measurements) * 3 - 4

    otol = float(orientation_tolerance)
    xtol = coordinate_tolerance.x
    ytol = coordinate_tolerance.y
    ztol = coordinate_tolerance.z

    x = np.array([1, 1, 1, 1])
    iterations = 0
    while (
        (
            abs(x[0]) > otol
            or abs(x[1]) > xtol
            or abs(x[2]) > ytol
            or abs(x[3]) > ztol
        )
        and iterations < max_iterations
    ):
        design_float, obs_float = _build_matrices(
            measurements,
            targets,
            station,
            orientation
        )
        design = np.array(design_float)
        obs = np.array(obs_float)

        norm = design.T @ weights @ design
        norminv = np.linalg.pinv(norm)
        x = -norminv @ design.T @ weights @ obs

        v = design @ x - obs
        m0 = np.sqrt(v.T @ weights @  v / defect)
        m = m0 * np.sqrt(np.diag(norminv))

        orientation = orientation + Angle(x[0])
        stdev_orientation = Angle(m[0])
        station = station + Coordinate(x[1], x[2], x[3])
        stdev_station = Coordinate(m[1], m[2], m[3])

        iterations += 1

    return orientation, stdev_orientation, station, stdev_station
