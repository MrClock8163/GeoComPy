"""
Description
===========

Module: ``geocompy.tps1200p.com``

Definitions for the TPS1200+ Communication subsystem.

Types
-----

- ``TPS1200PCOM``

"""
from __future__ import annotations

from typing import Never, Any
from typing_extensions import deprecated

from ..tps1100.com import TPS1100COM


class TPS1200PCOM(TPS1100COM):
    """
    Communication subsystem of the TPS1200+ GeoCom protocol.

    This subsystem contains functions relevant to the communication
    with the instrument.

    """

    @deprecated("This command was removed for TPS1200 instruments")
    def set_send_delay(
        self,
        *args: Any,
        **kwargs: Any
    ) -> Never:
        """
        RPC 109, ``COM_SetSendDelay``

        .. versionremoved:: GeoCom-TPS1200

        Raises
        ------
        AttributeError
        """
        raise AttributeError()

    @deprecated("This command was removed for TPS1200 instruments")
    def switch_signoff(
        self,
        *args: Any,
        **kwargs: Any
    ) -> Never:
        """
        RPC 115, ``COM_EnableSignOff``

        .. versionremoved:: GeoCom-TPS1200

        Raises
        ------
        AttributeError
        """
        raise AttributeError()
