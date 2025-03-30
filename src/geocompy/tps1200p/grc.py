"""
``geocompy.tps1200p.grc``
=========================

This module contains the TPS1200+ GeoCom return codes and function name
mapping for all subsystems, that are used during the parsing of an RPC
response.

Types
-----

- ``TPS1200PGRC``

"""
from .. import GeoComReturnCode


class TPS1200PGRC(GeoComReturnCode):
    """
    TPS1200+ GeoCom return codes from all subsystems.

    """

    def __bool__(self) -> bool:
        return self is TPS1200PGRC.OK

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
    """Fatal error - subsystem not initialized."""
    SHUT_DOWN = 12
    """Subsystem is down."""
    SYSBUSY = 13
    """
    System busy/already in use of another process. Cannot execute
    function.
    """
    HWFAILURE = 14
    """Fatal error - hardware failure."""
    ABORT_APPL = 15
    """Execution of application has been aborted (SHIFT-ESC)."""
    LOW_POWER = 16
    """Operation aborted - insufficient power supply level."""
    IVVERSION = 17
    """Invalid version of file."""
    BATT_EMPTY = 18
    """Battery empty."""
    NO_EVENT = 20
    """No event pending."""
    OUT_OF_TEMP = 21
    """Out of temperature range."""
    INSTRUMENT_TILT = 22
    """Instrument tilting out of range."""
    COM_SETTING = 23
    """Communication error."""
    NO_ACTION = 24
    """Input 'do no action'."""
    SLEEP_MODE = 25
    """Instr. run into the sleep mode."""
    NOTOK = 26
    """Function not successfully completed."""
    NA = 27
    """Not available."""
    OVERFLOW = 28
    """Overflow error."""
    STOPPED = 29
    """System or subsystem has been stopped."""

    ANG_ERROR = 257
    """Angles and Inclinations not valid."""
    ANG_INCL_ERROR = 258
    """Inclinations not valid."""
    ANG_BAD_ACC = 259
    """Value accuracies not reached."""
    ANG_BAD_ANGLE_ACC = 260
    """Angle-accuracies not reached."""
    ANG_BAD_INCLIN_ACC = 261
    """Inclination accuracies not reached."""
    ANG_WRITE_PROTECTED = 266
    """No write access allowed."""
    ANG_OUT_OF_RANGE = 267
    """Value out of range."""
    ANG_IR_OCCURED = 268
    """Function aborted due to interrupt."""
    ANG_HZ_MOVED = 269
    """Hz moved during incline measurement."""
    ANG_OS_ERROR = 270
    """Troubles with operation system."""
    ANG_DATA_ERROR = 271
    """Overflow at parameter values."""
    ANG_PEAK_CNT_UFL = 272
    """Too less peaks."""
    ANG_TIME_OUT = 273
    """Reading timeout."""
    ANG_TOO_MANY_EXPOS = 274
    """Too many exposures wanted."""
    ANG_PIX_CTRL_ERR = 275
    """Picture height out of range."""
    ANG_MAX_POS_SKIP = 276
    """Positive exposure dynamic overflow."""
    ANG_MAX_NEG_SKIP = 277
    """Negative exposure dynamic overflow."""
    ANG_EXP_LIMIT = 278
    """Exposure time overflow."""
    ANG_UNDER_EXPOSURE = 279
    """Picture underexposured."""
    ANG_OVER_EXPOSURE = 280
    """Picture overexposured."""
    ANG_TMANY_PEAKS = 300
    """Too many peaks detected."""
    ANG_TLESS_PEAKS = 301
    """Too less peaks detected."""
    ANG_PEAK_TOO_SLIM = 302
    """Peak too slim."""
    ANG_PEAK_TOO_WIDE = 303
    """Peak to wide."""
    ANG_BAD_PEAKDIFF = 304
    """Bad peak difference."""
    ANG_UNDER_EXP_PICT = 305
    """Too less peak amplitude."""
    ANG_PEAKS_INHOMOGEN = 306
    """Inhomogeneous peak amplitudes."""
    ANG_NO_DECOD_POSS = 307
    """No peak decoding possible."""
    ANG_UNSTABLE_DECOD = 308
    """Peak decoding not stable."""
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
    """Current (loaded) firmware doesn't support upload."""
    ATA_PS_NOT_READY = 538
    """PS-System is not ready."""
    ATA_ATR_SYSTEM_ERR = 539
    """ATR system error."""

    EDM_SYSTEM_ERR = 769
    """
    Fatal EDM sensor error. See for the exact reason the original EDM
    sensor error number. In the most cases a service problem.
    """
    EDM_INVALID_COMMAND = 770
    """Invalid command or unknown command, see command syntax."""
    EDM_BOOM_ERR = 771
    """Boomerang error."""
    EDM_SIGN_LOW_ERR = 772
    """
    Received signal to low, prism to far away, or natural barrier, bad
    environment, etc.
    """
    EDM_DIL_ERR = 773
    """Obsolete."""
    EDM_SIGN_HIGH_ERR = 774
    """Received signal to strong, prism to near, stranger light effect."""
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
    """
    Search result invalid. For the exact explanation, see in the
    description of the called function.
    """
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
    """
    Calculated checksum, resp. received data wrong (only in binary
    communication mode possible).
    """
    EDM_INIT_OR_STOP_ERR = 789
    """
    During start up or shut down phase an error occured. It is saved in
    the DEL buffer.
    """
    EDM_SRL_NOT_AVAILABLE = 790
    """Red laser not available on this sensor HW."""
    EDM_MEAS_ABORTED = 791
    """
    Measurement will be aborted (will be used for the laser security).
    """
    EDM_SLDR_TRANSFER_PENDING = 798
    """Multiple OpenTransfer calls."""
    EDM_SLDR_TRANSFER_ILLEGAL = 799
    """No open transfer happened."""
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

    TMC_NO_FULL_CORRECTION = 1283
    """Warning: measurement without full correction."""
    TMC_ACCURACY_GUARANTEE = 1284
    """Info: accuracy can not be guarantee."""
    TMC_ANGLE_OK = 1285
    """Warning: only angle measurement valid."""
    TMC_ANGLE_NOT_FULL_CORR = 1288
    """
    Warning: only angle measurement valid but without full correction.
    """
    TMC_ANGLE_NO_ACC_GUARANTY = 1289
    """
    Info: only angle measurement valid but accuracy can not be guarantee.
    """
    TMC_ANGLE_ERROR = 1290
    """Error: no angle measurement."""
    TMC_DIST_PPM = 1291
    """Error: wrong setting of PPM or MM on EDM."""
    TMC_DIST_ERROR = 1292
    """Error: distance measurement not done (no aim, etc.)."""
    TMC_BUSY = 1293
    """Error: system is busy (no measurement done)."""
    TMC_SIGNAL_ERROR = 1294
    """Error: no signal on EDM (only in signal mode)."""

    MOT_UNREADY = 1792
    """Motorization is not ready."""
    MOT_BUSY = 1793
    """Motorization is handling another task."""
    MOT_NOT_OCONST = 1794
    """Motorization is not in velocity mode."""
    MOT_NOT_CONFIG = 1795
    """Motorization is in the wrong mode or busy."""
    MOT_NOT_POSIT = 1796
    """Motorization is not in posit mode."""
    MOT_NOT_SERVICE = 1797
    """Motorization is not in service mode."""
    MOT_NOT_BUSY = 1798
    """Motorization is handling no task."""
    MOT_NOT_LOCK = 1799
    """Motorization is not in tracking mode."""
    MOT_NOT_SPIRAL = 1800
    """Motorization is not in spiral mode."""
    MOT_V_ENCODER = 1801
    """Certical encoder/motor error."""
    MOT_HZ_ENCODER = 1802
    """Horizontal encoder/motor error."""
    MOT_HZ_V_ENCODER = 1803
    """Horizontal and vertical encoder/motor error."""

    BMM_XFER_PENDING = 2305
    """Loading process already opened."""
    BMM_NO_XFER_OPEN = 2306
    """Transfer not opened."""
    BMM_UNKNOWN_CHARSET = 2307
    """Unknown character set."""
    BMM_NOT_INSTALLED = 2308
    """Display module not present."""
    BMM_ALREADY_EXIST = 2309
    """Character set already exists."""
    BMM_CANT_DELETE = 2310
    """Character set cannot be deleted."""
    BMM_MEM_ERROR = 2311
    """Memory cannot be allocated."""
    BMM_CHARSET_USED = 2312
    """Character set still used."""
    BMM_CHARSET_SAVED = 2313
    """Charset cannot be deleted or is protected."""
    BMM_INVALID_ADR = 2314
    """Attempt to copy a character block outside the allocated memory."""
    BMM_CANCELANDADR_ERROR = 2315
    """Error during release of allocated memory."""
    BMM_INVALID_SIZE = 2316
    """
    Number of bytes specified in header does not match the bytes read.
    """
    BMM_CANCELANDINVSIZE_ERROR = 2317
    """Allocated memory could not be released."""
    BMM_ALL_GROUP_OCC = 2318
    """Max. number of character sets already loaded."""
    BMM_CANT_DEL_LAYERS = 2319
    """Layer cannot be deleted."""
    BMM_UNKNOWN_LAYER = 2320
    """Required layer does not exist."""
    BMM_INVALID_LAYERLEN = 2321
    """Layer length exceeds maximum."""

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
    """TRANSACTIONS ID mismatch error."""
    COM_NOT_GEOCOM = 3094
    """Protocol not recognizable."""
    COM_UNKNOWN_PORT = 3095
    """(WIN) Invalid port address."""
    COM_ERO_END = 3099
    """ERO is terminating."""
    COM_OVERRUN = 3100
    """Internal error: data buffer overflow."""
    COM_SRVR_RX_CHECKSUM_ERRR = 3101
    """Invalid checksum on server side received."""
    COM_CLNT_RX_CHECKSUM_ERRR = 3102
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
    """Att to send cons reqs"""
    COM_SRVR_IS_SLEEPING = 3108
    """TPS has gone to sleep. Wait and try again."""
    COM_SRVR_IS_OFF = 3109
    """TPS has shut down. Wait and try again."""
    COM_NO_CHECKSUM = 3110
    """No checksum in ASCII protocol available."""

    AUT_TIMEOUT = 8704
    """Position not reached."""
    AUT_DETENT_ERROR = 8705
    """Positioning not possible due to mounted EDM."""
    AUT_ANGLE_ERROR = 8706
    """Angle measurement error."""
    AUT_MOTOR_ERROR = 8707
    """Motorisation error."""
    AUT_INCACC = 8708
    """Position not exactly reached."""
    AUT_DEV_ERROR = 8709
    """Deviation measurement error."""
    AUT_NO_TARGET = 8710
    """No target detected."""
    AUT_MULTIPLE_TARGETS = 8711
    """Multiple target detected."""
    AUT_BAD_ENVIRONMENT = 8712
    """Bad environment conditions."""
    AUT_DETECTOR_ERROR = 8713
    """Error in target acquisition."""
    AUT_NOT_ENABLED = 8714
    """Target acquisition not enabled."""
    AUT_CALACC = 8715
    """ATR-Calibration failed."""
    AUT_ACCURACY = 8716
    """Target position not exactly reached."""
    AUT_DIST_STARTED = 8717
    """Info: dist. measurement has been started."""
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
    KDM_NOT_AVAILABLE = 12544
    """KDM device is not available."""
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


