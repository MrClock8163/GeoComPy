from typing import Any

from geocompy.data import Angle
from geocompy.gsi.gsiformat import (
    GsiBlock,
    GsiWord,
    GsiValueWord,
    GsiUnknownWord,
    GsiUnit,
    GsiPointNameWord,
    GsiHorizontalAngleWord,
    GsiSlopeDistanceWord,
    GsiPPMPrismConstantWord,
    GsiAppVersionWord,
    GsiBenchmarkHeightWord,
    GsiInfo1Word,
    parse_gsi_word
)


file_tps_mixed = "tests/data/tps_data.gsi"
file_dna_mixed = "tests/data/dna_data.gsi"


word_table: list[
    tuple[
        type[GsiValueWord],
        tuple[Any, ...] | Any,
        str,
        GsiUnit | None,
        GsiUnit | None,
        bool
    ]
] = [
    (GsiPointNameWord, "P1", "11....+000000P1 ", None, None, False),
    (
        GsiHorizontalAngleWord,
        Angle(180, 'deg'),
        "21...3+18000000 ",
        GsiUnit.DEG,
        None,
        False
    ),
    (
        GsiSlopeDistanceWord,
        123123.456,
        "31...8+0000012312345600 ",
        None,
        GsiUnit.CENTIMILLI,
        True
    ),
    (
        GsiPPMPrismConstantWord,
        (11, -17),
        "51....+0011-017 ",
        None,
        None,
        False
    ),
    (
        GsiAppVersionWord,
        123.456,
        "590..6+01234560 ",
        None,
        GsiUnit.DECIMILLI,
        False
    )
]


def match_word_serialized(
    word: GsiWord,
    expected: str,
    angleunit: GsiUnit | None = GsiUnit.DEG,
    distunit: GsiUnit | None = GsiUnit.MILLI,
    gsi16: bool = False
) -> bool:
    return word.serialize(gsi16, angleunit, distunit) == expected


class TestGsiWords:
    def test_parsing(self) -> None:
        for wordtype, args, expected, angleunit, distunit, gsi16 in word_table:
            word = wordtype.parse(expected)
            assert word.value == args
            assert parse_gsi_word(expected).wi() == word.wi()

    def test_serialization(self) -> None:
        for wordtype, args, expected, angleunit, distunit, gsi16 in word_table:
            if isinstance(args, tuple):
                word = wordtype(*args)
            else:
                word = wordtype(args)

            assert word.serialize(
                gsi16,
                angleunit,
                distunit
            ) == expected


class TestGsiBlock:
    def run_parsing_test(
        self,
        filepath: str,
        count: int,
        dna: bool = False
    ) -> None:
        blocks: list[GsiBlock] = []
        with open(filepath, "rt", encoding="utf8") as file:
            for line in file:
                block = GsiBlock.parse(line.strip("\n"), dna, True)

                blocks.append(block)

        assert len(blocks) == count

        for block in blocks:
            for word in block.words:
                assert not isinstance(
                    word,
                    GsiUnknownWord
                ), f"{word.actual_wi()}"

    def test_parsing(self) -> None:
        self.run_parsing_test(file_tps_mixed, 8)
        self.run_parsing_test(file_dna_mixed, 7, True)

    def test_serialization(self) -> None:
        b1 = GsiBlock("P1", "measurement", 1)
        b1.words.append(
            GsiBenchmarkHeightWord(123.456)
        )
        text = b1.serialize(distunit=GsiUnit.CENTIMILLI, endl=False)
        assert text == "110001+000000P1 83...8+12345600 "

        b2 = GsiBlock("?..............2", "code", 2)
        b2.words.append(
            GsiInfo1Word("STN")
        )
        text = b2.serialize(True, endl=False)
        assert text == "*410002+?..............2 42....+0000000000000STN "
