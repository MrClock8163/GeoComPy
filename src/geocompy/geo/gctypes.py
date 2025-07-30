"""
Description
===========

Module: ``geocompy.geo.gctypes``

The GeoCom types module provides type definitions and general constants,
that are relevant to the GeoCom protocol.

Types
-----

- ``GeoComCode``
- ``GeoComResponse``
- ``GeoComType``
- ``GeoComSubsystem``
"""
from __future__ import annotations

from enum import IntEnum
from typing import TypeVar, Any, Generic, Callable, Iterable, overload
from abc import ABC, abstractmethod

from ..data import Angle, Byte


_T = TypeVar("_T")
_P = TypeVar("_P", bound=Any)


class GeoComCode(IntEnum):
    """
    GeoCom return codes from all subsystems and protocol versions.
    """

    def __bool__(self) -> bool:
        return self is type(self).OK

    OK = 0
    """Function successfully completed."""
    UNDEFINED = 1
    """Unknown error, result unspecified."""
    IVPARAM = 2
    """Invalid parameter detected. Result unspecified."""
    IVRESULT = 3
    """Invalid result."""
    FATAL = 4
    """Fatal error."""
    NOT_IMPL = 5
    """Not implemented yet."""
    TIME_OUT = 6
    """Function execution timed out. Result unspecified."""
    SET_INCOMPL = 7
    """Parameter setup for subsystem is incomplete."""
    ABORT = 8
    """Function execution has been aborted."""
    NOMEMORY = 9
    """Fatal error - not enough memory."""
    NOTINIT = 10
    """Fatal error - subsystem not initialised."""
    SHUT_DOWN = 12
    """Subsystem is down."""
    SYSBUSY = 13
    """System busy/already in use of another process. Cannot execute
    function."""
    HWFAILURE = 14
    """Fatal error - hardware failure."""
    ABORT_APPL = 15
    """Execution of application has been aborted (SHIFT-ESC)."""
    LOW_POWER = 16
    """Operation aborted - insufficient power supply level."""
    IVVERSION = 17
    """Invalid version of file, ..."""
    BATT_EMPTY = 18
    """Battery empty"""
    NO_EVENT = 20
    """no event pending."""
    OUT_OF_TEMP = 21
    """out of temperature range"""
    INSTRUMENT_TILT = 22
    """instrument tilting out of range"""
    COM_SETTING = 23
    """communication error"""
    NO_ACTION = 24
    """TYPE Input 'do no action'"""
    SLEEP_MODE = 25
    """Instr. run into the sleep mode"""
    NOTOK = 26
    """Function not successfully completed."""
    NA = 27
    """Not available."""
    OVERFLOW = 28
    """Overflow error."""
    STOPPED = 29
    """System or subsystem has been stopped."""

    AF_FAILED = 13864
    """AF failed ."""

    ANG_ERROR = 257
    """Angles and Inclinations not valid"""
    ANG_INCL_ERROR = 258
    """inclinations not valid"""
    ANG_BAD_ACC = 259
    """value accuracy not reached"""
    ANG_BAD_ANGLE_ACC = 260
    """angle-accuracy not reached"""
    ANG_BAD_INCLIN_ACC = 261
    """inclination accuracy not reached"""
    ANG_WRITE_PROTECTED = 266
    """no write access allowed"""
    ANG_OUT_OF_RANGE = 267
    """value out of range"""
    ANG_IR_OCCURED = 268
    """function aborted due to interrupt"""
    ANG_HZ_MOVED = 269
    """Hz moved during incline measurement"""
    ANG_OS_ERROR = 270
    """troubles with operation system"""
    ANG_DATA_ERROR = 271
    """overflow at parameter values"""
    ANG_PEAK_CNT_UFL = 272
    """too less peaks"""
    ANG_TIME_OUT = 273
    """reading timeout"""
    ANG_TOO_MANY_EXPOS = 274
    """too many exposures wanted"""
    ANG_PIX_CTRL_ERR = 275
    """picture height out of range"""
    ANG_MAX_POS_SKIP = 276
    """positive exposure dynamic overflow"""
    ANG_MAX_NEG_SKIP = 277
    """negative exposure dynamic overflow"""
    ANG_EXP_LIMIT = 278
    """exposure time overflow"""
    ANG_UNDER_EXPOSURE = 279
    """picture underexposured"""
    ANG_OVER_EXPOSURE = 280
    """picture overexposured"""
    ANG_TMANY_PEAKS = 300
    """too many peaks detected"""
    ANG_TLESS_PEAKS = 301
    """too less peaks detected"""
    ANG_PEAK_TOO_SLIM = 302
    """peak too slim"""
    ANG_PEAK_TOO_WIDE = 303
    """peak to wide"""
    ANG_BAD_PEAKDIFF = 304
    """bad peak difference"""
    ANG_UNDER_EXP_PICT = 305
    """too less peak amplitude"""
    ANG_PEAKS_INHOMOGEN = 306
    """inhomogen peak amplitudes"""
    ANG_NO_DECOD_POSS = 307
    """no peak decoding possible"""
    ANG_UNSTABLE_DECOD = 308
    """peak decoding not stable"""
    ANG_TLESS_FPEAKS = 309
    """Too less valid finepeaks."""
    ANG_INCL_OLD_PLANE = 316
    """Inclination plane out of time range."""
    ANG_INCL_NO_PLANE = 317
    """Inclination no plane available."""
    ANG_FAST_ANG_ERR = 326
    """Errors in 5kHz and or 2.5kHz angle."""
    ANG_FAST_ANG_ERR_5 = 327
    """Errors in 5kHz angle."""
    ANG_FAST_ANG_ERR_25 = 328
    """Errors in 2.5kHz angle."""
    ANG_TRANS_ERR = 329
    """LVDS transfer error detected."""
    ANG_TRANS_ERR_5 = 330
    """LVDS transfer error detected in 5kHz mode."""
    ANG_TRANS_ERR_25 = 331
    """LVDS transfer error detected in 2.5kHz mode."""

    ATA_NOT_READY = 512
    """ATR-System is not ready."""
    ATA_NO_RESULT = 513
    """Result isn't available yet."""
    ATA_SEVERAL_TARGETS = 514
    """Several Targets detected."""
    ATA_BIG_SPOT = 515
    """Spot is too big for analyse."""
    ATA_BACKGROUND = 516
    """Background is too bright."""
    ATA_NO_TARGETS = 517
    """No targets detected."""
    ATA_NOT_ACCURAT = 518
    """Accuracy worse than asked for."""
    ATA_SPOT_ON_EDGE = 519
    """Spot is on the edge of the sensing area."""
    ATA_BLOOMING = 522
    """Blooming or spot on edge detected."""
    ATA_NOT_BUSY = 523
    """ATR isn't in a continuous mode."""
    ATA_STRANGE_LIGHT = 524
    """Not the spot of the own target illuminator."""
    ATA_V24_FAIL = 525
    """Communication error to sensor (ATR)."""
    ATA_DECODE_ERROR = 526
    """Received Arguments cannot be decoded."""
    ATA_HZ_FAIL = 527
    """No Spot detected in Hz-direction."""
    ATA_V_FAIL = 528
    """No Spot detected in V-direction."""
    ATA_HZ_STRANGE_L = 529
    """Strange light in Hz-direction."""
    ATA_V_STRANGE_L = 530
    """Strange light in V-direction."""
    ATA_SLDR_TRANSFER_PENDING = 531
    """On multiple ATA_SLDR_OpenTransfer."""
    ATA_SLDR_TRANSFER_ILLEGAL = 532
    """No ATA_SLDR_OpenTransfer happened."""
    ATA_SLDR_DATA_ERROR = 533
    """Unexpected data format received."""
    ATA_SLDR_CHK_SUM_ERROR = 534
    """Checksum error in transmitted data."""
    ATA_SLDR_ADDRESS_ERROR = 535
    """Address out of valid range."""
    ATA_SLDR_INV_LOADFILE = 536
    """Firmware file has invalid format."""
    ATA_SLDR_UNSUPPORTED = 537
    """Current (loaded) Firmware doesn't support upload."""
    ATA_PS_NOT_READY = 538
    """PS-System is not ready."""
    ATA_ATR_SYSTEM_ERR = 539
    """ATR system error."""

    AUT_TIMEOUT = 8704
    """Position not reached"""
    AUT_DETENT_ERROR = 8705
    """Positioning not possible due to mounted EDM"""
    AUT_ANGLE_ERROR = 8706
    """Angle measurement error"""
    AUT_MOTOR_ERROR = 8707
    """Motorization error"""
    AUT_INCACC = 8708
    """Position not exactly reached"""
    AUT_DEV_ERROR = 8709
    """Deviation measurement error"""
    AUT_NO_TARGET = 8710
    """No target detected"""
    AUT_MULTIPLE_TARGETS = 8711
    """Multiple target detected"""
    AUT_BAD_ENVIRONMENT = 8712
    """Bad environment conditions"""
    AUT_DETECTOR_ERROR = 8713
    """Error in target acquisition"""
    AUT_NOT_ENABLED = 8714
    """Target acquisition not enabled"""
    AUT_CALACC = 8715
    """ATR-Calibration failed"""
    AUT_ACCURACY = 8716
    """Target position not exactly reached"""
    AUT_DIST_STARTED = 8717
    """Info dist. Measurement has been started"""
    AUT_SUPPLY_TOO_HIGH = 8718
    """External Supply voltage is too high."""
    AUT_SUPPLY_TOO_LOW = 8719
    """Int. or ext. Supply voltage is too low."""
    AUT_NO_WORKING_AREA = 8720
    """Working area not set."""
    AUT_ARRAY_FULL = 8721
    """Power search data array is filled."""
    AUT_NO_DATA = 8722
    """No data available."""
    AUT_SIDECOVER_ERR = 8723
    """motion cannot be executed because of sidecover."""
    AUT_OUT_OF_SYNC = 8724
    """
    angle requested for time not in collection (probably telescope out of
    sync).
    """
    AUT_NO_LOCK = 8725
    """lock mode not allowed."""

    BAP_CHANGE_ALL_TO_DIST = 9217
    """Command changed from ALL to DIST"""

    BAS_ILL_OPCODE = 9984
    """Illegal opcode."""
    BAS_DIV_BY_ZERO = 9985
    """Division by Zero occured."""
    BAS_STACK_UNDERFLOW = 9986
    """Interpreter stack underflow."""
    BAS_STACK_OVERFLOW = 9987
    """Interpreter stack overflow."""
    BAS_NO_DLG_EXIST = 9988
    """No dialog is defined."""
    BAS_DLG_ALREADY_EXIST = 9989
    """Only one dialog may be defined at once."""
    BAS_INSTALL_ERR = 9990
    """General error during installation."""
    BAS_FIL_INV_MODE = 9995
    """Invalid file access mode."""
    BAS_FIL_TABLE_FULL = 9996
    """Maximum number of open files overflow."""
    BAS_FIL_ILL_NAME = 9997
    """Illegal file name."""
    BAS_FIL_ILL_POS = 9998
    """Illegal file position, hence < 1."""
    BAS_FIL_ILL_OPER = 9999
    """Illegal operation on this kind of file."""
    BAS_MENU_ID_INVALID = 10000
    """Invalid menu id detected."""
    BAS_MENU_TABLE_FULL = 10001
    """Internal menu id table overflow."""

    BMM_XFER_PENDING = 2305
    """Loading process already opened"""
    BMM_NO_XFER_OPEN = 2306
    """Transfer not opened"""
    BMM_UNKNOWN_CHARSET = 2307
    """Unknown character set"""
    BMM_NOT_INSTALLED = 2308
    """Display module not present"""
    BMM_ALREADY_EXIST = 2309
    """Character set already exists"""
    BMM_CANT_DELETE = 2310
    """Character set cannot be deleted"""
    BMM_MEM_ERROR = 2311
    """Memory cannot be allocated"""
    BMM_CHARSET_USED = 2312
    """Character set still used"""
    BMM_CHARSET_SAVED = 2313
    """Char-set cannot be deleted or is protected"""
    BMM_INVALID_ADR = 2314
    """Attempt to copy a character block outside the allocated memory"""
    BMM_CANCELANDADR_ERROR = 2315
    """Error during release of allocated memory"""
    BMM_INVALID_SIZE = 2316
    """Number of bytes specified in header does not match the bytes read"""
    BMM_CANCELANDINVSIZE_ERROR = 2317
    """Allocated memory could not be released"""
    BMM_ALL_GROUP_OCC = 2318
    """Max. number of character sets already loaded"""
    BMM_CANT_DEL_LAYERS = 2319
    """Layer cannot be deleted"""
    BMM_UNKNOWN_LAYER = 2320
    """Required layer does not exist"""
    BMM_INVALID_LAYERLEN = 2321
    """Layer length exceeds maximum"""

    CAM_NOT_READY = 13824
    """CAM-System is not ready."""
    CAM_NOT_INIT = 13825
    """Camera is not initialised."""
    CAM_IMG_NOT_AVAILABLE = 13826
    """Image from the camera is not available."""
    CAM_IMAGE_SAVING_ERROR = 13828
    """Error while saving image."""
    CAM_BIT_DEPTH_ERROR = 13834
    """Bit depth of the image is wrong."""
    CAM_OUT_OF_MEMORY = 13835
    """There is no memory available."""
    CAM_SPOT_NOT_AVAIL = 13836
    """Required spot is not available."""
    CAM_NO_SPOTS_INLIST = 13837
    """Spot list is empty."""
    CAM_NO_TARGET = 13838
    """There are no spots in image."""
    CAM_TARGET_NOT_FOUND = 13839
    """Required target is not found."""
    CAM_NO_CALIB_INPUT_DATA = 13844
    """Calibration input data is missing."""
    CAM_MEAS_NOT_ACCURATE = 13845
    """Measurement is not accurate."""
    CAM_DIRTY = 13854
    """Camera cleanness check failed, camera is dirty."""

    COD_LIST_NOT_VALID = 9728
    """List not initialized."""
    COD_SHORTCUT_UNKNOWN = 9729
    """Shortcut or code unknown."""
    COD_NOT_SELECTED = 9730
    """Codelist selection wasn't possible."""
    COD_MANDATORY_FAIL = 9731
    """Mandatory field has no valid value."""
    COD_NO_MORE_ATTRIB = 9732
    """maximal number of attr. are defined."""

    COM_ERO = 3072
    """Initiate Extended Runtime Operation (ERO)."""
    COM_CANT_ENCODE = 3073
    """Cannot encode arguments in client."""
    COM_CANT_DECODE = 3074
    """Cannot decode results in client."""
    COM_CANT_SEND = 3075
    """Hardware error while sending."""
    COM_CANT_RECV = 3076
    """Hardware error while receiving."""
    COM_TIMEDOUT = 3077
    """Request timed out."""
    COM_WRONG_FORMAT = 3078
    """Packet format error."""
    COM_VER_MISMATCH = 3079
    """Version mismatch between client and server."""
    COM_CANT_DECODE_REQ = 3080
    """Cannot decode arguments in server."""
    COM_PROC_UNAVAIL = 3081
    """Unknown RPC, procedure ID invalid."""
    COM_CANT_ENCODE_REP = 3082
    """Cannot encode results in server."""
    COM_SYSTEM_ERR = 3083
    """Unspecified generic system error."""
    COM_FAILED = 3085
    """Unspecified error."""
    COM_NO_BINARY = 3086
    """Binary protocol not available."""
    COM_INTR = 3087
    """Call interrupted."""
    COM_REQUIRES_8DBITS = 3090
    """Protocol needs 8bit encoded characters."""
    COM_TR_ID_MISMATCH = 3093
    """Transaction ID mismatch error."""
    COM_NOT_GEOCOM = 3094
    """Protocol not recognisable."""
    COM_UNKNOWN_PORT = 3095
    """(WIN) Invalid port address."""
    COM_ERO_END = 3099
    """ERO is terminating."""
    COM_OVERRUN = 3100
    """Internal error data buffer overflow."""
    COM_SRVR_RX_CHECKSUM_ERROR = 3101
    """Invalid checksum on server side received."""
    COM_CLNT_RX_CHECKSUM_ERROR = 3102
    """Invalid checksum on client side received."""
    COM_PORT_NOT_AVAILABLE = 3103
    """(WIN) Port not available."""
    COM_PORT_NOT_OPEN = 3104
    """(WIN) Port not opened."""
    COM_NO_PARTNER = 3105
    """(WIN) Unable to find TPS."""
    COM_ERO_NOT_STARTED = 3106
    """Extended Runtime Operation could not be started."""
    COM_CONS_REQ = 3107
    """Attention to send cons requests"""
    COM_SRVR_IS_SLEEPING = 3108
    """TPS has gone to sleep. Wait and try again."""
    COM_SRVR_IS_OFF = 3109
    """TPS has shut down. Wait and try again."""
    COM_NO_CHECKSUM = 3110
    """No checksum in ASCII protocol available."""

    CNF_INI_NOTOPEN = 10497
    """INI-file not opened"""
    CNF_INI_NOTFOUND = 10498
    """Warning Could not find section or key"""
    CNF_CONT = 10499
    """Return code of system function"""
    CNF_ESC = 10500
    """Return code of system function"""
    CNF_QUIT = 10501
    """Return code of system function"""
    CNF_DATA_INVALID = 10502
    """Config. file data not valid"""
    CNF_DATA_OVERFLOW = 10503
    """Config. file data exceed valid amount"""
    CNF_NOT_COMPLETE = 10504
    """Config. file data not complete"""
    CNF_DLG_CNT_OVERFLOW = 10505
    """Too many executed dialogs"""
    CNF_NOT_EXECUTABLE = 10506
    """Item not executable"""
    CNF_AEXE_OVERFLOW = 10507
    """Autoexec table full"""
    CNF_PAR_LOAD_ERR = 10508
    """Error in loading parameter"""
    CNF_PAR_SAVE_ERR = 10509
    """Error in saving parameter"""
    CNF_FILE_MISSING = 10510
    """Parameter filename/path not valid"""
    CNF_SECTION_MISSING = 10511
    """Section in parameter file missing"""
    CNF_HEADER_FAIL = 10512
    """Default file wrong or an entry is missing"""
    CNF_PARMETER_FAIL = 10513
    """Parameter-line not complete or missing"""
    CNF_PARMETER_SET = 10514
    """Parameter-set caused an error"""
    CNF_RECMASK_FAIL = 10515
    """RecMask-line not complete or missing"""
    CNF_RECMASK_SET = 10516
    """RecMask-set caused an error"""
    CNF_MEASDLGLIST_FAIL = 10517
    """MeasDlgList-line not complete or missing"""
    CNF_MEASDLGLIST_SET = 10518
    """MeasDlgList-set caused an error"""
    CNF_APPL_OVERFLOW = 10519
    """Application table full"""

    DNA_TOO_DARK = 12032
    """Too dark or poor light"""
    DNA_TOO_BRIGHT = 12033
    """Too bright light"""
    DNA_TILT = 12034
    """Instrument is not level"""
    DNA_COARSE_CORR = 12035
    """
    Coarse correlation error. Too much coverage or insufficient code length.
    """
    DNA_FINE_CORR = 12036
    """
    Fine correlation error. Too much coverage or insufficient code length.
    """
    DNA_BAD_DISTANCE = 12037
    """Distance outside the permitted range."""
    DNA_INVERTED = 12038
    """Staff inverted or inverse mode activated."""
    DNA_BAD_FOCUS = 12039
    """Bad focusing."""

    DPL_NOCREATE = 3328
    """no file creation, fatal"""
    DPL_NOTOPEN = 3329
    """bank not open"""
    DPL_ALRDYOPEN = 3330
    """a databank is already open"""
    DPL_NOTFOUND = 3331
    """databank file does not exist"""
    DPL_EXISTS = 3332
    """databank already exists"""
    DPL_EMPTY = 3333
    """databank is empty"""
    DPL_BADATA = 3334
    """bad data detected"""
    DPL_BADFIELD = 3335
    """bad field type"""
    DPL_BADINDEX = 3336
    """bad index information"""
    DPL_BADKEY = 3337
    """bad key type"""
    DPL_BADMODE = 3338
    """bad mode"""
    DPL_BADRANGE = 3339
    """bad range"""
    DPL_DUPLICATE = 3340
    """duplicate keys not allowed"""
    DPL_INCOMPLETE = 3341
    """record is incomplete"""
    DPL_IVDBID = 3342
    """invalid db project id"""
    DPL_IVNAME = 3343
    """invalid name"""
    DPL_LOCKED = 3344
    """data locked"""
    DPL_NOTLOCKED = 3345
    """data not locked"""
    DPL_NODATA = 3346
    """no data found"""
    DPL_NOMATCH = 3347
    """no matching key found"""
    DPL_NOSPACE = 3348
    """no more (disk) space left"""
    DPL_NOCLOSE = 3349
    """could not close db (sys. error)"""
    DPL_RELATIONS = 3350
    """record still has relations"""
    DPL_NULLPTR = 3351
    """null pointer"""
    DPL_BADFORMAT = 3352
    """bad databank format, wrong version"""
    DPL_BADRECTYPE = 3353
    """bad record type"""
    DPL_OUTOFMEM = 3354
    """no more (memory) space left"""
    DPL_CODE_MISMATCH = 3355
    """code mismatch"""
    DPL_NOTINIT = 3356
    """db has not been initialized"""
    DPL_NOTEXIST = 3357
    """trf. for old db's does not exist"""
    DPL_NOTOK = 4864
    """not ok"""
    DPL_IVAPPL = 4865
    """invalid database system appl."""
    DPL_NOT_AVAILABLE = 4866
    """database not available"""
    DPL_NO_CODELIST = 4867
    """no codelist found"""
    DPL_TO_MANY_CODELISTS = 4868
    """more then DPL_MAX_CODELISTS found"""

    EDM_COMERR = 769
    """Communication with EDM failed"""
    EDM_NOSIGNAL = 770
    """no signal"""
    EDM_PPM_MM = 771
    """PPM and/or MM not zero"""
    EDM_METER_FEET = 772
    """EDM unit not set to meter"""
    EDM_ERR12 = 773
    """battery low"""
    EDM_DIL99 = 774
    """limit at 99 measurements (DIL)"""
    EDM_TIMEOUT = 775
    """
    Timeout, measuring time exceeded
    (signal too weak, beam interrupted,..).
    """
    EDM_FLUKT_ERR = 776
    """Too much turbulences or distractions."""
    EDM_FMOT_ERR = 777
    """Filter motor defective."""
    EDM_DEV_NOT_INSTALLED = 778
    """Device like EGL, DL is not installed."""
    EDM_NOT_FOUND = 779
    """Search result invalid. For the exact explanation see in the description
    of the called function."""
    EDM_ERROR_RECEIVED = 780
    """Communication ok, but an error reported from the EDM sensor."""
    EDM_MISSING_SRVPWD = 781
    """No service password is set."""
    EDM_INVALID_ANSWER = 782
    """Communication ok, but an unexpected answer received."""
    EDM_SEND_ERR = 783
    """Data send error, sending buffer is full."""
    EDM_RECEIVE_ERR = 784
    """Data receive error, like parity buffer overflow."""
    EDM_INTERNAL_ERR = 785
    """Internal EDM subsystem error."""
    EDM_BUSY = 786
    """Sensor is working already, abort current measuring first."""
    EDM_NO_MEASACTIVITY = 787
    """No measurement activity started."""
    EDM_CHKSUM_ERR = 788
    """Calculated checksum, resp. received data wrong (only in binary
    communication mode possible)."""
    EDM_INIT_OR_STOP_ERR = 789
    """During start up or shut down phase an error occured. It is saved in the
    DEL buffer."""
    EDM_SRL_NOT_AVAILABLE = 790
    """Red laser not available on this sensor HW."""
    EDM_MEAS_ABORTED = 791
    """Measurement will be aborted (will be used for the lasersecurity)"""
    EDM_SLDR_TRANSFER_PENDING = 798
    """Multiple OpenTransfer calls."""
    EDM_SLDR_TRANSFER_ILLEGAL = 799
    """No opentransfer happened."""
    EDM_SLDR_DATA_ERROR = 800
    """Unexpected data format received."""
    EDM_SLDR_CHK_SUM_ERROR = 801
    """Checksum error in transmitted data."""
    EDM_SLDR_ADDR_ERROR = 802
    """Address out of valid range."""
    EDM_SLDR_INV_LOADFILE = 803
    """Firmware file has invalid format."""
    EDM_SLDR_UNSUPPORTED = 804
    """Current (loaded) firmware doesn't support upload."""
    EDM_UNKNOW_ERR = 808
    """Undocumented error from the EDM sensor, should not occur."""
    EDM_DISTRANGE_ERR = 818
    """Out of distance range (dist too small or large)."""
    EDM_SIGNTONOISE_ERR = 819
    """Signal to noise ratio too small."""
    EDM_NOISEHIGH_ERR = 820
    """Noise to high."""
    EDM_PWD_NOTSET = 821
    """Password is not set."""
    EDM_ACTION_NO_MORE_VALID = 822
    """
    Elapsed time between prepare und start fast measurement for ATR too
    long.
    """
    EDM_MULTRG_ERR = 823
    """Possibly more than one target (also a sensor error)."""
    EDM_MISSING_EE_CONSTS = 824
    """Eeprom consts are missing."""
    EDM_NOPRECISE = 825
    """No precise measurement possible."""
    EDM_MEAS_DIST_NOT_ALLOWED = 826
    """Measured distance is to big (not allowed)."""
    EDM_NOT_EXECUTED = 827
    """Part or whole measurement was not executed."""
    EDM_SIG_FORM_ERR = 828
    """Sinus signal form error."""
    EDM_DIST_TOO_SHORT = 829
    """Measured distance too short."""
    EDM_SYNTH_ERR = 830
    """PLL-spg out of tolerance."""
    EDM_AMPL_RELATION_ERR = 831
    """Amplitude relation fine / rough error."""
    EDM_DIVISION_BY_ZERO = 832
    """Division by zero."""

    FIL_NO_ERROR = 3840
    """Operation completed successfully."""
    FIL_FILNAME_NOT_FOUND = 3845
    """File name not found."""
    FIL_NO_MAKE_DIRECTORY = 3880
    """Cannot create directory."""
    FIL_RENAME_FILE_FAILED = 3886
    """Rename of file failed."""
    FIL_INVALID_PATH = 3888
    """Invalid path specified."""
    FIL_FILE_NOT_DELETED = 3898
    """Cannot delete file."""
    FIL_ILLEGAL_ORIGIN = 3906
    """Illegal origin."""
    FIL_END_OF_FILE = 3924
    """End of file reached."""
    FIL_NO_MORE_ROOM_ON_MEDIUM = 3931
    """Medium full."""
    FIL_PATTERN_DOES_NOT_MATCH = 3932
    """Pattern does not match file names."""
    FIL_FILE_ALREADY_OPEND_FOR_WR = 3948
    """File is already open with write permission."""
    FIL_WRITE_TO_MEDIUM_FAILED = 3957
    """Write operation to medium failed."""
    FIL_START_SEARCH_NOT_CALLED = 3963
    """FIL_StartList not called."""
    FIL_NO_STORAGE_MEDIUM_IN_DEVICE = 3964
    """No medium existent in device."""
    FIL_ILLEGAL_FILE_OPEN_TYPE = 3965
    """Illegal file open type."""
    FIL_MEDIUM_NEWLY_INSERTED = 3966
    """Medium freshly inserted into device."""
    FIL_MEMORY_FAILED = 3967
    """Memory failure. No more memory available."""
    FIL_FATAL_ERROR = 3968
    """Fatal error during file operation."""
    FIL_FAT_ERROR = 3969
    """Fatal error in file allocation table."""
    FIL_ILLEGAL_DRIVE = 3970
    """Illegal drive chosen."""
    FIL_INVALID_FILE_DESCR = 3971
    """Illegal file descriptor."""
    FIL_SEEK_FAILED = 3972
    """Seek failed."""
    FIL_CANNOT_DELETE = 3973
    """Cannot delete file."""
    FIL_MEDIUM_WRITE_PROTECTED = 3974
    """Medium is write protected."""
    FIL_BATTERY_LOW = 3975
    """Medium backup battery is low."""
    FIL_BAD_FORMAT = 3976
    """Bad medium format."""
    FIL_UNSUPPORTED_MEDIUM = 3977
    """Unsupported PC-Card detected."""
    FIL_RENAME_DIR_FAILED = 3978
    """Directory exists already"""

    FTR_FILEACCESS = 13056
    """File access error."""
    FTR_WRONGFILEBLOCKNUMBER = 13057
    """Block number was not the expected one."""
    FTR_NOTENOUGHSPACE = 13058
    """Not enough space on device to proceed uploading."""
    FTR_INVALIDINPUT = 13059
    """Rename of file failed."""
    FTR_MISSINGSETUP = 13060
    """Invalid parameter as input."""

    GM_WRONG_AREA_DEF = 1025
    """Wrong Area Definition."""
    GM_IDENTICAL_PTS = 1026
    """Identical Points."""
    GM_PTS_IN_LINE = 1027
    """Points on one line."""
    GM_OUT_OF_RANGE = 1028
    """Out of range."""
    GM_PLAUSIBILITY_ERR = 1029
    """Plausibility error."""
    GM_TOO_FEW_OBSERVATIONS = 1030
    """To few Observations to calculate the average."""
    GM_NO_SOLUTION = 1031
    """No Solution."""
    GM_ONE_SOLUTION = 1032
    """Only one solution."""
    GM_TWO_SOLUTIONS = 1033
    """Second solution."""
    GM_ANGLE_SMALLER_15GON = 1034
    """Warning Intersection angle < 15gon."""
    GM_INVALID_TRIANGLE_TYPE = 1035
    """Invalid triangle."""
    GM_INVALID_ANGLE_SYSTEM = 1036
    """Invalid angle unit."""
    GM_INVALID_DIST_SYSTEM = 1037
    """Invalid distance unit."""
    GM_INVALID_V_SYSTEM = 1038
    """Invalid vertical angle."""
    GM_INVALID_TEMP_SYSTEM = 1039
    """Invalid temperature system."""
    GM_INVALID_PRES_SYSTEM = 1040
    """Invalid pressure unit."""
    GM_RADIUS_NOT_POSSIBLE = 1041
    """Invalid radius."""
    GM_NO_PROVISIONAL_VALUES = 1042
    """GM2 insufficient data."""
    GM_SINGULAR_MATRIX = 1043
    """GM2 bad data"""
    GM_TOO_MANY_ITERATIONS = 1044
    """GM2 bad data distr."""
    GM_IDENTICAL_TIE_POINTS = 1045
    """GM2 same tie points."""
    GM_SETUP_EQUALS_TIE_POINT = 1046
    """GM2 sta/tie point same."""

    IOS_CHNL_DISABLED = 10240
    """channel is disabled"""
    IOS_NO_MORE_CHAR = 10241
    """no more data available"""
    IOS_MAX_BLOCK_LEN = 10242
    """reached max. block length"""
    IOS_HW_BUF_OVERRUN = 10243
    """hardware buffer overrun (highest priority)"""
    IOS_PARITY_ERROR = 10244
    """parity error"""
    IOS_FRAMING_ERROR = 10245
    """framing error"""
    IOS_DECODE_ERROR = 10246
    """decode error"""
    IOS_CHKSUM_ERROR = 10247
    """checksum error (lowest priority)"""
    IOS_COM_ERROR = 10248
    """general communication error"""
    IOS_FL_RD_ERROR = 10280
    """flash read error"""
    IOS_FL_WR_ERROR = 10281
    """flash write error"""
    IOS_FL_CL_ERROR = 10282
    """flash erase error"""

    KDM_NOT_AVAILABLE = 12544
    """KDM device is not available."""

    LDR_PENDING = 2048
    """Transfer is already open"""
    LDR_PRGM_OCC = 2049
    """Maximal number of applications reached"""
    LDR_TRANSFER_ILLEGAL = 2050
    """No Transfer is open"""
    LDR_NOT_FOUND = 2051
    """Function or program not found"""
    LDR_ALREADY_EXIST = 2052
    """Loadable object already exists"""
    LDR_NOT_EXIST = 2053
    """Can't delete. Object does not exist"""
    LDR_SIZE_ERROR = 2054
    """Error in loading object"""
    LDR_MEM_ERROR = 2055
    """Error at memory allocation/release"""
    LDR_PRGM_NOT_EXIST = 2056
    """Can't load text-object because application does not exist"""
    LDR_FUNC_LEVEL_ERR = 2057
    """Call-stack limit reached"""
    LDR_RECURSIV_ERR = 2058
    """Recursive calling of an loaded function"""
    LDR_INST_ERR = 2059
    """Error in installation function"""
    LDR_FUNC_OCC = 2060
    """Maximal number of functions reached"""
    LDR_RUN_ERROR = 2061
    """Error during a loaded application program"""
    LDR_DEL_MENU_ERR = 2062
    """Error during deleting of menu entries of an application"""
    LDR_OBJ_TYPE_ERROR = 2063
    """Loadable object is unknown"""
    LDR_WRONG_SECKEY = 2064
    """Wrong security key"""
    LDR_ILLEGAL_LOADADR = 2065
    """Illegal application memory address"""
    LDR_IEEE_ERROR = 2066
    """Loadable object file is not IEEE format"""
    LDR_WRONG_APPL_VERSION = 2067
    """Bad application version number"""

    MEM_OUT_OF_MEMORY = 1536
    """out of memory"""
    MEM_OUT_OF_HANDLES = 1537
    """out of memory handles"""
    MEM_TAB_OVERFLOW = 1538
    """memory table overflow"""
    MEM_HANDLE_INVALID = 1539
    """used handle is invalid"""
    MEM_DATA_NOT_FOUND = 1540
    """memory data not found"""
    MEM_DELETE_ERROR = 1541
    """memory delete error"""
    MEM_ZERO_ALLOC_ERR = 1542
    """tried to allocate 0 bytes"""
    MEM_REORG_ERR = 1543
    """can't reorganize memory"""

    MMI_BUTTON_ID_EXISTS = 2817
    """Button ID already exists"""
    MMI_DLG_NOT_OPEN = 2818
    """Dialog not open"""
    MMI_DLG_OPEN = 2819
    """Dialog already open"""
    MMI_DLG_SPEC_MISMATCH = 2820
    """Number of fields specified with OpenDialogDef does not match"""
    MMI_DLGDEF_EMPTY = 2821
    """Empty dialog definition"""
    MMI_DLGDEF_NOT_OPEN = 2822
    """Dialog definition not open"""
    MMI_DLGDEF_OPEN = 2823
    """Dialog definition still open"""
    MMI_FIELD_ID_EXISTS = 2824
    """Field ID already exists"""
    MMI_ILLEGAL_APP_ID = 2825
    """Illegal application ID"""
    MMI_ILLEGAL_BUTTON_ID = 2826
    """Illegal button ID"""
    MMI_ILLEGAL_DLG_ID = 2827
    """Illegal dialog ID"""
    MMI_ILLEGAL_FIELD_COORDS = 2828
    """Illegal field coordinates or length/height"""
    MMI_ILLEGAL_FIELD_ID = 2829
    """Illegal field ID"""
    MMI_ILLEGAL_FIELD_TYPE = 2830
    """Illegal field type"""
    MMI_ILLEGAL_FIELD_FORMAT = 2831
    """Illegal field format"""
    MMI_ILLEGAL_FIXLINES = 2832
    """Illegal number of fix dialog lines"""
    MMI_ILLEGAL_MB_TYPE = 2833
    """Illegal message box type"""
    MMI_ILLEGAL_MENU_ID = 2834
    """Illegal menu ID"""
    MMI_ILLEGAL_MENUITEM_ID = 2835
    """Illegal menu item ID"""
    MMI_ILLEGAL_NEXT_ID = 2836
    """Illegal next field ID"""
    MMI_ILLEGAL_TOPLINE = 2837
    """Illegal topline number"""
    MMI_NOMORE_BUTTONS = 2838
    """No more buttons per dialog/menu available"""
    MMI_NOMORE_DLGS = 2839
    """No more dialogs available"""
    MMI_NOMORE_FIELDS = 2840
    """No more fields per dialog available"""
    MMI_NOMORE_MENUS = 2841
    """No more menus available"""
    MMI_NOMORE_MENUITEMS = 2842
    """No more menu items available"""
    MMI_NOMORE_WINDOWS = 2843
    """No more windows available"""
    MMI_SYS_BUTTON = 2844
    """The button belongs to the MMI"""
    MMI_VREF_UNDEF = 2845
    """The parameter list for OpenDialog is uninitialized"""
    MMI_EXIT_DLG = 2846
    """The MMI should exit the dialog"""
    MMI_KEEP_FOCUS = 2847
    """The MMI should keep focus within field being edited"""
    MMI_NOMORE_ITEMS = 2848
    """Notification to the MMI that no more items available"""

    MOT_UNREADY = 1792
    """Motorization not ready"""
    MOT_BUSY = 1793
    """Motorization is handling another task"""
    MOT_NOT_OCONST = 1794
    """Not in velocity mode"""
    MOT_NOT_CONFIG = 1795
    """Motorization is in the wrong mode or busy"""
    MOT_NOT_POSIT = 1796
    """Not in posit mode"""
    MOT_NOT_SERVICE = 1797
    """Not in service mode"""
    MOT_NOT_BUSY = 1798
    """Motorization is handling no task"""
    MOT_NOT_LOCK = 1799
    """Not in tracking mode"""
    MOT_NOT_SPIRAL = 1800
    """Not in spiral mode"""
    MOT_V_ENCODER = 1801
    """Certical encoder/motor error."""
    MOT_HZ_ENCODER = 1802
    """Horizontal encoder/motor error."""
    MOT_HZ_V_ENCODER = 1803
    """Horizontal and vertical encoder/motor error."""
    MOT_HZ_MOTOR_ERROR = 1804
    """azimuth motor error."""
    MOT_V_MOTOR_ERROR = 1805
    """elevation motor error."""
    MOT_TIMEOUT = 1806
    """general timeout."""
    MOT_HZ_TIMEOUT = 1807
    """timeout of azimuth positioning system."""
    MOT_V_TIMEOUT = 1808
    """timeout of elevation positioning system."""
    MOT_SCAN_STOPPED = 1809
    """scan stopped with error."""
    MOT_SUPPLY_CHANGED = 1810
    """scan paused because power supply has changed."""

    SAP_ILLEGAL_SYSMENU_NUM = 9473
    """Illegal system menu number"""

    TMC_NO_FULL_CORRECTION = 1283
    """Warning measurement without full correction"""
    TMC_ACCURACY_GUARANTEE = 1284
    """Info accuracy can not be guaranteed"""
    TMC_ANGLE_OK = 1285
    """Warning only angle measurement valid"""
    TMC_ANGLE_NO_FULL_CORRECTION = 1288
    """Warning only angle measurement valid but without full correction"""
    TMC_ANGLE_ACCURACY_GUARANTEE = 1289
    """Info only angle measurement valid but accuracy can not be guarantee"""
    TMC_ANGLE_ERROR = 1290
    """Error no angle measurement"""
    TMC_DIST_PPM = 1291
    """Error wrong setting of PPM or MM on EDM"""
    TMC_DIST_ERROR = 1292
    """Error distance measurement not done (no aim, etc.)"""
    TMC_BUSY = 1293
    """Error system is busy (no measurement done)"""
    TMC_SIGNAL_ERROR = 1294
    """Error no signal on EDM (only in signal mode)"""
    TMC_OLD_PLANE = 1380
    """Warning inclination out of time range."""
    TMC_NO_PLANE = 1381
    """Warning measurement without planeinclination correction."""
    TMC_INC_ERROR = 1392
    """Warning measurement without sensorinclination correction."""
    TMC_INCLINE_ACC = 1383
    """Info inclination accuracy can not be guaranteed."""

    TXT_OTHER_LANG = 2560
    """text found, but in an other language"""
    TXT_UNDEF_TOKEN = 2561
    """text not found, token is undefined"""
    TXT_UNDEF_LANG = 2562
    """language is not defined"""
    TXT_TOOMANY_LANG = 2563
    """maximal number of languages reached"""
    TXT_GROUP_OCC = 2564
    """desired text group is already in use"""
    TXT_INVALID_GROUP = 2565
    """text group is invalid"""
    TXT_OUT_OF_MEM = 2566
    """out of text memory"""
    TXT_MEM_ERROR = 2567
    """memory write / allocate error"""
    TXT_TRANSFER_PENDING = 2568
    """text transfer is already open"""
    TXT_TRANSFER_ILLEGAL = 2569
    """text transfer is not opened"""
    TXT_INVALID_SIZE = 2570
    """illegal text data size"""
    TXT_ALREADY_EXIST = 2571
    """language already exists"""

    WIR_PTNR_OVERFLOW = 5121
    """point number overflow"""
    WIR_NUM_ASCII_CARRY = 5122
    """carry from number to ASCII conversion"""
    WIR_PTNR_NO_INC = 5123
    """can't increment point number"""
    WIR_STEP_SIZE = 5124
    """wrong step size"""
    WIR_BUSY = 5125
    """resource occupied"""
    WIR_CONFIG_FNC = 5127
    """user function selected"""
    WIR_CANT_OPEN_FILE = 5128
    """can't open file"""
    WIR_FILE_WRITE_ERROR = 5129
    """can't write into file"""
    WIR_MEDIUM_NOMEM = 5130
    """no anymore memory on PC-Card"""
    WIR_NO_MEDIUM = 5131
    """no PC-Card"""
    WIR_EMPTY_FILE = 5132
    """empty GSI file"""
    WIR_INVALID_DATA = 5133
    """invalid data in GSI file"""
    WIR_F2_BUTTON = 5134
    """F2 button pressed"""
    WIR_F3_BUTTON = 5135
    """F3 button pressed"""
    WIR_F4_BUTTON = 5136
    """F4 button pressed"""
    WIR_F5_BUTTON = 5137
    """F5 button pressed"""
    WIR_F6_BUTTON = 5138
    """F6 button pressed"""
    WIR_SHF2_BUTTON = 5139
    """SHIFT F2 button pressed"""


