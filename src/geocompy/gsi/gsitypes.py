"""
Description
===========

Module: ``geocompy.gis.gsitypes``

The GSI Online types module provides type definitions and general
constants, that are relevant to the GSI Online protocol.

Types
-----

- ``GsiOnlineResponse``
- ``GsiOnlineType``
- ``GsiOnlineSubsystem``
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Callable, Literal

from .gsiformat import GsiWord


_T = TypeVar("_T")
_P = TypeVar("_P")
_G = TypeVar("_G", bound=GsiWord)


class GsiOnlineResponse(Generic[_T]):
    """Container class for parsed GSI Online responses."""

    def __init__(
        self,
        desc: str,
        cmd: str,
        response: str,
        value: _T | None,
        comment: str = ""
    ):
        """
        Parameters
        ----------
        desc : str
            Description of the GSI Online command, that invoked this
            response.
        cmd : str
            Full, serialized command, that invoked this response.
        response : str
            Full, received response.
        value
            Parsed response value. The content is dependent on the
            executed command.
        comment : str
            Additional comment (e.g. explanation of an error).
        """
        self.desc: str = desc
        """Description of the GSI Online command, that invoked this
        response."""
        self.cmd: str = cmd
        """Full, serialized command, that invoked this response."""
        self.response: str = response
        """Full, received response."""
        self.value: _T | None = value
        """Parsed response value. The content is dependent on the
        executed command."""
        self.comment: str = comment
        """Additional comment (e.g. explanation of an error)."""

    def __str__(self) -> str:
        success = (
            "success"
            if self.value is not None
            else f"fail ({self.comment})"
        )
        return (
            f"GsiOnlineResponse({self.desc}) "
            f"{success}, "
            f"value: {self.value}, "
            f"(cmd: '{self.cmd}', response: '{self.response}')"
        )

    def __bool__(self) -> bool:
        return self.value is not None

    def map_value(
        self,
        transformer: Callable[[_T | None], _P | None]
    ) -> GsiOnlineResponse[_P]:
        """
        Returns a new response object with the metadata maintained, but
        the value transformed with the supplied function.

        Parameters
        ----------
        transformer : Callable[[_T  |  None], _P  |  None]
            Function to transform the value to a new value.

        Returns
        -------
        GeoComResponse
            Response with transformed value.
        """
        try:
            value = transformer(self.value)
        except Exception:
            value = None

        return GsiOnlineResponse(
            self.desc,
            self.cmd,
            self.response,
            value,
            self.comment
        )


class GsiOnlineType(ABC):
    """
    Interface definition for the GSI Online protocol handler type.
    """
    @property
    @abstractmethod
    def is_client_gsi16(self) -> bool: ...

    @is_client_gsi16.setter
    @abstractmethod
    def is_client_gsi16(self, value: bool) -> None: ...

    @abstractmethod
    def setrequest(
        self,
        param: int,
        value: int
    ) -> GsiOnlineResponse[bool]: ...

    @abstractmethod
    def confrequest(
        self,
        param: int,
        parser: Callable[[str], _T]
    ) -> GsiOnlineResponse[_T]: ...

    @abstractmethod
    def putrequest(
        self,
        word: _G
    ) -> GsiOnlineResponse[bool]: ...

    @abstractmethod
    def getrequest(
        self,
        mode: Literal['I', 'M', 'C'],
        wordtype: type[_G]
    ) -> GsiOnlineResponse[_G]: ...

    @abstractmethod
    def request(
        self,
        cmd: str,
        desc: str = ""
    ) -> GsiOnlineResponse[bool]: ...


class GsiOnlineSubsystem:
    """
    Base class for GSI Online subsystems.
    """

    def __init__(self, parent: GsiOnlineType):
        """
        Parameters
        ----------
        parent : GsiOnlineType
            The parent protocol instance of this subsystem.
        """
        self._parent: GsiOnlineType = parent
        """Parent protocol instance"""
        self._setrequest = self._parent.setrequest
        """Shortcut to the `setrequest` method of the parent protocol."""
        self._confrequest = self._parent.confrequest
        """Shortcut to the `confrequest` method of the parent protocol."""
        self._putrequest = self._parent.putrequest
        """Shortcut to the `putrequest` method of the parent protocol."""
        self._getrequest = self._parent.getrequest
        """Shortcut to the `getrequest` method of the parent protocol."""


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
"""Mapping of parameter indices to short descriptions."""


word_descriptions: dict[int, str] = {
    11: "Point ID",
    71: "Note",
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
"""Mapping of GSI word indices to short descriptions."""
