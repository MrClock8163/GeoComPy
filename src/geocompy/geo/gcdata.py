"""
Description
===========

Module: ``geocompy.geo.gcdata``

The GeoCom data module provides utility types, that are specific to
GeoCom protocol.


Enums
-----

- AUT

  - ``Adjust``
  - ``ATR``
  - ``Position``
  - ``Turn``

- BAP

  - ``ATRMode``
  - ``Prism``
  - ``Program``
  - ``Reflector``
  - ``UserProgram``
  - ``Target``

- CAM

  - ``Camera``
  - ``CameraFunctions``
  - ``Compression``
  - ``JPEGQuality``
  - ``Resolution``
  - ``Zoom``
  - ``WhiteBalance``

- COM

  - ``Shutdown``
  - ``Startup``

- CSV

  - ``Capabilities``
  - ``DeviceClass``
  - ``PowerSource``
  - ``Property``
  - ``Reflectorless``

- EDM

  - ``EDMMode``
  - ``EDMModeV1``
  - ``EDMModeV2``
  - ``Guidelight``
  - ``MeasurementType``
  - ``Tracklight``

- FTR

  - ``Device``
  - ``File``

- MOT

  - ``ATRLock``
  - ``Controller``
  - ``Stop``

- SOP

  - ``AutoPower``

- TMC

  - ``Face``
  - ``Inclination``
  - ``Measurement``

- WIR

  - ``Format``
"""
from enum import Enum, Flag


#######
# AUT #
#######


class Adjust(Enum):
    """
    ATR adjustment tolerance mode.

    ``AUT_ADJMODE``
    """
    NORMAL = 0
    """Angle tolerance."""
    POINT = 1
    """Point tolerance."""


class ATR(Enum):
    """
    ATR mode.

    ``AUT_ATRMODE``
    """
    POSITION = 0
    """Position to angles."""
    TARGET = 1
    """Position to target near angles."""


class Position(Enum):
    """
    Positioning mode.

    ``AUT_POSMODE``
    """
    NORMAL = 0
    """Fast positioning."""
    PRECISE = 1
    """Percise positioning."""


class Turn(Enum):
    """Turning direction."""
    CLOCKWISE = 1
    COUNTERCLOCKWISE = -1


#######
# BAP #
#######


class ATRMode(Enum):
    """
    ATR visibility modes.

    .. versionadded:: GeoCom-TPS1200

    ``BAP_ATRSETTING``
    """

    NORMAL = 0
    """Normal mode."""
    LOWVIS = 1
    """Low visibility on."""
    ALWAYSLOWVIS = 2
    """Low visibility always on."""
    HIGHREFL = 3
    """High reflectivity on."""
    ALWAYSHIGHREFL = 4
    """Hight reflectivity always on."""


class Prism(Enum):
    """
    Reflector prism type.
        .. versionadded:: GeoCom-TPS1100

    ``BAP_PRISMTYPE``
    """
    ROUND = 0
    """Leica Circular Prism"""
    MINI = 1
    """Leica Mini Prism"""
    TAPE = 2
    """Leica Reflector Tape"""
    THREESIXTY = 3
    """Leica 360° Prism."""
    USER1 = 4
    USER2 = 5
    USER3 = 6
    MINI360 = 7
    """
    Leica Mini 360° Prism.

    .. versionadded:: GeoCom-TPS1200
    """
    MINIZERO = 8
    """
    Leica Mini Zero Prism.

    .. versionadded:: GeoCom-TPS1200
    """
    USER = 9
    """
    User defined prism.

    .. versionadded:: GeoCom-TPS1200
    """
    NDSTAPE = 10
    """
    Leica HDS Target.

    .. versionadded:: GeoCom-TPS1200
    """
    GRZ121 = 11
    """
    Leica GRZ121 360° Prism.

    .. versionadded:: GeoCom-TPS1200
    """
    MPR122 = 12
    """
    Leica MPR122 360° Prism.

    .. versionadded:: GeoCom-TPS1200
    """


