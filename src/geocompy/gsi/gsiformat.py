from __future__ import annotations

from abc import ABC, abstractmethod
from re import compile
from datetime import datetime
from enum import Enum
from typing import Literal, Self, Any

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
    NONE = -1
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
    _GSI = compile(r"^[\d\.]{6}(?:\+|-)[a-zA-Z0-9\.\?]{8,16} $")
    # _WI = 1

    @classmethod
    @abstractmethod
    def parse(cls, value: str) -> GsiWord:
        raise NotImplementedError()

    @property
    @abstractmethod
    def wi(self) -> int: ...

    @abstractmethod
    def serialize(
        self,
        gsi16: bool = False,
        angleunit: GsiUnit = GsiUnit.NONE,
        distunit: GsiUnit = GsiUnit.NONE
    ) -> str:
        raise NotImplementedError()

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
    def _check_format(cls, value: str) -> None:
        if len(value) not in (16, 24):
            raise ValueError(f"'{value}' has unexpected length for a GSI word")

        if not cls._GSI.match(value):
            raise ValueError(
                f"'{value}' is not a valid serialized representation of "
                f"'{cls.__name__}'"
            )


class GsiUnknownWord(GsiWord):
    def __init__(
        self,
        wordindex: int,
        data: str = "",
        meta: str = "",
        negative: bool = False,
    ):
        self._wi = wordindex
        self.info = meta
        self.data = data
        self.negative = negative

    @property
    def wi(self) -> int:
        return self._wi

    @classmethod
    def parse(cls, value: str) -> GsiUnknownWord:
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

    def serialize(
        self,
        gsi16: bool = False,
        angleunit: GsiUnit = GsiUnit.NONE,
        distunit: GsiUnit = GsiUnit.NONE
    ) -> str:
        return self.format(
            self.wi,
            self.data,
            self.info,
            self.negative,
            gsi16
        )


class GsiValueWord(GsiWord):
    _GSI = compile(r"^\d{2}\.{4}\+(?:[a-zA-Z0-9]{8,16}) $")

    def __init__(self, value: Any):
        self.value: Any = value

    @classmethod
    def parse(cls, value: str) -> Self:
        cls._check_format(value)

        return cls(
            value[7:-1].lstrip("0")
        )

    def serialize(
        self,
        gsi16: bool = False,
        angleunit: GsiUnit = GsiUnit.NONE,
        distunit: GsiUnit = GsiUnit.NONE
    ) -> str:
        return self.format(
            self.wi,
            str(self.value),
            gsi16=gsi16
        )


class GsiPointnameWord(GsiValueWord):
    _GSI = compile(r"^11[\d\.]{4}\+(?:[a-zA-Z0-9]{8,16}) $")

    @property
    def wi(self) -> int:
        return 11

    def __init__(self, name: str):
        super().__init__(name)


class GsiSerialnumberWord(GsiValueWord):
    _GSI = compile(r"^12[\d\.]{4}\+(?:[0-9]{8,16}) $")

    @property
    def wi(self) -> int:
        return 12

    def __init__(self, serialnumber: str):
        super().__init__(serialnumber)


class GsiInstrumenttypeWord(GsiValueWord):
    _GSI = compile(r"^13[\d\.]{4}\+(?:[a-zA-Z0-9]{8,16}) $")

    @property
    def wi(self) -> int:
        return 13


class GsiStationnameWord(GsiPointnameWord):
    _GSI = compile(r"^16[\d\.]{4}\+(?:[a-zA-Z0-9]{8,16}) $")

    @property
    def wi(self) -> int:
        return 16