class GeoComResponse(Generic[_P]):
    """
    Container class for parsed GeoCom responses.

    The response encapsulates the original command, that was sent, and the
    response received, as well as the codes and parameters extracted from
    the response.

    The `params` usually takes 3 types of values:

    - **None**: the response explicitly returned no values
    - **Scalar**: the response returned a single parameter
    - **Sequence** (usually a `tuple`): the response returned multiple
      parameters

    Warning
    -------
    The `params` will be also `None`, if the parameter parsing failed for
    some reason, to signal the unsuccessful operation. This error case must
    be handled before using the returned values.
    """

    def __init__(
        self,
        rpcname: str,
        cmd: str,
        response: str,
        comcode: GeoComCode,
        rpccode: GeoComCode,
        trans: int,
        params: _P | None = None
    ):
        """
        Parameters
        ----------
        rpcname : str
            Name of the GeoCom function, that corresponds to the RPC,
            that invoked this response.
        cmd : str
            Full, serialized request, that invoked this response.
        response : str
            Full, received response.
        comcode : GeoComCode
            Parsed COM return code indicating the success/failure of
            communication.
        rpccode : GeoComCode
            Parsed RPC return code indicating the success/failure of
            the command.
        trans : int
            Parsed transaction ID.
        params : Any | None, optional
            Collection of parsed response parameters. The content
            is dependent on the executed function. (default: None)
        """
        self.rpcname: str = rpcname
        """Name of the GeoCom function, that correspondes to the RPC,
            that invoked this response."""
        self.cmd: str = cmd
        """Full, serialized request, that invoked this response."""
        self.response: str = response
        """Full, received response."""
        self.error: GeoComCode = (
            comcode
            if not comcode
            else rpccode
        )
        """Parsed return code indicating the success/failure of the
        request."""
        self.trans: int = trans
        """Parsed transaction ID."""
        self.params: _P | None = params
        """Collection of parsed response parameters. The content
            is dependent on the executed function."""

    def __str__(self) -> str:
        return (
            f"GeoComResponse({self.rpcname}) code: {self.error.name:s}, "
            f"tr: {self.trans:d}, "
            f"params: {self.params}, "
            f"(cmd: '{self.cmd}', response: '{self.response}')"
        )

    def __bool__(self) -> bool:
        return bool(self.error)

    def map_params(
        self,
        transformer: Callable[[_P | None], _T | None]
    ) -> GeoComResponse[_T]:
        """
        Returns a new response object with the metadata maintained, but
        the parameters transformed with the supplied function.

        Parameters
        ----------
        transformer : Callable[[_P  |  None], _T  |  None]
            Function to transform the params to new values.

        Returns
        -------
        GeoComResponse
            Response with transformed parameters.
        """
        try:
            params = transformer(self.params)
        except Exception:
            params = None

        return GeoComResponse(
            self.rpcname,
            self.cmd,
            self.response,
            self.error,
            self.error,
            self.trans,
            params
        )


