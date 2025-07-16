import os
from datetime import datetime
from logging import getLogger
from typing import Iterator, Literal
from itertools import chain
import pathlib

try:
    from click_extra import (
        extra_command,
        argument,
        option,
        option_group,
        Choice,
        IntRange,
        file_path,
        dir_path
    )
    from cloup.constraints import mutually_exclusive
except ModuleNotFoundError:
    print(
        """
Missing dependencies. The Set Measurement needs the following dependencies:
- cloup
- click-extra

Install the missing dependencies manually, or install GeoComPy with the
'apps' extra:

pip install geocompy[apps]
"""
    )
    exit(3)

from ...data import Angle, Coordinate
from ...communication import open_serial
from ...geo import GeoCom
from ...geo.gctypes import GeoComCode
from ...geo.gcdata import Face
from .. import make_logger
from ..targets import (
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


@extra_command(
    "measure",
    params=None,
    context_settings={"auto_envvar_prefix": None}
)  # type: ignore[misc]
@argument(
    "port",
    type=str,
    help="serial port (e.g. COM1)"
)
@argument(
    "targets",
    type=file_path(exists=True),
    help="JSON file containing target definitions"
)
@argument(
    "directory",
    type=dir_path(),
    help="directory to save measurement output to"
)
@option_group(
    "Connection options",
    "Options related to the serial connection",
    option(
        "-b",
        "--baud",
        help="serial speed",
        type=int,
        default=9600
    ),
    option(
        "-t",
        "--timeout",
        help="serial timeout",
        type=IntRange(min=0),
        default=15
    ),
    option(
        "-r",
        "--retry",
        help="number of connection retry attempts",
        type=IntRange(min=0, max=10),
        default=1
    ),
    option(
        "--sync-after-timeout",
        help="attempt to synchronize message que after a connection timeout",
        is_flag=True
    )
)
@option(
    "--prefix",
    type=str,
    default="setmeasurement_",
    help="prefix to prepend to the set measurement output files"
)
@option(
    "-c",
    "--cycles",
    type=IntRange(min=1),
    default=1,
    help="number of measurement cycles"
)
@option(
    "-o",
    "--order",
    help="measurement order (capital letter: face 1, lower case: face 2)",
    type=Choice(["AaBb", "AabB", "ABab", "ABba", "ABCD"]),
    default="ABba"
)
@option(
    "-s",
    "--sync-time",
    help="synchronize instrument time and date with the computer",
    is_flag=True
)
@option(
    "-p",
    "--points",
    type=str,
    help=(
        "targets to use from loaded target definition "
        "(comma separated list, empty to use all)"
    ),
    default=""
)
@option_group(
    "Logging options",
    "Options related to the logging functionalities.",
    option(
        "--debug",
        is_flag=True
    ),
    option(
        "--info",
        is_flag=True
    ),
    option(
        "--warning",
        is_flag=True
    ),
    option(
        "--error",
        is_flag=True
    ),
    constraint=mutually_exclusive
)
def cli(
    port: str,
    targets: pathlib.Path,
    directory: pathlib.Path,
    baud: int = 9600,
    timeout: int = 15,
    retry: int = 1,
    sync_after_timeout: bool = False,
    prefix: str = "setmeasurement_",
    cycles: int = 1,
    order: Literal['AaBb', 'AabB', 'ABab', 'ABba', 'ABCD'] = "ABba",
    sync_time: bool = True,
    points: str = "",
    debug: bool = False,
    info: bool = False,
    warning: bool = False,
    error: bool = False,
) -> None:
    """Run sets of measurements to predefined targets."""

    log = make_logger("TPS", debug, info, warning, error)
    applog = make_logger("APP", debug, info, warning, error)
    applog.info("Starting measurement session")

    with open_serial(
        port,
        retry=retry,
        sync_after_timeout=sync_after_timeout,
        speed=baud,
        timeout=timeout
    ) as com:
        tps = GeoCom(com, log)
        if sync_time:
            tps.csv.set_datetime(datetime.now())

        session = measure_set(
            tps,
            str(targets),
            order,
            cycles,
            points
        )

    applog.info("Finished measurement session")

    timestamp = session.cycles[0].time.strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(
        directory,
        f"{prefix}{timestamp}.json"
    )
    session.export_to_json(filename)
    applog.info(f"Saved measurement results at '{filename}'")
