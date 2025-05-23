import argparse
import glob
import json
from itertools import chain
from typing import Any

from .sessions import SessionDict
from .. import make_directory


def run_merge(args: argparse.Namespace) -> None:
    sessions: list[SessionDict] = []
    for path in chain.from_iterable(args.inputs):
        with open(path, "rt", encoding="utf8") as file:
            sessions.append(json.load(file))

    if len(sessions) == 0:
        print("> There were no sessions found to merge")
        return

    data: dict[str, Any] = {}
    if args.concatenate:
        data = {"sessions": sessions}
    elif args.aggregate:
        data = {
            "station": sessions[0]["station"],
            "time": sessions[0]["time"],
            "points": [p for s in sessions for p in s["points"]]
        }

    make_directory(args.output)
    with open(args.output, "wt", encoding="utf8") as file:
        json.dump(
            data,
            file,
            indent=4
        )

    print(f"> Merged {len(sessions)} sessions")


def cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        "process",
        description="Process the results of set measurements.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    subparsers = parser.add_subparsers()
    parser_merge = subparsers.add_parser(
        "merge",
        description="Merge the output of multiple set measurement sessions.",
        help="merge the output of multiple set measurement sessions"
    )
    group_merge_mode = parser_merge.add_mutually_exclusive_group(required=True)
    group_merge_mode.add_argument(
        "--concatenate",
        help="preserve sessions and simply put them into a single file",
        action="store_true"
    )
    group_merge_mode.add_argument(
        "--aggregate",
        help="aggregate all points into a single session",
        action="store_true"
    )
    parser_merge.add_argument(
        "output",
        help="output file",
        type=str
    )
    parser_merge.add_argument(
        "inputs",
        help="set measurement session JSON files (glob notation)",
        nargs="+",
        type=glob.glob
    )
    parser_merge.set_defaults(func=run_merge)

    return parser


if __name__ == "__main__":
    parser = cli()
    args = parser.parse_args()
    # print(args)
    args.func(args)
