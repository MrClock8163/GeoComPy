import os
from logging import DEBUG, ERROR, INFO, WARNING, Logger
from typing import Callable, Any, cast
import argparse

from click_extra import echo, style, Color

from ..communication import get_logger


EXIT_CODE_DESCRIPTIONS: dict[int, str] = {
    1: "Unknown",
    2: "Keyboard interrupt",
    3: "Missing dependencies",
    4: "Malformed data",
    1100: "Error in target point CSV",
    1101: "Duplicate targets between CSV and existing JSON",
    1102: "Error while opening point CSV",
    1103: "Target CSV file does not exist",
    1200: "Unknown measurement order"
}


def echo_color(
    message: Any,
    color: str,
    newline: bool = True,
    error: bool = False
) -> None:
    echo(
        style(
            message,
            color
        ),
        nl=newline,
        err=error
    )


def echo_red(
    message: Any,
    newline: bool = True,
    error: bool = False
) -> None:
    echo_color(message, Color.red, newline, error)


def echo_green(
    message: Any,
    newline: bool = True,
    error: bool = False
) -> None:
    echo_color(message, Color.green, newline, error)


def echo_yellow(
    message: Any,
    newline: bool = True,
    error: bool = False
) -> None:
    echo_color(message, Color.yellow, newline, error)


def make_directory(filepath: str) -> None:
    dirname = os.path.dirname(filepath)
    if dirname == "":
        return

    os.makedirs(dirname, exist_ok=True)


def make_logger(name: str, args: argparse.Namespace) -> Logger:
    if args.debug:
        loglevel = DEBUG
    elif args.info:
        loglevel = INFO
    elif args.warning:
        loglevel = WARNING
    elif args.error:
        loglevel = ERROR
    else:
        return get_logger(name)

    return get_logger(name, "stdout", loglevel)


def run_cli_app(
    name: str,
    runner: Callable[..., Any],
    args: argparse.Namespace
) -> None:
    logger = make_logger("APP", args)
    try:
        logger.info(f"Starting '{name}' application")
        runner(args)
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt...")
        exit(2)
    except SystemExit as ex:
        if ex.code == 0:
            logger.info(f"Application '{name}' exited without error")
            raise ex

        logger.error(
            f"Application exited with {ex.code} "
            f"({EXIT_CODE_DESCRIPTIONS.get(cast(int, ex.code), 'Unknown')})"
        )
        raise ex
    except Exception:
        logger.exception(
            f"Application '{name}' exited due to an unhandled exception"
        )
        exit(1)

    logger.info(f"Application '{name}' finished without error")
    exit(0)
