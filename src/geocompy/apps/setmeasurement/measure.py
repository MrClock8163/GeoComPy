import os
from datetime import datetime
import argparse
from logging import getLogger
from typing import Iterator, Literal
from itertools import chain

from ...data import Angle, Coordinate
from ...communication import open_serial
from ...geo import GeoCom
from ...geo.gctypes import GeoComCode
from ...geo.gcdata import Face
from .. import make_logger, run_cli_app
from .targets import (
    TargetPoint,
    TargetList,
    load_targets_from_json
)
from .sessions import (
    Session,
    Cycle
)


def iter_targets(
    points: TargetList,
    order: str
) -> Iterator[tuple[Face, TargetPoint]]:
    match order:
        case "AaBb":
            return ((f, t) for t in points for f in (Face.F1, Face.F2))
        case "AabB":
            return (
                (f, t) for i, t in enumerate(points)
                for f in (
                    (Face.F1, Face.F2)
                    if i % 2 == 0 else
                    (Face.F2, Face.F1)
                )
            )
        case "ABab":
            return chain(
                ((Face.F1, t) for t in points),
                ((Face.F2, t) for t in points)
            )
        case "ABba":
            return chain(
                ((Face.F1, t) for t in points),
                ((Face.F2, t) for t in reversed(points))
            )
        case "ABCD":
            return ((Face.F1, t) for t in points)

    exit(1200)


def measure_set(
    tps: GeoCom,
    filepath: str,
    order_spec: Literal['AaBb', 'AabB', 'ABab', 'ABba', 'ABCD'],
    count: int = 1,
    pointnames: str = ""
) -> Session:
    applog = getLogger("APP")
    points = load_targets_from_json(filepath)
    if pointnames != "":
        use_points = set(pointnames.split(","))
        loaded_points = set(points.get_target_names())
        excluded_points = loaded_points - use_points
        applog.debug(f"Excluding points: {excluded_points}")
        for pt in excluded_points:
            points.pop_target(pt)

    tps.aut.turn_to(0, Angle(180, 'deg'))
    incline = tps.tmc.get_angle_inclination('MEASURE').params
    temp = tps.csv.get_internal_temperature().params
    battery = tps.csv.check_power().params
    resp_station = tps.tmc.get_station().params
    if resp_station is None:
        station = Coordinate(0, 0, 0)
        iheight = 0.0
        applog.warning(
            "Could not retrieve station and instrument height, using default"
        )
    else:
        station, iheight = resp_station

    session = Session(station, iheight)
    for i in range(count):
        applog.info(f"Starting set cycle {i + 1}")
        output = Cycle(
            datetime.now(),
            battery[0] if battery is not None else None,
            temp,
            (incline[4], incline[5]) if incline is not None else None
        )

        for f, t in iter_targets(points, order_spec):
            applog.info(f"Measuring {t.name} ({f.name})")
            rel_coords = (
                (t.coords + Coordinate(0, 0, t.height))
                - (station + Coordinate(0, 0, iheight))
            )
            hz, v, _ = rel_coords.to_polar()
            if f == Face.F2:
                hz = (hz + Angle(180, 'deg')).normalized()
                v = Angle(360, 'deg') - v

            tps.aut.turn_to(hz, v)
            resp_atr = tps.aut.fine_adjust(0.5, 0.5)
            if resp_atr.error != GeoComCode.OK:
                applog.error(
                    f"ATR fine adjustment failed ({resp_atr.error.name}), "
                    "skipping point"
                )
                continue

            tps.bap.set_prism_type(t.prism)
            tps.tmc.do_measurement()
            resp_angle = tps.tmc.get_simple_measurement(10)
            if resp_angle.params is None:
                applog.error(
                    f"Error during measurement ({resp_angle.error.name}), "
                    "skipping point"
                )
                continue

            output.add_measurement(
                t.name,
                f,
                t.height,
                resp_angle.params
            )
            applog.info("Done")

        session.cycles.append(output)

    tps.aut.turn_to(0, Angle(180, 'deg'))

    return session


def main(args: argparse.Namespace) -> None:
    log = make_logger("TPS", args)
    applog = getLogger("APP")
    applog.info("Starting measurement session")

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
            args.order,
            args.cycles,
            args.points
        )

    applog.info("Finished measurement session")

    timestamp = session.cycles[0].time.strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(
        args.directory,
        f"{args.prefix}{timestamp}.json"
    )
    session.export_to_json(filename)
    applog.info(f"Saved measurement results at '{filename}'")


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
        "-o",
        "--order",
        help="measurement order (capital letter: face 1, lower case: face 2)",
        choices=["AaBb", "AabB", "ABab", "ABba", "ABCD"],
        default="ABba",
        type=str
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
            "(comma separated list, empty to use all)"
        ),
        default=""
    )
    group_logging = parser.add_argument_group("logging")
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
    args = parser.parse_args()
    run_cli_app(
        "SETMEASUREMENT.MEASURE",
        main,
        args
    )
