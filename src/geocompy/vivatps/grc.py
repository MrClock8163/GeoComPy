from .. import GeoComReturnCode


class VivaTPSGRC(GeoComReturnCode):
    def __bool__(self) -> bool:
        return self is VivaTPSGRC.OK

    OK = 0
    UNDEFINED = 1
    IVPARAM = 2
    IVRESULT = 3
    FATAL = 4
    NOT_IMPL = 5
    TIME_OUT = 6
    SET_INCOMPL = 7
    ABORT = 8
    NOMEMORY = 9
    NOTINIT = 10
    SHUT_DOWN = 12
    SYSBUSY = 13
    HWFAILURE = 14
    ABORT_APPL = 15
    LOW_POWER = 16
    IVVERSION = 17
    BATT_EMPTY = 18
    NO_EVENT = 20
    OUT_OF_TEMP = 21
    INSTRUMENT_TILT = 22
    COM_SETTING = 23
    NO_ACTION = 24
    SLEEP_MODE = 25
    NOTOK = 26
    NA = 27
    OVERFLOW = 28
    STOPPED = 29

    ANG_ERROR = 257
    ANG_INCL_ERROR = 258
    ANG_BAD_ACC = 259
    ANG_BAD_ANGLE_ACC = 260
    ANG_BAD_INCLIN_ACC = 261
    ANG_WRITE_PROTECTED = 266
    ANG_OUT_OF_RANGE = 267
    ANG_IR_OCCURED = 268
    ANG_HZ_MOVED = 269
    ANG_OS_ERROR = 270
    ANG_DATA_ERROR = 271
    ANG_PEAK_CNT_UFL = 272
    ANG_TIME_OUT = 273
    ANG_TOO_MANY_EXPOS = 274
    ANG_PIX_CTRL_ERR = 275
    ANG_MAX_POS_SKIP = 276
    ANG_MAX_NEG_SKIP = 277
    ANG_EXP_LIMIT = 278
    ANG_UNDER_EXPOSURE = 279
    ANG_OVER_EXPOSURE = 280
    ANG_TMANY_PEAKS = 300
    ANG_TLESS_PEAKS = 301
    ANG_PEAK_TOO_SLIM = 302
    ANG_PEAK_TOO_WIDE = 303
    ANG_BAD_PEAKDIFF = 304
    ANG_UNDER_EXP_PICT = 305
    ANG_PEAKS_INHOMOGEN = 306
    ANG_NO_DECOD_POSS = 307
    ANG_UNSTABLE_DECOD = 308
    ANG_TLESS_FPEAKS = 309
    ANG_INCL_OLD_PLANE = 316
    ANG_INCL_NO_PLANE = 317
    ANG_FAST_ANG_ERR = 326
    ANG_FAST_ANG_ERR_5 = 327
    ANG_FAST_ANG_ERR_25 = 328
    ANG_TRANS_ERR = 329
    ANG_TRANS_ERR_5 = 330
    ANG_TRANS_ERR_25 = 331

    ATA_NOT_READY = 512
    ATA_NO_RESULT = 513
    ATA_SEVERAL_TARGETS = 514
    ATA_BIG_SPOT = 515
    ATA_BACKGROUND = 516
    ATA_NO_TARGETS = 517
    ATA_NOT_ACCURAT = 518
    ATA_SPOT_ON_EDGE = 519
    ATA_BLOOMING = 522
    ATA_NOT_BUSY = 523
    ATA_STRANGE_LIGHT = 524
    ATA_V24_FAIL = 525
    ATA_DECODE_ERROR = 526
    ATA_HZ_FAIL = 527
    ATA_V_FAIL = 528
    ATA_HZ_STRANGE_L = 529
    ATA_V_STRANGE_L = 530
    ATA_SLDR_TRANSFER_PENDING = 531
    ATA_SLDR_TRANSFER_ILLEGAL = 532
    ATA_SLDR_DATA_ERROR = 533
    ATA_SLDR_CHK_SUM_ERROR = 534
    ATA_SLDR_ADDRESS_ERROR = 535
    ATA_SLDR_INV_LOADFILE = 536
    ATA_SLDR_UNSUPPORTED = 537
    ATA_PS_NOT_READY = 538
    ATA_ATR_SYSTEM_ERR = 539

    EDM_SYSTEM_ERR = 769
    EDM_INVALID_COMMAND = 770
    EDM_BOOM_ERR = 771
    EDM_SIGN_LOW_ERR = 772
    EDM_DIL_ERR = 773
    EDM_SIGN_HIGH_ERR = 774
    EDM_TIMEOUT = 775
    EDM_FLUKT_ERR = 776
    EDM_FMOT_ERR = 777
    EDM_DEV_NOT_INSTALLED = 778
    EDM_NOT_FOUND = 779
    EDM_ERROR_RECEIVED = 780
    EDM_MISSING_SRVPWD = 781
    EDM_INVALID_ANSWER = 782
    EDM_SEND_ERR = 783
    EDM_RECEIVE_ERR = 784
    EDM_INTERNAL_ERR = 785
    EDM_BUSY = 786
    EDM_NO_MEASACTIVITY = 787
    EDM_CHKSUM_ERR = 788
    EDM_INIT_OR_STOP_ERR = 789
    EDM_SRL_NOT_AVAILABLE = 790
    EDM_MEAS_ABORTED = 791
    EDM_SLDR_TRANSFER_PENDING = 798
    EDM_SLDR_TRANSFER_ILLEGAL = 799
    EDM_SLDR_DATA_ERROR = 800
    EDM_SLDR_CHK_SUM_ERROR = 801
    EDM_SLDR_ADDR_ERROR = 802
    EDM_SLDR_INV_LOADFILE = 803
    EDM_SLDR_UNSUPPORTED = 804
    EDM_UNKNOW_ERR = 808
    EDM_DISTRANGE_ERR = 818
    EDM_SIGNTONOISE_ERR = 819
    EDM_NOISEHIGH_ERR = 820
    EDM_PWD_NOTSET = 821
    EDM_ACTION_NO_MORE_VALID = 822
    EDM_MULTRG_ERR = 823
    EDM_MISSING_EE_CONSTS = 824
    EDM_NOPRECISE = 825
    EDM_MEAS_DIST_NOT_ALLOWED = 826
    EDM_NOT_EXECUTED = 827
    EDM_SIG_FORM_ERR = 828
    EDM_DIST_TOO_SHORT = 829
    EDM_SYNTH_ERR = 830
    EDM_AMPL_RELATION_ERR = 831
    EDM_DIVISION_BY_ZERO = 832

    TMC_NO_FULL_CORRECTION = 1283
    TMC_ACCURACY_GUARANTEE = 1284
    TMC_ANGLE_OK = 1285
    TMC_ANGLE_NOT_FULL_CORR = 1288
    TMC_ANGLE_NO_ACC_GUARANTY = 1289
    TMC_ANGLE_ERROR = 1290
    TMC_DIST_PPM = 1291
    TMC_DIST_ERROR = 1292
    TMC_BUSY = 1293
    TMC_SIGNAL_ERROR = 1294
    TMC_OLD_PLANE = 1380
    TMC_NO_PLANE = 1381
    TMC_INC_ERROR = 1392
    TMC_INCLINE_ACC = 1383

    MOT_UNREADY = 1792
    MOT_BUSY = 1793
    MOT_NOT_OCONST = 1794
    MOT_NOT_CONFIG = 1795
    MOT_NOT_POSIT = 1796
    MOT_NOT_SERVICE = 1797
    MOT_NOT_BUSY = 1798
    MOT_NOT_LOCK = 1799
    MOT_NOT_SPIRAL = 1800
    MOT_V_ENCODER = 1801
    MOT_HZ_ENCODER = 1802
    MOT_HZ_V_ENCODER = 1803
    MOT_HZ_MOTOR_ERROR = 1804
    MOT_V_MOTOR_ERROR = 1805
    MOT_TIMEOUT = 1806
    MOT_HZ_TIMEOUT = 1807
    MOT_V_TIMEOUT = 1808
    MOT_SCAN_STOPPED = 1809
    MOT_SUPPLY_CHANGED = 1810

    # BMM_XFER_PENDING = 2305
    # BMM_NO_XFER_OPEN = 2306
    # BMM_UNKNOWN_CHARSET = 2307
    # BMM_NOT_INSTALLED = 2308
    # BMM_ALREADY_EXIST = 2309
    # BMM_CANT_DELETE = 2310
    # BMM_MEM_ERROR = 2311
    # BMM_CHARSET_USED = 2312
    # BMM_CHARSET_SAVED = 2313
    # BMM_INVALID_ADR = 2314
    # BMM_CANCELANDADR_ERROR = 2315
    # BMM_INVALID_SIZE = 2316
    # BMM_CANCELANDINVSIZE_ERROR = 2317
    # BMM_ALL_GROUP_OCC = 2318
    # BMM_CANT_DEL_LAYERS = 2319
    # BMM_UNKNOWN_LAYER = 2320
    # BMM_INVALID_LAYERLEN = 2321

    COM_ERO = 3072
    COM_CANT_ENCODE = 3073
    COM_CANT_DECODE = 3074
    COM_CANT_SEND = 3075
    COM_CANT_RECV = 3076
    COM_TIMEDOUT = 3077
    COM_WRONG_FORMAT = 3078
    COM_VER_MISMATCH = 3079
    COM_CANT_DECODE_REQ = 3080
    COM_PROC_UNAVAIL = 3081
    COM_CANT_ENCODE_REP = 3082
    COM_SYSTEM_ERR = 3083
    COM_FAILED = 3085
    COM_NO_BINARY = 3086
    COM_INTR = 3087
    COM_REQUIRES_8DBITS = 3090
    COM_TR_ID_MISMATCH = 3093
    COM_NOT_GEOCOM = 3094
    COM_UNKNOWN_PORT = 3095
    COM_ERO_END = 3099
    COM_OVERRUN = 3100
    COM_SRVR_RX_CHECKSUM_ERRR = 3101
    COM_CLNT_RX_CHECKSUM_ERRR = 3102
    COM_PORT_NOT_AVAILABLE = 3103
    COM_PORT_NOT_OPEN = 3104
    COM_NO_PARTNER = 3105
    COM_ERO_NOT_STARTED = 3106
    COM_CONS_REQ = 3107
    COM_SRVR_IS_SLEEPING = 3108
    COM_SRVR_IS_OFF = 3109
    COM_NO_CHECKSUM = 3110

    AUT_TIMEOUT = 8704
    AUT_DETENT_ERROR = 8705
    AUT_ANGLE_ERROR = 8706
    AUT_MOTOR_ERROR = 8707
    AUT_INCACC = 8708
    AUT_DEV_ERROR = 8709
    AUT_NO_TARGET = 8710
    AUT_MULTIPLE_TARGETS = 8711
    AUT_BAD_ENVIRONMENT = 8712
    AUT_DETECTOR_ERROR = 8713
    AUT_NOT_ENABLED = 8714
    AUT_CALACC = 8715
    AUT_ACCURACY = 8716
    AUT_DIST_STARTED = 8717
    AUT_SUPPLY_TOO_LOW = 8719
    AUT_NO_WORKING_AREA = 8720
    AUT_ARRAY_FULL = 8721
    AUT_NO_DATA = 8722
    AUT_SIDECOVER_ERR = 8723
    AUT_OUT_OF_SYNC = 8724
    AUT_NO_LOCK = 8725

    KDM_NOT_AVAILABLE = 12544

    FTR_FILEACCESS = 13056
    FTR_WRONGFILEBLOCKNUMBER = 13057
    FTR_NOTENOUGHSPACE = 13058
    FTR_INVALIDINPUT = 13059
    FTR_MISSINGSETUP = 13060

    CAM_NOT_READY = 13824
    CAM_NOT_INIT = 13825
    CAM_IMG_NOT_AVAILABLE = 13826
    CAM_IMAGE_SAVING_ERROR = 13828
    CAM_BIT_DEPTH_ERROR = 13834
    CAM_OUT_OF_MEMORY = 13835
    CAM_SPOT_NOT_AVAIL = 13836
    CAM_NO_SPOTS_INLIST = 13837
    CAM_NO_TARGET = 13838
    CAM_TARGET_NOT_FOUND = 13839
    CAM_NO_CALIB_INPUT_DATA = 13844
    CAM_MEAS_NOT_ACCURATE = 13845
    CAM_DIRTY = 13854
    AF_FAILED = 13864


