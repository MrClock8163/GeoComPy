"""
Description
===========

Module: ``geocompy.geo.dna``

Definitions for the GeoCom Digital level subsystem.

Types
-----

- ``GeoComDNA``

"""
from __future__ import annotations

from ..data import (
    parsebool,
    enumparser,
    toenum,
    Angle
)
from .gcdata import StaffType
from .gctypes import (
    GeoComSubsystem,
    GeoComResponse
)


class GeoComDNA(GeoComSubsystem):
    """
    Digital level subsystem of the GeoCom protocol.

    .. versionadded:: GeoCom-LS
    """

    def get_reading(
        self,
        wait: int = 5000
    ) -> GeoComResponse[
        tuple[float, float]
    ]:
        """
        RPC 29005, ``DNA_GetMeasResult``

        Gets the current staff reading in memory. A measurement has to be
        completed in advance.

        Parameters
        ----------
        wait : int, optional
            Time to wait for a measurement to complete [ms], by default 5000

        Returns
        -------
        GeoComResponse
            Params:
                - `float`: Staff reading.
                - `float`: Staff distance.

        """
        def filter(
            value: tuple[
                float,
                float,
                int,
                int,
                int,
                float,
                int,
                int
            ] | None
        ) -> tuple[float, float] | None:
            if value is None:
                return None

            return value[0], value[1]

        response = self._request(
            29005,
            [wait],
            (
                float,  # staff reading
                float,  # distance
                int,
                int,
                int,  # system time [ms] awake
                float,  # distance accuracy?
                int,
                int
            )
        )

        return response.map_params(filter)

    def switch_staffmode(
        self,
        inverted: bool
    ) -> GeoComResponse[None]:
        """
        RPC 29010, ``DNA_SetRodPos``

        Sets the levelling staff reading mode.

        Parameters
        ----------
        inverted : bool
            Upside down reading (inverted staff).

        Returns
        -------
        GeoComResponse

        """
        return self._request(
            29010,
            [inverted]
        )

    def get_staffmode_status(self) -> GeoComResponse[bool]:
        """
        RPC 29011, ``DNA_GetRodPos``

        Gets the current the levelling staff reading mode.

        Returns
        -------
        GeoComResponse
            Params:
                - `bool`: Upside down reading (inverted staff).

        """
        return self._request(
            29011,
            parsers=parsebool
        )

    def do_measurement(self) -> GeoComResponse[None]:
        """
        RPC 29036, ``DNA_StartMeasurement``

        Carries out a staff reading. The results are not returend, but
        retained in memory, and used by other commands.

        Returns
        -------
        GeoComResponse
        """
        return self._request(
            29036
        )

    def autofocus(self) -> GeoComResponse[None]:
        """
        RPC 29068, ``DNA_StartAutofocus``

        Executes a camera autofocus cycle.

        Returns
        -------
        GeoComResponse
        """
        return self._request(
            29068
        )

    def get_inclination_cross(self) -> GeoComResponse[Angle]:
        """
        RPC 29070, ``DNA_GetTiltX``

        Gets the current cross inclination.

        Returns
        -------
        GeoComResponse
            Params:
                - `Angle`: Cross inclination.

        """
        return self._request(
            29070,
            parsers=Angle.parse
        )

    def get_inclination_length(self) -> GeoComResponse[Angle]:
        """
        RPC 29104, ``DNA_GetTiltL``

        Gets the current length inclination.

        Returns
        -------
        GeoComResponse
            Params:
                - `Angle`: Length inclination.

        """
        return self._request(
            29104,
            parsers=Angle.parse
        )

    def get_compass_bearing(self) -> GeoComResponse[Angle]:
        """
        RPC 29072, ``DNA_GetCompassData``

        Gets the current digital magnetic compass bearing.

        Returns
        -------
        GeoComResponse
            Params:
                - `Angle`: Compass bearing.

        """
        return self._request(
            29072,
            parsers=Angle.parse
        )

    def switch_curvature_correction(
        self,
        enabled: bool
    ) -> GeoComResponse[None]:
        """
        RPC 29107, ``DNA_SwitchEarthCurvature``

        Enables or disables the Earth curvature correction.

        Parameters
        ----------
        enabled : bool
            Enable curvature correction.

        Returns
        -------
        GeoComResponse

        """
        return self._request(
            29107,
            [enabled]
        )

    def get_curvature_correction_status(
        self
    ) -> GeoComResponse[bool]:
        """
        RPC 29108, ``DNA_GetEarthCurvatureStatus``

        Gets the current status of the Earth curvature correction.

        Returns
        -------
        GeoComResponse
            Params:
                - `bool`: Curvature correction is enabled.

        """
        return self._request(
            29108,
            parsers=parsebool
        )

    def get_job_number(self) -> GeoComResponse[int]:
        """
        RPC 29109, ``DNA_GetJobNumber``

        Gets the number of stored jobs and code lists.

        Returns
        -------
        GeoComResponse
            Params:
                - `int`: Number of jobs and code lists.

        """
        return self._request(
            29109,
            parsers=int
        )

    def wake_up(self) -> GeoComResponse[None]:
        """
        RPC 29110, ``DNA_WakeUpInstrument``

        Wake up the instrument from stadby mode.

        Returns
        -------
        GeoComResponse

        """
        return self._request(29110)

    def set_staff_type(
        self,
        staff: StaffType | str
    ) -> GeoComResponse[None]:
        """
        RPC 29127, ``DNA_SetStaffLength``

        Sets the levelling staff length

        Returns
        -------
        GeoComResponse

        """
        _staff = toenum(StaffType, staff)
        return self._request(
            29127,
            [_staff.value]
        )

    def get_staff_type(self) -> GeoComResponse[StaffType]:
        """
        RPC 29126, ``DNA_GetStaffLength``

        Gets the currently set levelling staff length.

        Returns
        -------
        GeoComResponse
            Params:
                - `StaffType`: Staff length type.

        """
        return self._request(
            29126,
            parsers=enumparser(StaffType)
        )
