"""
Description
===========

Module: ``geocompy.tps1200p.ftr``

Definitions for the TPS1200+ File transfer subsystem.

Types
-----

- ``TPS1200PFTR``

"""
from __future__ import annotations

from datetime import datetime

from ..data import (
    Byte,
    parsestr,
    parsebool,
    toenum
)
from ..data_geocom import (
    Device,
    File
)
from ..protocols import (
    GeoComSubsystem,
    GeoComResponse
)


class TPS1200PFTR(GeoComSubsystem):
    """
    File transfer subsystem of the TPS1200+ GeoCom protocol.

    This subsystem provides access to the internal file system of the
    instrument, and provides methods to list or download files.

    """

    def setup_list(
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
                - **modified** (`datetime` | None): Date and time of last
                  modification.
            Error codes:
                - ``FTR_MISSINGSETUP``: No active listing setup.
                - ``FTR_INVALIDINPUT``: First item is missing, or last
                  call was already the last.

        See Also
        --------
        setup_list
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
                    int(params[3]) + 2000,
                    int(params[4]),
                    int(params[5]),
                    int(params[6]),
                    int(params[7]),
                    int(params[8]) * 10000
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
        setup_list
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
