"""
Description
===========

Module: ``geocompy.vivatps.ftr``

Definitions for the VivaTPS File transfer subsystem.

Types
-----

- ``VivaTPSFTR``

"""
from __future__ import annotations

from enum import Enum
from datetime import datetime

from ..data import (
    Byte,
    parsestr,
    toenum
)
from ..protocols import GeoComResponse
from ..tps1200p.ftr import TPS1200PFTR


class VivaTPSFTR(TPS1200PFTR):
    """
    File transfer subsystem of the VivaTPS GeoCom protocol.

    This subsystem provides access to the internal file system of the
    instrument, and provides methods to list or download files.

    """
    class DEVICETYPE(Enum):
        INTERNAL = 0
        PCPARD = 1
        SDCARD = 4
        USB = 5
        RAM = 6

    class FILETYPE(Enum):
        POINTRELATEDDB = 103
        IMAGES = 170
        IMAGES_OVC_JPG = 171
        IMAGES_OVC_BMP = 172
        IMAGES_OAV_JPG = 173
        IMAGES_OAV_BMP = 174
        SCANS = 175,
        UNKNOWN = 200
        LAST = 201

    def delete_dir(
        self,
        dirname: str,
        time: datetime | None = None,
        device: DEVICETYPE | str = DEVICETYPE.INTERNAL
    ) -> GeoComResponse[int]:
        """
        RPC 23315, ``FTR_DeleteDir``

        Deletes one or more directories. Wildcards can be used to delete
        multiple items. If a date is given, only directories older than
        that date are deleted.

        Parameters
        ----------
        dirname : str
            Directory name.
        time : datetime | None, optional
            Deletion limit date, by default None
        device : DEVICETYPE | str, optional
            Memory device, by default PCPARD

        Returns
        -------
        GeoComResponse
            - Params:
                - **deleted** (`int`): Number of directories deleted.
            - Error codes:
                - ``IVPARAM``: Memory device unavailable, or cannot find
                  file path.

        See Also
        --------
        list

        """
        _device = toenum(self.DEVICETYPE, device)
        _filetype = self.FILETYPE.POINTRELATEDDB

        if time is None:
            params = [
                _device.value, _filetype.value,
                Byte(0), Byte(0), Byte(0),
                dirname
            ]
        else:
            params = [
                _device.value, _filetype.value,
                Byte(time.day), Byte(time.month), Byte(time.year - 2000),
                dirname
            ]
        return self._request(
            23315,
            params,
            int
        )

    def setup_download_large(
        self,
        filename: str,
        blocksize: int,
        device: DEVICETYPE | str = DEVICETYPE.INTERNAL,
        filetype: FILETYPE | str = FILETYPE.UNKNOWN
    ) -> GeoComResponse[int]:
        """
        RPC 23313, ``FTR_SetupDownloadLarge``

        Prepares download of the specified large file of the specified
        type, on the selected memory device.

        Parameters
        ----------
        filename : str
            File name (or full path if type is unknown).
        blocksize : int
            Download data block size.
        device : DEVICETYPE | str, optional
            Memory device, by default PCPARD
        filetype : FILETYPE | str, optional
            File type, by default UNKNOWN

        Returns
        -------
        GeoComResponse
            - Params:
                - **blockcount** (`int`): Number of download blocks needed.
            - Error codes:
                - ``IVPARAM``: Memory device unavailable, or cannot find
                  file path.
                - ``NOTOK``: Setup already exists, previous setup was not
                  aborted.
                - ``FTR_INVALIDINPUT``: Block size too big.
                - ``FTR_FILEACCESS``: File access error.

        See Also
        --------
        download_xl
        abort_download

        """
        _device = toenum(self.DEVICETYPE, device)
        _filetype = toenum(self.FILETYPE, filetype)
        return self._request(
            23313,
            [_device.value, _filetype.value, filename, blocksize],
            int
        )

    def download_xl(
        self,
        block: int
    ) -> GeoComResponse[tuple[str, int]]:
        """
        RPC 23314, ``FTR_DownloadXL``

        Downloads a single data block of a previously defined large file
        download sequence.

        Parameters
        ----------
        block : int
            Number of data block to download.

        Returns
        -------
        GeoComResponse
            - Params:
                - **value** (`str`): Data block as serialized bytes.
                - **length** (`int`): Length of data block.
            - Error codes:
                - ``FTR_MISSINGSETUP``: No active download setup.
                - ``FTR_INVALIDINPUT``: First block is missing.
                - ``FTR_FILEACCESS``: File access error.

        See Also
        --------
        setup_download_large
        abort_download

        """
        return self._request(
            23314,
            [block],
            (
                parsestr,
                int
            )
        )
