from typing import Any

from geocompy.data import Angle
from geocompy.gsi.gsiformat import (
    GsiBlock,
    GsiValueWord,
    GsiUnknownWord,
    GsiUnit,
    GsiPointNameWord,
    GsiCodeWord,
    GsiHorizontalAngleWord,
    GsiSlopeDistanceWord,
    GsiPPMPrismConstantWord,
    GsiAppVersionWord,
    GsiBenchmarkHeightWord,
    GsiInfo1Word,
    parse_gsi_word,
    parse_gsi_blocks_from_file
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
        GsiCodeWord,
        ("2", True),
        "41....+?......2 ",
        None,
        None,
        False
    ),
    (
        GsiCodeWord,
        ("2", False),
        "41....+00000002 ",
        None,
        None,
        False
    ),
    (
        GsiCodeWord,
        ("2", True),
        "41....+?..............2 ",
        None,
        None,
        True
    ),
    (
        GsiCodeWord,
        ("2", False),
        "41....+0000000000000002 ",
        None,
        None,
        True
    ),
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


class TestGsiWords:
    def test_parsing(self) -> None:
        for wordtype, args, expected, angleunit, distunit, gsi16 in word_table:
            word = wordtype.parse(expected)
            assert word.value == args
            assert parse_gsi_word(expected).wi == word.wi

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
        with open(filepath, "rt", encoding="utf8") as file:
            blocks = parse_gsi_blocks_from_file(file, dna, True)

        assert len(blocks) == count

        for block in blocks:
            for word in block._words:
                assert not isinstance(
                    word,
                    GsiUnknownWord
                ), f"Block contains unknown word 'WI{word.wi}'"

    def test_parsing(self) -> None:
        self.run_parsing_test(file_tps_mixed, 8)
        self.run_parsing_test(file_dna_mixed, 7, True)

    def test_serialization(self) -> None:
        b1 = GsiBlock(
            "P1",
            "measurement",
            GsiBenchmarkHeightWord(123.456),
            address=0
        )
        text = b1.serialize(1, distunit=GsiUnit.CENTIMILLI, endl=False)
        assert text == "110001+000000P1 83...8+12345600 "

        b2 = GsiBlock(
            "2",
            "specialcode",
            GsiInfo1Word("STN"),
            address=2
        )
        text = b2.serialize(None, True, endl=False)
        assert text == "*410002+?..............2 42....+0000000000000STN "

        b3 = GsiBlock(
            "2",
            "code",
            GsiInfo1Word("STN"),
            address=3
        )
        text = b3.serialize(None, True, endl=False)
        assert text == "*410003+0000000000000002 42....+0000000000000STN "