class GsiDateWord(GsiValueWord):
    _GSI = compile(r"^17[\d\.]{4}\+(?:[0-9]{8,16}) $")

    @property
    def wi(self) -> int:
        return 17

    def __init__(self, date: datetime):
        self.value: datetime
        super().__init__(date)

    @classmethod
    def parse(cls, value: str) -> Self:
        cls._check_format(value)

        return cls(
            datetime(
                int(value[-5:-1]),
                int(value[-7:-5]),
                int(value[-9:-7])
            )
        )

    def serialize(
        self,
        gsi16: bool = False,
        angleunit: GsiUnit = GsiUnit.NONE,
        distunit: GsiUnit = GsiUnit.NONE
    ) -> str:
        return self.format(
            self.wi,
            self.value.strftime("%d%m%Y"),
            gsi16=gsi16
        )


class GsiTimeWord(GsiValueWord):
    _GSI = compile(r"^19[\d\.]{4}\+(?:[0-9]{8,16}) $")

    @property
    def wi(self) -> int:
        return 19

    def __init__(self, time: datetime):
        self.value: datetime
        super().__init__(time)

    @classmethod
    def parse(cls, value: str) -> Self:
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

    def serialize(
        self,
        gsi16: bool = False,
        angleunit: GsiUnit = GsiUnit.NONE,
        distunit: GsiUnit = GsiUnit.NONE
    ) -> str:
        return self.format(
            self.wi,
            self.value.strftime("%m%d%H%M"),
            gsi16=gsi16
        )


class GsiAngleWord(GsiWord):
    _GSI = compile(r"^2[12]\.\d{3}\+(?:[0-9]{8,16}) $")

    @property
    def wi(self) -> int:
        if self.type == 'hz':
            return 21

        return 22

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
    def parse(cls, value: str) -> GsiAngleWord:
        cls._check_format(value)

        angletype: Literal['hz', 'v'] = "hz" if value[:2] == "21" else "v"
        index = GsiIndexMode(int(value[3]))
        source = GsiInputMode(int(value[4]))
        unit = GsiUnit(int(value[5]))
        match unit:
            case GsiUnit.GON:
                data = float(f"{value[7:10]}.{value[10:-1]}")
                angle = Angle(data * 360 / 400, 'deg')
            case GsiUnit.DEG:
                data = float(f"{value[7:10]}.{value[10:-1]}")
                angle = Angle(data, 'deg')
            case GsiUnit.DMS:
                angle = Angle.from_dms(
                    f"{value[7:10]}-{value[10:12]}-{value[12:14]}."
                    f"{value[14:-1]}"
                )
            case GsiUnit.MIL:
                data = float(f"{value[7:11]}.{value[11:-1]}")
                angle = Angle(data * 360 / 6400, 'deg')
            case _:
                raise ValueError(f"Invalid angle unit: '{unit}'")

        return cls(
            angle,
            index,
            source,
            angletype
        )

    def serialize(
        self,
        gsi16: bool = False,
        angleunit: GsiUnit = GsiUnit.DEG,
        distunit: GsiUnit = GsiUnit.NONE
    ) -> str:
        match angleunit:
            case GsiUnit.DEG | GsiUnit.GON:
                value = self.angle.normalized().asunit('deg')
                if angleunit is GsiUnit.GON:
                    value *= 400 / 360

                if gsi16:
                    data = f"{value:.13f}".replace(".", "")
                else:
                    data = f"{value:.5f}".replace(".", "")
            case GsiUnit.DMS:
                dms = self.angle.normalized().to_dms(9 if gsi16 else 1)
                data = dms.replace("-", "").replace(".", "")

            case GsiUnit.MIL:
                value = self.angle.normalized().asunit('deg') * 6400 / 360
                if gsi16:
                    data = f"{value:.12f}".replace(".", "")
                else:
                    data = f"{value:.4f}".replace(".", "")

            case _:
                raise ValueError(f"Invalid angle unit: '{angleunit}'")

        return self.format(
            21 if self.type == 'hz' else 22,
            data,
            f"{self.indexmode.value:d}{self.source.value:d}3",
            gsi16=gsi16
        )


