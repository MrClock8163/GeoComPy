from __future__ import annotations

from abc import ABC, abstractmethod
from re import compile
from datetime import datetime
from enum import Enum
from typing import Literal, Self

from ..data import Angle


class GsiIndexMode(Enum):
    OFF = 0
    OPERATING1 = 1
    OPERATING3 = 3


class GsiInputMode(Enum):
    TRANSFERRED = 0
    MANUAL = 1
    MEASURED_HZCORR_ON = 2
    MEASURED_HZCORR_OFF = 3
    SPECIAL = 4


class GsiInputModeDNA(Enum):
    MEASURED_CURVCORR_OFF = 0
    MANUAL_CURVCORR_OFF = 1
    MEASURED_CURVCORR_ON = 2
    MANUAL_CURVCORR_ON = 5


class GsiUnit(Enum):
    MILLIMETER = 0
    MILLIFEET = 1
    GON = 2  # 400gon/360deg
    DEG = 3
    DMS = 4
    MIL = 5  # 6400mil/360deg
    DECIMM = 6  # 0.0001m
    DECIMF = 7  # 0.0001ft
    CENTIMM = 8  # 0.00001m


class GsiWord(ABC):
    _GSI = compile(r"^[0-9\.]{6}(?:\+|-)[a-zA-Z0-9\.\?]{8,16} $")
    _WI = 1

    @classmethod
    @abstractmethod
    def parse(cls, value: str) -> GsiWord: ...

    @abstractmethod
    def serialize(self, gsi16: bool = False) -> str: ...

    def __str__(self) -> str:
        return self.serialize(True)

    @staticmethod
    def format(
        wordindex: int,
        data: str,
        meta: str = "",
        negative: bool = False,
        gsi16: bool = False
    ) -> str:
        if wordindex >= 1000 or wordindex < 0:
            raise ValueError(f"GSI word index out of range ({wordindex})")

        if meta != "" and (not meta.isdigit() or len(meta) > 3):
            raise ValueError(f"GSI word meta data is invalid ({meta})")

        wi = str(wordindex)
        filler = "." * (6 - len(wi) - len(meta))

        header = f"{wi}{filler}{meta}"
        sign = "-" if negative else "+"

        if gsi16:
            data = f"{data[-16:]:>.16s}".zfill(16)
        else:
            data = f"{data[-8:]:>.8s}".zfill(8)

        return f"{header:6.6s}{sign}{data} "

    @classmethod
    def format_with_address(
        cls,
        wordindex: int,
        data: str,
        address: int,
        negative: bool = False,
        gsi16: bool = False
    ) -> str:
        value = cls.format(
            wordindex,
            data,
            "",
            negative,
            gsi16
        )

        return f"{value[:2]}{address % 10000:04d}{value[6:]}"

    @classmethod
    def _check_format(cls, value: str) -> None:
        if len(value) not in (16, 24):
            raise ValueError(f"'{value}' has unexpected length for a GSI word")

        if not cls._GSI.match(value):
            raise ValueError(
                f"'{value}' is not a valid serialized representation of "
                f"'{cls.__name__}'"
            )


class GsiUnknown(GsiWord):
    def __init__(
        self,
        wordindex: int,
        data: str = "",
        meta: str = "",
        negative: bool = False,
    ):
        self.wi = wordindex
        self.info = meta
        self.data = data
        self.negative = negative

    @classmethod
    def parse(cls, value: str) -> GsiUnknown:
        cls._check_format(value)
        wi = int(value[:3].rstrip("."))
        data = value[7:-1]
        meta = value[3:6].lstrip(".")
        negative = value[6] == "-"

        return cls(
            wi,
            data,
            meta,
            negative
        )

    def serialize(self, gsi16: bool = False) -> str:
        return self.format(
            self.wi,
            self.data,
            self.info,
            self.negative,
            gsi16
        )


class GsiPointName(GsiWord):
    _GSI = compile(r"^11[\d\.]{4}\+(?:[a-zA-Z0-9]{8,16}) $")
    _WI = 11

    def __init__(self, name: str):
        self.name = name

    def serialize(self, gsi16: bool = False) -> str:
        return self.format(
            self._WI,
            self.name,
            gsi16=gsi16
        )

    @classmethod
    def parse(cls, value: str) -> GsiPointName:
        cls._check_format(value)
        return cls(value[7:-1].lstrip("0"))


class GsiCode(GsiPointName):
    _GSI = compile(r"^41[\d\.]{4}\+(?:[a-zA-Z0-9]{8,16}) $")
    _WI = 41