class Program(Enum):
    """
    Basic measurement programs.

    ``BAP_MEASURE_PRG``
    """
    NOMEASURE = 0
    """No measurement, take last value."""
    NODISTANCE = 1
    """No distance measurement, angles only."""
    DISTANCE = 2
    """Default distance measurement."""
    TRACK = 3
    """Tracking distance measurement.

    .. versionremoved:: GeoCom-TPS1100
    """
    RAPIDTRACK = 4
    """Rapid tracking distance measurement.

    .. versionremoved:: GeoCom-TPS1100
    """
    CLEAR = 5
    """Clear distances."""
    STOPTRACK = 6
    """Stop tracking."""


class Reflector(Enum):
    """
    Reflector type.

    ``BAP_REFLTYPE``
    """

    UNDEFINED = 0
    """Reflector not defined."""
    PRISM = 1
    """Reflector prism."""
    TAPE = 2
    """Reflector tape."""


class UserProgram(Enum):
    """
    Distance measurement programs.

    .. versionadded:: GeoCom-TPS1100

    ``BAP_USER_MEASPRG``
    """
    SINGLE_REF_STANDARD = 0
    """Standard measurement with reflector."""
    SINGLE_REF_FAST = 1
    """Fast measurement with reflector."""
    SINGLE_REF_VISIBLE = 2
    """Long range measurement with reflector."""
    SINGLE_RLESS_VISIBLE = 3
    """Standard measurement without reflector."""
    CONT_REF_STANDARD = 4
    """Tracking with reflector."""
    CONT_REF_FAST = 5
    """Fast tracking with reflector."""
    CONT_RLESS_VISIBLE = 6
    """Fast tracking without reflector."""
    AVG_REF_STANDARD = 7
    """Averaging measurement with reflector."""
    AVG_REF_VISIBLE = 8
    """Averaging long range measurement with reflector."""
    AVG_RLESS_VISIBLE = 9
    """Averaging measurement without reflector."""
    CONT_REF_SYNCHRO = 10
    """
    Synchro tracking with reflector.

    .. versionadded:: GeoCom-TPS1200
    """
    SINGLE_REF_PRECISE = 11
    """
    Precise measurement with reflector (TS/TM30).

    .. versionadded:: GeoCom-TPS1200
    """


class Target(Enum):
    """
    Target type.
        .. versionadded:: GeoCom-TPS1100

    ``BAP_TARGET_TYPE``
    """
    REFLECTOR = 0
    """Reflector."""
    DIRECT = 1
    """Not reflector."""


#######
# CAM #
#######


class Camera(Enum):
    """
    Camera types.

    .. versionadded:: GeoCom-VivaTPS

    ``CAM_ID_TYPE``
    """
    OVERVIEW = 0
    TELESCOPIC = 1


class CameraFunctions(Flag):
    """
    Imaging camera settings.
    """
    TESTIMAGE = 1
    """Test image."""
    AUTOTIME = 2
    """Automatic exposure time."""
    SS2 = 4
    """2-times subsampling."""
    SS4 = 8
    """4-times subsampling."""


class Compression(Enum):
    """
    Image compression.

    .. versionadded:: GeoCom-VivaTPS

    ``CAM_COMPRESSION_TYPE``
    """
    JPEG = 0
    RAW = 1


class JPEGQuality(Enum):
    """
    JPEG image quality.

    .. versionadded:: GeoCom-VivaTPS

    ``CAM_JPEG_COMPR_QUALITY_TYPE``
    """
    STANDARD = 0
    BEST = 1
    IGNORE = 2


class Resolution(Enum):
    """
    Image resolutions.

    .. versionadded:: GeoCom-VivaTPS

    ``CAM_RESOLUTION_TYPE``
    """
    R2560X1920 = 0
    R1280X960 = 3
    R640X480 = 4
    R320X240 = 5


