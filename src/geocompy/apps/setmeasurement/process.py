import argparse
import glob
import json
from itertools import chain

from .sessions import SessionDict
from .. import make_directory


def run_merge(args: argparse.Namespace) -> None:
    session: SessionDict = {"cycles": []}
    count_sessions = 0
    for path in chain.from_iterable(args.inputs):
        with open(path, "rt", encoding="utf8") as file:
            loaded_cycles: SessionDict = json.load(file)
            session["cycles"].extend(loaded_cycles["cycles"])
            count_sessions += 1

    if len(session["cycles"]) == 0:
        print("There were no sessions found to merge")
        exit(0)

    make_directory(args.output)
    with open(args.output, "wt", encoding="utf8") as file:
        json.dump(
            session,
            file,
            indent=4
        )

    print(
        f"Merged {len(session["cycles"])} cycles "
        f"from {count_sessions} sessions"
    )


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
    args.func(args)