class GsiDistanceWord(GsiWord):
    _GSI = compile(r"^(?:3[123])\.\.[\d\.]\d[\+-](?:[0-9]{8,16}) $")

    _WI_TO_TYPE = {
        31: "slope",
        32: "horizontal",
        33: "vertical"
    }
    _TYPE_TO_WI = {v: k for k, v in _WI_TO_TYPE.items()}

    @property
    def wi(self) -> int:
        return self._TYPE_TO_WI[self.type]

    def __init__(
        self,
        value: float,
        source: GsiInputMode | None,
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
            GsiInputMode(int(value[4]))
            if value[4] != "."
            else None
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
        angleunit: GsiUnit = GsiUnit.NONE,
        distunit: GsiUnit = GsiUnit.NONE
    ) -> str:
        match distunit:
            case GsiUnit.MILLIMETER:
                value = self.value * 1e3
            case GsiUnit.MILLIFEET:
                value = self.value / 3.048e-4
            case GsiUnit.DECIMM:
                value = self.value * 1e4
            case GsiUnit.DECIMF:
                value = self.value / 3.048e-5
            case GsiUnit.CENTIMM:
                value = self.value * 1e5
            case _:
                raise ValueError(f"Unknown distance unit: '{distunit}'")

        source = f"{self.source.value:d}" if self.source is not None else ""
        return self.format(
            self._TYPE_TO_WI[self.type],
            f"{abs(value):.0f}",
            f"{source}{distunit.value:d}",
            self.value < 0,
            gsi16
        )


class GsiCodeWord(GsiValueWord):
    _GSI = compile(r"^41[\d\.]{4}\+(?:[a-zA-Z0-9]{8,16}) $")

    @property
    def wi(self) -> int:
        return 41


class GsiInfo1Word(GsiCodeWord):
    _GSI = compile(r"^42[\d\.]{4}\+(?:[a-zA-Z0-9]{8,16}) $")

    @property
    def wi(self) -> int:
        return 42


class GsiInfo2Word(GsiCodeWord):
    _GSI = compile(r"^43[\d\.]{4}\+(?:[a-zA-Z0-9]{8,16}) $")

    @property
    def wi(self) -> int:
        return 43


class GsiInfo3Word(GsiCodeWord):
    _GSI = compile(r"^44[\d\.]{4}\+(?:[a-zA-Z0-9]{8,16}) $")

    @property
    def wi(self) -> int:
        return 44


class GsiInfo4Word(GsiCodeWord):
    _GSI = compile(r"^45[\d\.]{4}\+(?:[a-zA-Z0-9]{8,16}) $")

    @property
    def wi(self) -> int:
        return 45


class GsiInfo5Word(GsiCodeWord):
    _GSI = compile(r"^46[\d\.]{4}\+(?:[a-zA-Z0-9]{8,16}) $")

    @property
    def wi(self) -> int:
        return 46


class GsiInfo6Word(GsiCodeWord):
    _GSI = compile(r"^47[\d\.]{4}\+(?:[a-zA-Z0-9]{8,16}) $")

    @property
    def wi(self) -> int:
        return 47


class GsiInfo7Word(GsiCodeWord):
    _GSI = compile(r"^48[\d\.]{4}\+(?:[a-zA-Z0-9]{8,16}) $")

    @property
    def wi(self) -> int:
        return 48


class GsiInfo8Word(GsiCodeWord):
    _GSI = compile(r"^49[\d\.]{4}\+(?:[a-zA-Z0-9]{8,16}) $")

    @property
    def wi(self) -> int:
        return 49


class GsiRemark1Word(GsiValueWord):
    _GSI = compile(r"^71[\d\.]{4}\+(?:[a-zA-Z0-9]{8,16}) $")

    @property
    def wi(self) -> int:
        return 71


class GsiRemark2Word(GsiRemark1Word):
    _GSI = compile(r"^72[\d\.]{4}\+(?:[a-zA-Z0-9]{8,16}) $")

    @property
    def wi(self) -> int:
        return 72


