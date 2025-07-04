import argparse
from time import sleep

from geocompy import open_serial, GeoCom


def morse_beep(tps: GeoCom, args: argparse.Namespace) -> None:
    def letter_beep(letter: str) -> None:
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
            beepstart(intensity)
            match signal:
                case ".":
                    sleep(unit)
                case "-":
                    sleep(unit * 3)
            beepstop()
            if i != len(code) - 1:
                sleep(unit)

    unit = args.unit * 1e-3
    intensity = args.intensity
    beepstart = tps.bmm.beep_start
    beepstop = tps.bmm.beep_stop
    if args.compatibility == "TPS1000":
        beepstart = tps.bmm.beep_on
        beepstop = tps.bmm.beep_off
    words = args.message.lower().split(" ")
    for i, word in enumerate(words):
        for j, letter in enumerate(word):
            letter_beep(letter)

            if j != len(word) - 1:
                sleep(unit * 3)

        if i != len(words) - 1:
            sleep(unit * 7)


def main(args: argparse.Namespace) -> None:
    with open_serial(args.port, speed=args.baud, timeout=args.timeout) as com:
        ts = GeoCom(com)
        morse_beep(ts, args)


def cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        "morse",
        description=(
            "Play a Morse encoded ASCII message through the beep signals "
            "of a GeoCom capable total station."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    group_com = parser.add_argument_group("communication")
    group_com.add_argument("port", help="serial port", type=str)
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
        help="timeout",
        type=int,
        default=15
    )
    parser.add_argument(
        "-u",
        "--unit",
        help="beep unit time in milliseconds",
        type=int,
        default=50
    )
    parser.add_argument(
        "-c",
        "--compatibility",
        help="instrument compatibility mode",
        type=str,
        choices=["TPS1000"]
    )
    parser.add_argument("intensity", help="beep intensity [1-100]", type=int)
    parser.add_argument("message", help="message to encode", type=str)

    return parser


if __name__ == "__main__":
    parser = cli()
    args = parser.parse_args()
    main(args)
