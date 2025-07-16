from click_extra import (
    extra_group,
)

from . import morse
from . import terminal
from . import setup
from . import setmeasurement
from . import geocomtest


@extra_group(
    "geocom",
    params=None
)  # type: ignore[misc]
def cli() -> None:
    """Command line applications of the GeoComPy Python package."""
    pass


cli.add_command(morse.cli)
cli.add_command(terminal.cli)
cli.add_command(setup.cli)
cli.add_command(setmeasurement.cli)
cli.add_command(geocomtest.cli)