class GsiRemark3Word(GsiRemark1Word):
    _GSI = compile(r"^73[\d\.]{4}\+(?:[a-zA-Z0-9]{8,16}) $")

    @property
    def wi(self) -> int:
        return 73


class GsiRemark4Word(GsiRemark1Word):
    _GSI = compile(r"^74[\d\.]{4}\+(?:[a-zA-Z0-9]{8,16}) $")

    @property
    def wi(self) -> int:
        return 74


class GsiRemark5Word(GsiRemark1Word):
    _GSI = compile(r"^75[\d\.]{4}\+(?:[a-zA-Z0-9]{8,16}) $")

    @property
    def wi(self) -> int:
        return 75


class GsiRemark6Word(GsiRemark1Word):
    _GSI = compile(r"^76[\d\.]{4}\+(?:[a-zA-Z0-9]{8,16}) $")

    @property
    def wi(self) -> int:
        return 76


class GsiRemark7Word(GsiRemark1Word):
    _GSI = compile(r"^77[\d\.]{4}\+(?:[a-zA-Z0-9]{8,16}) $")

    @property
    def wi(self) -> int:
        return 77


class GsiRemark8Word(GsiRemark1Word):
    _GSI = compile(r"^78[\d\.]{4}\+(?:[a-zA-Z0-9]{8,16}) $")

    @property
    def wi(self) -> int:
        return 78


class GsiRemark9Word(GsiRemark1Word):
    _GSI = compile(r"^79[\d\.]{4}\+(?:[a-zA-Z0-9]{8,16}) $")

    @property
    def wi(self) -> int:
        return 79


class GsiCoordinateWord(GsiDistanceWord):
    _GSI = compile(r"^(?:8[123456])\.\.[\d\.]\d[\+-](?:[0-9]{8,16}) $")

    _WI_TO_TYPE = {
        81: "easting",
        82: "northing",
        83: "height",
        84: "stationeasting",
        85: "stationnorthing",
        86: "stationheight"
    }
    _TYPE_TO_WI = {v: k for k, v in _WI_TO_TYPE.items()}


class GsiEquipmentHeightWord(GsiDistanceWord):
    _GSI = compile(r"^(?:8[78])\.\.[\d\.]\d[\+-](?:[0-9]{8,16}) $")

    _WI_TO_TYPE = {
        87: "instrument",
        88: "target"
    }
    _TYPE_TO_WI = {v: k for k, v in _WI_TO_TYPE.items()}


class GsiDistanceDNAWord(GsiWord):
    _GSI = compile(r"^(?:32|83)\.\.[\d\.]\d[\+-](?:[0-9]{8,16}) $")

    _WI_TO_TYPE = {
        32: "staffdist",
        83: "benchmarkheight"
    }
    _TYPE_TO_WI = {v: k for k, v in _WI_TO_TYPE.items()}

    @property
    def wi(self) -> int:
        return self._TYPE_TO_WI[self.type]

    def __init__(
        self,
        value: float,
        source: GsiInputModeDNA | None,
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
            else None
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
        angleunit: GsiUnit = GsiUnit.NONE,
        distunit: GsiUnit = GsiUnit.NONE
    ) -> str:
        match distunit:
            case GsiUnit.MILLIMETER:
                value = self.value * 1e3
            case GsiUnit.MILLIFEET:
                value = self.value / 3.048e-4
            case GsiUnit.DECIMM:
                value = self.value * 1e4
            case GsiUnit.DECIMF:
                value = self.value / 3.048e-5
            case GsiUnit.CENTIMM:
                value = self.value * 1e5
            case _:
                raise ValueError(f"Unknown distance unit: '{distunit}'")

        source = f"{self.source.value:d}" if self.source is not None else ""
        return self.format(
            self._TYPE_TO_WI[self.type],
            f"{abs(value):.0f}",
            f"{source}{distunit.value:d}",
            self.value < 0,
            gsi16
        )


