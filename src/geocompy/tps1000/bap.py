"""
Description
===========

Module: ``geocompy.tps1000.bap``

Definitions for the TPS1000 Basic applications subsystem.

Types
-----

- ``TPS1000BAP``

"""
from __future__ import annotations

from ..data import (
    Angle,
    toenum,
    enumparser
)
from ..data_geocom import Program
from ..protocols import (
    GeoComSubsystem,
    GeoComResponse
)


class TPS1000BAP(GeoComSubsystem):
    """
    Basic applications subsystem of the TPS1000 GeoCom protocol.

    This subsystem contains high-level functions that are also accessible
    through the user interface. The commands combine several subcommands
    for ease of operation.

    """

    def get_last_displayed_error(self) -> GeoComResponse[tuple[int, int]]:
        """
        RPC 17003, ``BAP_GetLastDisplayedError``

        Retrieves the number of the last displayed system error.

        Returns
        -------
        GeoComResponse
            Params:
                - `int`: Last error, warning or info number.
                - `int`: Corresponding GSI error number.
            Error codes:
                - ``IVRESULT``: No error was displayed since last call.

        Note
        ----
        The error code will be reset once command is executed. A repeated
        call will be unsuccessful.
        """
        return self._request(
            17003,
            parsers=(
                int,
                int
            )
        )

    def meas_distance_angle(
        self,
        mode: Program | str = Program.DISTANCE
    ) -> GeoComResponse[tuple[Angle, Angle, float, Program]]:
        """
        RPC 17017, ``BAP_MeasDistanceAngle``

        Take an angle and distance measuremnt depending on the distance
        mode.

        Parameters
        ----------
        mode : Program | str, optional
            Distance measurement mode to use, by default
            Program.DISTANCE

        Returns
        -------
        GeoComResponse
            Params:
                - `Angle`: Horizontal angle.
                - `Angle`: Vertical angle.
                - `float`: Slope distance.
                - `MEASUREPRG`: Actual distance mode.
            Info codes:
                - ``TMC_ACCURACY_GUARANTEE``: Accuracy cannot be guaranteed.
                - ``TMC_ANGLE_ACCURACY_GUARANTEE``: Only angle measurement
                  valid, accuracy cannot be guaranteed.
            Warning codes:
                - ``TMC_ANGLE_NO_FULL_CORRECTION``: Only angle measurement
                  valid, accuracy cannot be guaranteed.
                - ``TMC_ANGLE_OK``: Only angle measurement valid.
                - ``TMC_NO_FULL_CORRECTION``: Measurement without full
                  correction.
            Error codes:
                - ``AUT_ANGLE_ERROR``: Angle measurement error.
                - ``AUT_BAD_ENVIRONMENT``: Bad environmental conditions.
                - ``AUT_CALACC``: ATR calibration failed.
                - ``AUT_DETECTOR_ERROR``: Error in target acquisition.
                - ``AUT_DETENT_ERROR``: Positioning not possible.
                - ``AUT_DEV_ERROR``: Error in angle deviation calculation.
                - ``AUT_INCACC``: Position not exactly reached.
                - ``AUT_MOTOR_ERROR``: Motorization error.
                - ``AUT_MULTIPLE_TARGETS``: Multiple targets detected.
                - ``AUT_NO_TARGET``: No target detected.
                - ``AUT_TIMEOUT``: Position not reached.
                - ``BAP_CHANGE_ALL_TO_DIST``: Prism not detected, changed
                  command to ALL.
                - ``TMC_ANGLE_ERROR``: No valid angle measurement.
                - ``TMC_BUSY``: TMC submodule already in use by another
                  subsystem, command not processed.
                - ``TMC_DIST_ERROR``: An error occurred during distance
                  measurement.
                - ``TMC_DIST_PPM``: Wrong PPM setting.
                - ``TMC_SIGNAL_ERROR``: No signal on EDM (only in signal
                  mode).
                - ``ABORT``: Measurement aborted.
                - ``COM_TIMEDOUT``: Communication timeout.
                - ``IVPARAM``: Invalid distance mode.
                - ``SHUT_DOWN``: System stopped.

        """
        _mode = toenum(Program, mode)
        return self._request(
            17017,
            [_mode.value],
            (
                Angle.parse,
                Angle.parse,
                float,
                enumparser(Program)
            )
        )