class Zoom(Enum):
    """
    Camera zoom levels.

    .. versionadded:: GeoCom-VivaTPS

    ``CAM_ZOOM_FACTOR_TYPE``
    """
    X1 = 1
    X2 = 2
    X4 = 4
    X8 = 8


class WhiteBalance(Enum):
    """
    Camera whitebalance settings.

    .. versionadded:: GeoCom-VivaTPS

    ``CAM_COMPRESSION_TYPE``
    """
    AUTO = 0
    INDOOR = 1
    OUTDOOR = 2


#######
# COM #
#######


class Shutdown(Enum):
    """
    Instrument software stop mode.

    ``COM_TPS_STOP_MODE``
    """
    SHUTDOWN = 0
    SLEEP = 1
    GUI = 2
    """
    Close onboard software.

    .. versionadded:: GeoCom-VivaTPS
    """


class Startup(Enum):
    """
    Instrument startup mode.

    ``COM_TPS_STARTUP_MODE``
    """
    LOCAL = 0
    """
    Manual mode.

    .. deprecated:: GeoCom-VivaTPS
    """
    REMOTE = 1
    """GeoCom mode."""
    GUI = 2
    """
    Start onboard software.

    .. versionadded:: GeoCom-VivaTPS
    """


#######
# CSV #
#######


class Capabilities(Flag):
    """
    Instrument capabilities.

    ``TPS_DEVICE_TYPE``
    """

    THEODOLITE = 0x00000
    """Theodolite"""
    TC1 = 0x00001  # TPS1000
    TC2 = 0x00002  # TPS1000
    MOTORIZED = 0x00004
    """Motorized"""
    ATR = 0x00008
    """ATR"""
    EGL = 0x00010
    """Guide Light"""
    DATABASE = 0x00020
    """Database"""
    DIODELASER = 0x00040
    """Diode laser"""
    LASERPLUMB = 0x00080
    """Laser plumb"""
    AUTOCOLLIMATION = 0x00100
    """
    Autocollimation lamp

    .. versionadded:: GeoCom-TPS1100
    """
    POINTER = 0x00200
    """
    Laserpointer

    .. versionadded:: GeoCom-TPS1100
    """
    REFLECTORLESS = 0x00400
    """
    Reflectorless EDM

    .. versionadded:: GeoCom-TPS1100
    """
    POWERSEARCH = 0x00800
    """
    PowerSearch

    .. versionadded:: GeoCom-TPS1200
    """