class GsiStaffReadingWord(GsiDistanceDNAWord):
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
    11: GsiPointnameWord,
    12: GsiSerialnumberWord,
    13: GsiInstrumenttypeWord,
    16: GsiStationnameWord,
    17: GsiDateWord,
    19: GsiTimeWord,
    21: GsiAngleWord,
    22: GsiAngleWord,
    31: GsiDistanceWord,
    32: GsiDistanceWord,
    33: GsiDistanceWord,
    41: GsiCodeWord,
    81: GsiCoordinateWord,
    82: GsiCoordinateWord,
    83: GsiCoordinateWord,
    84: GsiCoordinateWord,
    85: GsiCoordinateWord,
    86: GsiCoordinateWord,
    87: GsiEquipmentHeightWord,
    88: GsiEquipmentHeightWord
}
_WI_TO_TYPE_DNA: dict[int, type[GsiWord]] = {
    11: GsiPointnameWord,
    12: GsiSerialnumberWord,
    13: GsiInstrumenttypeWord,
    32: GsiDistanceDNAWord,
    41: GsiCodeWord,
    83: GsiDistanceDNAWord,
    330: GsiStaffReadingWord,
    331: GsiStaffReadingWord,
    332: GsiStaffReadingWord,
    333: GsiStaffReadingWord,
    334: GsiStaffReadingWord,
    335: GsiStaffReadingWord,
    336: GsiStaffReadingWord
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

    def __repr__(self) -> str:
        return str(self)

    @classmethod
    def parse(cls, data: str, dna: bool = False) -> Self:
        wordsize = 16
        if data[0] == "*":
            wordsize = 24
            data = data[1:]

        # Sometimes the last space before the linebreak is missing
        if data[-1] != " ":
            data += " "

        if len(data) < wordsize:
            raise ValueError("Block must be at least one word long")

        if (len(data) % wordsize) != 0:
            raise ValueError(
                f"Block length does not match expected wordsizes: {len(data)}"
            )

        wi = int(data[:2])
        match wi:
            case 11:
                try:
                    header: GsiValueWord = GsiPointnameWord.parse(
                        data[:wordsize]
                    )
                except Exception:
                    raise ValueError(
                        "First word in measurement block must be point name"
                    )
                type = "measurement"
            case 41:
                try:
                    header = GsiCodeWord.parse(data[:wordsize])
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

        output = cls(header.value, type, address)
        indices: set[int] = {11}
        for i in range(wordsize, len(data), wordsize):
            word = data[i:i+wordsize]

            wi = int(word[:3].rstrip("."))
            if wi in indices:
                raise ValueError(f"Duplicate word type in block: '{wi:d}'")

            indices.add(wi)

            wordtype = mapping.get(wi, GsiUnknownWord)
            try:
                output.words.append(wordtype.parse(word))
            except Exception:
                output.words.append(GsiUnknownWord.parse(word))

        return output

    def serialize(
        self,
        gsi16: bool = False,
        angleunit: GsiUnit = GsiUnit.DEG,
        distunit: GsiUnit = GsiUnit.DECIMM
    ) -> str:
        match self.type:
            case "measurement":
                header = GsiPointnameWord(self.name).serialize(gsi16)
            case "code":
                header = GsiCodeWord(self.name).serialize(gsi16)
            case _:
                raise ValueError(f"Unknown block type: '{self.type}'")

        if self.address is not None:
            header = f"{header[:2]}{self.address % 10000:04d}{header[6:]}"

        output = header + "".join(
            [w.serialize(gsi16, angleunit, distunit) for w in self.words]
        )

        if gsi16:
            output = "*" + output

        return output

    def drop_unknowns(self) -> None:
        keep = [w for w in self.words if not isinstance(w, GsiUnknownWord)]
        self.words.clear()
        for w in keep:
            self.words.append(w)