rpcnames: dict[int, str] = {
    18006: "AUS_GetUserAtrState",
    18008: "AUS_GetUserLockState",
    18005: "AUS_SetUserAtrState",
    18007: "AUS_SetUserLockState",
    9081: "AUT_CAM_PositToPixelCoord",
    9028: "AUT_ChangeFace",
    9037: "AUT_FineAdjust",
    9030: "AUT_GetFineAdjustMode",
    9102: "AUT_GetLockFlyMode",
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
    9103: "AUT_SetLockFlyMode",
    9043: "AUT_SetSearchArea",
    9011: "AUT_SetTimeout",
    9007: "AUT_SetTol",
    9041: "AUT_SetUserSpiral",
    17039: "BAP_GetATRPrecise",
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
    17008: "BAP_SetPrismType",
    17030: "BAP_SetPrismType2",
    17021: "BAP_SetTargetType",
    17032: "BAP_SetUserPrismDef",
    11004: "BMM_BeepAlarm",
    11003: "BMM_BeepNormal",
    23669: "CAM_AF_ContinuousAutofocus",
    23663: "CAM_AF_FocusContrastArroundCurrent",
    23668: "CAM_AF_GetChipWindowSize",
    23644: "CAM_AF_GetMotorPosition",
    23652: "CAM_AF_PositFocusMotorToDist",
    23677: "CAM_AF_PositFocusMotorToInfinity",
    23645: "CAM_AF_SetMotorPosition",
    23662: "CAM_AF_SingleShotAutofocus",
    23619: "CAM_GetCameraFoV",
    23636: "CAM_GetCameraPowerSwitch",
    23611: "CAM_GetCamPos",
    23613: "CAM_GetCamViewingDir",
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
    113: "COM_GetBinaryAvailable",
    108: "COM_GetDoublePrecision",
    110: "COM_GetSWVersion",
    0: "COM_NullProc",
    114: "COM_SetBinaryAvailable",
    107: "COM_SetDoublePrecision",
    112: "COM_SwitchOffTPS",
    111: "COM_SwitchOnTPS",
    5039: "CSV_CheckPower",
    5162: "CSV_GetCharging",
    5008: "CSV_GetDateTime",
    5117: "CSV_GetDateTimeCentiSec",
    5035: "CSV_GetDeviceConfig",
    5004: "CSV_GetInstrumentName",
    5003: "CSV_GetInstrumentNo",
    5011: "CSV_GetIntTemp",
    5041: "CSV_GetLaserlotIntens",
    5042: "CSV_GetLaserlotStatus",
    5164: "CSV_GetPreferredPowerSource",
    5100: "CSV_GetReflectorlessClass",
    5156: "CSV_GetStartUpMessageMode",
    5034: "CSV_GetSWVersion",
    5165: "CSV_GetVoltage",
    5161: "CSV_SetCharging",
    5007: "CSV_SetDateTime",
    5040: "CSV_SetLaserlotIntens",
    5163: "CSV_SetPreferredPowerSource",
    5155: "CSV_SetStartUpMessageMode",
    5043: "CSV_SwitchLaserlot",
    1058: "EDM_GetEglIntensity",
    1070: "EDM_IsContMeasActive",
    1004: "EDM_Laserpointer",
    1061: "EDM_SetBoomerangFilter",
    1059: "EDM_SetEglIntensity",
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
    2024: "TMC_SetPrismCorr",
    2030: "TMC_SetRefractiveCorr",
    2090: "TMC_SetRefractiveMethod",
    2010: "TMC_SetStation"
}
