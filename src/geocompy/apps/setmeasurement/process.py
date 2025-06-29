import os
import argparse
import glob
import json
import math
from itertools import chain
from typing import Sequence

try:
    from jmespath import search
    from jsonschema import validate, ValidationError
except ModuleNotFoundError:
    print(
        """
Missing dependencies. The Set Measurement processing needs the following
dependencies:
- jmespath
- jsonschema

Install the missing dependencies manually, or install GeoComPy with the
'apps' extra:

pip install geocompy[apps]
"""
    )
    exit(3)

from ...data import Angle, Coordinate
from .sessions import SessionDict
from .. import make_directory


class SessionValidator:
    def __init__(
        self,
        twoface: bool
    ) -> None:
        self._twoface = twoface
        with open(
            os.path.join(
                os.path.dirname(__file__),
                "schema_session.json"
            ),
            "rt",
            encoding="utf8"
        ) as file_schema:
            self._schema = json.load(file_schema)

    def validate(self, data: SessionDict) -> None:
        validate(data, self._schema)

        ptids = search("cycles[*].points[*].name", data)
        if len(ptids) == 0:
            return

        first = ptids[0]
        for ids in ptids[1:]:
            if ids != first:
                raise ValueError("Mismatching points between cycles")

        if not self._twoface:
            return

        for i, c in enumerate(data["cycles"]):
            for p in c["points"]:
                if p.get("face2") is None:
                    raise ValueError(
                        f"Point {p['name']} is missing face 2 "
                        f"measurements in cycle {i + 1}"
                    )

    def validate_for_merge(self, data: Sequence[SessionDict]) -> None:
        for s in data:
            validate(s, self._schema)


def run_validate(args: argparse.Namespace) -> None:
    sessions: list[SessionDict] = []
    for path in chain.from_iterable(args.inputs):
        with open(path, "rt", encoding="utf8") as file:
            sessions.append(json.load(file))

    validator = SessionValidator(not args.allow_oneface)
    if args.schema_only:
        try:
            validator.validate_for_merge(sessions)
            print("Schema validation succeeded")
            exit(0)
        except ValidationError as ve:
            print(
                "One of the input files does not follow the required schema"
            )
            print(ve)
            exit(4)

    try:
        for s in sessions:
            validator.validate(s)

        print("Validation succeeded")
        exit(0)
    except ValidationError as ve:
        print(
            "One of the input files does not follow the required schema"
        )
        print(ve)
        exit(4)
    except ValueError as e:
        print(f"The merged output could not be validated ({e})")
        exit(4)


def run_merge(args: argparse.Namespace) -> None:
    sessions: list[SessionDict] = []
    for path in chain.from_iterable(args.inputs):
        with open(path, "rt", encoding="utf8") as file:
            sessions.append(json.load(file))

    validator = SessionValidator(not args.allow_oneface)
    try:
        validator.validate_for_merge(sessions)
    except ValidationError as ve:
        print("One of the input files does not follow the required schema")
        print(ve)
        exit(4)

    if len(sessions) == 0:
        print("There were no sessions found to merge")
        exit(0)

    session: SessionDict = {
        "station": sessions[0]["station"],
        "instrumentheight": sessions[0]["instrumentheight"],
        "cycles": [c for s in sessions for c in s["cycles"]]
    }

    try:
        validator.validate(session)
    except ValidationError as ve:
        print("The merging process caused a schema error")
        print(ve)
        exit(4)
    except ValueError as e:
        print(f"The merged output could not be validated ({e})")
        exit(4)

    make_directory(args.output)
    with open(args.output, "wt", encoding="utf8") as file:
        json.dump(
            session,
            file,
            indent=4
        )

    print(
        f"Merged {len(session['cycles'])} cycles "
        f"from {len(sessions)} sessions"
    )


def calc_angles(
    hz_f1: Angle,
    v_f1: Angle,
    hz_f2: Angle,
    v_f2: Angle
) -> tuple[Angle, Angle, Angle, Angle]:
    temp = hz_f2 - hz_f1
    if temp < 0:
        collim = (temp + Angle(180, 'deg')) / 2
    else:
        collim = (temp - Angle(180, 'deg')) / 2

    hz = hz_f1 + collim

    index = (Angle(360, 'deg') - v_f1 - v_f2) / 2
    v = v_f1 + index

    return hz, v, collim, index