class DeviceClass(Enum):
    """
    Instrument accuracy class.

    ``TPS_DEVICE_CLASS``
    """

    CLASS_1100 = 0
    """TPS1000 3\""""
    CLASS_1700 = 1
    """TPS1000 1.5\""""
    CLASS_1800 = 2
    """TPS1000 1\""""
    CLASS_5000 = 3
    """TPS2000"""
    CLASS_6000 = 4
    """TPS2000"""
    CLASS_1500 = 5
    """TPS1000"""
    CLASS_2003 = 6
    """
    TPS2000

    .. versionadded:: GeoCom-TPS1100
    """
    CLASS_5005 = 7
    """
    TPS5000

    .. versionadded:: GeoCom-TPS1100
    """
    CLASS_5100 = 8
    """
    TPS5000

    .. versionadded:: GeoCom-TPS1100
    """
    CLASS_1102 = 100
    """
    TPS1100 2\"

    .. versionadded:: GeoCom-TPS1100
    """
    CLASS_1103 = 101
    """
    TPS1100 3\"

    .. versionadded:: GeoCom-TPS1100
    """
    CLASS_1105 = 102
    """
    TPS1100 5\"

    .. versionadded:: GeoCom-TPS1100
    """
    CLASS_1101 = 103
    """
    TPS1100 1\"

    .. versionadded:: GeoCom-TPS1100
    """
    CLASS_1202 = 200
    """
    TPS1200 2"

    .. versionadded:: GeoCom-TPS1200
    """
    CLASS_1203 = 201
    """
    TPS1200 3"

    .. versionadded:: GeoCom-TPS1200
    """
    CLASS_1205 = 202
    """
    TPS1200 5"

    .. versionadded:: GeoCom-TPS1200
    """
    CLASS_1201 = 203
    """
    TPS1200 1"

    .. versionadded:: GeoCom-TPS1200
    """
    CLASS_Tx30 = 300
    """
    TS30, MS30 0.5"

    .. versionadded:: GeoCom-TPS1200
    """
    CLASS_Tx31 = 301
    """
    TS30, MS30 1"

    .. versionadded:: GeoCom-TPS1200
    """
    CLASS_TDRA = 350
    """
    TDRA 0.5"

    .. versionadded:: GeoCom-VivaTPS
    """
    CLASS_TS01 = 500
    """
    1"

    .. versionadded:: GeoCom-VivaTPS
    """
    CLASS_TS02 = 501
    """
    2"

    .. versionadded:: GeoCom-VivaTPS
    """
    CLASS_TS03 = 502
    """
    3"

    .. versionadded:: GeoCom-VivaTPS
    """
    CLASS_TS05 = 503
    """
    5"

    .. versionadded:: GeoCom-VivaTPS
    """
    CLASS_TS06 = 504
    """
    6"

    .. versionadded:: GeoCom-VivaTPS
    """
    CLASS_TS07 = 505
    """
    7"

    .. versionadded:: GeoCom-VivaTPS
    """
    CLASS_TS10 = 506
    """
    10"

    .. versionadded:: GeoCom-VivaTPS
    """
    CLASS_TS1X_1 = 600
    """
    Viva 1"

    .. versionadded:: GeoCom-VivaTPS
    """
    CLASS_TS1X_2 = 601
    """
    Viva 2"

    .. versionadded:: GeoCom-VivaTPS
    """
    CLASS_TS1X_3 = 602
    """
    Viva 3"

    .. versionadded:: GeoCom-VivaTPS
    """
    CLASS_TS1X_4 = 603
    """
    Viva 4"

    .. versionadded:: GeoCom-VivaTPS
    """
    CLASS_TS1X_5 = 604
    """
    Viva 5"

    .. versionadded:: GeoCom-VivaTPS
    """
    CLASS_TS50_05 = 650
    """
    TPS1300 TS50/TM50 0.5"

    .. versionadded:: GeoCom-VivaTPS
    """
    CLASS_TS50_1 = 651
    """
    TPS1300 TS50/TM50 1"

    .. versionadded:: GeoCom-VivaTPS
    """


class PowerSource(Enum):
    """
    Instrument power supply.

    .. versionadded:: GeoCom-TPS1100

    ``CSV_POWER_PATH``
    """
    CURRENT = 0
    EXTERNAL = 1
    INTERNAL = 2


class Property(Enum):
    """
    Instrument properties.

    ``CSV_PROPERTY``
    """
    PURCHASE_MODE_NORMAL = 0
    PURCHASE_MODE_PREPAY = 1
    RTK_RANGE_5000 = 2
    RTK_RANGE_UNLIMITED = 3
    RTK_NETWORK = 4
    RTK_REFERENCE_STN = 5
    RTK_LEICA_LITE = 6
    RTK_NETWORK_LOCKDOWN = 7
    POSITION_RATE_5HZ = 8
    POSITION_RATE_20HZ = 9
    GPS_L2 = 10
    GPS_L5 = 11
    GLONASS = 12
    GALILEO = 13
    RAWDATA_LOGGING = 14
    RINEX_LOGGING = 15
    NMEA_OUT = 16
    DGPS_RTCM = 17
    OWI = 18
    NETWORK_PROVIDER_ACCESS_RESET = 19
    NO_AREA_LIMITATION = 20
    SMARTWORX_FULL = 21
    SMARTWORX_LITE = 22
    DEMO_LICENSE = 23
    INTERNAL_WIT2450 = 24
    GEOCOM_ROBOTICS = 25
    GEOCOM_IMAGING = 26
    GEOCOM_GPS = 27
    GEOCOM_LIMITED_AUT = 28
    IMAGING_WITH_OVC = 29
    SERIAL_NUMBER = 30
    PRODUCTION_FLAG = 31
    SYSTEMTIME_VALID = 32


