import os
import argparse
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

    with open_serial(args.port) as com:
        tps = GeoCom(com, log)
        targets = setup_set(tps, args.output)
        if targets is None:
            print("Setup was cancelled or no targets were recorded.")
            return

        export_targets_to_json(args.output, targets)


def run_measure(args: argparse.Namespace) -> None:
    if args.log is not None:
        log = get_logger("TPS", "file", DEBUG, args.log)
    else:
        log = get_logger("TPS")

    with open_serial(args.port) as com:
        tps = GeoCom(com, log)
        session = measure_set(tps, args.targets, args.twoface, args.repeat)

    timestamp = session.start.time.strftime("%Y%m%d_%H%M%S")

    filename = os.path.join(
        args.directory,
        f"{args.prefix}_{timestamp}.json"
    )
    export_session_to_json(filename, session)


parser = argparse.ArgumentParser(
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
    help="path to save the JSON containing the recorded targets"
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
    default="setmeasurement",
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
parser_measure.set_defaults(func=run_measure)

args = parser.parse_args()

args.func(args)
