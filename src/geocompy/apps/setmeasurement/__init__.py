import os
from datetime import datetime
from itertools import chain, repeat
from typing import Callable, TypeVar, Iterable

from ...data import Angle, Coordinate
from ...geo import GeoCom
from ...geo.gcdata import Prism, Face
from .targets import (
    TargetList,
    TargetPoint,
    load_targets_from_json
)
from .sessions import (
    Session,
    SessionMeta,
    Point
)


_T = TypeVar("_T")


def user_input(prompt: str, parser: Callable[[str], _T]) -> _T:
    while True:
        ans = input(f"> {prompt}\n")
        try:
            return parser(ans)
        except Exception as e:
            print(e)


def parse_yesno(value: str) -> bool:
    match value.lower():
        case "yes" | "y":
            return True
        case "no" | "n":
            return False
        case _:
            raise ValueError(f"> {value} is not an acceptable input")


def parse_action(value: str) -> str:
    match value.lower():
        case "cancel" | "c":
            return "cancel"
        case "replace" | "r":
            return "replace"
        case "append" | "a":
            return "append"
        case _:
            raise ValueError(f"> {value} is not an acceptable input")


def setup_set(tps: GeoCom, filepath: str) -> TargetList | None:
    if os.path.exists(filepath):
        action = user_input(
            f"{filepath} already exists. Action? (cancel/replace/append)",
            parse_action
        )
        match action:
            case "cancel":
                return None
            case "append":
                points = load_targets_from_json(filepath)
                print(f"> Loaded targest: {points.get_target_names()}")
            case _:
                points = TargetList()
    else:
        points = TargetList()

    log = tps._logger
    log.info("Set measurement setup started")
    while ptid := user_input("Point ID? (or nothing to finish)", str):
        if ptid in points:
            remove = user_input(
                f"{ptid} already exists. Overwrite? (yes/no)",
                parse_yesno
            )
            if remove:
                points.pop_target(ptid)
            else:
                continue

        resp_target = tps.bap.get_prism_type()
        if resp_target.params is None:
            print("> Could not retrieve target type. Using default.")
            target = Prism.MINI
        elif resp_target.params == Prism.USER:
            print("> User defined prism types are currently not supported.")
            continue
        else:
            target = resp_target.params

        user_input("Aim at target, then press ENTER...", str)

        tps.aut.fine_adjust(0.5, 0.5)
        tps.tmc.do_measurement()
        resp = tps.tmc.get_simple_coordinate(10000)
        if resp.params is None:
            print("> Could not measure target. Restart the observation!")
            continue

        points.add_target(
            TargetPoint(
                ptid,
                target,
                resp.params
            )
        )

        if not user_input(
            "Do you want to add more targets? (yes/no)",
            parse_yesno
        ):
            break

    print("> Set measurement setup finished")

    log.info("Set measurement setup finished")

    return points


def measure_set(
    tps: GeoCom,
    filepath: str,
    two_faces: bool,
    count: int = 1,
    pointnames: str = ""
) -> Session:
    points = load_targets_from_json(filepath)
    if pointnames != "":
        use_points = set(pointnames.split(","))
        loaded_points = set(points.get_target_names())
        excluded_points = loaded_points - use_points
        for pt in excluded_points:
            points.pop_target(pt)

    time = datetime.now()
    temp = tps.csv.get_internal_temperature().params
    battery = tps.csv.check_power().params
    incline = tps.tmc.get_angle_inclination('MEASURE').params
    start = SessionMeta(
        time,
        temp,
        battery[0] if battery is not None else None,
        (incline[4], incline[5]) if incline is not None else None
    )

    output = Session(start)
    resp_station = tps.tmc.get_station().params
    if resp_station is None:
        station = Coordinate(0, 0, 0)
    else:
        station = resp_station[0]

    for i in range(count):
        tps._logger.info(f"Starting set cycle {i + 1}")
        face: Iterable[Face] = repeat(Face.F1, len(points))
        target: Iterable[TargetPoint] = points
        if two_faces:
            face = chain(
                repeat(Face.F1, len(points)),
                repeat(Face.F2, len(points))
            )
            target = chain(
                points,
                reversed(points)
            )

        for f, t in zip(face, target):
            tps._logger.info(f"Measuring {t.name} ({f.name})")
            rel_coords = t.coords - station
            hz, v, _ = rel_coords.to_polar()
            if f == Face.F2:
                hz = (hz + Angle(180, 'deg')).normalized()
                v = Angle(360, 'deg') - v

            tps.aut.turn_to(hz, v)
            tps.aut.fine_adjust(0.5, 0.5)
            tps.bap.set_prism_type(t.prism)
            tps.tmc.do_measurement()
            resp_angle = tps.tmc.get_simple_measurement(10000)
            resp_coords = tps.tmc.get_simple_coordinate(10000)

            if resp_angle.params is None or resp_coords.params is None:
                tps._logger.error(
                    f"Error during measurement ({resp_coords.error.name})"
                )
                continue

            output.add_point(
                Point(
                    t.name,
                    f,
                    resp_angle.params,
                    resp_coords.params
                )
            )

    tps.aut.turn_to(0, Angle(180, 'deg'))

    time = datetime.now()
    temp = tps.csv.get_internal_temperature().params
    battery = tps.csv.check_power().params
    incline = tps.tmc.get_angle_inclination('MEASURE').params
    end = SessionMeta(
        time,
        temp,
        battery[0] if battery is not None else None,
        (incline[4], incline[5]) if incline is not None else None
    )
    output.finished(end)

    return output
