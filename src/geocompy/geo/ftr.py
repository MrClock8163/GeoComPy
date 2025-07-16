"""
Description
===========

Module: ``geocompy.geo.ftr``

Definitions for the GeoCom File transfer subsystem.

Types
-----

- ``GeoComPFTR``

"""
from __future__ import annotations

from datetime import datetime

from ..data import (
    Byte,
    parsestr,
    parsebool,
    toenum
)
from .gcdata import (
    Device,
    File
)
from .gctypes import (
    GeoComSubsystem,
    GeoComResponse
)


class GeoComFTR(GeoComSubsystem):
    """
    File transfer subsystem of the GeoCom protocol.

    This subsystem provides access to the internal file system of the
    instrument, and provides methods to list or download files.

    .. versionadded:: GeoCom-TPS1200
    """

    def setup_listing(
        self,
        device: Device | str = Device.CFCARD,
        filetype: File | str = File.UNKNOWN,
        path: str = ""
    ) -> GeoComResponse[None]:
        """
        RPC 23306, ``FTR_SetupList``

        Prepares file listing of the specified file type, on the selected
        memory device.

        Parameters
        ----------
        device : Device | str, optional
            Memory device, by default CFCARD
        filetype : File | str, optional
            File type, by default UNKNOWN
        path : str, optional
            Search path, by default ""

        Returns
        -------
        GeoComResponse
            Error codes:
                - ``IVPARAM``: Memory device unavailable, or cannot find
                  search path.
                - ``NOTOK``: Setup already exists, previous setup was not
                  aborted.
                - ``FTR_FILEACCESS``: File access error.

        See Also
        --------
        list
        abort_list

        """
        _device = toenum(Device, device)
        _filetype = toenum(File, filetype)
        return self._request(
            23306,
            [_device.value, _filetype.value, path]
        )

    def list(
        self,
        next: bool = False
    ) -> GeoComResponse[tuple[bool, str, int, datetime | None]]:
        """
        RPC 23307, ``FTR_List``

        Gets a single file entry according to the predefined listing
        setup.

        Parameters
        ----------
        next : bool, optional
            Get the next item, after a previous call (get first item
            otherwise), by default False

        Returns
        -------
        GeoComResponse
            Params:
                - `bool`: If file is last in listing.
                - `str`: Name of the file.
                - `int`: File size [byte].
                - `datetime` | None: Date and time of last modification.
            Error codes:
                - ``FTR_MISSINGSETUP``: No active listing setup.
                - ``FTR_INVALIDINPUT``: First item is missing, or last
                  call was already the last.

        See Also
        --------
        setup_listing
        abort_list

        """
        def transform(
            params: tuple[
                bool, str, int,
                Byte, Byte, Byte, Byte, Byte, Byte, Byte
            ] | None
        ) -> tuple[bool, str, int, datetime | None] | None:
            if params is None:
                return None

            return (
                params[0],
                params[1],
                params[2],
                datetime(
                    int(params[9]) + 2000,
                    int(params[8]),
                    int(params[7]),
                    int(params[3]),
                    int(params[4]),
                    int(params[5]),
                    int(params[6]) * 10000
                ) if params[1] != "" else None
            )

        response = self._request(
            23307,
            [next],
            (
                parsebool,
                parsestr,
                int,
                Byte.parse,
                Byte.parse,
                Byte.parse,
                Byte.parse,
                Byte.parse,
                Byte.parse,
                Byte.parse
            )
        )
        return response.map_params(transform)

    def abort_list(self) -> GeoComResponse[None]:
        """
        RPC 23308, ``FTR_AbortList``

        Aborts current file listing setup.

        Returns
        -------
        GeoComResponse

        See Also
        --------
        setup_listing
        list

        """
        return self._request(23308)

    def setup_download(
        self,
        filename: str,
        blocksize: int,
        device: Device | str = Device.CFCARD,
        filetype: File | str = File.UNKNOWN,
    ) -> GeoComResponse[int]:
        """
        RPC 23303, ``FTR_SetupDownload``

        Prepares download of the specified file of the specified type, on
        the selected memory device.

        Parameters
        ----------
        filename : str
            File name (or full path if type is unknown).
        blocksize : int
            Download data block size.
        device : Device | str, optional
            Memory device, by default CFCARD
        filetype : File | str, optional
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
        download
        abort_download

        """
        _device = toenum(Device, device)
        _filetype = toenum(File, filetype)
        return self._request(
            23303,
            [_device.value, _filetype.value, filename, blocksize],
            int
        )

    def download(
        self,
        block: int
    ) -> GeoComResponse[tuple[str, int]]:
        """
        RPC 23304, ``FTR_Download``

        Downloads a single data block of a previously defined download
        sequence.

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
        setup_download
        abort_download

        """
        return self._request(
            23304,
            [block],
            (
                parsestr,
                int
            )
        )

    def abort_download(self) -> GeoComResponse[None]:
        """
        RPC 23305, ``FTR_AbortDownload``

        Aborts current file download setup.

        Returns
        -------
        GeoComResponse

        See Also
        --------
        setup_download
        download

        """
        return self._request(23305)

    def delete(
        self,
        filename: str,
        time: datetime | None = None,
        device: Device | str = Device.CFCARD,
        filetype: File | str = File.UNKNOWN
    ) -> GeoComResponse[int]:
        """
        RPC 23309, ``FTR_Delete``

        Deletes one or more files. Wildcards can be used to delete
        multiple items. If a date is given, only files older than that
        date are deleted.

        Parameters
        ----------
        filename : str
            File name (or full path if type is unknown).
        time : datetime | None, optional
            Deletion limit date, by default None
        device : Device | str, optional
            Memory device, by default CFCARD
        filetype : File | str, optional
            File type, by default UNKNOWN

        Returns
        -------
        GeoComResponse
            Params:
                - `int`: Number of files deleted.
            Error codes:
                - ``IVPARAM``: Memory device unavailable, or cannot find
                  file path.

        See Also
        --------
        list

        """
        _device = toenum(Device, device)
        _filetype = toenum(File, filetype)
        if time is None:
            params = [
                _device.value, _filetype.value,
                Byte(0), Byte(0), Byte(0),
                filename
            ]
        else:
            params = [
                _device.value, _filetype.value,
                Byte(time.day), Byte(time.month), Byte(time.year - 2000),
                filename
            ]
        return self._request(
            23309,
            params,
            int
        )

    def delete_directory(
        self,
        dirname: str,
        time: datetime | None = None,
        device: Device | str = Device.INTERNAL
    ) -> GeoComResponse[int]:
        """
        RPC 23315, ``FTR_DeleteDir``

        .. versionadded:: GeoCom-VivaTPS

        Deletes one or more directories. Wildcards can be used to delete
        multiple items. If a date is given, only directories older than
        that date are deleted.

        Parameters
        ----------
        dirname : str
            Directory name.
        time : datetime | None, optional
            Deletion limit date, by default None
        device : Device | str, optional
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
        _device = toenum(Device, device)
        _filetype = File.DATABASE

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

    def setup_large_download(
        self,
        filename: str,
        blocksize: int,
        device: Device | str = Device.INTERNAL,
        filetype: File | str = File.UNKNOWN
    ) -> GeoComResponse[int]:
        """
        RPC 23313, ``FTR_SetupDownloadLarge``

        .. versionadded:: GeoCom-VivaTPS

        Prepares download of the specified large file of the specified
        type, on the selected memory device.

        Parameters
        ----------
        filename : str
            File name (or full path if type is unknown).
        blocksize : int
            Download data block size.
        device : Device | str, optional
            Memory device, by default INTERNAL
        filetype : File | str, optional
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
        download_large
        abort_download

        """
        _device = toenum(Device, device)
        _filetype = toenum(File, filetype)
        return self._request(
            23313,
            [_device.value, _filetype.value, filename, blocksize],
            int
        )

    def download_large(
        self,
        block: int
    ) -> GeoComResponse[tuple[str, int]]:
        """
        RPC 23314, ``FTR_DownloadXL``

        .. versionadded:: GeoCom-VivaTPS

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
        setup_large_download
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
