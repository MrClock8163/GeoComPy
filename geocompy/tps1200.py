from __future__ import annotations

import re
from typing import Callable, Any
from types import TracebackType
from enum import Enum

from serial import Serial, SerialException, SerialTimeoutException

from .communication import (
    Connection,
    parsebyte,
    parsestr,
    tostr,
    tobyte,
    toenum
)

from . import (
    GeoComProtocol,
    GeoComSubsystem,
    GeoComResponse,
    GeoComReturnCode
)


class TPS1200GRC(GeoComReturnCode):
    def __bool__(self) -> bool:
        return self is TPS1200GRC.OK

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
    SHUT_DOWN = 11
    SYSBUSY = 12
    HWFAILURE = 13
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
    ANG_PEAL_TOO_WIDE = 303
    ANG_BAD_PEAKDIFF = 304
    ANG_UNDER_EXP_PICT = 305
    ANG_PEAKS_INHOMOGEN = 306
    ANG_NO_DECOD_POSS = 307
    ANG_UNSTABLE_DECOD = 308
    ANG_TLESS_FPEAKS = 309

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

    MOT_UNREADY = 1792
    MOT_BUSY = 1793
    MOT_NOT_OCONST = 1794
    MOT_NOT_CONFIG = 1795
    MOT_NOT_POSIT = 1796
    MOT_NOT_SERVICE = 1797
    MOT_NOT_BUSY = 1798
    MOT_NOT_LOCK = 1799
    MOT_NOT_SPIRAL = 1800

    BMM_XFER_PENDING = 2305
    BMM_NO_XFER_OPEN = 2306
    BMM_UNKNOWN_CHARSET = 2307
    BMM_NOT_INSTALLED = 2308
    BMM_ALREADY_EXIST = 2309
    BMM_CANT_DELETE = 2310
    BMM_MEM_ERROR = 2311
    BMM_CHARSET_USED = 2312
    BMM_CHARSET_SAVED = 2313
    BMM_INVALID_ADR = 2314
    BMM_CANCELANDADR_ERROR = 2315
    BMM_INVALID_SIZE = 2316
    BMM_CANCELANDINVSIZE_ERROR = 2317
    BMM_ALL_GROUP_OCC = 2318
    BMM_CANT_DEL_LAYERS = 2319
    BMM_UNKNOWN_LAYER = 2320
    BMM_INVALID_LAYERLEN = 2321

    COM_ERO = 3072
    COM_CANT_ENCODE = 3073
    COM_CANT_DECODE = 3074
    COM_CANT_SEND = 3075
    COM_CANT_RECV = 3076
    COM_TIMEOUT = 3077
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
    COM_SRVR_RX_CHECKSUM_ERROR = 3101
    COM_CLNT_RX_CHECKSUM_ERROR = 3102
    COM_PORT_NOT_AVAILABLE = 3103
    COM_PORT_NOT_OPEN = 3104
    COM_NO_PARTNER = 3105
    COM_ERO_NOT_STARTED = 3106
    COM_CONS_REQ = 3107
    COM_SRVR_IS_SLEEPING = 3108
    COM_SRVR_IS_OFF = 3109

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
    AUT_SUPPLY_TOO_HIGH = 8718
    AUT_SUPPLY_TOO_LOW = 8719
    AUT_NO_WORKING_AREA = 8720
    AUT_ARRAY_FULL = 8721
    AUT_NO_DATA = 8722

    AUT_NOT_AVAILABLE = 12544

    FTR_FILEACCESS = 13056
    FTR_WRONGFILEBLOCKNUMBER = 13057
    FTR_NOTENOUGHSPACE = 13058
    FTR_INVALIDINPUT = 13059
    FTR_MISSINGSETUP = 13060


class TPS1200Subsystem(GeoComSubsystem):
    def __init__(self, parent: TPS1200):
        self._parent: TPS1200 = parent