class Reflectorless(Enum):
    """
    Reflectorless EDM class.

    .. versionadded:: GeoCom-TPS1200

    ``TPS_REFLESS_CLASS``
    """
    NONE = 0
    R100 = 1
    R300 = 2
    R400 = 3
    R1000 = 4
    R30 = 5


#######
# DNA #
#######


class StaffType(Enum):
    """
    Digital invar levelling staff type.

    .. versionadded:: GeoCom-LS
    """
    AUTO = 0
    GPCL2 = 3
    """2 m invar staff"""
    GPCL3 = 2
    """3 m invar staff"""


#######
# EDM #
#######


class EDMMode(Enum):
    """
    Distance measurement mode typing base enum.

    ``EDM_MODE``
    """


class EDMModeV1(EDMMode):
    """
    Distance measurement modes for ``TPS1000``.

    .. deprecated:: GeoCom-TPS1100
        Superseded by `EDMMODEV2`.

    ``EDM_MODE``
    """
    SINGLE_STANDARD = 0,
    """Standard single measurement."""
    SINGLE_EXACT = 1,
    """Exact single measurement."""
    SINGLE_FAST = 2,
    """Fast single measurement."""
    CONT_STANDARD = 3,
    """Repeated measurement."""
    CONT_EXACT = 4,
    """Repeated average measurement."""
    CONT_FAST = 5,
    """Fast repeated measurement."""
    UNDEFINED = 6
    """Not defined."""


class EDMModeV2(EDMMode):
    """
    Distance measurement modes for ``TPS1100`` and onwards.

    .. versionadded:: GeoCom-TPS1100
        These settings replace the `EDMMODEV1` options.

    ``EDM_MODE``
    """
    NOTUSED = 0
    """Initialization mode."""
    SINGLE_TAPE = 1
    """IR standard with reflector tape."""
    SINGLE_STANDARD = 2
    """IR standard."""
    SINGLE_FAST = 3
    """IR fast."""
    SINGLE_LRANGE = 4
    """LO standard."""
    SINGLE_SRANGE = 5
    """RL standard."""
    CONT_STANDARD = 6
    """Continuous standard."""
    CONT_DYNAMIC = 7
    """IR tracking."""
    CONT_REFLESS = 8
    """RL tracking."""
    CONT_FAST = 9
    """Continuous fast."""
    AVERAGE_IR = 10
    """IR average."""
    AVERAGE_SR = 11
    """RL average."""
    AVERAGE_LR = 12
    """LO average."""
    PRECISE_IR = 13
    """
    IR precise (TS30, MS30).

    .. versionadded:: GeoCom-TPS1200
    """
    PRECISE_TAPE = 14
    """
    IR precise with reflector tape (TS30, MS30).

    .. versionadded:: GeoCom-TPS1200
    """


class Guidelight(Enum):
    """
    Guide light intensity.

    .. versionadded:: GeoCom-TPS1100

    ``EDM_EGLINTENSITY_TYPE``
    """
    OFF = 0
    LOW = 1
    MID = 2
    HIGH = 3


class MeasurementType(Enum):
    """
    Measurement types.

    ``EDM_MEASUREMENT_TYPE``
    """
    SIGNAL = 1
    FREQ = 2
    DIST = 3
    ANY = 4


class Tracklight(Enum):
    """
    Tracking light brightness

    .. deprecated:: GeoCom-TPS1100
        Superseded by `GUIDELIGHT`.

    ``EDM_TRKLIGHT_BRIGHTNESS``
    """
    LOW = 0
    MID = 1
    HIGH = 2


#######
# FTR #
#######


