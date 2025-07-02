from time import sleep
from typing import Literal

from tap import Tap

from geocompy import open_serial, GeoCom


class MorseArguments(Tap):
    """
    Play a Morse encoded ASCII message through the beep signals
    of a GeoCom capable total station.
    """

    port: str
    """serial port"""
    baud: int = 9600
    """speed"""
    timeout: int = 15
    """timeout in seconds"""

    unit: int = 50
    """beep unit time in milliseconds"""
    compatibility: Literal['TPS1000'] | None = None
    """instrument compatibility mode"""

    intensity: int
    """beep intensity [1-100]"""
    message: str
    """message to relay"""

    def configure(self) -> None:
        self.add_argument("port")
        self.add_argument("-b", "--baud")
        self.add_argument("-t", "--timeout")
        self.add_argument("-u", "--unit")
        self.add_argument("-c", "--compatibility")
        self.add_argument("intensity")
        self.add_argument("message")


def morse_beep(tps: GeoCom, args: MorseArguments) -> None:
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


def main(args: MorseArguments) -> None:
    with open_serial(args.port, speed=args.baud, timeout=args.timeout) as com:
        ts = GeoCom(com)
        morse_beep(ts, args)


if __name__ == "__main__":
    parser = MorseArguments()
    args = parser.parse_args()
    main(args)
