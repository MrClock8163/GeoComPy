from __future__ import annotations

from enum import StrEnum


param_descriptions: dict[int, str] = {
    30: "Beep intensity",
    31: "Display illumination",
    32: "Display constrast",
    41: "Distance unit",
    42: "Temperature unit",
    51: "Decimals displayed",
    70: "Serial speed",
    71: "Parity",
    73: "Terminator",
    75: "Protocol",
    76: "Recording device",
    78: "Send delay",
    90: "Battery level",
    91: "Internal temperature",
    95: "Auto off",
    106: "Display heater",
    125: "Earth curvature correction",
    127: "Staff direction",
    137: "GSI type",
    138: "Code recording mode"
}


word_descriptions: dict[int, str] = {
    11: "Point ID",
    71: "Remark",
    560: "Time",
    561: "Date",
    562: "Year",
    32: "Distance",
    330: "Reading",
    95: "Internal temperature",
    12: "Serial number",
    13: "Instrument type",
    17: "Full date",
    19: "Date and time",
    599: "Software version"
}


class DNAErrors(StrEnum):
    W_BUSY = "@W400"
    W_INVCMD = "@W427"
    E_UNKNOWN = "@E0"
    E_TILT = "@E458"
    E_NOMEASURE = "@E439"
