"""
Description
===========

Module: ``geocompy.tps1100.mot``

Definitions for the TPS1100 Motorization subsystem.

Types
-----

- ``TPS1100MOT``

"""
from __future__ import annotations

from ..tps1000.mot import TPS1000MOT


class TPS1100MOT(TPS1000MOT):
    """
    Motorization subsystem of the TPS1100 GeoCom protocol.

    This subsystem provides access to motoriztaion parameters and control.

    """
