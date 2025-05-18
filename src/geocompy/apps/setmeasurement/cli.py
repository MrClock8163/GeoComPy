import os
import argparse
from datetime import datetime
from logging import DEBUG

from ...communication import open_serial, get_logger
from ...geo import GeoCom
from . import setup_set, measure_set
from .targets import export_targets_to_json
from .sessions import export_session_to_json


def run_setup(args: argparse.Namespace) -> None:
    if args.log is not None:
        log = get_logger("TPS", "file", DEBUG, args.log)
    else:
        log = get_logger("TPS")

    log.info("Starting setup session")

    with open_serial(args.port) as com:
        tps = GeoCom(com, log)
        targets = setup_set(tps, args.output)
        if targets is None:
            print("Setup was cancelled or no targets were recorded.")
            return

    log.info("Finished setup session")

    export_targets_to_json(args.output, targets)
    log.info(f"Saved setup results at '{targets}'")


def run_measure(args: argparse.Namespace) -> None:
    if args.log is not None:
        log = get_logger("TPS", "file", DEBUG, args.log)
    else:
        log = get_logger("TPS")

    log.info("Starting measurement session")

    with open_serial(args.port) as com:
        tps = GeoCom(com, log)
        if args.sync_time:
            tps.csv.set_datetime(datetime.now())
        session = measure_set(tps, args.targets, args.twoface, args.repeat)

    log.info("Finished measurement session")

    timestamp = session.start.time.strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(
        args.directory,
        f"{args.prefix}{timestamp}.json"
    )
    export_session_to_json(filename, session)
    log.info(f"Saved measurement results at '{filename}'")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="setmeasurement",
        description="Conduct sets of measurements to target points",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    subparsers = parser.add_subparsers()

    parser_setup = subparsers.add_parser(
        "setup",
        description="Record target points for set measurement",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser_setup.add_argument(
        "port",
        type=str,
        help="serial port (e.g. COM1)"
    )
    parser_setup.add_argument(
        "output",
        type=str,
        help=(
            "path to save the JSON containing the recorded targets "
            "(if the file already exists, the new targets can be appended)"
        )
    )
    parser_setup.add_argument(
        "--log",
        type=str,
        help="logging file"
    )
    parser_setup.set_defaults(func=run_setup)

    parser_measure = subparsers.add_parser(
        "measure",
        description="Run set measurement",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser_measure.add_argument(
        "port",
        type=str,
        help="serial port (e.g. COM1)"
    )
    parser_measure.add_argument(
        "targets",
        type=str,
        help="JSON file containing target definitions"
    )
    parser_measure.add_argument(
        "directory",
        type=str,
        help="directory to save measurement output to"
    )
    parser_measure.add_argument(
        "--prefix",
        type=str,
        default="setmeasurement_",
        help="prefix to prepend to the set measurement output files"
    )
    parser_measure.add_argument(
        "--log",
        type=str,
        help="logging file"
    )
    parser_measure.add_argument(
        "--repeat",
        type=int,
        default=1,
        help="number of measurement repetitions"
    )
    parser_measure.add_argument(
        "--twoface",
        action="store_true",
        help="measure in both face 1 and face 2"
    )
    parser_measure.add_argument(
        "--sync-time",
        action="store_true",
        help="synchronize instrument time and date with the computer"
    )
    parser_measure.set_defaults(func=run_measure)

    return parser
