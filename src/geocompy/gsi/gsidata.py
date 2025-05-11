"""
Description
===========

Module: ``geocompy.gsi.gsidata``

The GSI Online data module provides utility types, that are specific to
the GSI Online protocol.

Enums
-----

- ``AutoOff``
- ``BeepIntensity``
- ``Communication``
- ``GSIFormat``
- ``Illumination``
- ``RecordCode``
- ``Recorder``
- ``Units``
"""
from enum import Enum


class Communication:
    """GSI Online serial communication settings."""
    class Baud(Enum):
        """Serial speed."""
        B1200 = 2
        B2400 = 3
        B4800 = 4
        B9600 = 5
        B19200 = 6

    class Parity(Enum):
        """Serial parity."""
        NONE = 0
        ODD = 1
        EVEN = 2

    class Terminator(Enum):
        """Message terminator."""
        CR = 0
        CRLF = 1


class Units:
    """GSI Online measurement units."""
    class Temperature(Enum):
        """Temperature unit."""
        CELSIUS = 0
        FAHRENHEIT = 1

    class Distance(Enum):
        """Distance unit."""
        METER = 0
        USFEET = 1
        FEET = 2
        USFEETINCH = 5


class BeepIntensity(Enum):
    """GSI Online beep signal intensitie."""
    OFF = 0
    MEDIUM = 1
    LOUD = 2


class Illumination(Enum):
    """GSI Online illumination setting."""
    OFF = 0
    LEVELONLY = 2
    BOTH = 3


class Recorder(Enum):
    """GSI Online data recorder device."""
    INTERNAL = 0
    RS232 = 1


class AutoOff(Enum):
    """GSI Online automatic shutdown."""
    OFF = 0
    ON = 1
    SLEEP = 2


class RecordCode(Enum):
    """GSI Online automatic code recording."""
    BEFORE = 0
    """Record code before measurement."""
    AFTER = 1
    """Record code after measurement."""


class GSIFormat(Enum):
    """GSI Online recording format."""
    GSI8 = 0
    GSI16 = 1