rpcnames: dict[int, str] = {
    18006: "AUS_GetUserAtrState",
    18008: "AUS_GetUserLockState",
    18005: "AUS_SetUserAtrState",
    18007: "AUS_SetUserLockState",
    9028: "AUT_ChangeFace",
    9037: "AUT_FineAdjust",
    9030: "AUT_GetFineAdjustMode",
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
    9031: "AUT_SetFineAdjustMode",
    9043: "AUT_SetSearchArea",
    9011: "AUT_SetTimeout",
    9007: "AUT_SetTol",
    9041: "AUT_SetUserSpiral",
    17018: "BAP_GetMeasPrg",
    17023: "BAP_GetPrismDef",
    17009: "BAP_GetPrismType",
    17031: "BAP_GetPrismType",
    17022: "BAP_GetTargetType",
    17033: "BAP_GetUserPrismDef",
    17017: "BAP_MeasDistanceAngle",
    17020: "BAP_SearchTarget",
    17019: "BAP_SetMeasPrg",
    17008: "BAP_SetPrismType",
    17030: "BAP_SetPrismType",
    17021: "BAP_SetTargetType",
    17032: "BAP_SetUserPrismDef",
    11004: "BMM_BeepAlarm",
    11003: "BMM_BeepNormal",
    113: "COM_GetBinaryAvailable",
    108: "COM_GetDoublePrecision",
    110: "COM_GetSWVersion",
    0: "COM_NullProc",
    114: "COM_SetBinaryAvailable",
    107: "COM_SetDoublePrecision",
    112: "COM_SwitchOffTPS",
    111: "COM_SwitchOnTPS",
    5008: "CSV_GetDateTime",
    5117: "CSV_GetDateTimeCentiSec",
    5035: "CSV_GetDeviceConfig",
    5004: "CSV_GetInstrumentName",
    5003: "CSV_GetInstrumentNo",
    5011: "CSV_GetIntTemp",
    5100: "CSV_GetReflectorlessClass",
    5034: "CSV_GetSWVersion",
    5007: "CSV_SetDateTime",
    5039: "CSV_CheckPower",
    1058: "EDM_GetEglIntensity",
    1004: "EDM_Laserpointer",
    1059: "EDM_SetEglIntensity",
    23400: "IMG_GetTccConfig",
    23401: "IMG_SetTccConfig",
    23402: "IMG_TakeTccImage",
    20000: "IOS_BeepOff",
    20001: "IOS_BeepOn",
    6021: "MOT_ReadLockStatus",
    6004: "MOT_SetVelocity",
    6001: "MOT_StartController",
    6002: "MOT_StopController",
    14001: "SUP_GetConfig",
    14002: "SUP_SetConfig",
    2008: "TMC_DoMeasure",
    2003: "TMC_GetAngle1",
    2107: "TMC_GetAngle5",
    2014: "TMC_GetAngSwitch",
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
    2030: "TMC_SetRefractiveCorr",
    2090: "TMC_SetRefractiveMethod",
    2010: "TMC_SetStation",
}
"""Mapping of RPC numbers to GeoCom function names."""
