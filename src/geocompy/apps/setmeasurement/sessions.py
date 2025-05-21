from __future__ import annotations

import json
from datetime import datetime
from typing import TypedDict

from ...data import Angle, Coordinate
from ...geo.gcdata import Face


class PointDict(TypedDict):
    name: str
    face: str
    polar: tuple[float, float, float]
    cartesian: tuple[float, float, float]


class SessionMetaDict(TypedDict):
    time: str
    temperature: float | None
    battery: int | None
    inclination: tuple[float, float] | None


class SessionDict(TypedDict):
    start: SessionMetaDict
    end: SessionMetaDict
    points: list[PointDict]


class SessionListDict(TypedDict):
    sessions: list[SessionDict]


class Point:
    def __init__(
        self,
        name: str,
        face: Face,
        polar: tuple[Angle, Angle, float],
        cartesian: Coordinate
    ) -> None:
        self.name = name
        self.face = face
        self.polar = polar
        self.cartesian = cartesian

    def to_dict(self) -> PointDict:
        return {
            "name": self.name,
            "face": self.face.name,
            "polar": (
                float(self.polar[0]),
                float(self.polar[1]),
                self.polar[2]
            ),
            "cartesian": (
                self.cartesian.x,
                self.cartesian.y,
                self.cartesian.z
            )
        }


class SessionMeta:
    def __init__(
        self,
        time: datetime,
        temperature: float | None,
        battery: int | None,
        inclination: tuple[Angle, Angle] | None
    ) -> None:
        self.time = time
        self.temperature = temperature
        self.battery = battery
        self.inclination = inclination

    def to_dict(self) -> SessionMetaDict:
        return {
            "time": str(self.time),
            "temperature": self.temperature,
            "battery": self.battery,
            "inclination": (
                float(self.inclination[0]),
                float(self.inclination[1])
            ) if self.inclination is not None else None
        }


class Session:
    def __init__(
        self,
        start: SessionMeta
    ) -> None:
        self.start = start
        self.points: list[Point] = []

    def finished(self, end: SessionMeta) -> None:
        self.end = end

    def add_point(self, point: Point) -> None:
        self.points.append(point)

    def to_dict(self) -> SessionDict:
        return {
            "start": self.start.to_dict(),
            "end": self.end.to_dict(),
            "points": [p.to_dict() for p in self.points]
        }


def export_session_to_json(filepath: str, session: Session) -> None:
    with open(filepath, "wt", encoding="utf8") as file:
        json.dump(session.to_dict(), file, indent=4)


def export_session_to_log(filepath: str, session: Session) -> None:
    with open(filepath, "at", encoding="utf8") as file:
        file.write(
            f"# SESSION start={session.start.time}, "
            f"temperature={session.start.temperature}C, "
            f"battery={session.start.battery}%\n"
            "# point,face,azimut[deg],zenith[deg],slope,east,north,height\n"
        )

        for point in session.points:
            hz, v, d = point.polar
            x, y, z = point.cartesian
            file.write(
                f"{point.name},{point.face.name},"
                f"{hz.asunit('deg')},{v.asunit('deg')},{d},"
                f"{x},{y},{z}\n"
            )

        file.write(
            f"# SESSION end={session.end.time}, "
            f"temperature={session.end.temperature}C, "
            f"battery={session.end.battery}%\n"
        )
