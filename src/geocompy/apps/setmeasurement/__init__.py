import argparse
from logging import Logger, DEBUG, INFO, WARNING, ERROR

from ...communication import get_logger


def make_logger(args: argparse.Namespace) -> Logger:
    if args.debug:
        loglevel = DEBUG
    elif args.info:
        loglevel = INFO
    elif args.warning:
        loglevel = WARNING
    elif args.error:
        loglevel = ERROR
    else:
        return get_logger("TPS")

    if args.log_file is None:
        return get_logger("TPS", "stdout", loglevel)

    return get_logger("TPS", "file", loglevel, file=args.log_file)