class GsiSerialNumber(GsiWord):
    _GSI = compile(r"^12[\d\.]{4}\+(?:[0-9]{8,16}) $")
    _WI = 12

    def __init__(self, serialnumber: str):
        self.serialnumber = serialnumber

    def serialize(self, gsi16: bool = False) -> str:
        return self.format(
            self._WI,
            self.serialnumber,
            gsi16=gsi16
        )

    @classmethod
    def parse(cls, value: str) -> GsiSerialNumber:
        cls._check_format(value)
        return cls(value[7:-1].lstrip("0"))


class GsiInstrumentType(GsiWord):
    _GSI = compile(r"^13[\d\.]{4}\+(?:[a-zA-Z0-9]{8,16}) $")
    _WI = 13

    def __init__(self, name: str):
        self.name = name

    def serialize(self, gsi16: bool = False) -> str:
        return self.format(
            self._WI,
            self.name,
            gsi16=gsi16
        )

    @classmethod
    def parse(cls, value: str) -> GsiInstrumentType:
        cls._check_format(value)
        return cls(value[7:-1].lstrip("0"))


class GsiStationName(GsiPointName):
    _GSI = compile(r"^16[\d\.]{4}\+(?:[a-zA-Z0-9]{8,16}) $")
    _WI = 16


class GsiDate(GsiWord):
    _GSI = compile(r"^17[\d\.]{4}\+(?:[0-9]{8,16}) $")
    _WI = 17

    def __init__(self, date: datetime):
        self.date = date

    @classmethod
    def parse(cls, value: str) -> GsiDate:
        cls._check_format(value)

        return cls(
            datetime(
                int(value[-5:-1]),
                int(value[-7:-5]),
                int(value[-9:-7])
            )
        )

    def serialize(self, gsi16: bool = False) -> str:
        return self.format(
            self._WI,
            self.date.strftime("%d%m%Y"),
            gsi16=gsi16
        )


class GsiTime(GsiWord):
    _GSI = compile(r"^19[\d\.]{4}\+(?:[0-9]{8,16}) $")
    _WI = 17

    def __init__(self, time: datetime):
        self.time = time

    @classmethod
    def parse(cls, value: str) -> GsiTime:
        cls._check_format(value)

        return cls(
            datetime(
                1,
                int(value[-9:-7]),
                int(value[-7:-5]),
                int(value[-5:-3]),
                int(value[-3:-1])
            )
        )

    def serialize(self, gsi16: bool = False) -> str:
        return self.format(
            self._WI,
            self.time.strftime("%m%d%H%M"),
            gsi16=gsi16
        )


class GsiAngle(GsiWord):
    _GSI = compile(r"^2[12]\.\d{3}\+(?:[0-9]{8,16}) $")

    def __init__(
        self,
        angle: Angle,
        index: GsiIndexMode,
        source: GsiInputMode,
        type: Literal['hz', 'v'] = "hz"
    ):
        self.angle = angle
        self.indexmode = index
        self.source = source
        self.type = type

    @classmethod
    def parse(cls, value: str) -> GsiAngle:
        cls._check_format(value)

        angletype: Literal['hz', 'v'] = "hz" if value[:2] == "21" else "v"
        index = GsiIndexMode(int(value[3]))
        source = GsiInputMode(int(value[4]))
        unit = GsiUnit(int(value[5]))
        match unit:
            case GsiUnit.GON:
                data = float(f"{value[7:10]}.{value[10:]}")
                angle = Angle(data * 360 / 400, 'deg')
            case GsiUnit.DEG:
                data = float(f"{value[7:10]}.{value[10:]}")
                angle = Angle(data, 'deg')
            case GsiUnit.DMS:
                deg = int(value[7:10])
                min = int(value[10:12])
                sec = float(f"{value[12:14]}.{value[14:]}")
                angle = Angle(
                    (
                        deg
                        + min / 60
                        + sec / 3600
                    ),
                    'deg'
                )
            case GsiUnit.MIL:
                data = float(f"{value[7:11]}.{value[11:]}")
                angle = Angle(data * 360 / 6400, 'deg')
            case _:
                raise ValueError(f"Invalid angle unit: '{unit}'")

        return cls(
            angle,
            index,
            source,
            angletype
        )

    def serialize(self, gsi16: bool = False) -> str:
        data = f"{self.angle.normalized().asunit('deg'):.5f}".replace(".", "")
        if gsi16:
            data = f"{self.angle.normalized().asunit('deg'):.13f}".replace(
                ".",
                ""
            )

        return self.format(
            21 if self.type == 'hz' else 22,
            data,
            f"{self.indexmode.value:d}{self.source.value:d}3",
            gsi16=gsi16
        )