def calc_coords(
    coords: list[Coordinate]
) -> tuple[Coordinate, Coordinate]:
    def adjust(values: list[float]) -> tuple[float, float]:
        n = len(values)
        adjusted = math.fsum(values) / n
        dev = math.sqrt(math.fsum([(v - adjusted)**2 for v in values]) / n)
        return adjusted, dev

    xi = [c.x for c in coords]
    yi = [c.y for c in coords]
    zi = [c.z for c in coords]

    x, x_dev = adjust(xi)
    y, y_dev = adjust(yi)
    z, z_dev = adjust(zi)

    return Coordinate(x, y, z), Coordinate(x_dev, y_dev, z_dev)


def run_calc(args: argparse.Namespace) -> None:
    with open(args.input, "rt", encoding="utf8") as file:
        data: SessionDict = json.load(file)

    validator = SessionValidator(not args.allow_oneface)
    try:
        validator.validate(data)
    except ValidationError as ve:
        print("Input data does not follow the required schema")
        print(ve)
        exit(4)
    except ValueError as e:
        print("The input data did not pass validation")
        print(e)
        exit(4)

    points = {"points": search("cycles[].points[]", data)}
    ptids = list(set(search("points[].name", points)))

    station = Coordinate(
        *data["station"]
    ) + Coordinate(
        0,
        0,
        data["instrumentheight"]
    )
    coords: dict[str, list[Coordinate]] = {}
    for pt in ptids:
        measurements = search(
            f"points[?name=='{pt}'].[height, face1, face2]",
            points
        )
        if pt not in coords:
            coords[pt] = []
        for cycle in measurements:
            height = cycle[0]
            hz = Angle(cycle[1][0])
            v = Angle(cycle[1][1])
            d = cycle[1][2]

            if cycle[2] is not None:
                hz_f2 = Angle(cycle[2][0])
                v_f2 = Angle(cycle[2][1])
                d_f2 = cycle[2][2]

                hz, v, co, z = calc_angles(
                    hz,
                    v,
                    hz_f2,
                    v_f2
                )

                d = (d + d_f2) / 2
            elif not args.allow_oneface:
                print("Not all measurements have data for both faces")
                exit(4)

            c = station + Coordinate.from_polar(
                hz,
                v,
                d
            ) - Coordinate(
                0,
                0,
                height
            )
            coords[pt].append(c)

    final: list[tuple[str, Coordinate, Coordinate]] = []
    for name, coo in coords.items():
        coord, dev = calc_coords(coo)
        final.append((name, coord, dev))

    with open(args.output, "wt", encoding="utf8") as file:
        if args.header:
            file.write(
                args.delimiter.join(
                    ["id", "e", "n", "h", "sigma_e", "sigma_n", "sigma_h"]
                ) + "\n"
            )

        fmt = "{0:." + str(args.precision) + "f}"
        for name, coord, dev in final:
            fields = [
                name,
                fmt.format(coord.x),
                fmt.format(coord.y),
                fmt.format(coord.z),
                fmt.format(dev.x),
                fmt.format(dev.y),
                fmt.format(dev.z)
            ]
            file.write(
                args.delimiter.join(fields) + "\n"
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
    parser_merge.add_argument(
        "--allow-oneface",
        help="accept points with face 1 measurements only as well",
        action="store_true"
    )
    parser_merge.set_defaults(func=run_merge)

    parser_calc = subparsers.add_parser(
        "calculate",
        description="Calculate results from set measurements",
        help="calculate results from set measurements"
    )
    parser_calc.add_argument(
        "input",
        help="input session file to process",
        type=str
    )
    parser_calc.add_argument(
        "output",
        help="output CSV file",
        type=str
    )
    parser_calc.add_argument(
        "--header",
        help="write column headers",
        action="store_true"
    )
    parser_calc.add_argument(
        "-d",
        "--delimiter",
        help="column delimiter character",
        type=str,
        default=","
    )
    parser_calc.add_argument(
        "-p",
        "--precision",
        help="decimal precision",
        type=int,
        default=4
    )
    parser_calc.add_argument(
        "--allow-oneface",
        help="accept points with face 1 measurements only as well",
        action="store_true"
    )
    parser_calc.set_defaults(func=run_calc)

    parser_validate = subparsers.add_parser(
        "validate",
        description="Validate session output files",
        help="validate session output files"
    )
    parser_validate.add_argument(
        "inputs",
        help="set measurement session JSON files (glob notation)",
        nargs="+",
        type=glob.glob
    )
    parser_validate.add_argument(
        "-s",
        "--schema-only",
        help="only validate the JSON schema",
        action="store_true"
    )
    parser_validate.add_argument(
        "--allow-oneface",
        help="accept points with face 1 measurements only as well",
        action="store_true"
    )
    parser_validate.set_defaults(func=run_validate)

    return parser


if __name__ == "__main__":
    parser = cli()
    args = parser.parse_args()
    args.func(args)
