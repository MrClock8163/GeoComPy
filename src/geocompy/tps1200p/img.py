"""
Description
===========

Module: ``geocompy.tps1200p.img``

Definitions for the TPS1200+ Imaging subsystem.

Types
-----

- ``TPS1200PIMG``

"""
from __future__ import annotations

from ..data import (
    toenum,
    enumparser,
    DEVICE,
    CAMERAFUNCTIONS
)
from ..protocols import (
    GeoComSubsystem,
    GeoComResponse
)


class TPS1200PIMG(GeoComSubsystem):
    """
    Imaging subsystem of the TPS1200+ GeoCom protocol.

    This subsystem provides access to the telescoping camera functions
    for instruments that possess such functionality.

    """

    def get_tcc_config(
        self,
        at: DEVICE | str = DEVICE.CFCARD
    ) -> GeoComResponse[tuple[int, int, CAMERAFUNCTIONS, str]]:
        """
        RPC 23400, ``IMG_GetTccConfig``

        Gets the current telescopic camera settings on the specified
        memory device.

        Parameters
        ----------
        at : DEVICE | str, optional
            Memory device, by default CFCARD

        Returns
        -------
        GeoComResponse
            Params:
                - `int`: Current image number.
                - `int`: JPEG compression quality [0; 100]%
                - `CAMERAFUNCTIONS`: Current camera function combination.
                - `str`: File name prefix.
            Error codes:
                - ``FATAL``: CF card is not available, or config file does
                  not exist.
                - ``IVVERSION``: Config file version differs from system
                  software.
                - ``NA``: Imaging license not found.

        See Also
        --------
        set_tcc_config

        """
        _device = toenum(DEVICE, at)
        return self._request(
            23400,
            [_device.value],
            parsers=(
                int,
                int,
                enumparser(CAMERAFUNCTIONS),
                str
            )
        )

    def set_tcc_config(
        self,
        imgnumber: int,
        quality: int,
        functions: CAMERAFUNCTIONS | int,
        saveto: DEVICE | str = DEVICE.CFCARD,
    ) -> GeoComResponse[None]:
        """
        RPC 23401, ``IMG_SetTccConfig``

        Sets the telescopic camera settings on the specified memory device.

        Parameters
        ----------
        imgnumber : int
            Image number.
        quality : int
            JPEG compression quality [0; 100]%.
        functions : CAMERAFUNCTIONS | int
            Camera function combination.
        saveto : DEVICE | str, optional
            Memory device, by default CFCARD

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``FATAL``: CF card is not available or full, or any
                  parameter is out of valid range.
                - ``NA``: Imaging license not found.

        See Also
        --------
        get_tcc_config
        take_tcc_img

        """
        _device = toenum(DEVICE, saveto)
        if isinstance(functions, CAMERAFUNCTIONS):
            functions = functions.value
        return self._request(
            23401,
            [_device.value, imgnumber, quality, functions]
        )

    def take_tcc_img(
        self,
        device: DEVICE | str = DEVICE.CFCARD
    ) -> GeoComResponse[int]:
        """
        RPC 23401, ``IMG_SetTccConfig``

        Takes image with the telescopic camera, on the specified memory
        device.

        Parameters
        ----------
        device : DEVICE | str, optional
            Memory device, by default CFCARD

        Returns
        -------
        GeoComResponse
            Params:
                - `int`: Number of new image.
            Error codes:
                - ``IVRESULT``: Not supported by telescope firmware.
                - ``FATAL``: CF card is not available or is full.
                - ``NA``: Imaging license not found.

        See Also
        --------
        get_tcc_config
        set_tcc_config

        """
        _device = toenum(DEVICE, device)
        return self._request(
            23402,
            [_device.value],
            int
        )
