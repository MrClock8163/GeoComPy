from __future__ import annotations

import json
from datetime import datetime
from typing import TypedDict, NotRequired

from ...data import Angle, Coordinate
from ...geo.gcdata import Face
from ..utils import make_directory


class PointDict(TypedDict):
    name: str
    height: float
    face1: tuple[float, float, float]
    face2: NotRequired[tuple[float, float, float]]


class CycleDict(TypedDict):
    time: str
    battery: float | None
    inclination: tuple[float, float] | None
    temperature: float | None
    points: list[PointDict]


class SessionDict(TypedDict):
    station: tuple[float, float, float]
    instrumentheight: float
    cycles: list[CycleDict]


class Point:
    def __init__(
        self,
        name: str,
        height: float
    ) -> None:
        self.name = name
        self.height = height
        self.face1: tuple[Angle, Angle, float] | None = None
        self.face2: tuple[Angle, Angle, float] | None = None

    @classmethod
    def from_dict(cls, data: PointDict) -> Point:
        output = cls(
            data["name"],
            data["height"]
        )
        if data.get("face1") is not None:
            output.face1 = (
                Angle(data["face1"][0]),
                Angle(data["face1"][1]),
                data["face1"][2]
            )
        if data.get("face2") is not None:
            output.face2 = (
                Angle(data["face2"][0]),
                Angle(data["face2"][1]),
                data["face2"][2]
            )

        return output

    def to_dict(self) -> PointDict:
        if self.face1 is None:
            raise ValueError("Cannot export point due to missing F1 data")

        output: PointDict = {
            "name": self.name,
            "height": self.height,
            "face1": (
                float(self.face1[0]),
                float(self.face1[1]),
                self.face1[2]
            )
        }

        if self.face2 is not None:
            output["face2"] = (
                float(self.face2[0]),
                float(self.face2[1]),
                self.face2[2]
            )

        return output


class Cycle:
    def __init__(
        self,
        time: datetime,
        battery: float | None,
        temperature: float | None,
        inclination: tuple[Angle, Angle] | None
    ) -> None:
        self.time = time
        self.battery = battery
        self.temperature = temperature
        self.inclination = inclination
        self._points: dict[str, Point] = {}

    @classmethod
    def from_dict(cls, data: CycleDict) -> Cycle:
        output = cls(
            datetime.fromisoformat(data["time"]),
            data["battery"],
            data["temperature"],
            (
                Angle(data["inclination"][0]),
                Angle(data["inclination"][1])
            ) if data["inclination"] is not None else None
        )

        for p in data["points"]:
            output.add_measurement(
                p["name"],
                Face.F1,
                p["height"],
                (
                    Angle(p["face1"][0]),
                    Angle(p["face1"][1]),
                    p["face1"][2]
                )
            )
            if p.get("face2") is None:
                continue

            output.add_measurement(
                p["name"],
                Face.F2,
                p["height"],
                (
                    Angle(p["face2"][0]),
                    Angle(p["face2"][1]),
                    p["face2"][2]
                )
            )

        return output

    def add_measurement(
        self,
        ptid: str,
        face: Face,
        height: float,
        measurement: tuple[Angle, Angle, float]
    ) -> None:
        if ptid not in self._points:
            self._points[ptid] = Point(ptid, height)

        point = self._points[ptid]
        if face == Face.F1:
            if point.face1 is not None:
                raise ValueError(
                    f"Face 1 observation already exists for {ptid}"
                )

            point.face1 = measurement
            return

        if point.face2 is not None:
            raise ValueError(f"Face 2 observation already exists for {ptid}")

        point.face2 = measurement

    def to_dict(self) -> CycleDict:
        return {
            "time": self.time.isoformat(),
            "battery": self.battery,
            "inclination": (
                float(self.inclination[0]),
                float(self.inclination[1])
            ) if self.inclination is not None else None,
            "temperature": self.temperature,
            "points": [p.to_dict() for p in self._points.values()]
        }


class Session:
    def __init__(self, station: Coordinate, iheight: float) -> None:
        self.station = station
        self.iheight = iheight
        self.cycles: list[Cycle] = []

    @classmethod
    def from_dict(cls, data: SessionDict) -> Session:
        output = cls(
            Coordinate(
                data["station"][0],
                data["station"][1],
                data["station"][2]
            ),
            data["instrumentheight"]
        )

        output.cycles = [Cycle.from_dict(c) for c in data["cycles"]]

        return output

    def to_dict(self) -> SessionDict:
        return {
            "station": (
                self.station.x,
                self.station.y,
                self.station.z
            ),
            "instrumentheight": self.iheight,
            "cycles": [c.to_dict() for c in self.cycles]
        }

    def export_to_json(
        self,
        filepath: str
    ) -> None:
        make_directory(filepath)
        with open(filepath, "wt", encoding="utf8") as file:
            json.dump(
                self.to_dict(),
                file,
                indent=4
            )
