"""
``geocompy.tps1200p.ftr``
=========================

Definitions for the TPS1200+ File transfer subsystem.

Types
-----

- ``TPS1200PFTR``

"""
from __future__ import annotations

from enum import Enum
from datetime import datetime

from .. import (
    GeoComSubsystem,
    GeoComResponse
)
from ..data import (
    Byte,
    parsestr,
    toenum
)


class TPS1200PFTR(GeoComSubsystem):
    """
    File transfer subsystem of the TPS1200+ GeoCom protocol.

    This subsystem provides access to the internal file system of the
    instrument, and provides methods to list or download files.

    """
    class DEVICETYPE(Enum):
        INTERNAL = 0
        PCPARD = 1

    class FILETYPE(Enum):
        UNKNOWN = 0  # ?
        IMAGE = 170

    def setup_list(
        self,
        device: DEVICETYPE | str = DEVICETYPE.PCPARD,
        filetype: FILETYPE | str = FILETYPE.UNKNOWN,
        path: str = ""
    ) -> GeoComResponse:
        """
        RPC 23306, ``FTR_SetupList``

        Prepares file listing of the specified file type, on the selected
        memory device.

        Parameters
        ----------
        device : DEVICETYPE | str, optional
            Memory device, by default PCPARD
        filetype : FILETYPE | str, optional
            File type, by default UNKNOWN
        path : str, optional
            Search path, by default ""

        Returns
        -------
        GeoComResponse
            - Error codes:
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
        _device = toenum(self.DEVICETYPE, device)
        _filetype = toenum(self.FILETYPE, filetype)
        return self._request(
            23306,
            [_device.value, _filetype.value, path]
        )

    def list(
        self,
        next: bool = False
    ) -> GeoComResponse:
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
            - Params:
                - **last** (`bool`): If file is last in listing.
                - **filename** (`str`): Name of the file.
                - **size** (`int`): File size [byte].
                - **modified** (`datetime` | None): Date and time of last
                  modification.
            - Error codes:
                - ``FTR_MISSINGSETUP``: No active listing setup.
                - ``FTR_INVALIDINPUT``: First item is missing, or last
                  call was already the last.

        See Also
        --------
        setup_list
        abort_list

        """
        response = self._request(
            23307,
            [next],
            {
                "last": bool,
                "filename": parsestr,
                "size": int,
                "hour": Byte.parse,
                "minute": Byte.parse,
                "second": Byte.parse,
                "centisec": Byte.parse,
                "day": Byte.parse,
                "month": Byte.parse,
                "year": Byte.parse
            }
        )
        time: datetime | None = None
        if (
            response.comcode
            and response.rpccode
            and response.params["filename"] != ""
        ):
            time = datetime(
                int(response.params["year"]) + 2000,
                int(response.params["month"]),
                int(response.params["day"]),
                int(response.params["hour"]),
                int(response.params["minute"]),
                int(response.params["second"]),
                int(response.params["centisec"]) * 10000
            )
        response.params = {
            "last": response.params["last"],
            "filename": response.params["filename"],
            "size": response.params["size"],
            "modified": time
        }
        return response

    def abort_list(self) -> GeoComResponse:
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
        device: DEVICETYPE | str = DEVICETYPE.PCPARD,
        filetype: FILETYPE | str = FILETYPE.UNKNOWN,
    ) -> GeoComResponse:
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
        download
        abort_download

        """
        _device = toenum(self.DEVICETYPE, device)
        _filetype = toenum(self.FILETYPE, filetype)
        return self._request(
            23303,
            [_device.value, _filetype.value, filename, blocksize],
            {
                "blockcount": int
            }
        )

    def download(
        self,
        block: int
    ) -> GeoComResponse:
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
            - Params:
                - **value** (`str`): Data block as serialized bytes.
                - **length** (`int`): Length of data block.
            - Error codes:
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
            {
                "value": parsestr,
                "length": int
            }
        )

    def abort_download(self) -> GeoComResponse:
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
        device: DEVICETYPE | str = DEVICETYPE.PCPARD,
        filetype: FILETYPE | str = FILETYPE.UNKNOWN
    ) -> GeoComResponse:
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
        device : DEVICETYPE | str, optional
            Memory device, by default PCPARD
        filetype : FILETYPE | str, optional
            File type, by default UNKNOWN

        Returns
        -------
        GeoComResponse
            - Params:
                - **deleted** (`int`): Number of files deleted.
            - Error codes:
                - ``IVPARAM``: Memory device unavailable, or cannot find
                  file path.

        See Also
        --------
        list

        """
        _device = toenum(self.DEVICETYPE, device)
        _filetype = toenum(self.FILETYPE, filetype)
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
            {
                "deleted": int
            }
        )
