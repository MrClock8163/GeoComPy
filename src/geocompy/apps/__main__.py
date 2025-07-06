from click_extra import (
    extra_group,
)

from . import morse


@extra_group(
    "geocom",
    params=None
)  # type: ignore[misc]
def cli() -> None:
    """Command line applications of the GeoComPy Python package."""
    pass


cli.add_command(morse.cli)
