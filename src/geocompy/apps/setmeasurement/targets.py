from __future__ import annotations

import os
import json
from typing import TypedDict, Iterator, Any

try:
    from jsonschema import validate
except Exception:
    validate = lambda *args: None  # noqa: E731

from ...data import Coordinate
from ...geo.gcdata import Prism


class TargetPointDict(TypedDict):
    name: str
    prism: str
    coords: tuple[float, float, float]


class TargetListDict(TypedDict):
    targets: list[TargetPointDict]


class TargetPoint:
    def __init__(self, name: str, target: Prism, coords: Coordinate) -> None:
        self.name = name
        self.prism = target
        self.coords = coords

    @classmethod
    def from_dict(cls, data: TargetPointDict) -> TargetPoint:
        return cls(
            data["name"],
            Prism[data["prism"]],
            Coordinate(*data["coords"])
        )

    def to_dict(self) -> TargetPointDict:
        return {
            "name": self.name,
            "prism": self.prism.name,
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
    with open(filepath, "wt") as file:
        json.dump(targets.to_dict(), file, indent=4)


def load_targets_from_json(filepath: str) -> TargetList:
    with (
        open(filepath, "rt") as file,
        open(
            os.path.join(
                os.path.dirname(__file__),
                "target_schema.json"
            ),
            "rt"
        ) as file_schema
    ):
        data: TargetListDict = json.load(file)
        schema: dict[str, Any] = json.load(file_schema)

    validate(data, schema)

    return TargetList.from_dict(data)
