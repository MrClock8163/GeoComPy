import argparse
import glob
import json
from itertools import chain
from typing import Literal

from .sessions import (
    SessionDict,
    SessionListDict,
    Session,
    export_sessions_to_json
)
from .. import make_directory


def run_merge(args: argparse.Namespace) -> None:
    sessions: list[SessionDict] = []
    for path in chain.from_iterable(args.inputs):
        with open(path, "rt", encoding="utf8") as file:
            sessions.extend(json.load(file)["sessions"])

    if len(sessions) == 0:
        print("There were no sessions found to merge")
        exit(0)

    data: SessionListDict = {"sessions": []}
    if args.concatenate:
        data["sessions"] = sessions
    elif args.aggregate:
        data["sessions"].append(
            {
                "time": sessions[0]["time"],
                "battery": sessions[0]["battery"],
                "inclination": sessions[0]["inclination"],
                "temperature": sessions[0]["temperature"],
                "station": sessions[0]["station"],
                "instrumentheight": sessions[0]["instrumentheight"],
                "order": sessions[0]["order"],
                "cycles": sum(s["cycles"] for s in sessions),
                "points": [p for s in sessions for p in s["points"]]
            }
        )

    make_directory(args.output)
    with open(args.output, "wt", encoding="utf8") as file:
        json.dump(
            data,
            file,
            indent=4
        )

    print(f"Merged {len(sessions)} sessions")


def run_pair(args: argparse.Namespace) -> None:
    with open(args.input, "rt", encoding="utf8") as file:
        data: dict[Literal['sessions'], list[SessionDict]] = json.load(file)

    sessions: list[Session] = []
    for s in data["sessions"]:
        session = Session.from_dict(s)
        count_points = len(session.points)

        if session.order != "ABCD" and count_points % 2 != 0:
            print(
                f"Unexpected measurement count ({count_points}) "
                f"for {session.order} order"
            )
            exit()

        session.reorder_to_pairs()
        sessions.append(session)

    export_sessions_to_json(args.output, sessions)


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

    parser_pair = subparsers.add_parser(
        "pair",
        description="Reorder measurements to F1-F2 pairs for processing",
        help="reorder measurements to F1-F2 pairs for processing"
    )
    parser_pair.add_argument(
        "input",
        help="set measurement session JSON file",
        type=str
    )
    parser_pair.add_argument(
        "output",
        help="output file",
        type=str
    )
    parser_pair.set_defaults(func=run_pair)

    return parser


if __name__ == "__main__":
    parser = cli()
    args = parser.parse_args()
    args.func(args)
