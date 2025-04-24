"""
``geocompy.dna.settings``
=========================

Definitions for the DNA settings subsystem.

Types
-----

- ``DNASettings``
"""
from __future__ import annotations

from enum import IntEnum

from ..protocols import (
    GsiOnlineSubsystem,
    GsiOnlineResponse
)
from ..data import (
    toenum,
    enumparser
)


class DNASettings(GsiOnlineSubsystem):
    """
    Settings subsystem of the DNA GSI Online protocol.

    This subsystem gives access to the internal parameters of the
    instrument. Most parameters (with a few exceptions) can be both
    queried and set/changed.

    """
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
        """
        ``SET 30``

        Sets the intensity of the beep signals.

        Parameters
        ----------
        intensity : BEEPINTENSITY | str
            Beep intensity to set.

        Returns
        -------
        GsiOnlineResponse
            Success of the change.
        """
        _status = toenum(self.BEEPINTENSITY, intensity)
        return self._setrequest(30, _status.value)

    def get_beep(self) -> GsiOnlineResponse[BEEPINTENSITY | None]:
        """
        ``CONF 30``

        Gets the current set intensity of the beep signals.

        Returns
        -------
        GsiOnlineResponse
            Current beep intensity.

        Note
        ----
        The value in the response is ``None`` if the value could not be
        retrieved (i.e. an error occured during the request).
        """
        return self._confrequest(
            30,
            enumparser(self.BEEPINTENSITY)
        )

    def get_illumination(self) -> GsiOnlineResponse[ILLUMINATION | None]:
        """
        ``CONF 31``

        Gets the current status of the diplay and bubble illumination.

        Returns
        -------
        GsiOnlineResponse
            Illumination status.

        Note
        ----
        The value in the response is ``None`` if the value could not be
        retrieved (i.e. an error occured during the request).
        """
        return self._confrequest(
            31,
            enumparser(self.ILLUMINATION)
        )

    def set_contrast(
        self,
        contrast: int
    ) -> GsiOnlineResponse[bool]:
        """
        ``SET 32``

        Sets the display contrast level.

        Parameters
        ----------
        contrast : int
            Contrast level to set in [0; 100] range.

        Returns
        -------
        GsiOnlineResponse
            Success of the change.
        """
        return self._setrequest(32, contrast)

    def get_contrast(self) -> GsiOnlineResponse[int | None]:
        """
        ``CONF 32``

        Gets the current display contrast level.

        Returns
        -------
        GsiOnlineResponse
            Contrast level in [0; 100] range.

        Note
        ----
        The value in the response is ``None`` if the value could not be
        retrieved (i.e. an error occured during the request).
        """
        return self._confrequest(
            32,
            int
        )

    def set_distance_unit(
        self,
        unit: DISTUNIT | str
    ) -> GsiOnlineResponse[bool]:
        """
        ``SET 41``

        Sets the distance measurement unit.

        Parameters
        ----------
        unit : DISTUNIT | str
            Distance unit to set.

        Returns
        -------
        GsiOnlineResponse
            Success of the change.
        """
        _unit = toenum(self.DISTUNIT, unit)
        return self._setrequest(41, _unit.value)

    def get_distance_unit(self) -> GsiOnlineResponse[DISTUNIT | None]:
        """
        ``CONF 41``

        Gets the current distance measurement unit.

        Returns
        -------
        GsiOnlineResponse
            Distance unit.

        Note
        ----
        The value in the response is ``None`` if the value could not be
        retrieved (i.e. an error occured during the request).
        """
        return self._confrequest(
            41,
            enumparser(self.DISTUNIT)
        )

    def set_temperature_unit(
        self,
        unit: TEMPUNIT | str
    ) -> GsiOnlineResponse[bool]:
        """
        ``SET 42``

        Sets the temperature measurement unit.

        Parameters
        ----------
        unit : TEMPUNIT | str
            Temperature unit to set.

        Returns
        -------
        GsiOnlineResponse
            Success of the change.
        """
        _unit = toenum(self.TEMPUNIT, unit)
        return self._setrequest(42, _unit.value)

    def get_temperature_unit(self) -> GsiOnlineResponse[TEMPUNIT | None]:
        """
        ``CONF 42``

        Gets the current temperature measurement unit.

        Returns
        -------
        GsiOnlineResponse
            Temperature unit.

        Note
        ----
        The value in the response is ``None`` if the value could not be
        retrieved (i.e. an error occured during the request).
        """
        return self._confrequest(
            42,
            enumparser(self.TEMPUNIT)
        )

    def set_decimals(
        self,
        decimals: int
    ) -> GsiOnlineResponse[bool]:
        """
        ``SET 51``

        Sets the number of displayed decimal places.

        Parameters
        ----------
        decimals : int
            Number of decimal places to display.

        Returns
        -------
        GsiOnlineResponse
            Success of the change.
        """
        return self._setrequest(51, decimals)

    def get_decimals(self) -> GsiOnlineResponse[int | None]:
        """
        ``CONF 51``

        Gets the current number of displayed decimals.

        Returns
        -------
        GsiOnlineResponse
            Number of decimals.

        Note
        ----
        The value in the response is ``None`` if the value could not be
        retrieved (i.e. an error occured during the request).
        """
        return self._confrequest(
            51,
            int
        )

    def set_baud(
        self,
        baud: BAUD | str
    ) -> GsiOnlineResponse[bool]:
        """
        ``SET 70``

        Sets the communication speed.

        Parameters
        ----------
        baud: BAUD | str
            Communication speed to set.

        Returns
        -------
        GsiOnlineResponse
            Success of the change.
        """
        _baud = toenum(self.BAUD, baud)
        return self._setrequest(70, _baud.value)

    def get_baud(self) -> GsiOnlineResponse[BAUD | None]:
        """
        ``CONF 70``

        Gets the current communication speed.

        Returns
        -------
        GsiOnlineResponse
            Communication speed.

        Note
        ----
        The value in the response is ``None`` if the value could not be
        retrieved (i.e. an error occured during the request).
        """
        return self._confrequest(
            70,
            enumparser(self.BAUD)
        )

    def set_parity(
        self,
        parity: PARITY | str
    ) -> GsiOnlineResponse[bool]:
        """
        ``SET 71``

        Sets parity check bit behavior.

        Parameters
        ----------
        parity: PARITY | str
            Parity bit setting.

        Returns
        -------
        GsiOnlineResponse
            Success of the change.
        """
        _parity = toenum(self.PARITY, parity)
        return self._setrequest(71, _parity.value)

    def get_parity(self) -> GsiOnlineResponse[PARITY | None]:
        """
        ``CONF 71``

        Gets the current parity bit setting.

        Returns
        -------
        GsiOnlineResponse
            Parity bit setting.

        Note
        ----
        The value in the response is ``None`` if the value could not be
        retrieved (i.e. an error occured during the request).
        """
        return self._confrequest(
            71,
            enumparser(self.PARITY)
        )

    def set_terminator(
        self,
        terminator: TERMINATOR | str
    ) -> GsiOnlineResponse[bool]:
        """
        ``SET 73``

        Sets the message terminator character.

        Parameters
        ----------
        terminator: TERMINATOR | str
            Message terminator.

        Returns
        -------
        GsiOnlineResponse
            Success of the change.
        """
        _terminator = toenum(self.TERMINATOR, terminator)
        return self._setrequest(73, _terminator.value)

    def get_terminator(self) -> GsiOnlineResponse[TERMINATOR | None]:
        """
        ``CONF 73``

        Gets the current message terminator.

        Returns
        -------
        GsiOnlineResponse
            Message terminator.

        Note
        ----
        The value in the response is ``None`` if the value could not be
        retrieved (i.e. an error occured during the request).
        """
        return self._confrequest(
            73,
            enumparser(self.TERMINATOR)
        )

    def set_protocol(
        self,
        enabled: bool
    ) -> GsiOnlineResponse[bool]:
        """
        ``SET 75``

        Enables or disables the communication protocol.

        Parameters
        ----------
        enabled : bool

        Returns
        -------
        GsiOnlineResponse
            Success of the change.
        """
        return self._setrequest(75, enabled)

    def get_protocol(self) -> GsiOnlineResponse[bool | None]:
        """
        ``CONF 75``

        Gets the current status of the communication protocol.

        Returns
        -------
        GsiOnlineResponse
            Protocol status.

        Note
        ----
        The value in the response is ``None`` if the value could not be
        retrieved (i.e. an error occured during the request).
        """
        return self._confrequest(
            75,
            bool
        )

    def set_recorder(
        self,
        recorder: RECORDER | str
    ) -> GsiOnlineResponse[bool]:
        """
        ``SET 76``

        Sets the measurement recording device.

        Parameters
        ----------
        recorder : RECORDER | str
            Target device to store measurements.

        Returns
        -------
        GsiOnlineResponse
            Success of the change.
        """
        _recorder = toenum(self.TERMINATOR, recorder)
        return self._setrequest(76, _recorder.value)

    def get_recorder(self) -> GsiOnlineResponse[RECORDER | None]:
        """
        ``CONF 76``

        Gets the current measurement recording device.

        Returns
        -------
        GsiOnlineResponse
            Target recording device.

        Note
        ----
        The value in the response is ``None`` if the value could not be
        retrieved (i.e. an error occured during the request).
        """
        return self._confrequest(
            76,
            enumparser(self.RECORDER)
        )

    def set_delay(
        self,
        delay: int
    ) -> GsiOnlineResponse[bool]:
        """
        ``SET 78``

        Sets the delay between messages.

        Parameters
        ----------
        delay : int
            Time delay between sending two messages [0; 50] range in
            [10ms] units.

        Returns
        -------
        GsiOnlineResponse
            Success of the change.
        """
        return self._setrequest(78, delay)

    def get_delay(self) -> GsiOnlineResponse[int | None]:
        """
        ``CONF 78``

        Gets the current message delay.

        Returns
        -------
        GsiOnlineResponse
            Delay between two messages in [0; 50] range in [10ms] units.

        Note
        ----
        The value in the response is ``None`` if the value could not be
        retrieved (i.e. an error occured during the request).
        """
        return self._confrequest(
            78,
            int
        )

    def get_battery(self) -> GsiOnlineResponse[int | None]:
        """
        ``CONF 90``

        Gets the current level of the battery.

        Returns
        -------
        GsiOnlineResponse
            Remaining battery capacity in [0; 10] range.

        Note
        ----
        The value in the response is ``None`` if the value could not be
        retrieved (i.e. an error occured during the request).
        """
        return self._confrequest(
            90,
            int
        )

    def get_temperature(self) -> GsiOnlineResponse[int | None]:
        """
        ``CONF 91``

        Gets the current internal temperature.

        Returns
        -------
        GsiOnlineResponse
            Internal temperature.

        Note
        ----
        The value in the response is ``None`` if the value could not be
        retrieved (i.e. an error occured during the request).
        """
        return self._confrequest(
            91,
            int
        )

    def set_autooff(
        self,
        status: AUTOOFF | str
    ) -> GsiOnlineResponse[bool]:
        """
        ``SET 95``

        Sets the status of the automatic shutdown feature.

        Parameters
        ----------
        status : AUTOOFF | str
            Automatic shutdown mode.

        Returns
        -------
        GsiOnlineResponse
            Success of the change.
        """
        _mode = toenum(self.AUTOOFF, status)
        return self._setrequest(95, _mode.value)

    def get_autooff(self) -> GsiOnlineResponse[AUTOOFF | None]:
        """
        ``CONF 95``

        Gets the current status of the automatic shutdown feature.

        Returns
        -------
        GsiOnlineResponse
            Status of the automatic shutdown.

        Note
        ----
        The value in the response is ``None`` if the value could not be
        retrieved (i.e. an error occured during the request).
        """
        return self._confrequest(
            95,
            enumparser(self.AUTOOFF)
        )

    def set_display_heater(
        self,
        enabled: bool
    ) -> GsiOnlineResponse[bool]:
        """
        ``SET 106``

        Enables or disables the display heater unit.

        Parameters
        ----------
        enabled : bool

        Returns
        -------
        GsiOnlineResponse
            Success of the change.
        """
        return self._setrequest(106, enabled)

    def get_display_heater(self) -> GsiOnlineResponse[bool | None]:
        """
        ``CONF 106``

        Gets the current status of the display heater unit.

        Returns
        -------
        GsiOnlineResponse
            Status of the display heater.

        Note
        ----
        The value in the response is ``None`` if the value could not be
        retrieved (i.e. an error occured during the request).
        """
        return self._confrequest(
            106,
            bool
        )

    def set_curvature_correction(
        self,
        enabled: bool
    ) -> GsiOnlineResponse[bool]:
        """
        ``SET 125``

        Enables or disables the Earth curvature correction.

        Parameters
        ----------
        enabled : bool

        Returns
        -------
        GsiOnlineResponse
            Success of the change.
        """
        return self._setrequest(125, enabled)

    def get_curvature_correction(self) -> GsiOnlineResponse[bool | None]:
        """
        ``CONF 125``

        Gets the current status of the Earth curvature correction.

        Returns
        -------
        GsiOnlineResponse
            Status of the curvature correction.

        Note
        ----
        The value in the response is ``None`` if the value could not be
        retrieved (i.e. an error occured during the request).
        """
        return self._confrequest(
            125,
            bool
        )

    def set_staff_mode(
        self,
        inverted: bool
    ) -> GsiOnlineResponse[bool]:
        """
        ``SET 127``

        Sets the levelling staff mode.

        Parameters
        ----------
        inverted : bool
            Is the staff in an inverted position?

        Returns
        -------
        GsiOnlineResponse
            Success of the change.
        """
        return self._setrequest(127, inverted)

    def get_staff_mode(self) -> GsiOnlineResponse[bool | None]:
        """
        ``CONF 127``

        Gets the current mode of the levelling staff.

        Returns
        -------
        GsiOnlineResponse
            Is the levelling staff inverted?

        Note
        ----
        The value in the response is ``None`` if the value could not be
        retrieved (i.e. an error occured during the request).
        """
        return self._confrequest(
            127,
            bool
        )

    def set_format(
        self,
        format: FORMAT | str
    ) -> GsiOnlineResponse[bool]:
        """
        ``SET 137``

        Sets the GSI format of the instrument.

        Parameters
        ----------
        format : FORMAT | str
            GSI format.

        Returns
        -------
        GsiOnlineResponse
            Success of the change.

        Note
        ----
        If the request is successful, the internal format variable is
        updated accordingly to keep the communication in sync between
        the computer and the instrument.
        """
        _format = toenum(self.FORMAT, format)
        response = self._setrequest(137, _format.value)
        if response.value:
            self._parent._gsi16 = _format == self.FORMAT.GSI16

        return response

    def get_format(self) -> GsiOnlineResponse[FORMAT | None]:
        """
        ``CONF 137``

        Gets the current GSI communication format of the instrument.

        Returns
        -------
        GsiOnlineResponse
            GSI format.

        Note
        ----
        The value in the response is ``None`` if the value could not be
        retrieved (i.e. an error occured during the request).

        Note
        ----
        If the request is successful, the internal format variable is
        updated accordingly to keep the communication in sync between
        the computer and the instrument.
        """
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
        """
        ``SET 138``

        Sets the quick code recording mode.

        Parameters
        ----------
        mode : CODERECORD | str
            Quick code recording mode.

        Returns
        -------
        GsiOnlineResponse
            Success of the change.
        """
        _mode = toenum(self.CODERECORD, mode)
        return self._setrequest(138, _mode.value)
