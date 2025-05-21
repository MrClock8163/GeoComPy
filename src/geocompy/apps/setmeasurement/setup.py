import os
import argparse

from ...communication import open_serial
from ...geo import GeoCom
from ...geo.gcdata import Prism
from .. import user_input, parse_yes_no, parse_cancel_replace_append
from . import make_logger
from .targets import (
    TargetList,
    TargetPoint,
    load_targets_from_json,
    export_targets_to_json
)


def setup_set(tps: GeoCom, filepath: str) -> TargetList | None:
    if os.path.exists(filepath):
        action = user_input(
            f"{filepath} already exists. Action? (cancel/replace/append)",
            parse_cancel_replace_append
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
                parse_yes_no
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
            parse_yes_no
        ):
            break

    print("> Set measurement setup finished")

    log.info("Set measurement setup finished")

    return points


def main(args: argparse.Namespace) -> None:
    log = make_logger(args)
    log.info("Starting setup session")

    with open_serial(
        args.port,
        retry=args.retry,
        sync_after_timeout=args.sync_after_timeout,
        speed=args.baud,
        timeout=args.timeout
    ) as com:
        tps = GeoCom(com, log)
        targets = setup_set(tps, args.output)
        if targets is None:
            print("Setup was cancelled or no targets were recorded.")
            return

    log.info("Finished setup session")

    export_targets_to_json(args.output, targets)
    log.info(f"Saved setup results at '{targets}'")


def cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="setup",
        description="Record target definitions for set measurements.",
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
    parser.add_argument(
        "output",
        type=str,
        help=(
            "path to save the JSON containing the recorded targets "
            "(if the file already exists, the new targets can be appended)"
        )
    )

    return parser


if __name__ == "__main__":
    parser = cli()
    main(parser.parse_args())
