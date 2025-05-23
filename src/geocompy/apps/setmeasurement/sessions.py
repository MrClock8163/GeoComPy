from __future__ import annotations

import json
from datetime import datetime
from typing import TypedDict

from ...data import Angle, Coordinate
from ...geo.gcdata import Face
from .. import make_directory


class PointDict(TypedDict):
    name: str
    face: str
    measurement: tuple[float, float, float]


class SessionDict(TypedDict):
    time: str
    battery: float | None
    inclination: tuple[float, float] | None
    temperature: float | None
    station: tuple[float, float, float]
    points: list[PointDict]


class SessionListDict(TypedDict):
    sessions: list[SessionDict]


class Point:
    def __init__(
        self,
        name: str,
        face: Face,
        measurement: tuple[Angle, Angle, float]
    ) -> None:
        self.name = name
        self.face = face
        self.measurement = measurement

    def to_dict(self) -> PointDict:
        return {
            "name": self.name,
            "face": self.face.name,
            "measurement": (
                float(self.measurement[0]),
                float(self.measurement[1]),
                self.measurement[2]
            )
        }


class Session:
    def __init__(
        self,
        time: datetime,
        battery: float | None,
        temperature: float | None,
        inclination: tuple[Angle, Angle] | None,
        station: Coordinate
    ) -> None:
        self.time = time
        self.battery = battery
        self.temperature = temperature
        self.inclination = inclination
        self.station = station
        self.points: list[Point] = []

    def add_point(self, point: Point) -> None:
        self.points.append(point)

    def to_dict(self) -> SessionDict:
        return {
            "time": self.time.isoformat(),
            "battery": self.battery,
            "inclination": (
                float(self.inclination[0]),
                float(self.inclination[1])
            ) if self.inclination is not None else None,
            "temperature": self.temperature,
            "station": (
                self.station.x,
                self.station.y,
                self.station.z
            ),
            "points": [p.to_dict() for p in self.points]
        }


def export_session_to_json(filepath: str, session: Session) -> None:
    make_directory(filepath)
    with open(filepath, "wt", encoding="utf8") as file:
        json.dump(session.to_dict(), file, indent=4)


def export_session_to_log(filepath: str, session: Session) -> None:
    make_directory(filepath)
    with open(filepath, "at", encoding="utf8") as file:
        file.write(
            f"# SESSION start={session.time}, "
            f"temperature={session.temperature}C, "
            f"battery={session.battery}%\n"
            "# point,face,azimut[deg],zenith[deg],slope,east,north,height\n"
        )

        for point in session.points:
            hz, v, d = point.measurement
            file.write(
                f"{point.name},{point.face.name},"
                f"{hz.asunit('deg')},{v.asunit('deg')},{d}\n"
            )
