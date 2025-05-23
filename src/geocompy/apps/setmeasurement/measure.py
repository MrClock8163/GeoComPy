import os
from datetime import datetime
from itertools import chain, repeat
from typing import Iterable
import argparse

from ...data import Angle, Coordinate
from ...communication import open_serial
from ...geo import GeoCom
from ...geo.gcdata import Face
from . import make_logger
from .targets import (
    TargetPoint,
    load_targets_from_json
)
from .sessions import (
    Session,
    Point,
    export_session_to_json
)


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

    resp_station = tps.tmc.get_station().params
    if resp_station is None:
        station = Coordinate(0, 0, 0)
    else:
        station = resp_station[0]

    output = Session(
        time,
        battery[0] if battery is not None else None,
        temp,
        (incline[4], incline[5]) if incline is not None else None,
        station
    )

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

            if resp_angle.params is None:
                tps._logger.error(
                    f"Error during measurement ({resp_angle.error.name})"
                )
                continue

            output.add_point(
                Point(
                    t.name,
                    f,
                    resp_angle.params
                )
            )
            tps._logger.info("Done")

    tps.aut.turn_to(0, Angle(180, 'deg'))

    return output


def main(args: argparse.Namespace) -> None:
    log = make_logger(args)
    log.info("Starting measurement session")

    with open_serial(
        args.port,
        retry=args.retry,
        sync_after_timeout=args.sync_after_timeout,
        speed=args.baud,
        timeout=args.timeout
    ) as com:
        tps = GeoCom(com, log)
        if args.sync_time:
            tps.csv.set_datetime(datetime.now())
        session = measure_set(
            tps,
            args.targets,
            args.twoface,
            args.cycles,
            args.points
        )

    log.info("Finished measurement session")

    timestamp = session.time.strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(
        args.directory,
        f"{args.prefix}{timestamp}.json"
    )
    export_session_to_json(filename, session)
    log.info(f"Saved measurement results at '{filename}'")


def cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="measure",
        description="Conduct sets of measurements to target points.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    group_com = parser.add_argument_group("communication")
    group_com.add_argument(
        "port",
        type=str,
        help="serial port (e.g. COM1)"
    )
    group_com.add_argument(
        "-b",
        "--baud",
        type=int,
        default=9600,
        help="serial connection speed"
    )
    group_com.add_argument(
        "-t",
        "--timeout",
        type=int,
        default=15,
        help="connection timeout to set"
    )
    group_com.add_argument(
        "-r",
        "--retry",
        type=int,
        default=1,
        help="number of connection retry attempts"
    )
    group_com.add_argument(
        "-sat",
        "--sync-after-timeout",
        action="store_true",
        help="attempt to synchronize message que after a connection timeout"
    )
    group_program = parser.add_argument_group("program")
    group_program.add_argument(
        "targets",
        type=str,
        help="JSON file containing target definitions"
    )
    group_program.add_argument(
        "directory",
        type=str,
        help="directory to save measurement output to"
    )
    group_program.add_argument(
        "-p",
        "--prefix",
        type=str,
        default="setmeasurement_",
        help="prefix to prepend to the set measurement output files"
    )
    group_program.add_argument(
        "-c",
        "--cycles",
        type=int,
        default=1,
        help="number of measurement cycles"
    )
    group_program.add_argument(
        "-tf",
        "--twoface",
        action="store_true",
        help="measure in both face 1 and face 2"
    )
    group_program.add_argument(
        "-s",
        "--sync-time",
        action="store_true",
        help="synchronize instrument time and date with the computer"
    )
    group_program.add_argument(
        "-pt",
        "--points",
        type=str,
        help=(
            "targets to use from loaded target definition "
            "(comma separated list)"
        ),
        default=""
    )
    group_logging = parser.add_argument_group("logging")
    group_logging.add_argument(
        "-l",
        "--log-file",
        type=str,
        help="logging file"
    )
    group_logging_levels = (
        group_logging.add_mutually_exclusive_group()
    )
    group_logging_levels.add_argument(
        "--debug",
        help="set logging level to DEBUG",
        action="store_true"
    )
    group_logging_levels.add_argument(
        "--info",
        help="set logging level to INFO",
        action="store_true"
    )
    group_logging_levels.add_argument(
        "--warning",
        help="set logging level to WARNING",
        action="store_true"
    )
    group_logging_levels.add_argument(
        "--error",
        help="set logging level to ERROR",
        action="store_true"
    )

    return parser


if __name__ == "__main__":
    parser = cli()
    main(parser.parse_args())
