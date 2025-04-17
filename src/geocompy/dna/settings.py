from __future__ import annotations

from enum import IntEnum

from .. import (
    GsiOnlineSubsystem,
    GsiOnlineResponse
)
from ..data import (
    toenum,
    enumparser
)


class DNASettings(GsiOnlineSubsystem):
    class BEEPINTENSITY(IntEnum):
        OFF = 0
        MEDIUM = 1
        LOUD = 2

    class ILLUMINATION(IntEnum):
        OFF = 0
        LEVELONLY = 2
        BOTH = 3

    class DISTUNIT(IntEnum):
        METER = 0
        USFEET = 1
        FEET = 2
        USFEETINCH = 5

    class TEMPUNIT(IntEnum):
        CELSIUS = 0
        FAHRENHEIT = 1

    class BAUD(IntEnum):
        B1200 = 2
        B2400 = 3
        B4800 = 4
        B9600 = 5
        B19200 = 6

    class PARITY(IntEnum):
        NONE = 0
        ODD = 1
        EVEN = 2

    class TERMINATOR(IntEnum):
        CR = 0
        CRLF = 1

    class RECORDER(IntEnum):
        INTERNAL = 0
        RS232 = 1

    class AUTOOFF(IntEnum):
        OFF = 0
        ON = 1
        SLEEP = 2

    class FORMAT(IntEnum):
        GSI8 = 0
        GSI16 = 1

    class CODERECORD(IntEnum):
        BEFORE = 0
        AFTER = 1

    def set_beep(
        self,
        intensity: BEEPINTENSITY | str
    ) -> GsiOnlineResponse[bool]:
        _status = toenum(self.BEEPINTENSITY, intensity)
        return self._setrequest(30, _status.value)

    def get_beep(self) -> GsiOnlineResponse[BEEPINTENSITY | None]:
        return self._confrequest(
            30,
            enumparser(self.BEEPINTENSITY)
        )

    def get_illumination(self) -> GsiOnlineResponse[ILLUMINATION | None]:
        return self._confrequest(
            31,
            enumparser(self.ILLUMINATION)
        )

    def set_contrast(
        self,
        contrast: int
    ) -> GsiOnlineResponse[bool]:
        return self._setrequest(32, contrast)

    def get_contrast(self) -> GsiOnlineResponse[int | None]:
        return self._confrequest(
            32,
            int
        )

    def set_distance_unit(
        self,
        unit: DISTUNIT | str
    ) -> GsiOnlineResponse[bool]:
        _unit = toenum(self.DISTUNIT, unit)
        return self._setrequest(41, _unit.value)

    def get_distance_unit(self) -> GsiOnlineResponse[DISTUNIT | None]:
        return self._confrequest(
            41,
            enumparser(self.DISTUNIT)
        )

    def set_temperature_unit(
        self,
        unit: TEMPUNIT | str
    ) -> GsiOnlineResponse[bool]:
        _unit = toenum(self.TEMPUNIT, unit)
        return self._setrequest(42, _unit.value)

    def get_temperature_unit(self) -> GsiOnlineResponse[TEMPUNIT | None]:
        return self._confrequest(
            42,
            enumparser(self.TEMPUNIT)
        )

    def set_decimals(
        self,
        decimals: int
    ) -> GsiOnlineResponse[bool]:
        return self._setrequest(51, decimals)

    def get_decimals(self) -> GsiOnlineResponse[int | None]:
        return self._confrequest(
            51,
            int
        )

    def set_baud(
        self,
        baud: BAUD | str
    ) -> GsiOnlineResponse[bool]:
        _baud = toenum(self.BAUD, baud)
        return self._setrequest(70, _baud.value)

    def get_baud(self) -> GsiOnlineResponse[BAUD | None]:
        return self._confrequest(
            70,
            enumparser(self.BAUD)
        )

    def set_parity(
        self,
        parity: PARITY | str
    ) -> GsiOnlineResponse[bool]:
        _parity = toenum(self.PARITY, parity)
        return self._setrequest(71, _parity.value)

    def get_parity(self) -> GsiOnlineResponse[PARITY | None]:
        return self._confrequest(
            71,
            enumparser(self.PARITY)
        )

    def set_terminator(
        self,
        terminator: TERMINATOR | str
    ) -> GsiOnlineResponse[bool]:
        _terminator = toenum(self.TERMINATOR, terminator)
        return self._setrequest(73, _terminator.value)

    def get_terminator(self) -> GsiOnlineResponse[TERMINATOR | None]:
        return self._confrequest(
            73,
            enumparser(self.TERMINATOR)
        )

    def set_protocol(
        self,
        enabled: bool
    ) -> GsiOnlineResponse[bool]:
        return self._setrequest(75, enabled)

    def get_protocol(self) -> GsiOnlineResponse[bool | None]:
        return self._confrequest(
            75,
            bool
        )

    def set_recorder(
        self,
        recorder: RECORDER | str
    ) -> GsiOnlineResponse[bool]:
        _recorder = toenum(self.TERMINATOR, recorder)
        return self._setrequest(76, _recorder.value)

    def get_recorder(self) -> GsiOnlineResponse[RECORDER | None]:
        return self._confrequest(
            76,
            enumparser(self.RECORDER)
        )

    def set_delay(
        self,
        delay: int
    ) -> GsiOnlineResponse[bool]:
        return self._setrequest(78, delay)

    def get_delay(self) -> GsiOnlineResponse[int | None]:
        return self._confrequest(
            78,
            int
        )

    def get_battery(self) -> GsiOnlineResponse[int | None]:
        return self._confrequest(
            90,
            int
        )

    def get_temperature(self) -> GsiOnlineResponse[int | None]:
        return self._confrequest(
            91,
            int
        )

    def set_autooff(
        self,
        status: AUTOOFF | str
    ) -> GsiOnlineResponse[bool]:
        _mode = toenum(self.AUTOOFF, status)
        return self._setrequest(95, _mode.value)

    def get_autooff(self) -> GsiOnlineResponse[AUTOOFF | None]:
        return self._confrequest(
            95,
            enumparser(self.AUTOOFF)
        )

    def set_display_heater(
        self,
        enabled: bool
    ) -> GsiOnlineResponse[bool]:
        return self._setrequest(106, enabled)

    def get_display_heater(self) -> GsiOnlineResponse[bool | None]:
        return self._confrequest(
            106,
            bool
        )

    def set_curvature_correction(
        self,
        enabled: bool
    ) -> GsiOnlineResponse[bool]:
        return self._setrequest(125, enabled)

    def get_curvature_correction(self) -> GsiOnlineResponse[bool | None]:
        return self._confrequest(
            125,
            bool
        )

    def set_staff_mode(
        self,
        inverted: bool
    ) -> GsiOnlineResponse[bool]:
        return self._setrequest(127, inverted)

    def get_staff_mode(self) -> GsiOnlineResponse[bool | None]:
        return self._confrequest(
            127,
            bool
        )

    def set_format(
        self,
        format: FORMAT | str
    ) -> GsiOnlineResponse[bool]:
        _format = toenum(self.FORMAT, format)
        response = self._setrequest(137, _format.value)
        if response.value:
            self._parent._gsi16 = _format == self.FORMAT.GSI16

        return response

    def get_format(self) -> GsiOnlineResponse[FORMAT | None]:
        response = self._confrequest(
            137,
            enumparser(self.FORMAT)
        )
        if response.value:
            self._parent._gsi16 = response.value == self.FORMAT.GSI16
        return response

    def set_code_recording(
        self,
        mode: CODERECORD | str
    ) -> GsiOnlineResponse[bool]:
        _mode = toenum(self.CODERECORD, mode)
        return self._setrequest(138, _mode.value)
