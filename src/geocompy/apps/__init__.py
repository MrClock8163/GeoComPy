from typing import Callable, TypeVar, Iterable

_T = TypeVar("_T")


def user_input(
    prompt: str,
    parser: Callable[[str], _T],
    newline: bool = True
) -> _T:
    while True:
        ans = input(f"> {prompt}{"\n" if newline else ""}")
        try:
            return parser(ans)
        except Exception as e:
            print(e)


def parse_choices_map(
    value: str,
    choices: dict[str, _T],
    ignore_case: bool = True,
    allow_short: bool = True
) -> _T:
    if ignore_case:
        value = value.lower()
        choices.update({(k.lower(), v) for k, v in choices.items()})

    try:
        if allow_short:
            possible = list(
                filter(lambda k: k.startswith(value), choices.keys())
            )
            if len(possible) != 1:
                raise KeyError()
            value = possible[0]

        return choices[value]
    except KeyError:
        raise ValueError(
            f"> {value} is not in the list of acceptable inputs "
            f"({tuple(choices.keys())})"
        )


def parse_choices(
    value: str,
    choices: Iterable[str],
    ignore_case: bool = True,
    allow_short: bool = True
) -> str:
    return parse_choices_map(
        value,
        {k: k for k in choices},
        ignore_case,
        allow_short
    )


def parse_yes_no(value: str) -> bool:
    return parse_choices_map(
        value,
        {
            "yes": True,
            "no": False
        }
    )


def parse_cancel_replace_append(value: str) -> str:
    return parse_choices(
        value,
        ("cancel", "replace", "append")
    )
