from time import sleep

try:
    from click_extra import (
        extra_command,
        option,
        option_group,
        argument,
        version_option,
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
from .utils import echo_red, echo_green


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

    encoded = encode_message(message)
    with progressbar(
        encoded,
        label="Relaying message",
        show_eta=False
    ) as stream:
        for char in stream:
            match char:
                case ".":
                    beepstart(intensity)
                    sleep(unit_seconds)
                    beepstop()
                case "-":
                    beepstart(intensity)
                    sleep(3 * unit_seconds)
                    beepstop()
                case "|":
                    sleep(unit_seconds)
                case "_":
                    sleep(3 * unit_seconds)
                case " ":
                    sleep(7 * unit_seconds)
                case _:
                    raise ValueError(
                        f"Invalid morse stream character: '{char}'"
                    )


@extra_command(
    "morse",
    params=None,
    context_settings={"auto_envvar_prefix": None}
)  # type: ignore[misc]
@version_option()
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
        """
    try:
        message.casefold().encode("ascii")
    except UnicodeEncodeError:
        echo_red("The message contains non-ASCII characters.")
        exit(1)

    with open_serial(port, speed=baud, timeout=timeout) as com:
        ts = GeoCom(com)
        morse_message(
            ts,
            message,
            intensity,
            unit,
            compatibility
        )
        echo_green("Message complete.")


if __name__ == "__main__":
    cli()
