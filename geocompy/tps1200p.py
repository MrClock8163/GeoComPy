from __future__ import annotations

import re
from typing import Callable, Any, Iterable
from types import TracebackType
from enum import Enum, Flag
import logging
from time import sleep
from traceback import format_exc
from datetime import datetime

from serial import Serial, SerialException, SerialTimeoutException

from . import (
    GeoComProtocol,
    GeoComSubsystem,
    GeoComResponse,
    GeoComReturnCode
)

from .data import (
    Angle,
    AngleUnit,
    Byte,
    Coordinate
)

from .communication import (
    Connection,
    parsestr,
    toenum
)


class TPS1200PGRC(GeoComReturnCode):
    def __bool__(self) -> bool:
        return self is TPS1200PGRC.OK

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
    MOT_V_ENCODER = 1801
    MOT_HZ_ENCODER = 1802
    MOT_HZ_V_ENCODER = 1803

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
    AUT_SUPPLY_TOO_HIGH = 8718
    AUT_SUPPLY_TOO_LOW = 8719
    AUT_NO_WORKING_AREA = 8720
    AUT_ARRAY_FULL = 8721
    AUT_NO_DATA = 8722

    KDM_NOT_AVAILABLE = 12544

    FTR_FILEACCESS = 13056
    FTR_WRONGFILEBLOCKNUMBER = 13057
    FTR_NOTENOUGHSPACE = 13058
    FTR_INVALIDINPUT = 13059
    FTR_MISSINGSETUP = 13060


class TPS1200PSubsystem(GeoComSubsystem):
    def __init__(self, parent: TPS1200P):
        self._parent: TPS1200P = parent
        self._request = self._parent.request


