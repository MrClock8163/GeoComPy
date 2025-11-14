"""
Description
===========

Module: ``geocompy.gsi.gsiformat``

The GSI format module provides data types and utility functions to read and
write abritrary Leica GSI8 and GSI16 files.

Container types are implemented for all supported GSI words types and block
types. The types can handle parsing, as well as serialization of themselves.

Angular value parsing and serialization unit conversion is done automatically.

Length values are stored in meter units internally. Conversion is handled
during parsing. Storage of other decimal values can be done with using
scaler "units" (no feet, no angle).
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from re import compile, Pattern
from datetime import datetime
from enum import Enum
from typing import (
    cast,
    Any,
    Self,
    TypeVar,
    TextIO,
)
from collections.abc import (
    Iterator,
    Iterable,
    Generator
)

from ..data import Angle


class GsiCorrection(Enum):
    """Index correction state in angular measurements."""
    OFF = 0
    ON1 = 1
    ON3 = 3


class GsiValueType(Enum):
    """Source of measurement-like value."""
    TYPE0 = 0
    """
    TPS: measurement transferred from instrument

    DNA: measured without curvature correction
    """
    TYPE1 = 1
    """
    TPS: manual input

    DNA: manual input without curvature correction
    """
    TYPE2 = 2
    """
    TPS: measured with horizontal angle correction

    DNA: measured with curvature correction
    """
    TYPE3 = 3
    """
    TPS: measured without horizontal angle correction
    """
    TYPE4 = 4
    """TPS: computed"""
    TYPE5 = 5
    """DNA: manual input with curvature correction"""


class GsiUnit(Enum):
    """Unit of measurement-like value."""
    MILLI = 0
    """0.001m or 0.001 scaler factor"""
    MILLIFEET = 1
    """0.001ft"""
    GON = 2
    """Gradian/Gon (400gon / 360deg)"""
    DEG = 3
    """Deciaml degrees"""
    DMS = 4
    """Sexagesimal degrees (DDD-MM-SS.S)"""
    MIL = 5
    """NATO milliradians (6400mils / 360deg)"""
    DECIMILLI = 6
    """0.0001m or 0.0001 scaler factor"""
    DECIMILLIFEET = 7
    """0.0001ft"""
    CENTIMILLI = 8
    """0.00001m or 0.00001 scaler factor"""


def _regex_measurement(wi: int | None = None) -> Pattern[str]:
    if wi is not None and (wi > 999 or wi < 0):
        raise ValueError("Invalid wordindex")

    if wi is None:
        idx = r"\d{2}[\d\.]"
    else:
        idx = str(wi).ljust(3, ".")

    return compile(rf"^{idx}[\d\.]{{2}}\d[\+\-][0-9]{{8,16}} $")


def _regex_note(wi: int | None = None) -> Pattern[str]:
    if wi is not None and (wi > 999 or wi < 0):
        raise ValueError("Invalid wordindex")

    if wi is None:
        idx = r"\d{2}[\d\.]"
    else:
        idx = str(wi).ljust(3, ".")

    return compile(rf"^{idx}[\d\.]{{3}}\+[\w\.\?\-\+]{{8,16}} $")


def _regex_integer(wi: int | None = None) -> Pattern[str]:
    if wi is not None and (wi > 999 or wi < 0):
        raise ValueError("Invalid wordindex")

    if wi is None:
        idx = r"\d{2}[\d\.]"
    else:
        idx = str(wi).ljust(3, ".")

    return compile(rf"^{idx}[\d\.]{{3}}[\+\-]\d{{8,16}} $")


def format_gsi_word(
    wordindex: int,
    data: str,
    indexcorr: GsiCorrection | None = None,
    inputtype: GsiValueType | None = None,
    unit: GsiUnit | None = None,
    negative: bool = False,
    gsi16: bool = False
) -> str:
    """
    Format data into a GSI8 or GSI16 word.

    Parameters
    ----------
    wordindex : int
        Word index of the word type.
    data : str
        Preformatted data block.
    indexcorr : GsiCorrection | None, optional
        Status of the autmatic vertical index correction, by default None
    inputtype : GsiValueType | None, optional
        Source/input method of the value, by default None
    unit : GsiUnit | None, optional
        Unit/scaler coefficient of the stored numerical value, by default None
    negative : bool, optional
        Negative sign, by default False
    gsi16 : bool, optional
        Construct GSI16 word, by default False

    Returns
    -------
    str
        Formatted GSI word

    Raises
    ------
    ValueError
        If wordindex is not in valid range [0;999].
    """
    if wordindex >= 1000 or wordindex < 0:
        raise ValueError(f"GSI word index out of range ({wordindex})")

    meta = (
        (str(indexcorr.value) if indexcorr is not None else ".")
        + (str(inputtype.value) if inputtype is not None else ".")
        + (str(unit.value) if unit is not None else ".")
    )
    wi = str(wordindex).ljust(3, ".")
    sign = "-" if negative else "+"
    datalength = 16 if gsi16 else 8
    data = data[-datalength:].zfill(datalength)

    return wi + meta + sign + data + " "


class GsiWord(ABC):
    """Interface for all GSI word types."""
    _GSI = compile(r"^[\d\.]{6}(?:\+|-)[a-zA-Z0-9\.\?]{8,16} $")

    @classmethod
    @abstractmethod
    def parse(cls, value: str) -> Self:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def WI(cls) -> int:
        """Class word index (might be different from final runtime value)."""
        raise NotImplementedError()

    @property
    def wi(self) -> int:
        """Word index."""
        return self.WI()

    @abstractmethod
    def serialize(
        self,
        *,
        gsi16: bool = False,
        angleunit: GsiUnit | None = None,
        distunit: GsiUnit | None = None
    ) -> str:
        raise NotImplementedError()

    def __str__(self) -> str:
        return self.serialize(gsi16=True)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, GsiWord):
            return False

        return self.wi == other.wi

    @classmethod
    def _check_format(cls, value: str) -> None:
        if len(value) not in (16, 24):
            raise ValueError(f"'{value}' has unexpected length for a GSI word")

        if not cls._GSI.match(value):
            raise ValueError(
                f"'{value}' is not a valid serialized representation of "
                f"'{cls.__name__}'"
            )


_T = TypeVar("_T", bound=GsiWord)


class GsiUnknownWord(GsiWord):
    """Generic word type to hold unrecognized data for later processing."""

    def __init__(
        self,
        wordindex: int,
        data: str = "",
        indexcorr: GsiCorrection | None = None,
        inputtype: GsiValueType | None = None,
        unit: GsiUnit | None = None,
        negative: bool = False,
    ):
        """
        Parameters
        ----------
        wordindex : int
            GSI word index.
        data : str, optional
            Data block, by default ""
        indexcorr : GsiCorrection | None, optional
            Status of the autmatic vertical index correction, by default None
        inputtype : GsiValueType | None, optional
            Source/input method of the value, by default None
        unit : GsiUnit | None, optional
            Unit/scaler coefficient of the stored numerical value,
            by default None
        negative : bool, optional
            Negative sign, by default False
        """
        self._wi = wordindex
        self.indexcorr = indexcorr
        self.inputtype = inputtype
        self.unit = unit
        self.data = data
        self.negative = negative

    @classmethod
    def WI(cls) -> int:
        """Always returns 0 to indicate the unknown status of the data."""
        return 0

    @property
    def wi(self) -> int:
        return self._wi

    @classmethod
    def parse(cls, value: str) -> GsiUnknownWord:
        """
        Parses unknown word from a serialized value.

        Parameters
        ----------
        value : str
            Serialized GSI word.

        Returns
        -------
        GsiUnknownWord
            Retains all information its raw form to allow further manual
            processing and error correction.
        """
        cls._check_format(value)
        wi = int(value[:3].rstrip("."))
        data = value[7:-1]
        try:
            indexcorr = GsiCorrection(int(value[3]))
        except Exception:
            indexcorr = None
        try:
            inputtype = GsiValueType(int(value[4]))
        except Exception:
            inputtype = None
        try:
            unit = GsiUnit(int(value[5]))
        except Exception:
            unit = None

        negative = value[6] == "-"

        return cls(
            wi,
            data,
            indexcorr,
            inputtype,
            unit,
            negative
        )

    def serialize(
        self,
        *,
        gsi16: bool = False,
        angleunit: GsiUnit | None = None,
        distunit: GsiUnit | None = None
    ) -> str:
        """
        Serialize data to GSI word text.

        Parameters
        ----------
        gsi16 : bool, optional
            Create GSI16 word instead of GSI8, by default False
        angleunit : GsiUnit | None, optional
            Unused, by default None
        distunit : GsiUnit | None, optional
            Unused, by None

        Returns
        -------
        str
        """
        return format_gsi_word(
            self._wi,
            self.data,
            self.indexcorr,
            self.inputtype,
            self.unit,
            self.negative,
            gsi16
        )


class GsiValueWord(GsiWord):
    """Base type for GSI words with simple values and no meta flags."""
    _GSI = _regex_note()

    def __init__(self, value: Any):
        """
        Parameters
        ----------
        value : Any
            Arbitrary value to represent.
        """
        self.value: Any = value

    @classmethod
    def parse(cls, value: str) -> Self:
        """
        Parses a word from a serialized value.

        Parameters
        ----------
        value : str
            Serialized GSI word.

        Returns
        -------
        Self
        """
        cls._check_format(value)

        return cls(
            value[7:-1].lstrip("0")
        )

    def serialize(
        self,
        *,
        gsi16: bool = False,
        angleunit: GsiUnit | None = None,
        distunit: GsiUnit | None = None
    ) -> str:
        """
        Serialize data to GSI word text.

        Parameters
        ----------
        gsi16 : bool, optional
            Create GSI16 word instead of GSI8, by default False
        angleunit : GsiUnit | None, optional
            Unused, by default None
        distunit : GsiUnit | None, optional
            Unused, by default None

        Returns
        -------
        str
        """
        return format_gsi_word(
            self.wi,
            str(self.value),
            gsi16=gsi16
        )


class GsiIntegerValueWord(GsiWord):
    """
    Base type for GSI words with simple interger values and no meta flags.
    """
    _GSI = _regex_integer()

    def __init__(self, value: int):
        """
        Parameters
        ----------
        value : int
            Value to represent.
        """
        self.value: int = value

    @classmethod
    def parse(cls, value: str) -> Self:
        """
        Parses a word from a serialized value.

        Parameters
        ----------
        value : str
            Serialized GSI word.

        Returns
        -------
        Self
        """
        cls._check_format(value)

        return cls(
            int(value[6:-1])
        )

    def serialize(
        self,
        *,
        gsi16: bool = False,
        angleunit: GsiUnit | None = None,
        distunit: GsiUnit | None = None
    ) -> str:
        """
        Serialize data to GSI word text.

        Parameters
        ----------
        gsi16 : bool, optional
            Create GSI16 word instead of GSI8, by default False
        angleunit : GsiUnit | None, optional
            Unused, by default None
        distunit : GsiUnit | None, optional
            Unused, by default None

        Returns
        -------
        str
        """
        return format_gsi_word(
            self.wi,
            str(self.value),
            negative=self.value < 0,
            gsi16=gsi16
        )


class GsiPointNameWord(GsiValueWord):
    """``WI11`` Point name (first word in measurement block)."""
    _GSI = _regex_note(11)

    @classmethod
    def WI(cls) -> int:
        return 11

    def __init__(self, name: str):
        """
        Parameters
        ----------
        name : str
            Point name.
        """
        self.value: str
        super().__init__(name)


class GsiSerialnumberWord(GsiValueWord):
    """``WI12`` Instrument serial number."""
    _GSI = compile(r"^12[\d\.]{4}\+[0-9]{8,16} $")

    @classmethod
    def WI(cls) -> int:
        return 12

    def __init__(self, serialnumber: int):
        """
        Parameters
        ----------
        serialnumber : int
            Serial number.
        """
        self.value: int
        super().__init__(serialnumber)

    @classmethod
    def parse(cls, value: str) -> Self:
        """
        Parses serial number from a serialized GSI word.

        Parameters
        ----------
        value : str
            Serialized GSI word.

        Returns
        -------
        Self
        """
        cls._check_format(value)

        return cls(
            int(value[7:-1].lstrip("0"))
        )

    def serialize(
        self,
        *,
        gsi16: bool = False,
        angleunit: GsiUnit | None = None,
        distunit: GsiUnit | None = None
    ) -> str:
        """
        Serialize data to GSI word text.

        Parameters
        ----------
        gsi16 : bool, optional
            Create GSI16 word instead of GSI8, by default False
        angleunit : GsiUnit | None, optional
            Unused, by default None
        distunit : GsiUnit | None, optional
            Unused, by default None

        Returns
        -------
        str
        """
        return format_gsi_word(
            self.wi,
            str(self.value),
            gsi16=gsi16
        )


class GsiInstrumentTypeWord(GsiValueWord):
    """``WI13`` Instrument type name."""
    _GSI = _regex_note(13)

    @classmethod
    def WI(cls) -> int:
        return 13

    def __init__(self, name: str):
        """
        Parameters
        ----------
        name : str
            Instrument type.
        """
        self.value: str
        super().__init__(name)


class GsiStationNameWord(GsiPointNameWord):
    """``WI16`` Station point name."""
    _GSI = _regex_note(16)

    @classmethod
    def WI(cls) -> int:
        return 16


class GsiDateWord(GsiValueWord):
    """``WI17`` Full date."""
    _GSI = compile(r"^17[\d\.]{4}\+[0-9]{8,16} $")

    @classmethod
    def WI(cls) -> int:
        return 17

    def __init__(self, date: datetime):
        """
        Parameters
        ----------
        date : datetime
            Full year-month-day date.
        """
        self.value: datetime
        super().__init__(date)

    @classmethod
    def parse(cls, value: str) -> Self:
        """
        Parses a full date from a serialized GSI word.

        Parameters
        ----------
        value : str
            Serialized GSI word.

        Returns
        -------
        Self
        """
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
        *,
        gsi16: bool = False,
        angleunit: GsiUnit | None = None,
        distunit: GsiUnit | None = None
    ) -> str:
        """
        Serialize data to GSI word text.

        Parameters
        ----------
        gsi16 : bool, optional
            Create GSI16 word instead of GSI8, by default False
        angleunit : GsiUnit | None, optional
            Unused, by default None
        distunit : GsiUnit | None, optional
            Unused, by default None

        Returns
        -------
        str
        """
        return format_gsi_word(
            self.wi,
            self.value.strftime("%d%m%Y"),
            gsi16=gsi16
        )


class GsiTimeWord(GsiValueWord):
    """``WI19`` Partial date and time (month-day-hours-minutes)."""
    _GSI = compile(r"^19[\d\.]{4}\+[0-9]{8,16} $")

    @classmethod
    def WI(cls) -> int:
        return 19

    def __init__(self, time: datetime):
        """
        Parameters
        ----------
        time : datetime
            Date and time, where the year and seconds are ignored.
        """
        self.value: datetime
        super().__init__(time)

    @classmethod
    def parse(cls, value: str) -> Self:
        """
        Parses a partial date-time from a serialized GSI word
        (year is set to 1).

        Parameters
        ----------
        value : str
            Serialized GSI word.

        Returns
        -------
        Self
        """
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
        *,
        gsi16: bool = False,
        angleunit: GsiUnit | None = None,
        distunit: GsiUnit | None = None
    ) -> str:
        """
        Serialize data to GSI word text.

        Parameters
        ----------
        gsi16 : bool, optional
            Create GSI16 word instead of GSI8, by default False
        angleunit : GsiUnit | None, optional
            Unused, by default None
        distunit : GsiUnit | None, optional
            Unused, by default None

        Returns
        -------
        str
        """
        return format_gsi_word(
            self.wi,
            self.value.strftime("%m%d%H%M"),
            gsi16=gsi16
        )


class GsiAngleWord(GsiValueWord):
    """Base type for angular measurement words."""
    _GSI = _regex_measurement()

    def __init__(
        self,
        angle: Angle,
        indexcorr: GsiCorrection | None = None,
        inputtype: GsiValueType | None = None
    ):
        """
        Parameters
        ----------
        angle : Angle
            Measurement value.
        indexcorr : GsiCorrection | None, optional
            State of vertical index correction, by default None
        inputtype : GsiValueType | None, optional
            Value input source, by default None
        """
        self.value: Angle
        super().__init__(angle)
        self.indexcorr: GsiCorrection | None = indexcorr
        self.inputtype: GsiValueType | None = inputtype

    @classmethod
    def parse(cls, value: str) -> Self:
        """
        Parses an angular measurement value from a serialized GSI word.

        Parameters
        ----------
        value : str
            Serialized GSI word.

        Returns
        -------
        Self

        Raises
        ------
        ValueError
            If incorrect unit was found in value.
        """
        cls._check_format(value)

        index = (
            GsiCorrection(int(value[3]))
            if value[3] != "."
            else None
        )
        source = (
            GsiValueType(int(value[4]))
            if value[4] != "."
            else None
        )
        unit = GsiUnit(int(value[5]))
        match unit:
            case GsiUnit.GON | GsiUnit.DEG:
                data = float(f"{value[7:-6]}.{value[-6:-1]}")
                if unit is GsiUnit.GON:
                    data *= 360 / 400

                angle = Angle(data, 'deg')
            case GsiUnit.DMS:
                angle = Angle.from_dms(
                    f"{value[-9:-6]}-{value[-6:-4]}-{value[-4:-2]}."
                    f"{value[-2]}"
                )
            case GsiUnit.MIL:
                data = float(f"{value[7:-5]}.{value[-5:-1]}")
                angle = Angle(data * 360 / 6400, 'deg')
            case _:
                raise ValueError(f"Invalid angle unit: '{unit}'")

        return cls(
            angle,
            index,
            source
        )

    def serialize(
        self,
        *,
        gsi16: bool = False,
        angleunit: GsiUnit | None = GsiUnit.DEG,
        distunit: GsiUnit | None = None
    ) -> str:
        """
        Serialize data to GSI word text.

        Parameters
        ----------
        gsi16 : bool, optional
            Create GSI16 word instead of GSI8, by default False
        angleunit : GsiUnit | None, optional
            Angle unit to serialize as, by default GsiUnit.DEG
        distunit : GsiUnit | None, optional
            Unused, by default None

        Returns
        -------
        str

        Raises
        ------
        ValueError
            If invalid angular unit was given.
        """
        match angleunit:
            case GsiUnit.DEG | GsiUnit.GON:
                value = self.value.normalized().asunit('deg')
                if angleunit is GsiUnit.GON:
                    value *= 400 / 360

                data = f"{value:.5f}".replace(".", "")
            case GsiUnit.DMS:
                dms = self.value.normalized().to_dms(1)
                data = dms.replace("-", "").replace(".", "")
            case GsiUnit.MIL:
                value = self.value.normalized().asunit('deg') * 6400 / 360
                data = f"{value:.4f}".replace(".", "")

            case _:
                raise ValueError(f"Invalid angle unit: '{angleunit}'")

        return format_gsi_word(
            self.wi,
            data,
            self.indexcorr,
            self.inputtype,
            angleunit,
            gsi16=gsi16
        )


class GsiHorizontalAngleWord(GsiAngleWord):
    """``WI21`` Horizontal angle."""
    _GSI = _regex_measurement(21)

    @classmethod
    def WI(cls) -> int:
        return 21


class GsiVerticalAngleWord(GsiAngleWord):
    """``WI22`` Vertical angle."""
    _GSI = _regex_measurement(22)

    @classmethod
    def WI(cls) -> int:
        return 22


class GsiDistanceWord(GsiValueWord):
    """Base type for distance measurement and general scaled value words."""
    _GSI = _regex_measurement()

    def __init__(
        self,
        value: float,
        inputtype: GsiValueType | None = None
    ):
        """
        Parameters
        ----------
        value : float
            Measurement value (in meters distance value)
        inputtype : GsiValueType | None, optional
            Source of measurement-like value, by default None
        """
        self.value: float
        super().__init__(value)
        self.inputtype = inputtype

    @classmethod
    def parse(cls, value: str) -> Self:
        """
        Parses a distance measurement or measurement-like scaled value from a
        serialized GSI word.

        Parameters
        ----------
        value : str
            Serialized GSI word.

        Returns
        -------
        Self

        Raises
        ------
        ValueError
            If incorrect unit was found in value.
        """

        cls._check_format(value)

        source = (
            GsiValueType(int(value[4]))
            if value[4] != "."
            else None
        )
        unit = GsiUnit(int(value[5]))
        data = int(value[6:-1])
        match unit:
            case GsiUnit.MILLI:
                dist = data * 1e-3
            case GsiUnit.MILLIFEET:
                dist = data * 3.048e-4
            case GsiUnit.DECIMILLI:
                dist = data * 1e-4
            case GsiUnit.DECIMILLIFEET:
                dist = data * 3.048e-5
            case GsiUnit.CENTIMILLI:
                dist = data * 1e-5
            case _:
                raise ValueError(f"Invalid distance unit: '{unit}'")

        return cls(
            dist,
            source
        )

    def serialize(
        self,
        *,
        gsi16: bool = False,
        angleunit: GsiUnit | None = None,
        distunit: GsiUnit | None = GsiUnit.CENTIMILLI
    ) -> str:
        """
        Serialize data to GSI word text.

        Parameters
        ----------
        gsi16 : bool, optional
            Create GSI16 word instead of GSI8, by default False
        angleunit : GsiUnit | None, optional
            Unused, by default None
        distunit : GsiUnit | None, optional
            Distance unit (or scaler unit for generic values),
            by default None

        Returns
        -------
        str

        Raises
        ------
        ValueError
            If invalid distance/scaler unit was given.
        """
        match distunit:
            case GsiUnit.MILLI:
                value = self.value * 1e3
            case GsiUnit.MILLIFEET:
                value = self.value / 3.048e-4
            case GsiUnit.DECIMILLI:
                value = self.value * 1e4
            case GsiUnit.DECIMILLIFEET:
                value = self.value / 3.048e-5
            case GsiUnit.CENTIMILLI:
                value = self.value * 1e5
            case _:
                raise ValueError(f"Unknown distance unit: '{distunit}'")

        return format_gsi_word(
            self.wi,
            f"{abs(value):.0f}",
            None,
            self.inputtype,
            distunit,
            self.value < 0,
            gsi16
        )


class GsiSlopeDistanceWord(GsiDistanceWord):
    """``WI31`` Slope distance."""
    _GSI = _regex_measurement(31)

    @classmethod
    def WI(cls) -> int:
        return 31


class GsiHorizontalDistanceWord(GsiDistanceWord):
    """``WI32`` Horizontal distance."""
    _GSI = _regex_measurement(32)

    @classmethod
    def WI(cls) -> int:
        return 32


class GsiVerticalDistanceWord(GsiDistanceWord):
    """``WI33`` Vertical distance (height difference)."""
    _GSI = _regex_measurement(33)

    @classmethod
    def WI(cls) -> int:
        return 33


class GsiCodeWord(GsiValueWord):
    """``WI41`` Operation code (first word of code blocks)."""
    _GSI = _regex_note(41)
    _SPECIAL = compile(r"^41[\d\.]{4}\+\?\.+\d+ $")

    @classmethod
    def WI(cls) -> int:
        return 41

    def __init__(self, value: str, special: bool = False):
        """
        Parameters
        ----------
        value : tuple[str, bool]
            Code value and whether it is a special program code
            (applicable to digital levels).
        special : bool
            Code is special code (used in DNA output).
        """
        self.value: tuple[str, bool]
        super().__init__((value, special))

    @classmethod
    def parse(cls, value: str) -> Self:
        """
        Parses a word from a serialized value.

        Parameters
        ----------
        value : str
            Serialized GSI word.

        Returns
        -------
        Self
        """
        cls._check_format(value)
        if cls._SPECIAL.match(value):
            special = True
            value = value[8:-1].lstrip(".")
        else:
            special = False
            value = value[7:-1].lstrip("0")

        return cls(
            value,
            special
        )

    def serialize(
        self,
        *,
        gsi16: bool = False,
        angleunit: GsiUnit | None = None,
        distunit: GsiUnit | None = None
    ) -> str:
        """
        Serialize data to GSI word text.

        Parameters
        ----------
        gsi16 : bool, optional
            Create GSI16 word instead of GSI8, by default False
        angleunit : GsiUnit | None, optional
            Unused, by default None
        distunit : GsiUnit | None, optional
            Unused, by default None

        Returns
        -------
        str
        """
        data, special = self.value
        if special:
            data = "?" + data.rjust(15 if gsi16 else 7, ".")

        return format_gsi_word(
            self.wi,
            data,
            gsi16=gsi16
        )


class GsiInfo1Word(GsiValueWord):
    """``WI42`` Information 1."""
    _GSI = _regex_note(42)

    @classmethod
    def WI(cls) -> int:
        return 42

    def __init__(self, value: str):
        """
        Parameters
        ----------
        value : str
            Code value.
        """
        self.value: str
        super().__init__(value)


class GsiInfo2Word(GsiInfo1Word):
    """``WI43`` Information 2."""
    _GSI = _regex_note(43)

    @classmethod
    def WI(cls) -> int:
        return 43


class GsiInfo3Word(GsiInfo1Word):
    """``WI44`` Information 3."""
    _GSI = _regex_note(44)

    @classmethod
    def WI(cls) -> int:
        return 44


class GsiInfo4Word(GsiInfo1Word):
    """``WI45`` Information 4."""
    _GSI = _regex_note(45)

    @classmethod
    def WI(cls) -> int:
        return 45


class GsiInfo5Word(GsiInfo1Word):
    """``WI46`` Information 5."""
    _GSI = _regex_note(46)

    @classmethod
    def WI(cls) -> int:
        return 46


class GsiInfo6Word(GsiInfo1Word):
    """``WI47`` Information 6."""
    _GSI = _regex_note(47)

    @classmethod
    def WI(cls) -> int:
        return 47


class GsiInfo7Word(GsiInfo1Word):
    """``WI48`` Information 7."""
    _GSI = _regex_note(48)

    @classmethod
    def WI(cls) -> int:
        return 48


class GsiInfo8Word(GsiInfo1Word):
    """``WI49`` Information 8."""
    _GSI = _regex_note(49)

    @classmethod
    def WI(cls) -> int:
        return 49


class GsiPPMPrismConstantWord(GsiValueWord):
    """``WI51`` PPM correction and prism constant."""
    _GSI = compile(r"^51[\d\.]{3}$")

    @classmethod
    def WI(cls) -> int:
        return 51

    def __init__(self, ppm: int, constant: int):
        """
        Parameters
        ----------
        ppm : int
            Corretion factor.
        constant : int
            Prism constant in millimeters.
        """
        self.value: tuple[int, int]
        super().__init__((ppm, constant))

    @classmethod
    def parse(
        cls,
        value: str
    ) -> Self:
        """
        Parses PPM factor and prism constant from a serialized GSI word.

        Parameters
        ----------
        value : str
            Serialized GSI word.

        Returns
        -------
        Self
        """
        ppm = int(value[6:-5])
        constant = int(value[-5:-1])

        return cls(
            ppm,
            constant
        )

    def serialize(
        self,
        *,
        gsi16: bool = False,
        angleunit: GsiUnit | None = None,
        distunit: GsiUnit | None = None
    ) -> str:
        """
        Serialize data to GSI word text.

        Parameters
        ----------
        gsi16 : bool, optional
            Create GSI16 word instead of GSI8, by default False
        angleunit : GsiUnit | None, optional
            Unused, by default None
        distunit : GsiUnit | None, optional
            Unused, by default None

        Returns
        -------
        str

        Raises
        ------
        ValueError
            If values are out of their valid range, [-9999;9999] and [-999;999]
            respectively.
        """
        ppm, constant = self.value
        if (ppm > 9999 or ppm < -9999) or (constant > 999 or constant < -999):
            raise ValueError(
                "Cannot serialize GSI word because ppm or constant are out "
                f"of range ({ppm:d}, {constant:d})"
            )

        constant_str = (
            ("+" if constant >= 0 else "-")
            + str(abs(constant)).zfill(3)
        )
        return format_gsi_word(
            self.wi,
            f"{abs(ppm):d}{constant_str}",
            negative=ppm < 0,
            gsi16=gsi16
        )


class GsiPrismConstantWord(GsiDistanceWord):
    """``WI58`` Prism constant."""
    _GSI = _regex_measurement(58)

    @classmethod
    def WI(cls) -> int:
        return 58


class GsiPPMWord(GsiDistanceWord):
    """``WI59`` PPM correction factor."""
    _GSI = _regex_measurement(59)

    @classmethod
    def WI(cls) -> int:
        return 59


class GsiRemark1Word(GsiInfo1Word):
    """``WI71`` Note/Attribute 1."""
    _GSI = _regex_note(71)

    @classmethod
    def WI(cls) -> int:
        return 71


class GsiRemark2Word(GsiRemark1Word):
    """``WI72`` Note/Attribute 2."""
    _GSI = _regex_note(72)

    @classmethod
    def WI(cls) -> int:
        return 72


class GsiRemark3Word(GsiRemark1Word):
    """``WI73`` Note/Attribute 3."""
    _GSI = _regex_note(73)

    @classmethod
    def WI(cls) -> int:
        return 73


class GsiRemark4Word(GsiRemark1Word):
    """``WI74`` Note/Attribute 4."""
    _GSI = _regex_note(74)

    @classmethod
    def WI(cls) -> int:
        return 74


class GsiRemark5Word(GsiRemark1Word):
    """``WI75`` Note/Attribute 5."""
    _GSI = _regex_note(75)

    @classmethod
    def WI(cls) -> int:
        return 75


class GsiRemark6Word(GsiRemark1Word):
    """``WI76`` Note/Attribute 6."""
    _GSI = _regex_note(76)

    @classmethod
    def WI(cls) -> int:
        return 76


class GsiRemark7Word(GsiRemark1Word):
    """``WI77`` Note/Attribute 7."""
    _GSI = _regex_note(77)

    @classmethod
    def WI(cls) -> int:
        return 77


class GsiRemark8Word(GsiRemark1Word):
    """``WI78`` Note/Attribute 8."""
    _GSI = _regex_note(78)

    @classmethod
    def WI(cls) -> int:
        return 78


class GsiRemark9Word(GsiRemark1Word):
    """``WI79`` Note/Attribute 9."""
    _GSI = _regex_note(79)

    @classmethod
    def WI(cls) -> int:
        return 79


class GsiEastingWord(GsiDistanceWord):
    """``WI81`` Coordinate easting component."""
    _GSI = _regex_measurement(81)

    @classmethod
    def WI(cls) -> int:
        return 81


class GsiNorthingWord(GsiDistanceWord):
    """``WI82`` Coordinate northing component."""
    _GSI = _regex_measurement(82)

    @classmethod
    def WI(cls) -> int:
        return 82


class GsiHeightWord(GsiDistanceWord):
    """``WI83`` Coordinate height component."""
    _GSI = _regex_measurement(83)

    @classmethod
    def WI(cls) -> int:
        return 83


class GsiStationEastingWord(GsiDistanceWord):
    """``WI84`` Station coordinate easting component."""
    _GSI = _regex_measurement(84)

    @classmethod
    def WI(cls) -> int:
        return 84


class GsiStationNorthingWord(GsiDistanceWord):
    """``WI85`` Station coordinate northing component."""
    _GSI = _regex_measurement(85)

    @classmethod
    def WI(cls) -> int:
        return 85


class GsiStationHeightWord(GsiDistanceWord):
    """``WI86`` Station coordinate height component."""
    _GSI = _regex_measurement(86)

    @classmethod
    def WI(cls) -> int:
        return 86


class GsiTargetHeightWord(GsiDistanceWord):
    """``WI87`` Reflector/Target height."""
    _GSI = _regex_measurement(87)

    @classmethod
    def WI(cls) -> int:
        return 87


class GsiInstrumentHeightWord(GsiDistanceWord):
    """``WI88`` Instrument height."""
    _GSI = _regex_measurement(88)

    @classmethod
    def WI(cls) -> int:
        return 88


class GsiTemperatureWord(GsiDistanceWord):
    """``WI95`` Temperature."""
    _GSI = _regex_measurement(95)

    @classmethod
    def WI(cls) -> int:
        return 95


class GsiPressureWord(GsiDistanceWord):
    """``WI531`` Atmospheric pressure."""
    _GSI = _regex_measurement(531)

    @classmethod
    def WI(cls) -> int:
        return 531


class GsiRefractionCoefWord(GsiDistanceWord):
    """``WI538`` Refraction coefficient."""
    _GSI = _regex_measurement(538)

    @classmethod
    def WI(cls) -> int:
        return 538


class GsiNewTimeWord(GsiValueWord):
    """``WI560`` Full time (hours-minutes-seconds)."""
    _GSI = compile(r"^560\.{2}6\+[0-9]{8,16} $")

    @classmethod
    def WI(cls) -> int:
        return 560

    def __init__(self, time: datetime):
        """
        Parameters
        ----------
        time : datetime
            Full time.
        """
        self.value: datetime
        super().__init__(time)

    @classmethod
    def parse(cls, value: str) -> Self:
        """
        Parses a full time from a serialized GSI word
        (year, month and day are set to 1).

        Parameters
        ----------
        value : str
            Serialized GSI word.

        Returns
        -------
        Self
        """
        cls._check_format(value)

        return cls(
            datetime(
                1,
                1,
                1,
                int(value[-7:-5]),
                int(value[-5:-3]),
                int(value[-3:-1])
            )
        )

    def serialize(
        self,
        *,
        gsi16: bool = False,
        angleunit: GsiUnit | None = None,
        distunit: GsiUnit | None = None
    ) -> str:
        return format_gsi_word(
            self.wi,
            self.value.strftime("%H%M%S"),
            unit=GsiUnit.DECIMILLI,
            gsi16=gsi16
        )


class GsiNewDateWord(GsiValueWord):
    """``WI561`` Partial date (month-day)."""
    _GSI = compile(r"^561\.{2}6\+[0-9]{8,16} $")

    @classmethod
    def WI(cls) -> int:
        return 561

    def __init__(self, time: datetime):
        """
        Parameters
        ----------
        time : datetime
            Partial date (month-day)
        """
        self.value: datetime
        super().__init__(time)

    @classmethod
    def parse(cls, value: str) -> Self:
        """
        Parses a partial date from a serialized GSI word
        (year is set to 1).

        Parameters
        ----------
        value : str
            Serialized GSI word.

        Returns
        -------
        Self
        """
        cls._check_format(value)

        return cls(
            datetime(
                1,
                int(value[-7:-5]),
                int(value[-5:-3])
            )
        )

    def serialize(
        self,
        *,
        gsi16: bool = False,
        angleunit: GsiUnit | None = None,
        distunit: GsiUnit | None = None
    ) -> str:
        return format_gsi_word(
            self.wi,
            self.value.strftime("%m%d00"),
            unit=GsiUnit.DECIMILLI,
            gsi16=gsi16
        )


class GsiNewYearWord(GsiValueWord):
    """``WI562`` Year."""
    _GSI = compile(r"^562\.{3}\+[0-9]{8,16} $")

    @classmethod
    def WI(cls) -> int:
        return 562

    def __init__(self, year: datetime):
        """
        Parameters
        ----------
        year : datetime
            Year.
        """
        self.value: datetime
        super().__init__(year)

    @classmethod
    def parse(cls, value: str) -> Self:
        """
        Parses a year from a serialized GSI word
        (month and day are set to 1).

        Parameters
        ----------
        value : str
            Serialized GSI word.

        Returns
        -------
        Self
        """
        cls._check_format(value)

        return cls(
            datetime(
                int(value[-5:-1]),
                1,
                1
            )
        )

    def serialize(
        self,
        *,
        gsi16: bool = False,
        angleunit: GsiUnit | None = None,
        distunit: GsiUnit | None = None
    ) -> str:
        return format_gsi_word(
            self.wi,
            self.value.strftime("%Y"),
            gsi16=gsi16
        )


class GsiStaffDistanceWord(GsiDistanceWord):
    """``WI32`` Levelling staff distance."""
    _GSI = _regex_measurement(32)

    @classmethod
    def WI(cls) -> int:
        return 32


class GsiBenchmarkHeightWord(GsiDistanceWord):
    """``WI83`` Benchmark or running ground height."""
    _GSI = _regex_measurement(83)

    @classmethod
    def WI(cls) -> int:
        return 83


class GsiSimpleStaffReadingWord(GsiDistanceWord):
    """``WI330`` Staff reading in measure-only mode."""
    _GSI = _regex_measurement(330)

    @classmethod
    def WI(cls) -> int:
        return 330


class GsiB1StaffReadingWord(GsiDistanceWord):
    """``WI331`` Backsight staff reading."""
    _GSI = _regex_measurement(331)

    @classmethod
    def WI(cls) -> int:
        return 331


class GsiF1StaffReadingWord(GsiDistanceWord):
    """``WI332`` Foresight staff reading."""
    _GSI = _regex_measurement(332)

    @classmethod
    def WI(cls) -> int:
        return 332


class GsiIntermediateStaffReadingWord(GsiDistanceWord):
    """``WI332`` Intermediate staff reading."""
    _GSI = _regex_measurement(333)

    @classmethod
    def WI(cls) -> int:
        return 333


class GsiStakeoutStaffReadingWord(GsiDistanceWord):
    """``WI334`` Setting out staff reading."""
    _GSI = _regex_measurement(334)

    @classmethod
    def WI(cls) -> int:
        return 334


class GsiB2StaffReadingWord(GsiDistanceWord):
    """``WI335`` 2nd backsight staff reading in BFFB mode."""
    _GSI = _regex_measurement(335)

    @classmethod
    def WI(cls) -> int:
        return 335


class GsiF2StaffReadingWord(GsiDistanceWord):
    """``WI336`` 2nd foresight staff reading in BFFB mode."""
    _GSI = _regex_measurement(336)

    @classmethod
    def WI(cls) -> int:
        return 336


class GsiAppVersionWord(GsiValueWord):
    """``WI590`` Application version."""
    _GSI = compile(r"^590\.{2}6\+[0-9]{8,16} $")

    @classmethod
    def WI(cls) -> int:
        return 590

    def __init__(self, version: float):
        """
        Parameters
        ----------
        version : float
            Version number (major: integer part, minor: fractional part).
        """
        self.value: float
        super().__init__(version)

    @classmethod
    def parse(cls, value: str) -> Self:
        """
        Parses a version number from serialized GSI word.

        Parameters
        ----------
        value : str
            Serialized GSI word.

        Returns
        -------
        Self
        """
        cls._check_format(value)

        return cls(float(value[7:-1]) * 1e-4)

    def serialize(
        self,
        *,
        gsi16: bool = False,
        angleunit: GsiUnit | None = None,
        distunit: GsiUnit | None = None
    ) -> str:
        if self.value > 9999:
            raise ValueError(
                f"Cannot serialize version larger than 9999 ({self.value:.4f})"
            )

        return format_gsi_word(
            self.wi,
            f"{self.value * 1e4:.0f}",
            unit=GsiUnit.DECIMILLI,
            gsi16=gsi16
        )


class GsiOSVersionWord(GsiAppVersionWord):
    """``WI591`` Operating system version."""
    _GSI = compile(r"^591\.{2}6\+[0-9]{8,16} $")

    @classmethod
    def WI(cls) -> int:
        return 591


class GsiOSInterfaceVersionWord(GsiAppVersionWord):
    """``WI592`` OS interface version."""
    _GSI = compile(r"^592\.{2}6\+[0-9]{8,16} $")

    @classmethod
    def WI(cls) -> int:
        return 592


class GsiGeoComVersionWord(GsiAppVersionWord):
    """``WI593`` GeoCOM version."""
    _GSI = compile(r"^593\.{2}6\+[0-9]{8,16} $")

    @classmethod
    def WI(cls) -> int:
        return 593


class GsiVersionWord(GsiAppVersionWord):
    """``WI594`` GSI protocol version."""
    _GSI = compile(r"^594\.{2}6\+[0-9]{8,16} $")

    @classmethod
    def WI(cls) -> int:
        return 594


class GsiEDMVersionWord(GsiAppVersionWord):
    """``WI595`` EDM device version."""
    _GSI = compile(r"^595\.{2}6\+[0-9]{8,16} $")

    @classmethod
    def WI(cls) -> int:
        return 595


class GsiSoftwareVersionWord(GsiAppVersionWord):
    """``WI599`` On-board software version (digital level)."""
    _GSI = compile(r"^599\.{2}6\+[0-9]{8,16} $")

    @classmethod
    def WI(cls) -> int:
        return 599


class GsiJobWord(GsiRemark1Word):
    """``WI913`` Job name."""
    _GSI = _regex_note(913)

    @classmethod
    def WI(cls) -> int:
        return 913


class GsiOperatorWord(GsiRemark1Word):
    """``WI914`` Operator name."""
    _GSI = _regex_note(914)

    @classmethod
    def WI(cls) -> int:
        return 914


class GsiReadingCountWord(GsiIntegerValueWord):
    """``WI390`` Reading count."""
    _GSI = compile(r"^390[\d\.]{3}\+[0-9]{8,16} $")

    @classmethod
    def WI(cls) -> int:
        return 390

    def __init__(self, count: int):
        """
        Parameters
        ----------
        count : int
            Reading count.
        """
        self.value: int
        super().__init__(count)


class GsiReadingDeviationWord(GsiDistanceWord):
    """``WI391`` Staff reading deviation (mean mode)."""
    _GSI = _regex_measurement(391)

    @classmethod
    def WI(cls) -> int:
        return 391


class GsiReadingSpreadWord(GsiDistanceWord):
    """``WI392`` Staff reading spread (median mode)."""
    _GSI = _regex_measurement(392)

    @classmethod
    def WI(cls) -> int:
        return 392


class GsiBFFBStationDifferenceWord(GsiDistanceWord):
    """``WI571`` Difference between B1-F1 and B2-F2 height differences."""
    _GSI = _regex_measurement(571)

    @classmethod
    def WI(cls) -> int:
        return 571


class GsiRunningBFFBStationDifferenceWord(GsiDistanceWord):
    """``WI572`` Running station difference in BFFB mode."""
    _GSI = _regex_measurement(572)

    @classmethod
    def WI(cls) -> int:
        return 572


class GsiDistanceBalanceWord(GsiDistanceWord):
    """``WI573`` Instrument-staff distance balance."""
    _GSI = _regex_measurement(573)

    @classmethod
    def WI(cls) -> int:
        return 573


class GsiRunningDistanceWord(GsiDistanceWord):
    """``WI574`` Total level line length."""
    _GSI = _regex_measurement(574)

    @classmethod
    def WI(cls) -> int:
        return 574


_WI_TO_TYPE: dict[int, type[GsiWord]] = {
    t.WI(): t for t in (
        GsiPointNameWord,
        GsiSerialnumberWord,
        GsiInstrumentTypeWord,
        GsiStationNameWord,
        GsiDateWord,
        GsiTimeWord,
        GsiHorizontalAngleWord,
        GsiVerticalAngleWord,
        GsiSlopeDistanceWord,
        GsiHorizontalDistanceWord,
        GsiVerticalDistanceWord,
        GsiCodeWord,
        GsiInfo1Word,
        GsiInfo2Word,
        GsiInfo3Word,
        GsiInfo4Word,
        GsiInfo5Word,
        GsiInfo6Word,
        GsiInfo7Word,
        GsiInfo8Word,
        GsiPPMPrismConstantWord,
        GsiPrismConstantWord,
        GsiPPMWord,
        GsiRemark1Word,
        GsiRemark2Word,
        GsiRemark3Word,
        GsiRemark4Word,
        GsiRemark5Word,
        GsiRemark6Word,
        GsiRemark7Word,
        GsiRemark8Word,
        GsiRemark9Word,
        GsiEastingWord,
        GsiNorthingWord,
        GsiHeightWord,
        GsiStationEastingWord,
        GsiStationNorthingWord,
        GsiStationHeightWord,
        GsiTargetHeightWord,
        GsiInstrumentHeightWord,
        GsiPressureWord,
        GsiRefractionCoefWord,
        GsiNewTimeWord,
        GsiNewDateWord,
        GsiNewYearWord,
        GsiAppVersionWord,
        GsiOSVersionWord,
        GsiOSInterfaceVersionWord,
        GsiGeoComVersionWord,
        GsiVersionWord,
        GsiEDMVersionWord,
        GsiJobWord,
        GsiOperatorWord
    )
}

_WI_TO_TYPE_DNA: dict[int, type[GsiWord]] = {
    t.WI(): t for t in (
        GsiPointNameWord,
        GsiSerialnumberWord,
        GsiInstrumentTypeWord,
        GsiDateWord,
        GsiTimeWord,
        GsiStaffDistanceWord,
        GsiCodeWord,
        GsiInfo1Word,
        GsiInfo2Word,
        GsiInfo3Word,
        GsiInfo4Word,
        GsiInfo5Word,
        GsiInfo6Word,
        GsiInfo7Word,
        GsiInfo8Word,
        GsiRemark1Word,
        GsiBenchmarkHeightWord,
        GsiTemperatureWord,
        GsiSimpleStaffReadingWord,
        GsiB1StaffReadingWord,
        GsiF1StaffReadingWord,
        GsiIntermediateStaffReadingWord,
        GsiStakeoutStaffReadingWord,
        GsiB2StaffReadingWord,
        GsiF2StaffReadingWord,
        GsiNewTimeWord,
        GsiNewDateWord,
        GsiNewYearWord,
        GsiSoftwareVersionWord,
        GsiReadingCountWord,
        GsiReadingDeviationWord,
        GsiReadingSpreadWord,
        GsiBFFBStationDifferenceWord,
        GsiRunningBFFBStationDifferenceWord,
        GsiDistanceBalanceWord,
        GsiRunningDistanceWord
    )
}


def parse_gsi_word(
    value: str,
    *,
    dna: bool = False,
    strict: bool = False
) -> GsiWord:
    """
    Parses an arbitrary GSI word from a serialized value.

    Parameters
    ----------
    value : str
        Serialized GSI word.
    dna : bool, optional
        Use words applicable to digital levels, by default False
    strict : bool, optional
        Raise exception if word cannot be parsed (otherwise return
        unknown type word), by default False

    Returns
    -------
    GsiWord

    Raises
    ------
    ValueError
        If strict is enabled and word type cannot be parsed.
    Exception
        If strict is enabled and error occured during parsing.
    """
    value = value.strip("*")

    wi = int(value[:3].rstrip("."))
    if dna:
        wordtype = _WI_TO_TYPE_DNA.get(wi)
    else:
        wordtype = _WI_TO_TYPE.get(wi)

    if wordtype is None:
        if strict:
            raise ValueError(f"Unknown wordindex '{wi:d}'")

        wordtype = GsiUnknownWord

    try:
        word = wordtype.parse(value)
    except Exception as e:
        if strict:
            raise e

        word = GsiUnknownWord.parse(value)

    return word


class GsiBlock:
    """Container type for GSI words."""
    _TYPE_TO_WI = {
        "measurement": 11,
        "specialcode": 41,
        "code": 41
    }

    def __init__(
        self,
        value: str,
        type: str,
        *words: GsiWord,
        address: int | None = None
    ):
        """
        Parameters
        ----------
        value : str
            Point name or code value (depending on block type).
        type : str
            Block type ("measurement", "code" or "specialcode)
        *words : GsiWord
            Words to wrap into the block.
        address : int | None, optional
            Block record address, by default None

        Raises
        ------
        ValueError
            If an unknown block type was specified, or the list of words
            contains an item that cannot be added.
        """
        if type not in self._TYPE_TO_WI:
            raise ValueError(f"Unknown GSI block type: '{type}'")

        self._value = value
        self._type = type
        self._address: int | None = address
        self._words: dict[int, GsiWord] = {}

        for w in words:
            wi = w.wi
            if wi == self._TYPE_TO_WI[self._type]:
                raise ValueError(
                    "Cannot add word identical to the block header word"
                )

            if wi in self._words:
                raise ValueError(
                    f"Cannot add duplicate word type 'WI{wi:d}' to GSI block"
                )

            self._words[wi] = w

    def __str__(self) -> str:
        return (
            f"GSI {self.blocktype} block '{self.value}': "
            f"{len(self._words)} word(s)"
        )

    def __repr__(self) -> str:
        return str(self)

    @property
    def value(self) -> str:
        """Block header value (point name or code value)."""
        return self._value

    @property
    def blocktype(self) -> str:
        """Block type ("measurement", "code", "specialcode")"""
        return self._type

    @property
    def address(self) -> int | None:
        """Line address."""
        return self._address

    @classmethod
    def parse(
        cls,
        data: str,
        *,
        dna: bool = False,
        keep_unknowns: bool = False
    ) -> Self:
        """
        Parses a GSI block from a serialized value.

        The block cannot have the same GSI word type multiple times.

        Parameters
        ----------
        data : str
            Serialized GSI block.
        dna : bool, optional
            Use words applicable to digital levels, by default False
        keep_unknowns : bool, optional
            Keep words that could not be parsed to known types (otherwise
            discard them), by default False

        Returns
        -------
        Self
            Measurement or code type block.

        Raises
        ------
        ValueError
            If an error was found in the serialized value.
        """
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
                    header: GsiValueWord = GsiPointNameWord.parse(
                        data[:wordsize]
                    )
                except Exception:
                    raise ValueError(
                        "First word in measurement block must be point name"
                    )
                value = header.value
                type = "measurement"
            case 41:
                try:
                    header = GsiCodeWord.parse(data[:wordsize])
                except Exception:
                    raise ValueError(
                        "First word in code block must be code word"
                    )
                value, special = header.value
                type = "specialcode" if special else "code"
            case _:
                raise ValueError(
                    f"Unsupported block header word type: '{wi:d}'"
                )

        address: int | None = None
        if data[2:6].isdigit():
            address = int(data[2:6])

        words: list[GsiWord] = []
        for i in range(wordsize, len(data), wordsize):
            wordstring = data[i:i+wordsize]
            word = parse_gsi_word(
                wordstring,
                dna=dna,
                strict=False
            )
            if isinstance(word, GsiUnknownWord) and not keep_unknowns:
                continue

            words.append(word)

        return cls(
            value,
            type,
            *words,
            address=address
        )

    def __iter__(self) -> Iterator[GsiWord]:
        return iter(self._words.values())

    def __len__(self) -> int:
        return len(self._words)

    def get_word(self, wordtype: type[_T]) -> _T | None:
        """
        Get a word of a specific type from the block.

        Parameters
        ----------
        wordtype : type[_T]
            Word type to get.

        Returns
        -------
        GsiWord
            Return None if the block does not contain a word of the requested
            type.
        """
        return cast(_T | None, self._words.get(wordtype.WI()))

    def serialize(
        self,
        *,
        address: int | None = None,
        gsi16: bool = False,
        endl: bool = True,
        angleunit: GsiUnit | None = GsiUnit.DEG,
        distunit: GsiUnit | None = GsiUnit.DECIMILLI
    ) -> str:
        """
        Serializes the block to a list of GSI words.

        Parameters
        ----------
        address : int, optional
            Address override value (negative value disables addressing
            alltogether), by default None
        gsi16 : bool, optional
            Create GSI16 words isntead of GSI8, by default False
        endl : bool, optional
            Add newline to end of block (recommended for file writing),
            by default True
        angleunit : GsiUnit | None, optional
            Angular unit to serialize angles as, by default GsiUnit.DEG
        distunit : GsiUnit | None, optional
            Distance/Scaler unit for lengths and measurement-like scaled
            values, by default GsiUnit.DECIMILLI

        Returns
        -------
        str

        Raises
        ------
        ValueError
            If block has unknown type.
        """
        match self.blocktype:
            case "measurement":
                header = GsiPointNameWord(self.value).serialize(gsi16=gsi16)
            case "code":
                header = GsiCodeWord(self.value, False).serialize(gsi16=gsi16)
            case "specialcode":
                header = GsiCodeWord(self.value, True).serialize(gsi16=gsi16)
            case _:
                raise ValueError(f"Unknown block type: '{self.blocktype}'")

        if address is None:
            address = self.address

        if address is not None and address >= 0:
            header = f"{header[:2]}{address % 10000:04d}{header[6:]}"

        output = header + "".join(
            [
                w.serialize(
                    gsi16=gsi16,
                    angleunit=angleunit,
                    distunit=distunit
                )
                for w in self
            ]
        )

        if gsi16:
            output = "*" + output

        return output + ("\n" if endl else "")

    def without_unknowns(self) -> Self:
        """
        Returns a shallow copy of the block with the unknown words dropped.

        Returns
        -------
        Self
        """
        unknown = GsiUnknownWord.WI()
        words = [w for w in self if w.WI() != unknown]

        return type(self)(
            self.value,
            self.blocktype,
            *words,
            address=self.address
        )


def parse_gsi_blocks_from_file(
    file: TextIO,
    *,
    dna: bool = False,
    keep_unknowns: bool = False,
    strict: bool = False
) -> list[GsiBlock]:
    """
    Parser GSI blocks from text file.

    Parameters
    ----------
    file : TextIO
        GSI file.
    dna : bool, optional
        Use words applicable to digital levels, by default False
    keep_unknowns : bool, optional
        Retain unknown word types, by default False
    strict : bool, optional
        Raise errors during parsing, by default False

    Returns
    -------
    list
    """
    blocks: list[GsiBlock] = []
    for line in file:
        if not line.strip():
            continue
        try:
            block = GsiBlock.parse(
                line.strip("\n"),
                dna=dna,
                keep_unknowns=keep_unknowns
            )
        except Exception as e:
            if strict:
                raise e

        blocks.append(block)

    return blocks


def write_gsi_blocks_to_file(
    blocks: Iterable[GsiBlock],
    file: TextIO,
    *,
    gsi16: bool = False,
    angleunit: GsiUnit = GsiUnit.DEG,
    distunit: GsiUnit = GsiUnit.MILLI,
    address: int | None = 1
) -> None:
    """
    Write GSI blocks to file, with sequential addresses.

    Parameters
    ----------
    blocks : Iterable[GsiBlock]
        Blocks to write to file.
    file : TextIO
        Output file.
    gsi16 : bool, optional
        Use GSI16 instead of GSI8, by default False
    angleunit : GsiUnit | None, optional
        Angular unit to serialize angles as, by default GsiUnit.DEG
    distunit : GsiUnit | None, optional
        Distance/Scaler unit for lengths and measurement-like scaled
        values, by default GsiUnit.MILLI
    address : int | None, optional
        Starting point of the sequential addresses (not setting it preserves
        the address information in the blocks, negative value disables
        addressing alltogether), by default None
    """

    def get_addresser(
        address: int | None
    ) -> Generator[int | None, None, None]:
        if address is None or address < 0:
            while True:
                yield address
        else:
            while True:
                yield address
                address += 1

    addresser = get_addresser(address)

    for block in blocks:
        file.write(
            block.serialize(
                address=next(addresser),
                gsi16=gsi16,
                endl=True,
                angleunit=angleunit,
                distunit=distunit
            )
        )