class GeoComType(ABC):
    """
    Interface definition for the GeoCom protocol handler type.
    """

    @property
    @abstractmethod
    def precision(self) -> float: ...

    @precision.setter
    @abstractmethod
    def precision(self, value: float) -> None: ...

    @overload
    @abstractmethod
    def request(
        self,
        rpc: int,
        params: Iterable[int | float | bool | str | Angle | Byte] = (),
        parsers: Callable[[str], _T] | None = None
    ) -> GeoComResponse[_T]: ...

    @overload
    @abstractmethod
    def request(
        self,
        rpc: int,
        params: Iterable[int | float | bool | str | Angle | Byte] = (),
        parsers: Iterable[Callable[[str], Any]] | None = None
    ) -> GeoComResponse[tuple[Any, ...]]: ...

    @abstractmethod
    def request(
        self,
        rpc: int,
        params: Iterable[int | float | bool | str | Angle | Byte] = (),
        parsers: (
            Iterable[Callable[[str], Any]]
            | Callable[[str], Any]
            | None
        ) = None
    ) -> GeoComResponse[Any]: ...


class GeoComSubsystem:
    """
    Base class for GeoCom subsystems.
    """

    def __init__(self, parent: GeoComType):
        """
        Parameters
        ----------
        parent : GeoComType
            The parent protocol instance of this subsystem.
        """
        self._parent: GeoComType = parent
        """Parent protocol instance"""
        self._request = self._parent.request
        """Shortcut to the `request` method of the parent protocol."""


