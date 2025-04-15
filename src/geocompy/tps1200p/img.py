"""
``geocompy.tps1200p.img``
=========================

Definitions for the TPS1200+ Imaging subsystem.

Types
-----

- ``TPS1200PIMG``

"""
from __future__ import annotations

from enum import Enum, Flag

from .. import (
    GeoComSubsystem,
    GeoComResponse
)
from ..data import toenum


class TPS1200PIMG(GeoComSubsystem):
    """
    Imaging subsystem of the TPS1200+ GeoCom protocol.

    This subsystem provides access to the telescoping camera functions
    for instruments that possess such functionality.

    """
    class MEMTYPE(Enum):
        INTERNAL = 0
        PCCARD = 1

    class SUBFUNC(Flag):
        TESTIMG = 1  # : Test image.
        AUTOEXPTIME = 2  # : Automatic exposure time.
        SS2 = 4  # : x2 subsampling
        SS4 = 8  # : x4 subsampling

    def get_tcc_config(
        self,
        memtype: MEMTYPE | str = MEMTYPE.PCCARD
    ) -> GeoComResponse:
        """
        RPC 23400, ``IMG_GetTccConfig``

        Gets the current telescopic camera settings on the specified
        memory device.

        Parameters
        ----------
        memtype : MEMTYPE | str, optional
            Memory device, by default PCCARD

        Returns
        -------
        GeoComResponse
            - Params:
                - **imgnumber** (`int`): Current image number.
                - **quality** (`int`): JPEG compression quality [0; 100]%
                - **subfunc** (`SUBFUNC`): Current function combination.
                - **prefix** (`str`): File name prefix.
            - Error codes:
                - ``FATAL``: CF card is not available, or config file does
                  not exist.
                - ``IVVERSION``: Config file version differs from system
                  software.
                - ``NA``: Imaging license not found.

        See Also
        --------
        set_tcc_config

        """
        _memtype = toenum(self.MEMTYPE, memtype)
        return self._request(
            23400,
            [_memtype.value],
            parsers={
                "imgnumber": int,
                "quality": int,
                "subfunc": lambda x: self.SUBFUNC(int(x)),
                "prefix": str
            }
        )

    def set_tcc_config(
        self,
        imgnumber: int,
        quality: int,
        subfunc: SUBFUNC | int,
        memtype: MEMTYPE | str = MEMTYPE.PCCARD,
    ) -> GeoComResponse:
        """
        RPC 23401, ``IMG_SetTccConfig``

        Sets the telescopic camera settings on the specified memory device.

        Parameters
        ----------
        imgnumber : int
            Image number.
        quality : int
            JPEG compression quality [0; 100]%.
        subfunc : SUBFUNC | int
            Subfunction combination.
        memtype : MEMTYPE | str, optional
            Memory device, by default PCCARD

        Returns
        -------
        GeoComResponse
            - Error codes:
                - ``FATAL``: CF card is not available or full, or any
                  parameter is out of valid range.
                - ``NA``: Imaging license not found.

        See Also
        --------
        get_tcc_config
        take_tcc_img

        """
        _memtype = toenum(self.MEMTYPE, memtype)
        if isinstance(subfunc, self.SUBFUNC):
            subfunc = subfunc.value
        return self._request(
            23401,
            [_memtype.value, imgnumber, quality, subfunc]
        )

    def take_tcc_img(
        self,
        memtype: MEMTYPE | str = MEMTYPE.PCCARD
    ) -> GeoComResponse:
        """
        RPC 23401, ``IMG_SetTccConfig``

        Takes image with the telescopic camera, on the specified memory
        device.

        Parameters
        ----------
        memtype : MEMTYPE | str, optional
            Memory device, by default PCCARD

        Returns
        -------
        GeoComResponse
            - Error codes:
                - ``IVRESULT``: Not supported by telescope firmware.
                - ``FATAL``: CF card is not available or is full.
                - ``NA``: Imaging license not found.

        See Also
        --------
        get_tcc_config
        set_tcc_config

        """
        _memtype = toenum(self.MEMTYPE, memtype)
        return self._request(
            23402,
            [_memtype.value],
            {
                "imgnumber": int
            }
        )
