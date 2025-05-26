from __future__ import annotations

import json
from datetime import datetime
from typing import TypedDict, Iterable

from ...data import Angle, Coordinate
from ...geo.gcdata import Face
from .. import make_directory


class PointDict(TypedDict):
    name: str
    face: str
    height: float
    measurement: tuple[float, float, float]


class SessionDict(TypedDict):
    time: str
    battery: float | None
    inclination: tuple[float, float] | None
    temperature: float | None
    station: tuple[float, float, float]
    instrumentheight: float
    points: list[PointDict]


class SessionListDict(TypedDict):
    sessions: list[SessionDict]


class Point:
    def __init__(
        self,
        name: str,
        face: Face,
        height: float,
        measurement: tuple[Angle, Angle, float]
    ) -> None:
        self.name = name
        self.face = face
        self.height = height
        self.measurement = measurement

    def to_dict(self) -> PointDict:
        return {
            "name": self.name,
            "face": self.face.name,
            "height": self.height,
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
        station: Coordinate,
        instrumentheight: float
    ) -> None:
        self.time = time
        self.battery = battery
        self.temperature = temperature
        self.inclination = inclination
        self.station = station
        self.instrumentheight = instrumentheight
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
            "instrumentheight": self.instrumentheight,
            "points": [p.to_dict() for p in self.points]
        }


def export_sessions_to_json(
    filepath: str,
    sessions: Iterable[Session]
) -> None:
    make_directory(filepath)
    with open(filepath, "wt", encoding="utf8") as file:
        json.dump(
            {
                "sessions": [s.to_dict() for s in sessions]
            },
            file,
            indent=4
        )


def export_session_to_log(filepath: str, session: Session) -> None:
    make_directory(filepath)
    with open(filepath, "at", encoding="utf8") as file:
        file.write(
            f"# SESSION start={session.time}, "
            f"temperature={session.temperature}C, "
            f"battery={session.battery}%, "
            f"station={session.station}, "
            f"instrumentheight={session.instrumentheight}\n"
            "# point,face,azimut[deg],zenith[deg],slope,east,north,height\n"
        )

        for point in session.points:
            hz, v, d = point.measurement
            file.write(
                f"{point.name},{point.face.name},"
                f"{hz.asunit('deg')},{v.asunit('deg')},{d}\n"
            )
