from click_extra import extra_group

from . import process
from . import measure


@extra_group("sets", params=None)  # type: ignore[misc]
def cli() -> None:
    """Conduct sets of measurements to predefined targets."""


cli.add_command(process.cli_merge)
cli.add_command(process.cli_validate)
cli.add_command(process.cli_calc)
cli.add_command(measure.cli)
