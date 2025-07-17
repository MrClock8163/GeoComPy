from time import sleep
from typing import Callable, Any

try:
    from click_extra import (
        extra_command,
        option,
        option_group,
        argument,
        Choice,
        IntRange,
        progressbar
    )
except ModuleNotFoundError:
    print(
        """
Missing dependencies. The Morse app needs the following dependencies:
- click-extra

Install the missing dependencies manually, or install GeoComPy with the
'apps' extra:

pip install geocompy[apps]
"""
    )
    exit(3)

from ..geo import GeoCom
from ..communication import open_serial
from .utils import (
    echo_red,
    echo_green,
    com_baud_option,
    com_timeout_option
)


MORSE_TABLE = {
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
    "0": "-----",
    "&": ".-...",
    "'": ".----.",
    "@": ".--.-.",
    "(": "-.--.",
    ")": "-.--.-",
    ":": "---...",
    ",": "--..--",
    "=": "-...-",
    "!": "-.-.--",
    ".": ".-.-.-",
    "-": "-....-",
    "%": "------..-.-----",
    "+": ".-.-.",
    "\"": ".-..-.",
    "?": "..--..",
    "/": "-..-.",
    "\n": ".-.-"
}


def encode_message(
    message: str
) -> str:
    words: list[str] = []
    for word in message.lower().split(" "):
        w: list[str] = []
        for letter in word:
            w.append("|".join(MORSE_TABLE.get(letter, "")))

        words.append("_".join(w))

    return " ".join(words)


def relay_message(
    beepstart: Callable[[], Any],
    beepstop: Callable[[], Any],
    message: str,
    unittime: float
) -> None:
    encoded = encode_message(message)
    with progressbar(
        encoded,
        label="Relaying message",
        show_eta=False
    ) as stream:
        for char in stream:
            match char:
                case ".":
                    beepstart()
                    sleep(unittime)
                    beepstop()
                case "-":
                    beepstart()
                    sleep(3 * unittime)
                    beepstop()
                case "|":
                    sleep(unittime)
                case "_":
                    sleep(3 * unittime)
                case " ":
                    sleep(7 * unittime)
                case _:
                    raise ValueError(
                        f"Invalid morse stream character: '{char}'"
                    )


@extra_command(
    "morse",
    params=None,
    context_settings={"auto_envvar_prefix": None}
)  # type: ignore[misc]
@argument(
    "port",
    help=(
        "serial port that the instrument is connected to (must be a valid "
        "identifier like COM1 or /dev/usbtty0)"
    ),
    type=str
)
@argument(
    "message",
    help="message to relay as a string of ASCII characters",
    type=str
)
@option(
    "-i",
    "--intensity",
    help="beeping intensity",
    type=IntRange(0, 100),
    default=100
)
@option(
    "-u",
    "--unittime",
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
@option(
    "--ignore-non-ascii",
    help="suppress encoding errors and skip non-ASCII characters",
    is_flag=True
)
@option_group(
    "Connection options",
    "Options related to the serial connection",
    com_baud_option,
    com_timeout_option
)
def cli(
    port: str,
    message: str,
    intensity: int = 100,
    ignore_non_ascii: bool = False,
    baud: int = 9600,
    timeout: int = 15,
    unittime: int = 50,
    compatibility: str = "none",
) -> None:
    """Play a Morse encoded ASCII message through the beep signals
        of a GeoCom capable total station.
        """
    if not ignore_non_ascii:
        try:
            message.casefold().encode("ascii")
        except UnicodeEncodeError:
            echo_red("The message contains non-ASCII characters.")
            exit(1)

    with open_serial(port, speed=baud, timeout=timeout) as com:
        tps = GeoCom(com)
        beepstart = tps.bmm.beep_start
        beepstop = tps.bmm.beep_stop
        match compatibility.lower():
            case "tps1000":
                beepstart = tps.bmm.beep_on
                beepstop = tps.bmm.beep_off
            case "none":
                pass

        relay_message(
            lambda: beepstart(intensity),
            beepstop,
            message,
            unittime * 1e-3
        )
        echo_green("Message complete.")


if __name__ == "__main__":
    cli()
