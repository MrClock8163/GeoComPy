from __future__ import annotations

import os
import json
import re
from typing import TypedDict, Iterator, Any

try:
    from jsonschema import validate
except Exception:
    validate = lambda *args: None  # noqa: E731

from ..data import Coordinate
from ..geo.gcdata import Prism
from .utils import make_directory


class TargetPointDict(TypedDict):
    name: str
    prism: str
    height: float
    coords: tuple[float, float, float]


class TargetListDict(TypedDict):
    targets: list[TargetPointDict]


class TargetPoint:
    def __init__(
        self,
        name: str,
        prism: Prism,
        height: float,
        coords: Coordinate
    ) -> None:
        self.name = name
        self.prism = prism
        self.height = height
        self.coords = coords

    @classmethod
    def from_dict(cls, data: TargetPointDict) -> TargetPoint:
        return cls(
            data["name"],
            Prism[data["prism"]],
            data["height"],
            Coordinate(*data["coords"])
        )

    def to_dict(self) -> TargetPointDict:
        return {
            "name": self.name,
            "prism": self.prism.name,
            "height": self.height,
            "coords": (self.coords.x, self.coords.y, self.coords.z)
        }

    def __str__(self) -> str:
        return str(self.to_dict())


class TargetList:
    def __init__(self) -> None:
        self._targets: list[TargetPoint] = []
        self._targets_lookup: dict[str, TargetPoint] = {}

    @classmethod
    def from_dict(cls, data: TargetListDict) -> TargetList:
        output = cls()
        for item in data["targets"]:
            point = TargetPoint.from_dict(item)
            output._targets.append(point)
            output._targets_lookup[point.name] = point

        return output

    def to_dict(self) -> TargetListDict:
        return {"targets": [t.to_dict() for t in self._targets]}

    def __str__(self) -> str:
        return str(self.to_dict())

    def __contains__(self, name: str) -> bool:
        return name in self._targets_lookup

    def __len__(self) -> int:
        return len(self._targets)

    def __iter__(self) -> Iterator[TargetPoint]:
        return iter(self._targets)

    def __reversed__(self) -> Iterator[TargetPoint]:
        return reversed(self._targets)

    def add_target(self, target: TargetPoint) -> None:
        if target.name in self._targets_lookup:
            raise ValueError(f"Target {target.name} already exists")

        self._targets.append(target)
        self._targets_lookup[target.name] = target

    def pop_target(self, name: str) -> TargetPoint:
        target = self._targets_lookup[name]
        self._targets.remove(target)
        self._targets_lookup.pop(name)
        return target

    def get_target(self, name: str) -> TargetPoint:
        return self._targets_lookup[name]

    def get_target_names(self) -> list[str]:
        return list(self._targets_lookup.keys())


def export_targets_to_json(filepath: str, targets: TargetList) -> None:
    make_directory(filepath)
    with open(filepath, "wt", encoding="utf8") as file:
        json.dump(targets.to_dict(), file, indent=4)


def load_targets_from_json(filepath: str) -> TargetList:
    with (
        open(filepath, "rt", encoding="utf8") as file,
        open(
            os.path.join(
                os.path.dirname(__file__),
                "schema_targets.json"
            ),
            "rt",
            encoding="utf8"
        ) as file_schema
    ):
        data: TargetListDict = json.load(file)
        schema: dict[str, Any] = json.load(file_schema)

    validate(data, schema)

    return TargetList.from_dict(data)


_COLUMNS = re.compile(r"^[PENZ_]{4,}$")


def import_targets_from_csv(
    filepath: str,
    separator: str,
    columns: str,
    reflector: Prism,
    header: int = 0
) -> TargetList:
    columns = columns.upper()

    if not _COLUMNS.match(columns):
        raise ValueError("Invalid column spec")

    col_ptid = columns.find("P")
    col_east = columns.find("E")
    col_north = columns.find("N")
    col_height = columns.find("Z")

    if -1 in (col_ptid, col_east, col_north, col_height):
        raise ValueError(
            "Some of the PENZ columns were not found in the column spec"
        )

    output = TargetList()

    with open(filepath, "rt", encoding="utf8") as file:
        for i in range(header):
            next(file)

        for line in file:
            fields = line.strip().split(separator)
            point = TargetPoint(
                fields[col_ptid],
                reflector,
                0.0,
                Coordinate(
                    float(fields[col_east]),
                    float(fields[col_north]),
                    float(fields[col_height])
                )
            )
            output.add_target(point)

    return output
