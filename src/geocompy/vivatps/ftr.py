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

from datetime import datetime

from ..data import (
    Byte,
    parsestr,
    toenum,
    DEVICE,
    FILE
)
from ..protocols import GeoComResponse
from ..tps1200p.ftr import TPS1200PFTR


class VivaTPSFTR(TPS1200PFTR):
    """
    File transfer subsystem of the VivaTPS GeoCom protocol.

    This subsystem provides access to the internal file system of the
    instrument, and provides methods to list or download files.

    """

    def delete_dir(
        self,
        dirname: str,
        time: datetime | None = None,
        device: DEVICE | str = DEVICE.INTERNAL
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
        device : DEVICE | str, optional
            Memory device, by default PCPARD

        Returns
        -------
        GeoComResponse
            Params:
                - `int`: Number of directories deleted.
            Error codes:
                - ``IVPARAM``: Memory device unavailable, or cannot find
                  file path.

        See Also
        --------
        list

        """
        _device = toenum(DEVICE, device)
        _filetype = FILE.DATABASE

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
        device: DEVICE | str = DEVICE.INTERNAL,
        filetype: FILE | str = FILE.UNKNOWN
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
        device : DEVICE | str, optional
            Memory device, by default INTERNAL
        filetype : FILE | str, optional
            File type, by default UNKNOWN

        Returns
        -------
        GeoComResponse
            Params:
                - `int`: Number of download blocks needed.
            Error codes:
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
        _device = toenum(DEVICE, device)
        _filetype = toenum(FILE, filetype)
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
            Params:
                - `str`: Data block as serialized bytes.
                - `int`: Length of data block.
            Error codes:
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