rpcnames: dict[int, str] = {
    18010: "AUS_GetRcsSearchSwitch",
    18006: "AUS_GetUserAtrState",
    18008: "AUS_GetUserLockState",
    18005: "AUS_SetUserAtrState",
    18007: "AUS_SetUserLockState",
    18009: "AUS_SwitchRcsSearch",
    9081: "AUT_CAM_PositToPixelCoord",
    9028: "AUT_ChangeFace",
    9037: "AUT_FineAdjust",
    9019: "AUT_GetATRStatus",
    9030: "AUT_GetFineAdjustMode",
    9102: "AUT_GetLockFlyMode",
    9021: "AUT_GetLockStatus",
    9042: "AUT_GetSearchArea",
    9040: "AUT_GetUserSpiral",
    9013: "AUT_LockIn",
    9027: "AUT_MakePositioning",
    9048: "AUT_PS_EnableRange",
    9051: "AUT_PS_SearchNext",
    9052: "AUT_PS_SearchWindow",
    9047: "AUT_PS_SetRange",
    9012: "AUT_ReadTimeout",
    9008: "AUT_ReadTol",
    9029: "AUT_Search",
    9018: "AUT_SetATRStatus",
    9031: "AUT_SetFineAdjustMode",
    9103: "AUT_SetLockFlyMode",
    9020: "AUT_SetLockStatus",
    9043: "AUT_SetSearchArea",
    9011: "AUT_SetTimeout",
    9007: "AUT_SetTol",
    9041: "AUT_SetUserSpiral",
    17039: "BAP_GetATRPrecise",
    17003: "BAP_GetLastDisplayedError",
    17018: "BAP_GetMeasPrg",
    17023: "BAP_GetPrismDef",
    17009: "BAP_GetPrismType",
    17031: "BAP_GetPrismType2",
    17022: "BAP_GetTargetType",
    17033: "BAP_GetUserPrismDef",
    17017: "BAP_MeasDistanceAngle",
    17020: "BAP_SearchTarget",
    17040: "BAP_SetATRPrecise",
    17019: "BAP_SetMeasPrg",
    17024: "BAP_SetPrismDef",
    17008: "BAP_SetPrismType",
    17030: "BAP_SetPrismType2",
    17021: "BAP_SetTargetType",
    17032: "BAP_SetUserPrismDef",
    11004: "BMM_BeepAlarm",
    11003: "BMM_BeepNormal",
    11002: "BMM_BeepOff",
    11001: "BMM_BeepOn",
    23669: "CAM_AF_ContinuousAutofocus",
    23663: "CAM_AF_FocusContrastArroundCurrent",
    23668: "CAM_AF_GetChipWindowSize",
    23644: "CAM_AF_GetMotorPosition",
    23652: "CAM_AF_PositFocusMotorToDist",
    23677: "CAM_AF_PositFocusMotorToInfinity",
    23645: "CAM_AF_SetMotorPosition",
    23662: "CAM_AF_SingleShotAutofocus",
    23611: "CAM_GetCamPos",
    23613: "CAM_GetCamViewingDir",
    23619: "CAM_GetCameraFoV",
    23636: "CAM_GetCameraPowerSwitch",
    23609: "CAM_GetZoomFactor",
    23627: "CAM_IsCameraReady",
    23671: "CAM_OAC_GetCrossHairPos",
    23624: "CAM_OVC_GetActCameraCentre",
    23625: "CAM_OVC_SetActDistance",
    23622: "CAM_SetActualImageName",
    23637: "CAM_SetCameraPowerSwitch",
    23633: "CAM_SetCameraProperties",
    23626: "CAM_SetWhiteBalanceMode",
    23608: "CAM_SetZoomFactor",
    23675: "CAM_StartRemoteVideo",
    23676: "CAM_StopRemoteVideo",
    23623: "CAM_TakeImage",
    23638: "CAM_WaitForCameraReady",
    115: "COM_EnableSignOff",
    113: "COM_GetBinaryAvailable",
    108: "COM_GetDoublePrecision",
    110: "COM_GetSWVersion",
    1: "COM_Local",
    0: "COM_NullProc",
    114: "COM_SetBinaryAvailable",
    107: "COM_SetDoublePrecision",
    109: "COM_SetSendDelay",
    112: "COM_SwitchOffTPS",
    111: "COM_SwitchOnTPS",
    5039: "CSV_CheckPower",
    5162: "CSV_GetCharging",
    5008: "CSV_GetDateTime",
    5051: "CSV_GetDateTime2",
    5117: "CSV_GetDateTimeCentiSec",
    5035: "CSV_GetDeviceConfig",
    5004: "CSV_GetInstrumentName",
    5003: "CSV_GetInstrumentNo",
    5011: "CSV_GetIntTemp",
    5041: "CSV_GetLaserlotIntens",
    5042: "CSV_GetLaserlotStatus",
    5114: "CSV_GetMaintenanceEnd",
    5164: "CSV_GetPreferredPowerSource",
    5100: "CSV_GetReflectorlessClass",
    5038: "CSV_GetSWCreationDate",
    5034: "CSV_GetSWVersion",
    5156: "CSV_GetStartUpMessageMode",
    5006: "CSV_GetUserInstrumentName",
    5009: "CSV_GetVBat",
    5010: "CSV_GetVMem",
    5165: "CSV_GetVoltage",
    5073: "CSV_List",
    5161: "CSV_SetCharging",
    5007: "CSV_SetDateTime",
    5050: "CSV_SetDateTime2",
    5040: "CSV_SetLaserlotIntens",
    5163: "CSV_SetPreferredPowerSource",
    5155: "CSV_SetStartUpMessageMode",
    5072: "CSV_SetupList",
    5005: "CSV_SetUserInstrumentName",
    5043: "CSV_SwitchLaserlot",
    12003: "CTL_GetUpCounter",
    29072: "DNA_GetCompassData",
    29108: "DNA_GetEarthCurvatureStatus",
    29109: "DNA_GetJobNumber",
    29005: "DNA_GetMeasResult",
    29011: "DNA_GetRodPos",
    29126: "DNA_GetStaffLength",
    29104: "DNA_GetTiltL",
    29070: "DNA_GetTiltX",
    29010: "DNA_SetRodPos",
    29127: "DNA_SetStaffLength",
    29068: "DNA_StartAutofocus",
    29036: "DNA_StartMeasurement",
    29107: "DNA_SwitchEarthCurvature",
    29110: "DNA_WakeUpInstrument",
    1044: "EDM_GetBumerang",
    1058: "EDM_GetEglIntensity",
    1041: "EDM_GetTrkLightBrightness",
    1040: "EDM_GetTrkLightSwitch",
    1070: "EDM_IsContMeasActive",
    1004: "EDM_Laserpointer",
    1010: "EDM_On",
    1061: "EDM_SetBoomerangFilter",
    1007: "EDM_SetBumerang",
    1059: "EDM_SetEglIntensity",
    1032: "EDM_SetTrkLightBrightness",
    1031: "EDM_SetTrkLightSwitch",
    23305: "FTR_AbortDownload",
    23308: "FTR_AbortList",
    23309: "FTR_Delete",
    23315: "FTR_DeleteDir",
    23304: "FTR_Download",
    23314: "FTR_DownloadXL",
    23307: "FTR_List",
    23303: "FTR_SetupDownload",
    23313: "FTR_SetupDownloadLarge",
    23306: "FTR_SetupList",
    23400: "IMG_GetTccConfig",
    23403: "IMG_SetExposureTime",
    23401: "IMG_SetTccConfig",
    23402: "IMG_TakeTccImage",
    20000: "IOS_BeepOff",
    20001: "IOS_BeepOn",
    23108: "KDM_GetLcdPower",
    23107: "KDM_SetLcdPower",
    6021: "MOT_ReadLockStatus",
    6004: "MOT_SetVelocity",
    6001: "MOT_StartController",
    6002: "MOT_StopController",
    14001: "SUP_GetConfig",
    14002: "SUP_SetConfig",
    14006: "SUP_SetPowerFailAutoRestart",
    14003: "SUP_SwitchLowTempControl",
    2008: "TMC_DoMeasure",
    2014: "TMC_GetAngSwitch",
    2003: "TMC_GetAngle1",
    2107: "TMC_GetAngle5",
    2029: "TMC_GetAtmCorr",
    2082: "TMC_GetCoordinate",
    2021: "TMC_GetEdmMode",
    2026: "TMC_GetFace",
    2167: "TMC_GetFullMeas",
    2011: "TMC_GetHeight",
    2007: "TMC_GetInclineSwitch",
    2023: "TMC_GetPrismCorr",
    2031: "TMC_GetRefractiveCorr",
    2091: "TMC_GetRefractiveMethod",
    2022: "TMC_GetSignal",
    2116: "TMC_GetSimpleCoord",
    2108: "TMC_GetSimpleMea",
    2126: "TMC_GetSlopeDistCorr",
    2009: "TMC_GetStation",
    2114: "TMC_IfDataAzeCorrError",
    2115: "TMC_IfDataIncCorrError",
    2117: "TMC_QuickDist",
    2016: "TMC_SetAngSwitch",
    2028: "TMC_SetAtmCorr",
    2020: "TMC_SetEdmMode",
    2019: "TMC_SetHandDist",
    2012: "TMC_SetHeight",
    2006: "TMC_SetInclineSwitch",
    2113: "TMC_SetOrientation",
    2024: "TMC_SetPrismCorr",
    2030: "TMC_SetRefractiveCorr",
    2090: "TMC_SetRefractiveMethod",
    2010: "TMC_SetStation",
    8011: "WIR_GetRecFormat",
    8012: "WIR_SetRecFormat",
}
"""Mapping of RPC numbers to GeoCom function names."""