class GsiDistance(GsiWord):
    _GSI = compile(r"^(?:3[123])\.\.\d{2}[\+-](?:[0-9]{8,16}) $")

    _WI_TO_TYPE = {
        31: "slope",
        32: "horizontal",
        33: "vertical"
    }
    _TYPE_TO_WI = {v: k for k, v in _WI_TO_TYPE.items()}

    def __init__(
        self,
        value: float,
        source: GsiInputMode,
        type: str
    ):
        self.value = value
        if type not in self._TYPE_TO_WI:
            raise ValueError(f"Unknown distance type: '{type}'")

        self.type = type
        self.source = source

    @classmethod
    def parse(cls, value: str) -> Self:
        cls._check_format(value)

        disttype = cls._WI_TO_TYPE[int(value[:3].rstrip("."))]
        source = GsiInputMode(int(value[4]))
        unit = GsiUnit(int(value[5]))
        data = int(value[6:-1])
        match unit:
            case GsiUnit.MILLIMETER:
                dist = data * 1e-3
            case GsiUnit.MILLIFEET:
                dist = data * 3.048e-4
            case GsiUnit.DECIMM:
                dist = data * 1e-4
            case GsiUnit.DECIMF:
                dist = data * 3.048e-5
            case GsiUnit.CENTIMM:
                dist = data * 1e-5
            case _:
                raise ValueError(f"Invalid distance unit: '{unit}'")

        return cls(
            dist,
            source,
            disttype
        )

    def serialize(
        self,
        gsi16: bool = False,
        precision: Literal[3, 4, 5] = 4
    ) -> str:
        unit = {
            3: GsiUnit.MILLIMETER,
            4: GsiUnit.DECIMM,
            5: GsiUnit.CENTIMM
        }[precision]

        return self.format(
            self._TYPE_TO_WI[self.type],
            f"{abs(self.value * 10**precision):.0f}",
            f"{self.source.value:d}{unit.value:d}",
            self.value < 0,
            gsi16
        )


class GsiCoordinate(GsiDistance):
    _GSI = compile(r"^(?:8[123456])\.\.\d{2}[\+-](?:[0-9]{8,16}) $")

    _WI_TO_TYPE = {
        81: "easting",
        82: "northing",
        83: "height",
        84: "stationeasting",
        85: "stationnorthing",
        86: "stationheight"
    }
    _TYPE_TO_WI = {v: k for k, v in _WI_TO_TYPE.items()}


class GsiEquipmentHeight(GsiDistance):
    _GSI = compile(r"^(?:8[78])\.\.\d{2}[\+-](?:[0-9]{8,16}) $")

    _WI_TO_TYPE = {
        87: "instrument",
        88: "target"
    }
    _TYPE_TO_WI = {v: k for k, v in _WI_TO_TYPE.items()}


class GsiDistanceDNA(GsiWord):
    _GSI = compile(r"^(?:32|83)\.\.[\d\.]\d[\+-](?:[0-9]{8,16}) $")

    _WI_TO_TYPE = {
        32: "staffdist"
    }
    _TYPE_TO_WI = {v: k for k, v in _WI_TO_TYPE.items()}

    def __init__(
        self,
        value: float,
        source: GsiInputModeDNA,
        type: str
    ):
        self.value = value
        if type not in self._TYPE_TO_WI:
            raise ValueError(f"Unknown distance type: '{type}'")

        self.type = type
        self.source = source

    @classmethod
    def parse(cls, value: str) -> Self:
        cls._check_format(value)

        disttype = cls._WI_TO_TYPE[int(value[:3].rstrip("."))]
        source = (
            GsiInputModeDNA(int(value[4]))
            if value[4] != "."
            else GsiInputModeDNA.MEASURED_CURVCORR_OFF
        )
        unit = GsiUnit(int(value[5]))
        data = int(value[6:-1])
        match unit:
            case GsiUnit.MILLIMETER:
                dist = data * 1e-3
            case GsiUnit.MILLIFEET:
                dist = data * 3.048e-4
            case GsiUnit.DECIMM:
                dist = data * 1e-4
            case GsiUnit.DECIMF:
                dist = data * 3.048e-5
            case GsiUnit.CENTIMM:
                dist = data * 1e-5
            case _:
                raise ValueError(f"Invalid distance unit: '{unit}'")

        return cls(
            dist,
            source,
            disttype
        )

    def serialize(
        self,
        gsi16: bool = False,
        precision: Literal[3, 4, 5] = 4
    ) -> str:
        unit = {
            3: GsiUnit.MILLIMETER,
            4: GsiUnit.DECIMM,
            5: GsiUnit.CENTIMM
        }[precision]

        return self.format(
            self._TYPE_TO_WI[self.type],
            f"{abs(self.value * 10**precision):.0f}",
            f"{self.source.value:d}{unit.value:d}",
            self.value < 0,
            gsi16
        )