class TPS1200PAUS(TPS1200PSubsystem):
    class ONOFF(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PAUS.ONOFF:
            return cls(int(value))

        OFF = 0
        ON = 1

    def get_user_atr_state(self) -> GeoComResponse:
        return self._request(
            18006,
            parsers={
                "state": self.ONOFF.parse
            }
        )

    def set_user_atr_state(
        self,
        state: ONOFF | str
    ) -> GeoComResponse:
        _state = toenum(self.ONOFF, state)
        return self._request(18005, [_state.value])

    def get_user_lock_state(self) -> GeoComResponse:
        return self._request(
            18008,
            parsers={
                "state": self.ONOFF.parse
            }
        )

    def set_user_lock_state(
        self,
        state: ONOFF | str
    ) -> GeoComResponse:
        _state = toenum(self.ONOFF, state)
        return self._request(
            18007,
            [_state.value]
        )


class TPS1200PAUT(TPS1200PSubsystem):
    class POSMODE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PAUT.POSMODE:
            return cls(int(value))

        NORMAL = 0
        PRECISE = 1
        FAST = 2  # TS30 / MS30

    class ADJMODE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PAUT.ADJMODE:
            return cls(int(value))

        NORMAL = 0
        POINT = 1
        DEFINE = 2

    class ATRMODE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PAUT.ATRMODE:
            return cls(int(value))

        POSITION = 0
        TARGET = 1

    class DIRECTION(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PAUT.DIRECTION:
            return cls(int(value))

        CLOCKWISE = 1
        ANTICLOCKWISE = -1

    def read_tol(self) -> GeoComResponse:
        return self._request(
            9008,
            parsers={
                "hz": Angle.parse,
                "v": Angle.parse
            }
        )

    def set_tol(
        self,
        hz: Angle,
        v: Angle
    ) -> GeoComResponse:
        return self._request(9007, [hz, v])

    def read_timeout(self) -> GeoComResponse:
        return self._request(
            9012,
            parsers={
                "hz": float,
                "v": float
            }
        )

    def set_timeout(
        self,
        hz: float,
        v: float
    ) -> GeoComResponse:
        return self._request(
            9011,
            [hz, v]
        )

    def make_positioning(
        self,
        hz: Angle,
        v: Angle,
        posmode: POSMODE | str = POSMODE.NORMAL,
        atrmode: ATRMODE | str = ATRMODE.POSITION
    ) -> GeoComResponse:
        _posmode = toenum(self.POSMODE, posmode)
        _atrmode = toenum(self.ATRMODE, atrmode)
        return self._request(
            9027,
            [hz, v, _posmode.value, _atrmode.value, 0]
        )

    def change_face(
        self,
        posmode: POSMODE | str = POSMODE.NORMAL,
        atrmode: ATRMODE | str = ATRMODE.POSITION
    ) -> GeoComResponse:
        _posmode = toenum(self.POSMODE, posmode)
        _atrmode = toenum(self.ATRMODE, atrmode)
        return self._request(
            9028,
            [_posmode.value, _atrmode.value, 0]
        )

    def fine_adjust(
        self,
        width: Angle,
        height: Angle
    ) -> GeoComResponse:
        return self._request(
            9037,
            [width, height, 0]
        )

    def search(
        self,
        width: Angle,
        height: Angle
    ) -> GeoComResponse:
        return self._request(
            9029,
            [width, height, 0]
        )

    def get_fine_adjust_mode(self) -> GeoComResponse:
        return self._request(
            9030,
            parsers={
                "adjmode": self.ADJMODE.parse
            }
        )

    def set_fine_adjust_mode(
        self,
        adjmode: ADJMODE | str = ADJMODE.NORMAL
    ) -> GeoComResponse:
        _adjmode = toenum(self.ADJMODE, adjmode)
        return self._request(
            9031,
            [_adjmode.value]
        )

    def lock_in(self) -> GeoComResponse:
        return self._request(9013)

    def get_search_area(self) -> GeoComResponse:
        return self._request(
            9042,
            parsers={
                "hz": Angle.parse,
                "v": Angle.parse,
                "width": Angle.parse,
                "height": Angle.parse,
                "enabled": bool
            }
        )

    def set_search_area(
        self,
        hz: Angle,
        v: Angle,
        width: Angle,
        height: Angle,
        enabled: bool = True
    ) -> GeoComResponse:
        return self._request(
            9043,
            [hz, v, width, height, enabled]
        )

    def get_user_spiral(self) -> GeoComResponse:
        return self._request(
            9040,
            parsers={
                "width": Angle.parse,
                "height": Angle.parse
            }
        )

    def set_user_spiral(
        self,
        width: Angle,
        height: Angle
    ) -> GeoComResponse:
        return self._request(
            9041,
            [width, height]
        )

    def ps_enable_range(
        self,
        enable: bool
    ) -> GeoComResponse:
        return self._request(
            9048,
            [enable]
        )

    def ps_set_range(
        self,
        closest: int,
        farthest: int
    ) -> GeoComResponse:
        return self._request(
            9047,
            [closest, farthest]
        )

    def ps_search_window(self) -> GeoComResponse:
        return self._request(9052)

    def ps_search_next(
        self,
        direction: DIRECTION | str,
        swing: bool
    ) -> GeoComResponse:
        _direction = toenum(self.DIRECTION, direction)
        return self._request(
            9051,
            [_direction.value, swing]
        )


class TPS1200PBAP(TPS1200PSubsystem):
    class MEASUREPRG(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PBAP.MEASUREPRG:
            return cls(int(value))

        NOMEAS = 0
        NODIST = 1
        DEFDIST = 2
        CLEARDIST = 5
        STOPTRK = 6

    class USERMEASPRG(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PBAP.USERMEASPRG:
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
        CONT_REF_SYNCHRO = 10
        SINGLE_REF_PRECISE = 11

    class PRISMTYPE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PBAP.PRISMTYPE:
            return cls(int(value))

        ROUND = 0
        MINI = 1
        TAPE = 2
        THREESIXTY = 3
        USER1 = 4
        USER2 = 5
        USER3 = 6
        MINI360 = 7
        MINIZERO = 8
        USER = 9
        NDSTAPE = 10
        GRZ121 = 11
        MAMPR122 = 12

    class REFLTYPE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PBAP.REFLTYPE:
            return cls(int(value))

        UNDEF = 0
        PRISM = 1
        TAPE = 2

    class TARGETTYPE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PBAP.TARGETTYPE:
            return cls(int(value))

        REFL_USE = 0
        REFL_LESS = 1

    class ATRSETTING(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PBAP.ATRSETTING:
            return cls(int(value))

        NORMAL = 0
        LOWVISON = 1
        LOWVISAON = 2
        SRANGEON = 3
        SRANGEAON = 4

    class ONOFF(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PBAP.ONOFF:
            return cls(int(value))

        OFF = 0
        ON = 1

    def get_target_type(self) -> GeoComResponse:
        return self._request(
            17022,
            parsers={
                "targettype": self.TARGETTYPE.parse
            }
        )

    def set_target_type(
        self,
        targettype: TARGETTYPE | str
    ) -> GeoComResponse:
        _targettype = toenum(self.TARGETTYPE, targettype)
        return self._request(
            17021,
            [_targettype.value]
        )

    def get_prism_type(self) -> GeoComResponse:
        return self._request(
            17009,
            parsers={
                "prismtype": self.PRISMTYPE.parse
            }
        )

    def set_prism_type(
        self,
        prismtype: PRISMTYPE | str
    ) -> GeoComResponse:
        _prismtype = toenum(self.PRISMTYPE, prismtype)
        return self._request(
            17008,
            [_prismtype.value]
        )

    def get_prism_type2(self) -> GeoComResponse:
        return self._request(
            17031,
            parsers={
                "prismtype": self.PRISMTYPE.parse,
                "name": parsestr
            }
        )

    def set_prism_type2(
        self,
        prismtype: PRISMTYPE | str,
        name: str
    ) -> GeoComResponse:
        _prismtype = toenum(self.PRISMTYPE, prismtype)
        return self._request(
            17030,
            [_prismtype.value, name]
        )

    def get_prism_def(
        self,
        prismtype: PRISMTYPE | str
    ) -> GeoComResponse:
        _prismtype = toenum(self.PRISMTYPE, prismtype)
        return self._request(
            17023,
            [_prismtype.value],
            {
                "name": parsestr,
                "const": float,
                "refltype": self.REFLTYPE.parse
            }
        )

    def get_user_prism_def(
        self,
        name: str
    ) -> GeoComResponse:
        return self._request(
            17033,
            [name],
            {
                "const": float,
                "refltype": self.REFLTYPE.parse,
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
        _refltype = toenum(self.REFLTYPE, refltype)
        return self._request(
            17032,
            [name, const, _refltype.value, creator]
        )

    def get_meas_prg(self) -> GeoComResponse:
        return self._request(
            17018,
            parsers={
                "measprg": self.MEASUREPRG.parse
            }
        )

    def set_meas_prog(
        self,
        measprg: MEASUREPRG | str
    ) -> GeoComResponse:
        _measprg = toenum(self.MEASUREPRG, measprg)
        return self._request(
            17019,
            [_measprg.value]
        )

    def meas_distance_angle(
        self,
        distmode: MEASUREPRG | str = MEASUREPRG.DEFDIST
    ) -> GeoComResponse:
        _distmode = toenum(self.MEASUREPRG, distmode)
        return self._request(
            17017,
            [_distmode.value],
            {
                "hz": Angle.parse,
                "v": Angle.parse,
                "dist": float,
                "distmode": self.MEASUREPRG.parse
            }
        )

    def search_target(self) -> GeoComResponse:
        return self._request(17020, [0])

    def get_atr_setting(self) -> GeoComResponse:
        return self._request(
            17034,
            parsers={
                "atrsetting": self.ATRSETTING.parse
            }
        )

    def set_atr_setting(
        self,
        atrsetting: ATRSETTING | str
    ) -> GeoComResponse:
        _atrsetting = toenum(self.ATRSETTING, atrsetting)
        return self._request(
            17035,
            [_atrsetting.value]
        )

    def get_red_atr_fov(self) -> GeoComResponse:
        return self._request(
            17036,
            parsers={
                "redfov": self.ONOFF.parse
            }
        )

    def set_red_atr_fov(
        self,
        redfov: TPS1200PBAP.ONOFF | str
    ) -> GeoComResponse:
        _redfov = toenum(self.ONOFF, redfov)
        return self._request(
            17037,
            [_redfov.value]
        )


class TPS1200PBMM(TPS1200PSubsystem):
    def beep_alarm(self) -> GeoComResponse:
        return self._request(11004)

    def beep_normal(self) -> GeoComResponse:
        return self._request(11003)

    def beep_on(
        self,
        intensity: int
    ) -> GeoComResponse:
        return self._request(
            20001,
            [intensity]
        )

    def beep_off(self) -> GeoComResponse:
        return self._request(20000)


class TPS1200PCOM(TPS1200PSubsystem):
    class STOPMODE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PCOM.STOPMODE:
            return cls(int(value))

        SHUTDOWN = 0
        SLEEP = 1

    class STARTUPMODE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PCOM.STARTUPMODE:
            return cls(int(value))

        LOCAL = 0
        REMOTE = 1

    def get_sw_version(self) -> GeoComResponse:
        return self._request(
            110,
            parsers={
                "release": int,
                "version": int,
                "subversion": int
            }
        )

    def switch_on(
        self,
        onmode: STARTUPMODE | str = STARTUPMODE.LOCAL
    ) -> GeoComResponse:
        _onmode = toenum(self.STARTUPMODE, onmode)
        return self._request(
            111,
            [_onmode.value]
        )

    def switch_off(
        self,
        offmode: STOPMODE | str = STOPMODE.SHUTDOWN
    ) -> GeoComResponse:
        _offmode = toenum(self.STOPMODE, offmode)
        return self._request(
            112,
            [_offmode.value]
        )

    def nullproc(self) -> GeoComResponse:
        return self._request(0)

    def get_binary_available(self) -> GeoComResponse:
        return self._request(
            113,
            parsers={
                "available": bool
            }
        )

    def set_binary_available(
        self,
        available: bool
    ) -> GeoComResponse:
        return self._request(
            114,
            [available]
        )


class TPS1200PCSV(TPS1200PSubsystem):
    class DEVICECLASS(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PCSV.DEVICECLASS:
            return cls(int(value))

        CLASS_1100 = 0  # TPS1000 3"
        CLASS_1700 = 1  # TPS1000 1.5"
        CLASS_1800 = 2  # TPS1000 1"
        CLASS_5000 = 3  # TPS2000
        CLASS_6000 = 4  # TPS2000
        CLASS_1500 = 5  # TPS1000
        CLASS_2003 = 6  # TPS2000
        CLASS_5005 = 7  # TPS5000
        CLASS_5100 = 8  # TPS5000
        CLASS_1102 = 100  # TPS1100 2"
        CLASS_1103 = 101  # TPS1100 3"
        CLASS_1105 = 102  # TPS1100 5"
        CLASS_1101 = 103  # TPS1100 1"
        CLASS_1202 = 200  # TPS1200 2"
        CLASS_1203 = 201  # TPS1200 3"
        CLASS_1205 = 202  # TPS1200 5"
        CLASS_1201 = 203  # TPS1200 1"
        CLASS_Tx30 = 300  # TS30, MS30 0.5"
        CLASS_Tx31 = 301  # TS30, MS30 1"

    class DEVICETYPE(Flag):
        @classmethod
        def parse(cls, value: str) -> TPS1200PCSV.DEVICETYPE:
            return cls(int(value))

        T = 0x00000  # Theodolites
        MOT = 0x00004  # Motorized
        ATR = 0x00008  # ATR
        EGL = 0x00010  # Guide Light
        DB = 0x00020  # Database
        DL = 0x00040  # Diode laser
        LP = 0x00080  # Laser plumbed
        # TC1 = 0x00001 # TPS1000
        # TC2 = 0x00002 # TPS1000
        TC = 0x00001  # Tachymeter
        TCR = 0x00002  # Tachymeter (red laser)
        ATC = 0x00100  # Autocollimation lamp
        LPNT = 0x00200  # Laserpointer
        RLEXT = 0x00400  # Powersearch
        PS = 0x00800  # Powersearch
        # SIM = 0x04000 # TPSSim

    class REFLESSCLASS(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PCSV.REFLESSCLASS:
            return cls(int(value))

        NONE = 0
        R100 = 1
        R300 = 2
        R400 = 3
        R1000 = 4

    class POWERSOURCE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PCSV.POWERSOURCE:
            return cls(int(value))

        CURRENT = 0
        EXTERNAL = 1
        INTERNAL = 2

    def get_instrument_no(self) -> GeoComResponse:
        return self._request(
            5003,
            parsers={
                "serial": int
            }
        )

    def get_instrument_name(self) -> GeoComResponse:
        return self._request(
            5004,
            parsers={
                "name": parsestr
            }
        )

    def get_device_config(self) -> GeoComResponse:
        return self._request(
            5035,
            parsers={
                "deviceclass": self.DEVICECLASS.parse,
                "devicetype": lambda x: self.DEVICETYPE(int(x))
            }
        )

    def get_reflectorless_class(self) -> GeoComResponse:
        return self._request(
            5100,
            parsers={
                "reflessclass": self.REFLESSCLASS.parse
            }
        )

    def get_date_time(self) -> GeoComResponse:
        response = self._request(
            5008,
            parsers={
                "year": int,
                "month": Byte.parse,
                "day": Byte.parse,
                "hour": Byte.parse,
                "minute": Byte.parse,
                "second": Byte.parse
            }
        )
        time = datetime(
            int(response.params["year"]),
            int(response.params["month"]),
            int(response.params["day"]),
            int(response.params["hour"]),
            int(response.params["minute"]),
            int(response.params["second"])
        )
        response.params = {"time": time}
        return response

    def set_date_time(
        self,
        time: datetime
    ) -> GeoComResponse:
        return self._request(
            5007,
            [
                time.year, Byte(time.month), Byte(time.day),
                Byte(time.hour), Byte(time.minute), Byte(time.second)
            ]
        )

    def get_sw_version(self) -> GeoComResponse:
        return self._request(
            5034,
            parsers={
                "release": int,
                "version": int,
                "subversion": int
            }
        )

    def check_power(self) -> GeoComResponse:
        return self._request(
            5039,
            parsers={
                "capacity": int,
                "source": self.POWERSOURCE.parse,
                "suggested": self.POWERSOURCE.parse
            }
        )

    def get_int_temp(self) -> GeoComResponse:
        return self._request(
            5011,
            parsers={
                "temp": int
            }
        )

    def get_date_time_centisec(self) -> GeoComResponse:
        response = self._request(
            5117,
            parsers={
                "year": int,
                "month": int,
                "day": int,
                "hour": int,
                "minute": int,
                "second": int,
                "centisec": int
            }
        )
        time = datetime(
            response.params["year"],
            response.params["month"],
            response.params["day"],
            response.params["hour"],
            response.params["minute"],
            response.params["second"],
            response.params["centisec"] * 10000
        )
        response.params = {"time": time}
        return response


class TPS1200PEDM(TPS1200PSubsystem):
    class ONOFF(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PEDM.ONOFF:
            return cls(int(value))

        OFF = 0
        ON = 1

    class EGLINTENSITYTYPE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PEDM.EGLINTENSITYTYPE:
            return cls(int(value))

        OFF = 0
        LOW = 1
        MID = 2
        HIGH = 3

    def laserpointer(
        self,
        laser: ONOFF | str
    ) -> GeoComResponse:
        _laser = toenum(self.ONOFF, laser)
        return self._request(
            1004,
            [_laser.value]
        )

    def get_egl_intensity(self) -> GeoComResponse:
        return self._request(
            1058,
            parsers={
                "intensity": self.EGLINTENSITYTYPE.parse
            }
        )

    def set_egl_intensity(
        self,
        intensity: EGLINTENSITYTYPE | str
    ) -> GeoComResponse:
        _intesity = toenum(self.EGLINTENSITYTYPE, intensity)
        return self._request(
            1059,
            [_intesity.value]
        )


class TPS1200PFTR(TPS1200PSubsystem):
    class DEVICETYPE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PFTR.DEVICETYPE:
            return cls(int(value))

        INTERNAL = 0
        PCPARD = 1

    class FILETYPE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PFTR.FILETYPE:
            return cls(int(value))

        UNKNOWN = 0  # ?
        IMAGE = 170

    def setup_list(
        self,
        device: DEVICETYPE | str = DEVICETYPE.PCPARD,
        filetype: FILETYPE | str = FILETYPE.UNKNOWN,
        path: str = "/root"
    ) -> GeoComResponse:
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
        return self._request(23308)

    def setup_download(
        self,
        filename: str,
        blocksize: int,
        device: DEVICETYPE | str = DEVICETYPE.PCPARD,
        filetype: FILETYPE | str = FILETYPE.UNKNOWN,
    ) -> GeoComResponse:
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
        return self._request(
            23304,
            [block],
            {
                "value": parsestr,
                "length": int
            }
        )

    def abort_download(self) -> GeoComResponse:
        return self._request(23305)

    def delete(
        self,
        filename: str,
        time: datetime | None = None,
        device: DEVICETYPE | str = DEVICETYPE.PCPARD,
        filetype: FILETYPE | str = FILETYPE.UNKNOWN
    ) -> GeoComResponse:
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


class TPS1200PIMG(TPS1200PSubsystem):
    class MEMTYPE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PIMG.MEMTYPE:
            return cls(int(value))

        INTERNAL = 0x0
        PCCARD = 0x1

    class SUBFUNC(Flag):
        @classmethod
        def parse(cls, value: str) -> TPS1200PIMG.SUBFUNC:
            return cls(int(value))

        TESTIMG = 1
        AUTOEXPTIME = 2
        SS2 = 4
        SS4 = 8

    def get_tcc_config(
        self,
        memtype: MEMTYPE | str = MEMTYPE.PCCARD
    ) -> GeoComResponse:
        _memtype = toenum(self.MEMTYPE, memtype)
        return self._request(
            23400,
            parsers={
                "imgnumber": int,
                "quality": int,
                "subfunc": lambda x: self.SUBFUNC(int(x)),
                "prefix": str
            }
        )

    def set_tcc_config(
        self,
        imgnumber: int,
        quality: int,
        subfunc: SUBFUNC | int,
        memtype: MEMTYPE | str = MEMTYPE.PCCARD,
    ) -> GeoComResponse:
        _memtype = toenum(self.MEMTYPE, memtype)
        if isinstance(subfunc, self.SUBFUNC):
            subfunc = subfunc.value
        return self._request(
            23401,
            [_memtype.value, imgnumber, quality, subfunc]
        )

    def take_tcc_img(
        self,
        memtype: MEMTYPE | str = MEMTYPE.PCCARD
    ) -> GeoComResponse:
        _memtype = toenum(self.MEMTYPE, memtype)
        return self._request(
            23402,
            [_memtype.value],
            {
                "imgnumber": int
            }
        )


class TPS1200PMOT(TPS1200PSubsystem):
    class LOCKSTATUS(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PMOT.LOCKSTATUS:
            return cls(int(value))

        LOCKEDOUT = 0
        LOCKEDIN = 1
        PREDICTION = 2

    class STOPMODE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PMOT.STOPMODE:
            return cls(int(value))

        NORMAL = 0
        SHUTDOWN = 1

    class MODE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PMOT.MODE:
            return cls(int(value))

        POSIT = 0
        OCONST = 1
        MANUPOS = 2
        LOCK = 3
        BREAK = 4
        # 5, 6 do not use (why?)
        TERM = 7

    def read_lock_status(self) -> GeoComResponse:
        return self._request(
            6021,
            parsers={
                "status": self.LOCKSTATUS.parse
            }
        )

    def start_controller(
        self,
        mode: MODE | str = MODE.MANUPOS
    ) -> GeoComResponse:
        _mode = toenum(self.MODE, mode)
        return self._request(
            6001,
            [_mode.value]
        )

    def stop_controller(
        self,
        mode: STOPMODE | str = STOPMODE.NORMAL
    ) -> GeoComResponse:
        _mode = toenum(TPS1200PMOT.STOPMODE, mode)
        return self._request(
            6002,
            [_mode.value]
        )

    def set_velocity(
        self,
        horizontal: float,
        vertical: float
    ) -> GeoComResponse:
        horizontal = min(0.79, max(-0.79, horizontal))
        vertical = min(0.79, max(-0.79, vertical))
        return self._request(
            6004,
            [horizontal, vertical]
        )


class TPS1200PSUP(TPS1200PSubsystem):
    class ONOFF(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PSUP.ONOFF:
            return cls(int(value))

        OFF = 0
        ON = 1

    class AUTOPOWER(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PSUP.AUTOPOWER:
            return cls(int(value))

        DISABLED = 0
        OFF = 2

    def get_config(self) -> GeoComResponse:
        return self._request(
            14001,
            parsers={
                "reserved": int,
                "autopower": self.AUTOPOWER.parse,
                "timeout": int
            }
        )

    def set_config(
        self,
        autopower: AUTOPOWER | str = AUTOPOWER.OFF,
        timeout: int = 3_600_000,
        reserved: ONOFF | str = ONOFF.ON
    ) -> GeoComResponse:
        _autopower = toenum(self.AUTOPOWER, autopower)
        _reserved = toenum(self.ONOFF, reserved)
        return self._request(
            14002,
            [_reserved.value, _autopower.value, timeout]
        )


class TPS1200PTMC(TPS1200PSubsystem):
    class ONOFF(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PTMC.ONOFF:
            return cls(int(value))

        OFF = 0
        ON = 1

    class INCLINEPRG(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PTMC.INCLINEPRG:
            return cls(int(value))

        MEA = 0
        AUTO = 1
        PLANE = 2

    class MEASUREPRG(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PTMC.MEASUREPRG:
            return cls(int(value))

        STOP = 0
        DEFDIST = 1
        CLEAR = 3
        SIGNAL = 4
        DOMEASURE = 6
        RTRKDIST = 8
        REDTRKDIST = 10
        FREQUENCY = 11

    class EMDMODE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PTMC.EMDMODE:
            return cls(int(value))

        NOTUSED = 0
        SINGLE_TAPE = 1
        SINGLE_STANDARD = 2
        SINGLE_FAST = 3
        SINGLE_LRANGE = 4
        SINGLE_SRANGE = 5
        CONT_STANDARD = 6
        CONT_DYNAMIC = 7
        CONT_REFLESS = 8
        CONT_FAST = 9
        AVERAGE_IR = 10
        AVERAGE_SR = 11
        AVERAGE_LR = 12
        PRECISE_IR = 13  # TS30, MS30
        PRECISE_TAPE = 14  # TS30, MS30

    class FACEDEF(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PTMC.FACEDEF:
            return cls(int(value))

        NORMAL = 0
        TURN = 1

    class FACE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PTMC.FACE:
            return cls(int(value))

        FACE1 = 0
        FACE2 = 1

    def get_coordinate(
        self,
        wait: int = 5000,
        mode: INCLINEPRG | str = INCLINEPRG.AUTO
    ) -> GeoComResponse:
        _mode = toenum(self.INCLINEPRG, mode)
        response = self._request(
            2082,
            [wait, _mode.value],
            {
                "east": float,
                "north": float,
                "height": float,
                "time": int,
                "east_cont": float,
                "north_cont": float,
                "height_cont": float,
                "time_cont": int
            }
        )
        coord = Coordinate(
            response.params["east"],
            response.params["north"],
            response.params["height"]
        )
        coord_cont = Coordinate(
            response.params["east_cont"],
            response.params["north_cont"],
            response.params["height_cont"]
        )
        response.params = {
            "coord": coord,
            "time": response.params["time"],
            "coord_cont": coord_cont,
            "time_cont": response.params["time_cont"]
        }
        return response

    def get_simple_mea(
        self,
        wait: int = 5000,
        mode: INCLINEPRG | str = INCLINEPRG.AUTO
    ) -> GeoComResponse:
        _mode = toenum(self.INCLINEPRG, mode)
        return self._request(
            2108,
            [wait, _mode.value],
            {
                "hz": Angle.parse,
                "v": Angle.parse,
                "dist": float
            }
        )

    def get_angle_incline(
        self,
        mode: INCLINEPRG | str = INCLINEPRG.AUTO
    ) -> GeoComResponse:
        _mode = toenum(self.INCLINEPRG, mode)
        return self._request(
            2003,
            [_mode.value],
            {
                "hz": Angle.parse,
                "v": Angle.parse,
                "angleaccuracy": Angle.parse,
                "angletime": int,
                "crossincline": Angle.parse,
                "lengthincline": Angle.parse,
                "inclineaccuracy": Angle.parse,
                "inclinetime": int,
                "face": self.FACEDEF.parse
            }
        )

    def get_angle(
        self,
        mode: INCLINEPRG | str = INCLINEPRG.AUTO
    ) -> GeoComResponse:
        _mode = toenum(self.INCLINEPRG, mode)
        return self._request(
            2107,
            [_mode.value],
            {
                "hz": Angle.parse,
                "v": Angle.parse
            }
        )

    def quick_dist(self) -> GeoComResponse:
        return self._request(
            2117,
            parsers={
                "hz": Angle.parse,
                "v": Angle.parse,
                "dist": float
            }
        )

    def get_full_meas(
        self,
        wait: int = 5000,
        mode: INCLINEPRG | str = INCLINEPRG.AUTO
    ) -> GeoComResponse:
        _mode = toenum(self.INCLINEPRG, mode)
        return self._request(
            2167,
            [wait, _mode.value],
            {
                "hz": float,
                "v": float,
                "angleaccuracy": float,
                "crossincline": float,
                "lengthincline": float,
                "inclineaccuracy": float,
                "dist": float,
                "disttime": float
            }
        )

    def do_measure(
        self,
        command: MEASUREPRG | str = MEASUREPRG.DEFDIST,
        mode: INCLINEPRG | str = INCLINEPRG.AUTO
    ) -> GeoComResponse:
        _cmd = toenum(self.MEASUREPRG, command)
        _mode = toenum(self.INCLINEPRG, mode)
        return self._request(
            2008,
            [_cmd.value, _mode.value]
        )

    def set_hand_dist(
        self,
        distance: float,
        offset: float,
        mode: INCLINEPRG | str = INCLINEPRG.AUTO
    ) -> GeoComResponse:
        _mode = toenum(self.INCLINEPRG, mode)
        return self._request(
            2019,
            [distance, offset, _mode.value]
        )

    def get_height(self) -> GeoComResponse:
        return self._request(
            2011,
            parsers={
                "height": float
            }
        )

    def set_height(
        self,
        height: float
    ) -> GeoComResponse:
        return self._request(
            2012,
            [height]
        )

    def get_atm_corr(self) -> GeoComResponse:
        return self._request(
            2029,
            parsers={
                "wavelength": float,
                "pressure": float,
                "drytemp": float,
                "wettemp": float
            }
        )

    def set_atm_corr(
        self,
        wavelength: float,
        pressure: float,
        drytemp: float,
        wettemp: float
    ) -> GeoComResponse:
        return self._request(
            2028,
            [wavelength, pressure, drytemp, wettemp]
        )

    def set_orientation(
        self,
        orientation: float
    ) -> GeoComResponse:
        return self._request(
            2113,
            [orientation]
        )

    def get_prism_corr(self) -> GeoComResponse:
        return self._request(
            2023,
            parsers={
                "const": float
            }
        )

    def get_refractive_corr(self) -> GeoComResponse:
        return self._request(
            2031,
            parsers={
                "enabled": bool,
                "earthradius": float,
                "scale": float
            }
        )

    def set_refractive_corr(
        self,
        enabled: bool,
        earthradius: float,
        scale: float
    ) -> GeoComResponse:
        return self._request(
            2030,
            [enabled, earthradius, scale]
        )

    def get_refractive_method(self) -> GeoComResponse:
        return self._request(
            2091,
            parsers={
                "method": int
            }
        )

    def set_refractive_method(
        self,
        method: int
    ) -> GeoComResponse:
        return self._request(
            2090,
            [method]
        )

    def get_station(self) -> GeoComResponse:
        response = self._request(
            2009,
            parsers={
                "east": float,
                "north": float,
                "height": float,
                "hi": float
            }
        )
        coord = Coordinate(
            response.params["east"],
            response.params["north"],
            response.params["height"]
        )
        response.params = {
            "coord": coord,
            "hi": response.params["hi"]
        }
        return response

    def set_station(
        self,
        coord: Coordinate,
        hi: float
    ) -> GeoComResponse:
        return self._request(
            2010,
            [coord.x, coord.y, coord.z, hi]
        )

    def get_atm_ppm(self) -> GeoComResponse:
        return self._request(
            2151,
            parsers={
                "ppm": float
            }
        )

    def set_atm_ppm(
        self,
        ppm: float
    ) -> GeoComResponse:
        return self._request(
            2148,
            [ppm]
        )

    def get_geo_ppm(self) -> GeoComResponse:
        return self._request(
            2154,
            parsers={
                "automatic": bool,
                "meridianscale": float,
                "meridianoffset": float,
                "heightreduction": float,
                "individual": float
            }
        )

    def set_geo_ppm(
        self,
        automatic: bool,
        meridianscale: float,
        meridianoffset: float,
        heightreduction: float,
        individual: float
    ) -> GeoComResponse:
        return self._request(
            2153,
            [
                automatic,
                meridianscale, meridianoffset,
                heightreduction, individual
            ]
        )

    def get_face(self) -> GeoComResponse:
        return self._request(
            2026,
            parsers={
                "face": self.FACE.parse
            }
        )

    def get_signal(self) -> GeoComResponse:
        return self._request(
            2022,
            parsers={
                "intensity": float,
                "time": int
            }
        )

    def get_ang_switch(self) -> GeoComResponse:
        return self._request(
            2014,
            parsers={
                "inclinecorr": bool,
                "stdaxiscorr": bool,
                "collimcorr": bool,
                "tiltaxiscorr": bool
            }
        )

    def get_incline_switch(self) -> GeoComResponse:
        return self._request(
            2007,
            parsers={
                "correction": self.ONOFF.parse
            }
        )

    def set_incline_switch(
        self,
        correction: ONOFF | str
    ) -> GeoComResponse:
        _corr = toenum(self.ONOFF, correction)
        return self._request(
            2006,
            [_corr.value]
        )

    def get_edm_mode(self) -> GeoComResponse:
        return self._request(
            2021,
            parsers={
                "mode": self.EMDMODE.parse
            }
        )

    def set_edm_mode(
        self,
        mode: EMDMODE | str
    ) -> GeoComResponse:
        _mode = toenum(self.EMDMODE, mode)
        return self._request(
            2020,
            [_mode.value]
        )

    def get_simple_coord(
        self,
        wait: int = 5000,
        mode: INCLINEPRG | str = INCLINEPRG.AUTO
    ) -> GeoComResponse:
        _mode = toenum(self.INCLINEPRG, mode)
        return self._request(
            2116,
            parsers={
                "east": float,
                "north": float,
                "height": float
            }
        )

    def if_data_atr_corr_error(self) -> GeoComResponse:
        return self._request(
            2114,
            parsers={
                "atrerror": bool
            }
        )

    def if_data_inc_corr_error(self) -> GeoComResponse:
        return self._request(
            2115,
            parsers={
                "inclineerror": bool
            }
        )

    def set_ang_switch(
        self,
        inclinecorr: bool,
        stdaxiscorr: bool,
        collimcorr: bool,
        tiltaxiscorr: bool
    ) -> GeoComResponse:
        return self._request(
            2016,
            [inclinecorr, stdaxiscorr, collimcorr, tiltaxiscorr]
        )

    def get_slope_dist_corr(self) -> GeoComResponse:
        return self._request(
            2126,
            parsers={
                "ppmcorr": float,
                "prismcorr": float
            }
        )


class TPS1200P(GeoComProtocol):
    RESPPAT: re.Pattern = re.compile(
        r"^%R1P,"
        r"(?P<comrc>\d+),"
        r"(?P<tr>\d+):"
        r"(?P<rc>\d+)"
        r"(?:,(?P<params>.*))?$"
    )

    def __init__(
        self,
        connection: Connection,
        logger: logging.Logger | None = None,
        retry: int = 2
    ):
        super().__init__(connection, logger)
        self.aus = TPS1200PAUS(self)
        self.aut = TPS1200PAUT(self)
        self.bap = TPS1200PBAP(self)
        self.bmm = TPS1200PBMM(self)
        self.com = TPS1200PCOM(self)
        self.csv = TPS1200PCSV(self)
        self.edm = TPS1200PEDM(self)
        self.ftr = TPS1200PFTR(self)
        self.mot = TPS1200PMOT(self)
        self.sup = TPS1200PSUP(self)
        self.tmc = TPS1200PTMC(self)

        for i in range(retry):
            self._conn.send("\n")
            response = self.com.nullproc()
            if response.comcode and response.rpccode:
                break

            sleep(1)
        else:
            raise ConnectionError(
                "could not establish connection to instrument"
            )

        self._precision = 15
        resp = self.get_double_precision()
        if resp.comcode and resp.rpccode:
            self._precision = resp.params["digits"]

    def get_double_precision(self) -> GeoComResponse:
        return self.request(
            108,
            parsers={"digits": int}
        )

    def set_double_precision(
        self,
        digits: int
    ) -> GeoComResponse:
        response = self.request(107, [digits])
        if response.comcode and response.rpccode:
            self._precision = digits
        return response

    def request(
        self,
        rpc: int,
        params: Iterable[int | float | bool | str | Angle | Byte] = [],
        parsers: dict[str, Callable[[str], Any]] | None = None
    ) -> GeoComResponse:
        strparams: list[str] = []
        for item in params:
            match item:
                case Angle():
                    value = f"{round(float(item), self._precision):f}"
                    value = value.rstrip("0")
                    if value[-1] == ".":
                        value += "0"
                case Byte():
                    value = str(item)
                case float():
                    value = f"{round(item, self._precision):f}".rstrip("0")
                    if value[-1] == ".":
                        value += "0"
                case int():
                    value = f"{item:d}"
                case str():
                    value = f"\"{item}\""
                case _:
                    raise TypeError(f"unexpected parameter type: {type(item)}")

            strparams.append(value)

        cmd = f"%R1Q,{rpc}:{",".join(strparams)}"
        try:
            answer = self._conn.exchange1(cmd)
        except SerialTimeoutException as e:
            self.logger.error(format_exc())
            answer = (
                f"%R1P,{TPS1200PGRC.COM_TIMEOUT.value:d},"
                f"0:{TPS1200PGRC.FATAL.value:d}"
            )
        except SerialException as e:
            self.logger.error(format_exc())
            answer = (
                f"%R1P,{TPS1200PGRC.COM_CANT_SEND.value:d},"
                f"0:{TPS1200PGRC.FATAL.value:d}"
            )
        except Exception as e:
            self.logger.error(format_exc())
            answer = (
                f"%R1P,{TPS1200PGRC.FATAL.value:d},"
                f"0:{TPS1200PGRC.FATAL.value:d}"
            )

        response = self.parse_response(
            cmd,
            answer,
            parsers if parsers is not None else {}
        )
        self.logger.debug(response)
        return response

    def parse_response(
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
                TPS1200PGRC.COM_CANT_DECODE,
                TPS1200PGRC.UNDEFINED,
                0,
                {}
            )

        groups = m.groupdict()
        values = groups.get("params", "")
        if values is None:
            values = ""
        params: dict = {}
        try:
            for (name, func), value in zip(args.items(), values.split(",")):
                params[name] = func(value)
        except:
            return GeoComResponse(
                cmd,
                reply,
                TPS1200PGRC.COM_CANT_DECODE,
                TPS1200PGRC.UNDEFINED,
                0,
                {}
            )

        comrc = TPS1200PGRC(int(groups["comrc"]))
        rc = TPS1200PGRC(int(groups["rc"]))
        return GeoComResponse(
            cmd,
            reply,
            comrc,
            rc,
            int(groups["tr"]),
            params
        )
