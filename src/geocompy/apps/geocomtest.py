try:
    from click_extra import (
        extra_command,
        argument,
        echo,
        prompt
    )
except ModuleNotFoundError:
    print(
        """
Missing dependencies. The GeoCom test app needs the following dependencies:
- click-extra

Install the missing dependencies manually, or install GeoComPy with the
'apps' extra:

pip install geocompy[apps]
"""
    )
    exit(3)

from serial import SerialException

from ..data import Angle
from ..geo import GeoCom
from ..geo.gctypes import GeoComCode
from ..communication import open_serial
from .utils import (
    echo_red,
    echo_green,
    echo_yellow,
    com_baud_option,
    com_timeout_option
)


def tests(tps: GeoCom) -> None:
    echo("GeoCom connection successful")
    echo(
        "Various GeoCom functions will be tested. Certain settings will be "
        "changed on the instrument (ATR off, prism target off, etc.)."
    )
    echo(
        "The program will attempt to use motorized functions. Give "
        "appropriate clearance for the instrument!"
    )
    prompt("Press ENTER when ready to proceed...")

    echo("(Switching ATR off...)")
    tps.aut.switch_atr(False)
    tps.aus.switch_user_atr(False)
    echo("(Switching to reflectorless EDM mode...)")
    tps.bap.set_target_type('DIRECT')
    resp_measure = tps.tmc.do_measurement()
    resp_angles = tps.tmc.get_simple_measurement()
    if (
        resp_measure.error == GeoComCode.OK
        and resp_angles.error == GeoComCode.OK
    ):
        echo_green("Measurements available")
    else:
        echo_yellow(f"Measurements unavailable ({resp_measure.response})")

    resp_focus = tps.cam.set_focus_to_infinity()
    if resp_focus.error == GeoComCode.OK:
        echo_green("Imaging available")
    else:
        echo_yellow(f"Imaging unavailable ({resp_focus.response})")

    resp_changeface = tps.aut.turn_to(0, Angle(180, 'deg'))
    if resp_changeface.error == GeoComCode.OK:
        echo_green("Motorization available")
    else:
        echo_yellow(f"Mororization unavailable ({resp_changeface.response})")


@extra_command(
    "test",
    params=None,
    context_settings={"auto_envvar_prefix": None}
)  # type: ignore[misc]
@argument(
    "port",
    type=str,
    help="serial port (e.g. COM1)"
)
@com_baud_option
@com_timeout_option
def cli(
    port: str,
    baud: int = 9600,
    timeout: int = 15
) -> None:
    """Rudimentary tests for determining what GeoCom functions are
    available on an instrument.
    """

    try:
        with open_serial(
            port,
            speed=baud,
            timeout=timeout
        ) as com:
            tps = GeoCom(com)
            tests(tps)
    except (SerialException, ConnectionError) as e:
        echo_red(f"GeoCom connection was not successful ({e})")
