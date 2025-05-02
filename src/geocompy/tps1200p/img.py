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
    enumparser
)
from ..data_geocom import (
    CameraFunctions,
    Device
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

    def get_telescopic_configuration(
        self,
        at: Device | str = Device.CFCARD
    ) -> GeoComResponse[tuple[int, int, CameraFunctions, str]]:
        """
        RPC 23400, ``IMG_GetTccConfig``

        Gets the current telescopic camera settings on the specified
        memory device.

        Parameters
        ----------
        at : Device | str, optional
            Memory device, by default CFCARD

        Returns
        -------
        GeoComResponse
            Params:
                - `int`: Current image number.
                - `int`: JPEG compression quality [0; 100]%
                - `CameraFunctions`: Current camera function combination.
                - `str`: File name prefix.
            Error codes:
                - ``FATAL``: CF card is not available, or config file does
                  not exist.
                - ``IVVERSION``: Config file version differs from system
                  software.
                - ``NA``: Imaging license not found.

        See Also
        --------
        set_telescopic_configuration

        """
        _device = toenum(Device, at)
        return self._request(
            23400,
            [_device.value],
            parsers=(
                int,
                int,
                enumparser(CameraFunctions),
                str
            )
        )

    def set_telescopic_configuration(
        self,
        imgnumber: int,
        quality: int,
        functions: CameraFunctions | int,
        saveto: Device | str = Device.CFCARD,
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
        functions : CameraFunctions | int
            Camera function combination.
        saveto : Device | str, optional
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
        get_telescopic_configuration
        take_telescopic_image

        """
        _device = toenum(Device, saveto)
        if isinstance(functions, CameraFunctions):
            functions = functions.value
        return self._request(
            23401,
            [_device.value, imgnumber, quality, functions]
        )

    def take_telescopic_image(
        self,
        device: Device | str = Device.CFCARD
    ) -> GeoComResponse[int]:
        """
        RPC 23401, ``IMG_SetTccConfig``

        Takes image with the telescopic camera, on the specified memory
        device.

        Parameters
        ----------
        device : Device | str, optional
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
        get_telescopic_configuration
        set_telescopic_configuration

        """
        _device = toenum(Device, device)
        return self._request(
            23402,
            [_device.value],
            int
        )
