"""
``geocompy.vivatps.tmc``
=========================

Definitions for the VivaTPS Theodolite measurement and calculation
subsystem.

Types
-----

- ``VivaTPSTMC``

"""
from __future__ import annotations

from ..tps1200p.tmc import TPS1200PTMC


class VivaTPSTMC(TPS1200PTMC):
    """
    Theodolite measurement and calculation subsystem of the VivaTPS
    GeoCom protocol.

    This subsystem is the central module of measurement, calculation and
    geodetic control.

    The module handles:
        - measurement functions
        - measurement control functions
        - data setup functions
        - information functions
        - configuration functions

    Possible return codes:
        System
            General use codes.
        Informative/Warning
            Function terminated with success, but some restrictions may
            apply (e.g.: angle measurement succeded, distance measurement
            failed).
        Error
            Non-successful function termination."
    """
