import os
import argparse
from datetime import datetime
from logging import Logger, DEBUG, INFO, WARNING, ERROR

from ...communication import open_serial, get_logger
from ...geo import GeoCom
from . import setup_set, measure_set
from .targets import export_targets_to_json
from .sessions import export_session_to_json


def make_logger(args: argparse.Namespace) -> Logger:
    if args.log_debug:
        loglevel = DEBUG
    elif args.log_info:
        loglevel = INFO
    elif args.log_warning:
        loglevel = WARNING
    elif args.log_error:
        loglevel = ERROR
    else:
        return get_logger("TPS")

    if args.log_file is None:
        return get_logger("TPS", "stdout", loglevel)

    return get_logger("TPS", "file", loglevel, file=args.log_file)


def run_setup(args: argparse.Namespace) -> None:
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


def run_measure(args: argparse.Namespace) -> None:
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
        session = measure_set(tps, args.targets, args.twoface, args.cycles)

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
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        help="record target points for set measurement"
    )
    group_setup_com = parser_setup.add_argument_group("communication")
    group_setup_com.add_argument(
        "port",
        type=str,
        help="serial port (e.g. COM1)"
    )
    group_setup_com.add_argument(
        "-b",
        "--baud",
        type=int,
        default=9600,
        help="serial connection speed"
    )
    group_setup_com.add_argument(
        "-t",
        "--timeout",
        type=int,
        default=15,
        help="connection timeout to set"
    )
    group_setup_com.add_argument(
        "-r",
        "--retry",
        type=int,
        default=1,
        help="number of connection retry attempts"
    )
    group_setup_com.add_argument(
        "-sat",
        "--sync-after-timeout",
        action="store_true",
        help="attempt to synchronize message que after a connection timeout"
    )
    group_setup_logging = parser_setup.add_argument_group("logging")
    group_setup_logging.add_argument(
        "-l",
        "--log-file",
        type=str,
        help="logging file"
    )
    group_setup_logging_levels = (
        group_setup_logging.add_mutually_exclusive_group()
    )
    group_setup_logging_levels.add_argument(
        "--log-debug",
        "--debug",
        help="set logging level to DEBUG",
        action="store_true"
    )
    group_setup_logging_levels.add_argument(
        "--log-info",
        "--info",
        help="set logging level to INFO",
        action="store_true"
    )
    group_setup_logging_levels.add_argument(
        "--log-warning",
        "--warning",
        help="set logging level to WARNING",
        action="store_true"
    )
    group_setup_logging_levels.add_argument(
        "--log-error",
        "--error",
        help="set logging level to ERROR",
        action="store_true"
    )
    parser_setup.add_argument(
        "output",
        type=str,
        help=(
            "path to save the JSON containing the recorded targets "
            "(if the file already exists, the new targets can be appended)"
        )
    )
    parser_setup.set_defaults(func=run_setup)

    parser_measure = subparsers.add_parser(
        "measure",
        description="Run set measurement",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        help="run set measurements"
    )

    group_measure_com = parser_measure.add_argument_group("communication")
    group_measure_com.add_argument(
        "port",
        type=str,
        help="serial port (e.g. COM1)"
    )
    group_measure_com.add_argument(
        "-b",
        "--baud",
        type=int,
        default=9600,
        help="serial connection speed"
    )
    group_measure_com.add_argument(
        "-t",
        "--timeout",
        type=int,
        default=15,
        help="connection timeout to set"
    )
    group_measure_com.add_argument(
        "-r",
        "--retry",
        type=int,
        default=1,
        help="number of connection retry attempts"
    )
    group_measure_com.add_argument(
        "-sat",
        "--sync-after-timeout",
        action="store_true",
        help="attempt to synchronize message que after a connection timeout"
    )
    group_measure_program = parser_measure.add_argument_group("program")
    group_measure_program.add_argument(
        "targets",
        type=str,
        help="JSON file containing target definitions"
    )
    group_measure_program.add_argument(
        "directory",
        type=str,
        help="directory to save measurement output to"
    )
    group_measure_program.add_argument(
        "-p",
        "--prefix",
        type=str,
        default="setmeasurement_",
        help="prefix to prepend to the set measurement output files"
    )
    group_measure_program.add_argument(
        "-c",
        "--cycles",
        type=int,
        default=1,
        help="number of measurement cycles"
    )
    group_measure_program.add_argument(
        "-tf",
        "--twoface",
        action="store_true",
        help="measure in both face 1 and face 2"
    )
    group_measure_program.add_argument(
        "-s",
        "--sync-time",
        action="store_true",
        help="synchronize instrument time and date with the computer"
    )
    group_measure_program.add_argument(
        "-pt",
        "--points",
        type=str,
        help=(
            "targets to use from loaded target definition "
            "(comma separated list)"
        )
    )
    group_measure_logging = parser_measure.add_argument_group("logging")
    group_measure_logging.add_argument(
        "-l",
        "--log-file",
        type=str,
        help="logging file"
    )
    group_measure_logging_levels = (
        group_measure_logging.add_mutually_exclusive_group()
    )
    group_measure_logging_levels.add_argument(
        "--debug",
        "--log-debug",
        help="set logging level to DEBUG",
        action="store_true"
    )
    group_measure_logging_levels.add_argument(
        "--info",
        "--log-info",
        help="set logging level to INFO",
        action="store_true"
    )
    group_measure_logging_levels.add_argument(
        "--warning",
        "--log-warning",
        help="set logging level to WARNING",
        action="store_true"
    )
    group_measure_logging_levels.add_argument(
        "--error",
        "--log-error",
        help="set logging level to ERROR",
        action="store_true"
    )

    parser_measure.set_defaults(func=run_measure)

    return parser
