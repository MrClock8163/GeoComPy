"""
Description
===========

Module: ``geocompy.tps1000.rc``

This module contains the TPS1000 GeoCom return codes and function name
mapping for all subsystems, that are used during the parsing of an RPC
response.

Types
-----

- ``TPS1000RC``

"""
from ..protocols import GeoComReturnCode


class TPS1000RC(GeoComReturnCode):
    """
    TPS1000 GeoCom return codes from all subsystems.

    """

    def __bool__(self) -> bool:
        return self is TPS1000RC.OK

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
    """too less valid finepeaks"""

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
    ATA_HZ_FAIL = 527
    """No Spot detected in Hz-direction."""
    ATA_V_FAIL = 528
    """No Spot detected in V-direction."""
    ATA_HZ_STRANGE_L = 529
    """Strange light in Hz-direction."""
    ATA_V_STRANGE_L = 530
    """Strange light in V-direction."""

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
    WIR_SHF2_BUTTON = 5137
    """SHIFT F2 button pressed"""

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

    BAP_CHANGE_ALL_TO_DIST = 9217
    """Command changed from ALL to DIST"""


rpcnames: dict[int, str] = {
    9028: "AUT_ChangeFace4",
    9037: "AUT_FineAdjust3",
    9019: "AUT_GetATRStatus",
    9030: "AUT_GetFineAdjustMode",
    9021: "AUT_GetLockStatus",
    9013: "AUT_LockIn",
    9027: "AUT_MakePositioning4",
    9012: "AUT_ReadTimeout",
    9008: "AUT_ReadTol",
    9029: "AUT_Search2",
    9018: "AUT_SetATRStatus",
    9031: "AUT_SetFineAdjustMode",
    9020: "AUT_SetLockStatus",
    9011: "AUT_SetTimeout",
    9007: "AUT_SetTol",
    17003: "BAP_GetLastDisplayedError",
    17017: "BAP_MeasDistanceAngle",
    11004: "BMM_BeepAlarm",
    11003: "BMM_BeepNormal",
    11002: "BMM_BeepOff",
    11001: "BMM_BeepOn",
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
    5008: "CSV_GetDateTime",
    5035: "CSV_GetDeviceConfig",
    5004: "CSV_GetInstrumentName",
    5003: "CSV_GetInstrumentNo",
    5011: "CSV_GetIntTemp",
    5034: "CSV_GetSWVersion2",
    5006: "CSV_GetUserInstrumentName",
    5009: "CSV_GetVBat",
    5010: "CSV_GetVMem",
    5007: "CSV_SetDateTime",
    5005: "CSV_SetUserInstrumentName",
    12003: "CTL_GetUpCounter",
    1044: "EDM_GetBumerang",
    1041: "EDM_GetTrkLightBrightness",
    1040: "EDM_GetTrkLightSwitch",
    1004: "EDM_Laserpointer",
    1010: "EDM_On",
    1007: "EDM_SetBumerang",
    1032: "EDM_SetTrkLightBrightness",
    1031: "EDM_SetTrkLightSwitch",
    6021: "MOT_ReadLockStatus",
    6004: "MOT_SetVelocity",
    6001: "MOT_StartController",
    6002: "MOT_StopController",
    14001: "SUP_GetConfig",
    14002: "SUP_SetConfig",
    14003: "SUP_SwitchLowTempControl",
    2008: "TMC_DoMeasure",
    2003: "TMC_GetAngle1",
    2107: "TMC_GetAngle5",
    2014: "TMC_GetAngSwitch",
    2029: "TMC_GetAtmCorr",
    2082: "TMC_GetCoordinate1",
    2021: "TMC_GetEdmMode",
    2026: "TMC_GetFace",
    2011: "TMC_GetHeight",
    2007: "TMC_GetInclineSwitch",
    2023: "TMC_GetPrismCorr",
    2031: "TMC_GetRefractiveCorr",
    2091: "TMC_GetRefractiveMethod",
    2022: "TMC_GetSignal",
    2116: "TMC_GetSimpleCoord",
    2108: "TMC_GetSimpleMea",
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
    8012: "WIR_SetRecFormat"
}
"""Mapping of RPC numbers to GeoCom function names."""
