import argparse

from serial import SerialException

from geocompy import open_serial, GeoCom, GeoComCode, Angle


def tests(tps: GeoCom) -> None:
    print("GeoCom connection successful")
    print(
        "Various GeoCom functions will be tested. Certain settings will be "
        "changed on the instrument (ATR off, prism target off, etc.)."
    )
    print(
        "The program will attempt to use motorized functions. Give "
        "appropriate clearance for the instrument!"
    )
    input("Press ENTER when ready to proceed...")

    print("(Switching ATR off...)")
    tps.aut.switch_atr(False)
    tps.aus.switch_user_atr(False)
    print("(Switching to reflectorless EDM mode...)")
    tps.bap.set_target_type('DIRECT')
    resp_measure = tps.tmc.do_measurement()
    resp_angles = tps.tmc.get_simple_measurement()
    if (
        resp_measure.error == GeoComCode.OK
        and resp_angles.error == GeoComCode.OK
    ):
        print("Measurements available")
    else:
        print(f"Measurements unavailable ({resp_measure.response})")

    resp_focus = tps.cam.set_focus_to_infinity()
    if resp_focus.error == GeoComCode.OK:
        print("Imaging available")
    else:
        print(f"Imaging unavailable ({resp_focus.response})")

    resp_changeface = tps.aut.turn_to(0, Angle(180, 'deg'))
    if resp_changeface.error == GeoComCode.OK:
        print("Motorization available")
    else:
        print(f"Mororization unavailable ({resp_changeface.response})")


def cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        "tester",
        description=(
            "Rudimentary tests for determining what GeoCom functions are "
            "available on an instrument."
        )
    )
    group_com = parser.add_argument_group("communication")
    group_com.add_argument(
        "port",
        help="serial port",
        type=str
    )
    group_com.add_argument(
        "-b",
        "--baud",
        help="speed",
        type=int,
        default=9600
    )
    group_com.add_argument(
        "-t",
        "--timeout",
        help="timeout in seconds",
        type=int,
        default=15
    )

    return parser


if __name__ == "__main__":
    parser = cli()
    args = parser.parse_args()
    try:
        with open_serial(
            args.port,
            speed=args.baud,
            timeout=args.timeout
        ) as com:
            tps = GeoCom(com)
            tests(tps)
    except (SerialException, ConnectionError) as e:
        print(f"GeoCom connection was not successful ({e})")
