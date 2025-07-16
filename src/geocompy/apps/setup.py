import os

try:
    from click_extra import (
        extra_command,
        extra_group,
        argument,
        option,
        option_group,
        IntRange,
        Choice,
        prompt,
        confirm,
        echo
    )
except ModuleNotFoundError:
    print(
        """
Missing dependencies. The Setup app needs the following dependencies:
- click-extra

Install the missing dependencies manually, or install GeoComPy with the
'apps' extra:

pip install geocompy[apps]
"""
    )
    exit(3)

from ..communication import open_serial
from ..geo import GeoCom
from ..geo.gcdata import Prism
from . import (
    echo_green,
    echo_red,
    echo_yellow
)
from .targets import (
    TargetList,
    TargetPoint,
    load_targets_from_json,
    export_targets_to_json,
    import_targets_from_csv
)


def measure_targets(tps: GeoCom, filepath: str) -> TargetList | None:
    if os.path.exists(filepath):
        action: str = prompt(
            f"{filepath} already exists. Action",
            default="replace",
            type=Choice(["cancel", "replace", "append"])
        )
        match action:
            case "cancel":
                exit(0)
            case "append":
                points = load_targets_from_json(filepath)
                echo(f"Loaded targets: {points.get_target_names()}")
            case _:
                points = TargetList()
    else:
        points = TargetList()

    ptid: str
    while ptid := prompt("Point ID (or nothing to finish)", type=str):
        if ptid in points:
            remove = confirm(
                f"{ptid} already exists. Overwrite?"
            )
            if remove:
                points.pop_target(ptid)
            else:
                continue

        resp_target = tps.bap.get_prism_type()
        if resp_target.params is None:
            echo_yellow("Could not retrieve target type.")
            continue

        target = resp_target.params
        if target == Prism.USER:
            echo_yellow(
                "User defined prism types are currently not supported."
            )
            continue

        user_target: str = prompt(
            "Prism type",
            default=target.name,
            type=Choice([e.name for e in Prism if e.name != 'USER'])
        )
        target = Prism[user_target]

        resp_height = tps.tmc.get_target_height()
        if resp_height.params is None:
            echo_yellow("Could not retrieve target height.")
            continue

        height: float = prompt(
            "Target height",
            default=f"{resp_height.params:.4f}",
            type=float
        )

        prompt("Aim at target, then press ENTER...", prompt_suffix="")

        tps.aut.fine_adjust(0.5, 0.5)
        tps.tmc.do_measurement()
        resp = tps.tmc.get_simple_coordinate(10)
        if resp.params is None:
            echo_yellow("Could not measure target.")
            continue

        points.add_target(
            TargetPoint(
                ptid,
                target,
                height,
                resp.params
            )
        )

        echo(f"{ptid} stored")
        if not confirm("Record more targets?", default=True):
            break

    echo_green("Set measurement setup finished")

    return points


@extra_command("measure", params=None)  # type: ignore[misc]
@argument(
    "port",
    help="serial port (e.g. COM1)",
    type=str
)
@argument(
    "output",
    help=(
        "path to save the JSON containing the recorded targets "
        "(if the file already exists, the new targets can be appended)"
    ),
    type=str
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
def cli_measure(
    port: str,
    output: str,
    baud: int = 9600,
    timeout: int = 15,
    retry: int = 1,
    sync_after_timeout: bool = False
) -> None:
    """Measure target points.

    The program gives instructions in the terminal at each step.

    .. caution::
        :class: warning

        The appropriate prism type needs to be set on the instrument before
        recording each target point. The program will automatically request
        the type from the instrument after the point is measured.
    """

    with open_serial(
        port,
        retry=retry,
        sync_after_timeout=sync_after_timeout,
        speed=baud,
        timeout=timeout
    ) as com:
        tps = GeoCom(com)
        targets = measure_targets(tps, output)
        if targets is None:
            echo_red("Setup was cancelled or no targets were recorded.")
            exit(0)

    export_targets_to_json(output, targets)
    echo_green(f"Saved setup results at '{output}'")


@extra_command(
    "import",
    params=None,
    context_settings={"auto_envvar_prefix": None}
)  # type: ignore[misc]
@argument(
    "reflector",
    type=Choice([e.name for e in Prism if e.name != 'USER'])
)
@argument(
    "input",
    type=str
)
@argument(
    "output",
    type=str
)
@option(
    "-d",
    "--delimiter",
    help="column delimiter character",
    type=str,
    default=","
)
@option(
    "-c",
    "--columns",
    help=(
        "column spec "
        "(P: point ID, E: easting, N: northing, Z: height, _: ignore)"
    ),
    type=str,
    default="PENZ"
)
@option(
    "-s",
    "--skip",
    help="number of header rows to skip",
    type=IntRange(min=0),
    default=0
)
def cli_import(
    reflector: str,
    input: str,
    output: str,
    delimiter: str = ",",
    columns: str = "PENZ",
    skip: int = 0
) -> None:
    """Import target points.

    If a coordinate list already exists with the target points, it can
    be imported from CSV format.

    As a CSV file may contain any number and types of columns, the
    mapping to the relevant columns can be given with a column spec.
    A column spec is a string, with each character representing a
    column type.

    - ``P``: point ID
    - ``E``: easting
    - ``N``: northing
    - ``Z``: up/height
    - ``_``: ignore/skip column

    Every column spec must specify the ``PENZ`` fields in the appropriate
    order.

    Examples:

    - ``PENZ``: standard column order
    - ``P_ENZ``: skipping 2nd column containing point codes
    - ``EN_Z_P``: mixed column order and skipping
    """

    if os.path.exists(output):
        action: str = prompt(
            f"{output} already exists. Action",
            type=Choice(["cancel", "replace", "append"]),
            default="cancel"
        )
        match action:
            case "cancel":
                exit(0)
            case "append":
                points = load_targets_from_json(output)
                echo(
                    f"Loaded targets: {', '.join(points.get_target_names())}"
                )
            case _:
                points = TargetList()
    else:
        points = TargetList()

    try:
        imported_points = import_targets_from_csv(
            input,
            delimiter,
            columns,
            Prism[reflector],
            skip
        )
    except FileNotFoundError as fe:
        echo_red("Could not find CSV file (file does not exist)")
        echo_red(fe)
        exit(1103)
    except OSError as oe:
        echo_red(
            "Cannot import CSV data due to a file operation error "
            "(no access or other error)"
        )
        echo_red(oe)
        exit(1102)
    except Exception as e:
        echo_red(
            "Cannot import CSV data due to an error "
            "(duplicated points, the header was not skipped, malformed data "
            "or incorrect column spec)"
        )
        echo_red(e)
        exit(1100)

    conflicts = set(
        points.get_target_names()
    ).intersection(imported_points.get_target_names())

    if len(conflicts) > 0:
        echo(f"Duplicates: {', '.join(sorted(list(conflicts)))}")
        echo_red("Found duplicate targets between CSV and existing JSON")
        exit(1101)

    echo(f"Imported targets: {', '.join(imported_points.get_target_names())}",)

    for t in imported_points:
        points.add_target(t)

    export_targets_to_json(output, points)
    echo_green(f"Saved import results at '{os.path.abspath(output)}'")


@extra_group("targets", params=None)  # type: ignore[misc]
def cli() -> None:
    """Record target points for later automated measurements."""


cli.add_command(cli_measure)
cli.add_command(cli_import)

if __name__ == "__main__":
    cli()