class Device(Enum):
    """
    Data recording device.

    .. versionadded:: GeoCom-TPS1200-v1.50

    ``FTR_DEVICETYPE``
    """
    INTERNAL = 0
    """Internal memory."""
    CFCARD = 1
    """CF memory card."""
    IMGSDCARD = 2
    """SD memory card."""
    SDCARD = 4
    """SD memory card."""
    USB = 5
    """USB flash drive."""
    RAM = 6
    """Volatile RAM."""


class File(Enum):
    """
    File type.

    .. versionadded:: GeoCom-TPS1200-v1.50

    ``FTR_FILETYPE``
    """
    # UNKNOWN = 0  # ?
    IMAGE = 170
    DATABASE = 103
    IMAGES = 170
    IMAGES_OVERVIEW_JPG = 171
    IMAGES_OVERVIEW_BMP = 172
    IMAGES_TELESCOPIC_JPG = 173
    IMAGES_TELESCOPIC_BMP = 174
    SCANS = 175
    UNKNOWN = 200
    LAST = 201


#######
# MOT #
#######


class ATRLock(Enum):
    """
    ATR lock status.

    ``MOT_LOCK_STATUS``
    """

    NONE = 0
    """Disabled"""
    LOCK = 1
    """Enabled"""
    PREDICT = 2


class Controller(Enum):
    """
    Motor controller operation mode.

    ``MOT_MODE``
    """

    POSITIONING = 0
    """Relative positioning."""
    MOVE = 1
    """Constant speed."""
    MANUAL = 2
    """Manual positioning."""
    LOCK = 3
    """Lock-in controller."""
    BREAK = 4
    """Break controller."""
    # 5, 6 do not use (why?)
    TERMINATE = 7
    """Terminate current task."""


class Stop(Enum):
    """
    Servo motor stopping mode.

    ``MOT_STOPMODE``
    """

    NORMAL = 0
    """Slow down with current acceleration."""
    CUTOFF = 1
    """Slow down by motor power termination."""


#######
# SUP #
#######


class AutoPower(Enum):
    """
    Automatic power off mode.

    ``SUP_AUTO_POWER``
    """

    DISABLED = 0
    """Automatic poweroff disabled."""
    SLEEP = 1
    """Put instument into sleep mode."""
    SHUTDOWN = 2
    """Poweroff instrument."""


#######
# TMC #
#######


class Face(Enum):
    """
    Instrument view face.

    ``TMC_FACE``, ``TMC_FACE_DEF``
    """
    F1 = 0
    """Face left."""
    F2 = 1
    """Face right."""


class Inclination(Enum):
    """
    Inclination calculation mode.

    ``TMC_INCLINE_PRG``
    """

    MEASURE = 0
    """Measure inclination."""
    AUTO = 1
    """Automatic inclination handling."""
    MODEL = 2
    """Model inclination from previous measurements."""


class Measurement(Enum):
    """
    Measurement programs.

    ``TMC_MEASURE_PRG``
    """
    STOP = 0
    """Stop measurement program."""
    DISTANCE = 1
    """Default distance measurement."""
    TRACK = 2
    """
    Track distance.

    .. versionremoved:: GeoCom-TPS1200
    """
    CLEAR = 3
    """Clear current measurement data."""
    SIGNAL = 4
    """Signal intensity measurement."""
    DOMEASURE = 6
    """
    Start/Restart measurement.

    .. versionadded:: GeoCom-TPS1100
    """
    RAPIDTRACK = 8
    """Rapid track distance."""
    REFLESSTRACK = 10
    """
    Reflectorless tracking.

    .. versionadded:: GeoCom-TPS1100
    """
    FREQUENCY = 11
    """
    Frequency measurement.

    .. versionadded:: GeoCom-TPS1100
    """


#######
# WIR #
#######


class Format(Enum):
    """
    Recording format.

    ``WIR_RECFORMAT``
    """
    GSI8 = 0
    GSI16 = 1