class GsiStaffReading(GsiDistanceDNA):
    _GSI = compile(r"^(?:33[123456])\.\d{2}[\+-](?:[0-9]{8,16}) $")

    _WI_TO_TYPE = {
        330: "simple",
        331: "b1",
        332: "f1",
        333: "intermediate",
        334: "setout",
        335: "b2",
        336: "f2"
    }
    _TYPE_TO_WI = {v: k for k, v in _WI_TO_TYPE.items()}


_WI_TO_TYPE: dict[int, type[GsiWord]] = {
    11: GsiPointName,
    12: GsiSerialNumber,
    13: GsiInstrumentType,
    16: GsiStationName,
    17: GsiDate,
    19: GsiTime,
    21: GsiAngle,
    22: GsiAngle,
    31: GsiDistance,
    32: GsiDistance,
    33: GsiDistance,
    41: GsiCode,
    81: GsiCoordinate,
    82: GsiCoordinate,
    83: GsiCoordinate,
    84: GsiCoordinate,
    85: GsiCoordinate,
    86: GsiCoordinate,
    87: GsiEquipmentHeight,
    88: GsiEquipmentHeight
}
_WI_TO_TYPE_DNA: dict[int, type[GsiWord]] = {
    11: GsiPointName,
    12: GsiSerialNumber,
    13: GsiInstrumentType,
    32: GsiDistanceDNA,
    41: GsiCode,
    83: GsiDistanceDNA,
    330: GsiStaffReading,
    331: GsiStaffReading,
    332: GsiStaffReading,
    333: GsiStaffReading,
    334: GsiStaffReading,
    335: GsiStaffReading,
    336: GsiStaffReading
}


class GsiBlock:
    _TYPE_TO_WI = {
        "measurement": 11,
        "code": 41
    }
    _WI_TO_TYPE = {v: k for k, v in _TYPE_TO_WI.items()}

    def __init__(
        self,
        name: str,
        type: str,
        address: int | None = None
    ):
        if type not in self._TYPE_TO_WI:
            raise ValueError(f"Unknown GSI block type: '{type}'")

        self.name = name
        self.type = type
        self.address: int | None = address
        self.words: list[GsiWord] = []

    def __str__(self) -> str:
        return (
            f"GSI {self.type} block '{self.name}': "
            f"{len(self.words)} word(s)"
        )

    @classmethod
    def parse(cls, data: str, dna: bool = False) -> Self:
        wordsize = 16
        if data[0] == "*":
            wordsize = 24
            data = data[1:]

        if len(data) < wordsize:
            raise ValueError("Block must be at least one word long")

        if (len(data) % wordsize) != 0:
            raise ValueError("Block length does not match expected wordsizes")

        wi = int(data[:2])
        match wi:
            case 11:
                try:
                    header = GsiPointName.parse(data[:wordsize])
                except Exception:
                    raise ValueError(
                        "First word in measurement block must be point name"
                    )
                type = "measurement"
            case 41:
                try:
                    header = GsiCode.parse(data[:wordsize])
                except Exception:
                    raise ValueError(
                        "First word in code block must be code word"
                    )
                type = "code"
            case _:
                raise ValueError(
                    f"Unsupported block header word type: '{wi:d}'"
                )

        address: int | None = None
        if data[2:6].isdigit():
            address = int(data[2:6])

        mapping = _WI_TO_TYPE
        if dna:
            mapping = _WI_TO_TYPE_DNA

        output = cls(header.name, type, address)
        indices: set[int] = {11}
        for i in range(wordsize, len(data), wordsize):
            word = data[i:i+wordsize]

            wi = int(word[:3].rstrip("."))
            if wi in indices:
                raise ValueError(f"Duplicate word type in block: '{wi:d}'")

            indices.add(wi)

            wordtype = mapping.get(wi, GsiUnknown)
            try:
                output.words.append(wordtype.parse(word))
            except Exception:
                output.words.append(GsiUnknown.parse(word))

        return output

    def serialize(
        self,
        gsi16: bool = False
    ) -> str:
        match self.type:
            case "measurement":
                header = GsiPointName(self.name).serialize(gsi16)
            case "code":
                header = GsiCode(self.name).serialize(gsi16)
            case _:
                raise ValueError(f"Unknown block type: '{self.type}'")

        if self.address is not None:
            header = f"{header[:2]}{self.address % 10000:04d}{header[6:]}"

        output = header + "".join([w.serialize(gsi16) for w in self.words])

        if gsi16:
            output = "*" + output

        return output

    def drop_unknowns(self) -> None:
        keep = [w for w in self.words if not isinstance(w, GsiUnknown)]
        self.words.clear()
        for w in keep:
            self.words.append(w)
