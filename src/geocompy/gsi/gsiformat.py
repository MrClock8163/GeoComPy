from __future__ import annotations

from abc import ABC, abstractmethod
from re import compile


class GsiWord(ABC):
    _GSI = compile(r"^[0-9\.]{6}(?:\+|-)[a-zA-Z0-9\.\?]{8,16} $")

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
        data: str = "",
        meta: int | None = None,
        negative: bool = False,
        gsi16: bool = False
    ) -> str:
        if wordindex >= 1000 or wordindex < 0:
            raise ValueError(f"GSI word index out of range ({wordindex})")

        if meta is not None and (meta >= 1000 or meta < 0):
            raise ValueError(f"GSI word meta data out of range ({meta})")

        wi = str(wordindex)
        info = str(meta) if meta is not None else ""
        filler = "." * (6 - len(wi) - len(info))

        header = f"{wi}{filler}{info}"
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
                f"'{type(cls).__name__}'"
            )


class GsiUnknown(GsiWord):
    def __init__(
        self,
        wordindex: int,
        data: str = "",
        meta: int | None = None,
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
            int(meta) if meta != "" else None,
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
    _GSI = compile(r"11[\d\.]{4}\+(?:0*[a-zA-Z0-9]+)")

    def __init__(self, name: str):
        self.name = name

    def serialize(self, gsi16: bool = False) -> str:
        return self.format(
            11,
            self.name,
            gsi16=gsi16
        )

    @classmethod
    def parse(cls, value: str) -> GsiPointName:
        cls._check_format(value)
        return cls(value[7:-1].lstrip("0"))