class TPS1200AUS(TPS1200Subsystem):
    class ONOFF(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200AUS.ONOFF:
            return cls(int(value))

        OFF = 0
        ON = 1

    def get_user_atr_state(self) -> GeoComResponse:
        cmd = "%R1Q,18006:"
        return self._parent.exec1(
            cmd,
            {"state": TPS1200AUS.ONOFF.parse}
        )

    def set_user_atr_state(self, state: ONOFF | str) -> GeoComResponse:
        _state = toenum(TPS1200AUS.ONOFF, state)
        cmd = f"%R1Q,18005:{_state.value:d}"
        return self._parent.exec1(cmd)

    def get_user_lock_state(self) -> GeoComResponse:
        cmd = "%R1Q,18008:"
        return self._parent.exec1(
            cmd,
            {"state": TPS1200AUS.ONOFF.parse}
        )

    def set_user_lock_state(self, state: ONOFF) -> GeoComResponse:
        cmd = f"%R1Q,18007:{state.value:d}"
        return self._parent.exec1(cmd)


class TPS1200AUT(GeoComSubsystem):
    class POSMODE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200AUT.POSMODE:
            return cls(int(value))

        NORMAL = 0
        PRECISE = 1

    class ADJMODE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200AUT.ADJMODE:
            return cls(int(value))

        NORMAL_MODE = 0
        POINT_MODE = 1

    class ATRMODE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200AUT.ATRMODE:
            return cls(int(value))

        POSITION = 0
        TARGET = 1

    class DIRECTION(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200AUT.DIRECTION:
            return cls(int(value))

        CLOCKWISE = 1
        ANTICLOCKWISE = -1

    def __init__(self, parent: TPS1200):
        self._parent: TPS1200 = parent

    def read_tol(self) -> GeoComResponse:
        cmd = "%R1Q,9008:"
        return self._parent.exec1(
            cmd,
            {
                "tol_hz": float,
                "tol_v": float
            }
        )

    def set_tol(self, tol_hz: float, tol_v: float) -> GeoComResponse:
        cmd = f"%R1Q,9007:{tol_hz:f},{tol_v:f}"
        return self._parent.exec1(cmd)

    def read_timeout(self) -> GeoComResponse:
        cmd = "%R1Q,9012:"
        return self._parent.exec1(
            cmd,
            {
                "to_hz": float,
                "to_v": float
            }
        )

    def set_timeout(self, to_hz: float, to_v: float) -> GeoComResponse:
        cmd = f"%R1Q,9011:{to_hz:f},{to_v:f}"
        return self._parent.exec1(cmd)

    def make_positioning(
        self,
        hz: float,
        v: float,
        posmode: TPS1200AUT.POSMODE | str = POSMODE.NORMAL,
        atrmode: TPS1200AUT.ATRMODE | str = ATRMODE.POSITION
    ) -> GeoComResponse:
        _posmode = toenum(TPS1200AUT.POSMODE, posmode)
        _atrmode = toenum(TPS1200AUT.ATRMODE, atrmode)
        cmd = (
            f"%R1Q,9027:{hz:f},{v:f},"
            f"{_posmode.value:d},{_atrmode.value},0"
        )
        return self._parent.exec1(cmd)

    def change_face(
        self,
        posmode: TPS1200AUT.POSMODE | str = POSMODE.NORMAL,
        atrmode: TPS1200AUT.ATRMODE | str = ATRMODE.POSITION
    ) -> GeoComResponse:
        _posmode = toenum(TPS1200AUT.POSMODE, posmode)
        _atrmode = toenum(TPS1200AUT.ATRMODE, atrmode)
        cmd = f"%R1Q,9028:{_posmode.value:d},{_atrmode.value},0"
        return self._parent.exec1(cmd)

    def fine_adjust(self, width: float, height: float) -> GeoComResponse:
        cmd = f"%R1Q,9037:{width:f},{height:f},0"
        return self._parent.exec1(cmd)

    def search(self, width: float, height: float) -> GeoComResponse:
        cmd = f"%R1Q,9029:{width:f},{height:f},0"
        return self._parent.exec1(cmd)

    def get_fine_adjust_mode(self) -> GeoComResponse:
        cmd = "%R1Q,9030:"
        return self._parent.exec1(cmd, {"adjmode": TPS1200AUT.ADJMODE.parse})

    def set_fine_adjust_mode(
        self,
        adjmode: TPS1200AUT.ADJMODE | str
    ) -> GeoComResponse:
        _adjmode = toenum(TPS1200AUT.ADJMODE, adjmode)
        cmd = f"%R1Q,9031:{_adjmode.value:d}"
        return self._parent.exec1(cmd)

    def lock_in(self) -> GeoComResponse:
        return self._parent.exec1("%R1Q,9013:")

    def get_search_area(self) -> GeoComResponse:
        return self._parent.exec1(
            "%R1Q,9042:",
            {
                "hz": float,
                "v": float,
                "width": float,
                "height": float,
                "enabled": bool
            }
        )

    def set_search_area(
        self,
        hz: float,
        v: float,
        width: float,
        height: float,
        enabled: bool = True
    ) -> GeoComResponse:
        cmd = f"%R1Q,9043:{hz:f},{v:f},{width:f},{height:f},{enabled:d}"
        return self._parent.exec1(cmd)

    def get_user_spiral(self) -> GeoComResponse:
        return self._parent.exec1(
            "%R1Q,9040:",
            {
                "width": float,
                "height": float
            }
        )

    def set_user_spiral(
        self,
        width: float,
        height: float
    ) -> GeoComResponse:
        cmd = f"%R1Q,9041:{width:f},{height:f}"
        return self._parent.exec1(cmd)

    def ps_enable_range(self, enable: bool) -> GeoComResponse:
        return self._parent.exec1(f"%R1Q,9048:{enable:d}")

    def ps_set_range(
        self,
        closest: int,
        farthest: int
    ) -> GeoComResponse:
        return self._parent.exec1(f"%R1Q,9047:{closest:d},{farthest:d}")

    def ps_search_window(self) -> GeoComResponse:
        return self._parent.exec1("%R1Q,9052:")

    def ps_search_next(
        self,
        direction: DIRECTION | str,
        swing: bool
    ) -> GeoComResponse:
        _direction = toenum(TPS1200AUT.DIRECTION, direction)
        return self._parent.exec1(
            f"%R1Q,9051:{_direction.value:d},{swing:d}"
        )


class TPS1200BAP(TPS1200Subsystem):
    class MEASUREPRG(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200BAP.MEASUREPRG:
            return cls(int(value))

        NO_MEAS = 0
        NO_DIST = 1
        DEF_DIST = 2
        CLEAR_DIST = 5
        STOP_TRK = 6

    class USERMEASPRG(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200BAP.USERMEASPRG:
            return cls(int(value))

        SINGLE_REF_STANDARD = 0
        SINGLE_REF_FAST = 1
        SINGLE_REF_VISIBLE = 2
        SINGLE_RLESS_VISIBLE = 3
        CONT_REF_STANDARD = 4
        CONT_REF_FAST = 5
        CONT_RLESS_VISIBLE = 6
        AVG_REF_STANDARD = 7
        AVG_REF_VISIBLE = 8
        AVG_RLESS_VISIBLE = 9

    class PRISMTYPE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200BAP.PRISMTYPE:
            return cls(int(value))

        ROUND = 0
        MINI = 1
        TAPE = 2
        THREESIXTY = 3
        USER1 = 4
        USER2 = 5
        USER3 = 6
        MINI_360 = 7
        MINI_ZERO = 8
        USER = 9
        NDS_TAPE = 10

    class REFLTYPE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200BAP.REFLTYPE:
            return cls(int(value))

        UNDEF = 0
        PRISM = 1
        TAPE = 2

    class TARGETTYPE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200BAP.TARGETTYPE:
            return cls(int(value))

        REFL_USE = 0
        REFL_LESS = 1

    class ATRSETTING(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200BAP.ATRSETTING:
            return cls(int(value))

        LOWVIS_NORMAL = 0
        LOWVIS_ON = 1
        LOWVIS_ALWAYSON = 2
        LOWVIS_BOBBYON = 3
        LOWVIS_BOBBYALWAYSON = 4

    class ONOFF(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200BAP.ONOFF:
            return cls(int(value))

        OFF = 0
        ON = 1

    def get_target_type(self) -> GeoComResponse:
        return self._parent.exec1(
            "%R1Q,17022:",
            {"targettype": TPS1200BAP.TARGETTYPE.parse}
        )

    def set_target_type(
        self,
        targettype: TARGETTYPE | str
    ) -> GeoComResponse:
        _targettype = toenum(TPS1200BAP.TARGETTYPE, targettype)
        return self._parent.exec1(f"%R1Q,17021:{_targettype.value:d}")

    def get_prism_type(self) -> GeoComResponse:
        return self._parent.exec1(
            "%R1Q,17009:",
            {"prismtype": TPS1200BAP.PRISMTYPE.parse}
        )

    def set_prism_type(
        self,
        prismtype: PRISMTYPE | str
    ) -> GeoComResponse:
        _prismtype = toenum(TPS1200BAP.PRISMTYPE, prismtype)
        return self._parent.exec1(f"%R1Q,17008:{_prismtype.value:d}")

    def get_prism_type2(self) -> GeoComResponse:
        return self._parent.exec1(
            "%R1Q,17031:",
            {
                "prismtype": TPS1200BAP.PRISMTYPE.parse,
                "name": parsestr
            }
        )

    def set_prism_type2(
        self,
        prismtype: PRISMTYPE | str,
        name: str
    ) -> GeoComResponse:
        _prismtype = toenum(TPS1200BAP.PRISMTYPE, prismtype)
        return self._parent.exec1(
            f"%R1Q,17030:{_prismtype.value:d},{tostr(name):s}"
        )

    def get_prism_def(
        self,
        prismtype: PRISMTYPE | str
    ) -> GeoComResponse:
        _prismtype = toenum(TPS1200BAP.PRISMTYPE, prismtype)
        return self._parent.exec1(
            f"%R1Q,17023:{_prismtype.value:d}",
            {
                "name": parsestr,
                "const": float,
                "refltype": TPS1200BAP.REFLTYPE.parse
            }
        )

    def get_user_prism_def(
        self,
        name: str
    ) -> GeoComResponse:
        return self._parent.exec1(
            f"%R1Q,17033:{tostr(name):s}",
            {
                "const": float,
                "refltype": TPS1200BAP.REFLTYPE.parse,
                "creator": parsestr
            }
        )

    def set_user_prism_def(
        self,
        name: str,
        const: float,
        refltype: REFLTYPE | str,
        creator: str
    ) -> GeoComResponse:
        _refltype = toenum(TPS1200BAP.REFLTYPE, refltype)
        return self._parent.exec1(
            (
                f"%R1Q,17032:{tostr(name):s},{const:f},"
                f"{_refltype.value:d},{tostr(creator):s}"
            )
        )

    def get_meas_prg(self) -> GeoComResponse:
        return self._parent.exec1(
            "%R1Q,17018:",
            {"measprg": TPS1200BAP.MEASUREPRG.parse}
        )

    def set_meas_prog(
        self,
        measprg: MEASUREPRG | str
    ) -> GeoComResponse:
        _measprg = toenum(TPS1200BAP.MEASUREPRG, measprg)
        return self._parent.exec1(f"%R1Q,17019:{_measprg.value:d}")

    def meas_distance_angle(
        self,
        distmode: MEASUREPRG | str = MEASUREPRG.DEF_DIST
    ) -> GeoComResponse:
        _distmode = toenum(TPS1200BAP.MEASUREPRG, distmode)
        return self._parent.exec1(
            f"%R1Q,17017:{_distmode.value:d}",
            {
                "hz": float,
                "v": float,
                "dist": float,
                "distmode": TPS1200BAP.MEASUREPRG.parse
            }
        )

    def search_target(self) -> GeoComResponse:
        return self._parent.exec1("%R1Q,17020:0")

    def get_atr_setting(self) -> GeoComResponse:
        return self._parent.exec1(
            "%R1Q,17034:",
            {"atrsetting": TPS1200BAP.ATRSETTING.parse}
        )

    def set_atr_setting(
        self,
        atrsetting: ATRSETTING | str
    ) -> GeoComResponse:
        _atrsetting = toenum(TPS1200BAP.ATRSETTING, atrsetting)
        return self._parent.exec1(f"%R1Q,17035:{_atrsetting.value:d}")

    def get_red_atr_fov(self) -> GeoComResponse:
        return self._parent.exec1(
            f"%R1Q,17036:",
            {"redfov": TPS1200BAP.ONOFF.parse}
        )

    def set_red_atr_fov(
        self,
        redfov: TPS1200BAP.ONOFF | str
    ) -> GeoComResponse:
        _redfov = toenum(TPS1200BAP.ONOFF, redfov)
        return self._parent.exec1(f"%R1Q,17037:{_redfov.value:d}")


class TPS1200BMM(TPS1200Subsystem):
    def beep_alarm(self) -> GeoComResponse:
        return self._parent.exec1("%R1Q,11004:")

    def beep_normal(self) -> GeoComResponse:
        return self._parent.exec1("%R1Q,11003:")

    def beep_on(
        self,
        intensity: int
    ) -> GeoComResponse:
        return self._parent.exec1(f"%R1Q,20001:{intensity:d}")

    def beep_off(self) -> GeoComResponse:
        return self._parent.exec1("%R1Q,20000:")


class TPS1200COM(TPS1200Subsystem):
    class STOPMODE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200COM.STOPMODE:
            return cls(int(value))

        SHUTDOWN = 0
        SLEEP = 1

    class STARTUPMODE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200COM.STARTUPMODE:
            return cls(int(value))

        LOCAL = 0
        REMOTE = 1

    def get_sw_version(self) -> GeoComResponse:
        return self._parent.exec1(
            "%R1Q,110:",
            {
                "release": int,
                "version": int,
                "subversion": int
            }
        )

    def switch_on(
        self,
        onmode: STARTUPMODE | str = STARTUPMODE.LOCAL
    ) -> GeoComResponse:
        _onmode = toenum(TPS1200COM.STARTUPMODE, onmode)
        return self._parent.exec1(f"%R1Q,111:{_onmode.value:d}")

    def switch_off(
        self,
        offmode: STOPMODE | str = STOPMODE.SHUTDOWN
    ) -> GeoComResponse:
        _offmode = toenum(TPS1200COM.STOPMODE, offmode)
        return self._parent.exec1(
            f"%R1Q,112:{_offmode.value:d}"
        )

    def nullproc(self) -> GeoComResponse:
        return self._parent.exec1("%R1Q,0:")

    def get_binary_available(self) -> GeoComResponse:
        return self._parent.exec1(
            "%R1Q,113:",
            {"available": bool}
        )

    def set_binary_available(
        self,
        available: bool
    ) -> GeoComResponse:
        return self._parent.exec1(
            f"%R1Q,114:{available:d}"
        )


class TPS1200CSV(TPS1200Subsystem):
    class DEVICECLASS(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200CSV.DEVICECLASS:
            return cls(int(value))

        CLASS_1100 = 0
        CLASS_1700 = 1
        CLASS_1800 = 2
        CLASS_5000 = 3
        CLASS_6000 = 4
        CLASS_1500 = 5
        CLASS_2003 = 6
        CLASS_5005 = 7
        CLASS_5100 = 8
        CLASS_1102 = 100
        CLASS_1103 = 101
        CLASS_1105 = 102
        CLASS_1101 = 103
        CLASS_1202 = 200
        CLASS_1203 = 201
        CLASS_1205 = 202
        CLASS_1201 = 203

    class DEVICETYPE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200CSV.DEVICETYPE:
            return cls(int(value))

        T = 0x00000
        MOT = 0x00004
        ATR = 0x00008
        EGL = 0x00010
        DB = 0x00020
        DL = 0x00040
        LP = 0x00080
        # TC1 = 0x00001 # TPS1000
        # TC2 = 0x00002 # TPS1000
        TC = 0x00001
        TCR = 0x00002
        ATC = 0x00100
        LPNT = 0x00200
        RL_EXT = 0x00400
        PS = 0x00800
        # SIM = 0x04000 # TPSSim

    class REFLESSCLASS(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200CSV.REFLESSCLASS:
            return cls(int(value))

        NONE = 0
        R100 = 1
        R300 = 2
        R400 = 3  # not in the documentation?

    class POWERSOURCE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200CSV.POWERSOURCE:
            return cls(int(value))

        EXTERNAL = 1
        INTERNAL = 2

    def get_instrument_no(self) -> GeoComResponse:
        return self._parent.exec1(
            "%R1Q,5003:",
            {"serial": int}
        )

    def get_instrument_name(self) -> GeoComResponse:
        return self._parent.exec1(
            "%R1Q,5004:",
            {"name": parsestr}
        )

    def get_device_config(self) -> GeoComResponse:
        return self._parent.exec1(
            "%R1Q,5035:",
            {
                "deviceclass": TPS1200CSV.DEVICECLASS.parse,
                "devicetype": int
            }
        )

    def get_reflectorless_class(self) -> GeoComResponse:
        return self._parent.exec1(
            "%R1Q,5100:",
            {"reflessclass": TPS1200CSV.REFLESSCLASS.parse}
        )

    def get_date_time(self) -> GeoComResponse:
        return self._parent.exec1(
            "%R1Q,5008:",
            {
                "year": int,
                "month": parsebyte,
                "day": parsebyte,
                "hour": parsebyte,
                "minute": parsebyte,
                "second": parsebyte
            }
        )

    def set_date_time(
        self,
        year: int,
        month: int = 1,
        day: int = 1,
        hour: int = 0,
        minute: int = 0,
        second: int = 0
    ) -> GeoComResponse:
        cmd = (
            f"%R1Q,5007:"
            f"{year:d},{tobyte(month):s},{tobyte(day):s},"
            f"{tobyte(hour):d},{tobyte(minute):d},{tobyte(second):s}"
        )
        return self._parent.exec1(cmd)

    def get_sw_version(self) -> GeoComResponse:
        return self._parent.exec1(
            "%R1Q,5034:",
            {
                "release": int,
                "version": int,
                "subversion": int
            }
        )

    def check_power(self) -> GeoComResponse:
        return self._parent.exec1(
            "%R1Q,5039:",
            {
                "capacity": int,
                "source": TPS1200CSV.POWERSOURCE.parse,
                "suggestion": TPS1200CSV.POWERSOURCE.parse
            }
        )

    def get_int_temp(self) -> GeoComResponse:
        return self._parent.exec1(
            "%R1Q,5011:",
            {"temp": int}
        )


class TPS1200EDM(TPS1200Subsystem):
    class ONOFF(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200EDM.ONOFF:
            return cls(int(value))

        OFF = 0
        ON = 1

    class EGLINTENSITYTYPE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200EDM.EGLINTENSITYTYPE:
            return cls(int(value))

        OFF = 0
        LOW = 1
        MID = 2
        HIGH = 3

    def laserpointer(
        self,
        laser: ONOFF | str
    ) -> GeoComResponse:
        _laser = toenum(TPS1200EDM.ONOFF, laser)
        return self._parent.exec1(
            f"%R1Q,1004:{_laser.value:d}"
        )

    def get_egl_intensity(self) -> GeoComResponse:
        return self._parent.exec1(
            "%R1Q,1058",
            {
                "intensity": TPS1200EDM.EGLINTENSITYTYPE.parse
            }
        )

    def set_egl_intensity(
        self,
        intensity: EGLINTENSITYTYPE | str
    ) -> GeoComResponse:
        _intesity = toenum(TPS1200EDM.EGLINTENSITYTYPE, intensity)
        return self._parent.exec1(
            f"%R1Q,1059:{_intesity.value:d}"
        )


class TPS1200MOT(TPS1200Subsystem):
    class LOCKSTATUS(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200MOT.LOCKSTATUS:
            return cls(int(value))

        LOCKEDOUT = 0
        LOCKEDIN = 1
        PREDICTION = 23

    class STOPMODE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200MOT.STOPMODE:
            return cls(int(value))

        NORMAL = 0
        SHUTDOWN = 1

    class MODE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200MOT.MODE:
            return cls(int(value))

        POSIT = 0
        OCONST = 1
        MANUPOS = 2
        LOCK = 3
        BREAK = 4
        # 5, 6 do not use (why?)
        TERM = 7

    def read_lock_status(self) -> GeoComResponse:
        return self._parent.exec1(
            "%R1Q,6021:",
            {"status": TPS1200MOT.LOCKSTATUS.parse}
        )

    def start_controller(
        self,
        mode: MODE | str = MODE.MANUPOS
    ) -> GeoComResponse:
        _mode = toenum(TPS1200MOT.MODE, mode)
        return self._parent.exec1(
            f"%R1Q,6001:{_mode.value:d}"
        )

    def stop_controller(
        self,
        mode: STOPMODE | str = STOPMODE.NORMAL
    ) -> GeoComResponse:
        _mode = toenum(TPS1200MOT.STOPMODE, mode)
        return self._parent.exec1(
            f"%R1Q,6002:{_mode.value:d}"
        )

    def set_velocity(
        self,
        horizontal: float,
        vertical: float
    ) -> GeoComResponse:
        return self._parent.exec1(
            f"%R1Q,6004:{horizontal:f},{vertical:f}"
        )


class TPS1200SUP(TPS1200Subsystem):
    class ONOFF(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200SUP.ONOFF:
            return cls(int(value))

        OFF = 0
        ON = 1

    class AUTOPOWER(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200SUP.AUTOPOWER:
            return cls(int(value))

        DISABLED = 0
        OFF = 2

    def get_config(self) -> GeoComResponse:
        return self._parent.exec1(
            "%R1Q,14001:",
            {
                "reserved": int,
                "autopower": TPS1200SUP.AUTOPOWER.parse,
                "timeout": int
            }
        )

    def set_config(
        self,
        reserved: int,
        autopower: AUTOPOWER | str = AUTOPOWER.OFF,
        timeout: int = 3_600_000
    ) -> GeoComResponse:
        _autopowerd = toenum(TPS1200SUP.AUTOPOWER, autopower)
        return self._parent.exec1(
            f"%R1Q,14002:{reserved:d},{_autopowerd.value:d},{timeout:d}"
        )


class TPS1200(GeoComProtocol):
    RESPPAT: re.Pattern = re.compile(
        r"^%R1P,"
        r"(?P<comrc>\d+),"
        r"(?P<tr>\d+):"
        r"(?P<rc>\d+)"
        r"(?:,(?P<params>.*))?$"
    )

    def __init__(self, connection: Connection):
        super().__init__(connection)
        self.aus = TPS1200AUS(self)
        self.aut = TPS1200AUT(self)
        self.bap = TPS1200BAP(self)
        self.bmm = TPS1200BMM(self)
        self.com = TPS1200COM(self)
        self.csv = TPS1200CSV(self)
        self.edm = TPS1200EDM(self)

    def get_double_precision(self) -> GeoComResponse:
        return self.exec1(
            "%R1Q,108:",
            {"digits": int}
        )

    def set_double_precision(
        self,
        digits: int
    ) -> GeoComResponse:
        return self.exec1(f"%R1Q,107:{digits:d}")

    def exec1(
        self,
        cmd: str,
        args: dict[str, Callable[[str], Any]] | None = None
    ) -> GeoComResponse:
        try:
            reply = self._conn.exchange1(cmd)
        except SerialException as e:
            reply = (
                f"%R1P,{TPS1200GRC.COM_PORT_NOT_OPEN.value:d},"
                f"0:{TPS1200GRC.UNDEFINED.value}"
            )
        except SerialTimeoutException as e:
            reply = (
                f"%R1P,{TPS1200GRC.COM_TIMEOUT.value:d},"
                f"0:{TPS1200GRC.UNDEFINED.value}"
            )
        except Exception as e:
            reply = (
                f"%R1P,{TPS1200GRC.FATAL.value:d},"
                f"0:{TPS1200GRC.UNDEFINED.value}"
            )

        return self.parse_reply(
            cmd,
            reply,
            args if args is not None else {}
        )

    def parse_reply(
        cls,
        cmd: str,
        reply: str,
        args: dict[str, Callable[[str], Any]]
    ) -> GeoComResponse:
        m = cls.RESPPAT.match(reply)
        if not m:
            return GeoComResponse(
                cmd,
                reply,
                TPS1200GRC.COM_CANT_DECODE,
                TPS1200GRC.UNDEFINED,
                0,
                {}
            )

        groups = m.groupdict()
        values = groups.get("params", "")
        if values is None:
            values = ""
        params: dict = {}
        for (name, func), value in zip(args.items(), values.split(",")):
            params[name] = func(value)

        comrc = TPS1200GRC(int(groups["comrc"]))
        rc = TPS1200GRC(int(groups["rc"]))
        return GeoComResponse(
            cmd,
            reply,
            comrc,
            rc,
            int(groups["tr"]),
            params
        )


class EmulatedTPS1200Connection(Connection):
    def __init__(
        self,
        port: Serial,
        *,
        eom: str = "\r\n",
        eoa: str = "\r\n"
    ):
        super().__init__("")
        self.buffer: list[str] = []

    def __enter__(self) -> EmulatedTPS1200Connection:
        return self

    def __exit__(
        self,
        exc_type: BaseException,
        exc_value: BaseException,
        exc_tb: TracebackType
    ):
        pass

    def close(self):
        pass

    def is_open(self) -> bool:
        return True

    def send(self, message: str):
        self.buffer.append(message)

    def receive(self) -> str:
        self.buffer.pop(0)
        return "%R1P,0,0:0"

    def exchange(self, cmds: list[str]) -> list[str]:
        answers: list[str] = []
        for cmd in cmds:
            self.send(cmd)
            answers.append(self.receive())

        return answers

    def exchange1(self, cmd: str) -> str:
        self.send(cmd)
        return self.receive()
