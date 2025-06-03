from __future__ import annotations

import json
from datetime import datetime
from typing import TypedDict, Iterable, Literal

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
    order: Literal['AaBb', 'AabB', 'ABab', 'ABba', 'ABCD']
    cycles: int
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

    @classmethod
    def from_dict(cls, data: PointDict) -> Point:
        return cls(
            data["name"],
            Face[data["face"]],
            data["height"],
            (
                Angle(data["measurement"][0]),
                Angle(data["measurement"][1]),
                data["measurement"][2]
            )
        )

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
        order: Literal['AaBb', 'AabB', 'ABab', 'ABba', 'ABCD'],
        cycles: int,
        instrumentheight: float
    ) -> None:
        self.time = time
        self.battery = battery
        self.temperature = temperature
        self.inclination = inclination
        self.station = station
        self.instrumentheight = instrumentheight
        self.order = order
        self.cycles = cycles
        self.points: list[Point] = []

    @classmethod
    def from_dict(cls, data: SessionDict) -> Session:
        output = cls(
            datetime.fromisoformat(data["time"]),
            data["battery"],
            data["temperature"],
            (
                Angle(data["inclination"][0]),
                Angle(data["inclination"][1])
            ) if data["inclination"] is not None else None,
            Coordinate(*data["station"]),
            data["order"],
            data["cycles"],
            data["instrumentheight"]
        )

        for p in data["points"]:
            output.add_point(Point.from_dict(p))

        return output

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
            "order": self.order,
            "cycles": self.cycles,
            "points": [p.to_dict() for p in self.points]
        }

    @staticmethod
    def _reorder_cycle_to_pairs(
        order: Literal['AaBb', 'AabB', 'ABab', 'ABba', 'ABCD'],
        points: list[Point]
    ) -> list[Point]:
        match order:
            case "ABCD" | "AaBb":
                return points
            case "AabB":
                count_points = len(points)
                pairs: list[Point] = []
                for i in range(0, count_points, 2):
                    if i % 2 == 0:
                        pairs.extend(points[i:i+1])

                    pairs.extend(reversed(points[i:i+1]))

            case "ABab":
                count_targets = len(points) // 2
                face1 = points[:count_targets]
                face2 = points[count_targets:]
                pairs = [
                    p for pair in zip(face1, face2) for p in pair
                ]
            case "ABba":
                count_targets = len(points) // 2
                face1 = points[:count_targets]
                face2 = list(reversed(points[count_targets:]))
                pairs = [
                    p for pair in zip(face1, face2) for p in pair
                ]

            case _:
                raise ValueError(f"Unknown measurement order {order}")

        return pairs

    def reorder_to_pairs(self) -> None:
        count_points = len(self.points)
        count_targets = count_points // self.cycles
        pairs: list[Point] = []
        for i in range(0, count_points, count_points // self.cycles):
            pairs.extend(
                self._reorder_cycle_to_pairs(
                    self.order,
                    self.points[i:i+count_targets]
                )
            )

        iter_points = iter(pairs)
        for f1, f2 in zip(iter_points, iter_points):
            if f1.name != f2.name or f1.face != Face.F1 or f2.face != Face.F2:
                raise ValueError(
                    "Point names and/or faces do not match after reordering "
                    f"to pairs ({f1.name}-{f1.face} and {f2.name}-{f2.face})"
                )
        self.points = pairs
        self.order = "AaBb"


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
