import argparse

from geocompy import open_serial, GeoCom, GeoComCode


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

    tps.aut.switch_atr(False)
    tps.aus.switch_user_atr(False)
    tps.bap.set_target_type('DIRECT')
    resp_measure = tps.tmc.do_measurement()
    resp_angles = tps.tmc.get_simple_measurement()
    if (
        resp_measure.error == GeoComCode.OK
        and resp_angles.error == GeoComCode.OK
    ):
        print("Measurements available")
    else:
        print(f"Measurements unavailable {resp_measure.error}")

    resp_focus = tps.cam.set_focus_to_infinity()
    if resp_focus.error == GeoComCode.OK:
        print("Imaging available")
    else:
        print(f"Imaging unavailable {resp_focus.error}")

    resp_changeface = tps.aut.change_face()
    if resp_changeface.error == GeoComCode.OK:
        print("Motorization available")
        tps.aut.change_face()
    else:
        print(f"Mororization unavailable {resp_changeface.error}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group_com = parser.add_argument_group("communication")
    group_com.add_argument(
        "port",
        help="serial port",
        type=str
    )
    group_com.add_argument(
        "-b",
        "--baud",
        help="communication speed",
        type=int,
        default=9600
    )
    group_com.add_argument(
        "-t",
        "--timeout",
        help="communication timeout in seconds",
        type=int,
        default=15
    )

    args = parser.parse_args()
    with open_serial(
        args.port,
        speed=args.baud,
        timeout=args.timeout
    ) as com:
        tps = GeoCom(com)
        tests(tps)
