import argparse
from time import sleep

from serial import Serial

from geocompy.communication import SerialConnection
from geocompy import GeoCom


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
    parser.add_argument("port", help="serial port", type=str)
    parser.add_argument("intensity", help="beep intensity [1-100]", type=int)
    parser.add_argument("message", help="message to encode", type=str)

    args = parser.parse_args()

    port = Serial(args.port)
    with SerialConnection(port) as conn:
        ts = GeoCom(conn)

        morse_beep(ts, args.message, args.intensity)


if __name__ == "__main__":
    cli()
