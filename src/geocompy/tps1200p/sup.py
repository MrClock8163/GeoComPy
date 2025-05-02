"""
Description
===========

Module: ``geocompy.tps1200p.sup``

Definitions for the TPS1200+ Supervisor subsystem.

Types
-----

- ``TPS1200PSUP``

"""
from __future__ import annotations

from typing import Never
from typing_extensions import deprecated

from ..tps1100.sup import TPS1100SUP


class TPS1200PSUP(TPS1100SUP):
    """
    Supervisor subsystem of the TPS1200+ GeoCom protocol.

    This subsystem controls the continuous operation of the system, and it
    allows to automatically display status information.

    """

    @deprecated("This command was removed for TPS1200 instruments")
    def switch_low_temperature_control(
        self,
        *args
    ) -> Never:
        """
        RPC 14003, ``SUP_SwitchLowTempControl``

        .. versionremoved:: GeoCom-TPS1200

        Raises
        ------
        AttributeError
        """
        raise AttributeError()
