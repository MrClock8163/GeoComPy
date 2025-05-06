"""
Description
===========

Module: ``geocompy.tps1200p.aus``

Definitions for the TPS1200+ Alt user subsystem.

Types
-----

- ``TPS1200PAUS``

"""
from __future__ import annotations

from typing import Never, Any
from typing_extensions import deprecated

from ..tps1100.aus import TPS1100AUS


class TPS1200PAUS(TPS1100AUS):
    """
    Alt user subsystem of the TPS1200+ GeoCom protocol.

    This subsystem can be used to set and query the ATR and LOCK
    automation modes.

    """

    @deprecated("This command was removed for TPS1200 instruments")
    def get_rcs_search_status(self) -> Never:
        """
        RPC 18010, ``AUS_GetRcsSearchSwitch``

        .. versionremoved:: GeoCom-TPS1200

        Raises
        ------
        AttributeError
        """
        raise AttributeError()

    @deprecated("This command was removed for TPS1200 instruments")
    def switch_rcs_search(
        self,
        *args: Any,
        **kwargs: Any
    ) -> Never:
        """
        RPC 18009, ``AUS_SwitchRcsSearch``

        .. versionremoved:: GeoCom-TPS1200

        Raises
        ------
        AttributeError
        """
        raise AttributeError()
