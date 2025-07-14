from time import sleep
from typing import Callable, Any

from click_extra import (
    extra_command,
    option,
    option_group,
    argument,
    version_option,
    Choice,
    IntRange
)

from geocompy import open_serial, GeoCom


def morse_character(
    letter: str,
    unit: float,
    beepstart: Callable[[], Any],
    beepstop: Callable[[], Any]
) -> None:
    lookup = {
        "a": ".-",
        "b": "-...",
        "c": "-.-.",
        "d": "-..",
        "e": ".",
        "f": "..-.",
        "g": "--.",
        "h": "....",
        "i": "..",
        "j": ".---",
        "k": "-.-",
        "l": ".-..",
        "m": "--",
        "n": "-.",
        "o": "---",
        "p": ".--.",
        "q": "--.-",
        "r": ".-.",
        "s": "...",
        "t": "-",
        "u": "..-",
        "v": "...-",
        "w": ".--",
        "x": "-..-",
        "y": "-.--",
        "z": "--..",
        "1": ".----",
        "2": "..---",
        "3": "...--",
        "4": "....-",
        "5": ".....",
        "6": "-....",
        "7": "--...",
        "8": "---..",
        "9": "----.",
        "0": "-----"
    }
    code = lookup[letter]
    for i, signal in enumerate(code):
        beepstart()
        match signal:
            case ".":
                sleep(unit)
            case "-":
                sleep(unit * 3)
        beepstop()
        if i != len(code) - 1:
            sleep(unit)


def morse_message(
    tps: GeoCom,
    message: str,
    intensity: int,
    unit: float,
    compatibility: str
) -> None:
    unit_seconds = unit * 1e-3

    beepstart = tps.bmm.beep_start
    beepstop = tps.bmm.beep_stop
    match compatibility.lower():
        case "tps1000":
            beepstart = tps.bmm.beep_on
            beepstop = tps.bmm.beep_off
        case "none":
            pass
        case _:
            raise ValueError(f"Unknown compatibility option: {compatibility}")

    words = message.lower().split(" ")
    for i, word in enumerate(words):
        for j, letter in enumerate(word):
            morse_character(
                letter,
                unit_seconds,
                lambda: beepstart(intensity),
                beepstop
            )

            if j != len(word) - 1:
                sleep(unit_seconds * 3)

        if i != len(words) - 1:
            sleep(unit_seconds * 7)


@extra_command(
    "morse",
    params=None,
    context_settings={"auto_envvar_prefix": None}
)  # type: ignore[misc]
@version_option()
@argument("port", type=str)
@argument("message", type=str)
@option(
    "-i",
    "--intensity",
    help="beeping intensity",
    type=IntRange(0, 100),
    default=100
)
@option(
    "-u",
    "--unit",
    help="beep unit time in milliseconds [ms]",
    type=IntRange(min=50),
    default=50
)
@option(
    "-c",
    "--compatibility",
    help="instrument compatibility",
    type=Choice(["none", "TPS1000"], case_sensitive=False),
    default="none"
)
@option_group(
    "Connection options",
    "Options related to the serial connection",
    option(
        "-b",
        "--baud",
        help="serial speed",
        type=int,
        default=9600
    ),
    option(
        "-t",
        "--timeout",
        help="serial timeout",
        type=IntRange(min=0),
        default=15
    )
)
def cli(
    port: str,
    message: str,
    intensity: int = 100,
    baud: int = 9600,
    timeout: int = 15,
    unit: int = 50,
    compatibility: str = "none",
) -> None:
    """Play a Morse encoded ASCII message through the beep signals
        of a GeoCom capable total station.

        PORT is the serial port, that the instrument is connected to. It
        must be a valid identifier as a string (e.g. COM1 or /dev/usbtty0).

        MESSAGE is the message to relay, as a string of ASCII characters.
        """
    with open_serial(port, speed=baud, timeout=timeout) as com:
        ts = GeoCom(com)
        morse_message(
            ts,
            message,
            intensity,
            unit,
            compatibility
        )


if __name__ == "__main__":
    cli()
