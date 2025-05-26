import os
from logging import DEBUG, ERROR, INFO, WARNING, Logger
from typing import Callable, TypeVar, Iterable, Any, cast
import argparse

from ..communication import get_logger


_T = TypeVar("_T")


EXIT_CODE_DESCRIPTIONS: dict[int, str] = {
    1: "Unknown",
    2: "Keyboard interrupt",
    3: "Missing dependencies",
    1100: "Error in target point CSV",
    1101: "Duplicate targets between CSV and existing JSON",
    1102: "Error while opening point CSV",
    1103: "Target CSV file does not exist",
    1200: "Unknown measurement order"
}


def user_input(
    prompt: str,
    parser: Callable[[str], _T],
    newline: bool = True
) -> _T:
    while True:
        ans = input(f"> {prompt}{"\n" if newline else ""}")
        try:
            return parser(ans)
        except Exception as e:
            print(e)


def parse_choices_map(
    value: str,
    choices: dict[str, _T],
    ignore_case: bool = True,
    allow_short: bool = True
) -> _T:
    if ignore_case:
        value = value.lower()
        choices.update({(k.lower(), v) for k, v in choices.items()})

    try:
        if allow_short:
            possible = list(
                filter(lambda k: k.startswith(value), choices.keys())
            )
            if len(possible) != 1:
                raise KeyError()
            value = possible[0]

        return choices[value]
    except KeyError:
        raise ValueError(
            f"> {value} is not in the list of acceptable inputs "
            f"({tuple(choices.keys())})"
        )


def parse_choices(
    value: str,
    choices: Iterable[str],
    ignore_case: bool = True,
    allow_short: bool = True
) -> str:
    return parse_choices_map(
        value,
        {k: k for k in choices},
        ignore_case,
        allow_short
    )


def parse_yes_no(value: str) -> bool:
    return parse_choices_map(
        value,
        {
            "yes": True,
            "no": False
        }
    )


def parse_cancel_replace_append(value: str) -> str:
    return parse_choices(
        value,
        ("cancel", "replace", "append")
    )


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
            f"({EXIT_CODE_DESCRIPTIONS.get(cast(int, ex.code), "Unknown")})"
        )
        raise ex
    except Exception:
        logger.exception(
            f"Application '{name}' exited due to an unhandled exception"
        )
        exit(1)

    logger.info(f"Application '{name}' finished without error")
    exit(0)
