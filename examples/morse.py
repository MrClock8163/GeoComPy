import argparse
from time import sleep

from geocompy import open_serial, GeoCom


def morse_beep(tps: GeoCom, message: str, intensity: int) -> None:
    def letter_beep(tps: GeoCom, letter: str, intensity: int) -> None:
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
            tps.bmm.beep_on(intensity)
            match signal:
                case ".":
                    sleep(unit)
                case "-":
                    sleep(unit * 3)
            tps.bmm.beep_off()
            if i != len(code) - 1:
                sleep(unit)

    unit = 0.05
    words = message.lower().split(" ")
    for i, word in enumerate(words):
        for j, letter in enumerate(word):
            letter_beep(tps, letter, intensity)

            if j != len(word) - 1:
                sleep(unit * 3)

        if i != len(words) - 1:
            sleep(unit * 7)


def cli() -> None:
    parser = argparse.ArgumentParser()
    group_com = parser.add_argument_group("communication")
    group_com.add_argument("port", help="serial port", type=str)
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
        help="communication timeout",
        type=int,
        default=15
    )
    parser.add_argument("intensity", help="beep intensity [1-100]", type=int)
    parser.add_argument("message", help="message to encode", type=str)

    args = parser.parse_args()

    with open_serial(args.port, speed=args.baud, timeout=args.timeout) as com:
        ts = GeoCom(com)
        morse_beep(ts, args.message, args.intensity)


if __name__ == "__main__":
    cli()
