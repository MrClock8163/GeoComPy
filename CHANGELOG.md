# Changelog

## v0.6.0 (in development)

### Added

- `retry` option to `open_serial`
- Interactive Terminal CLI application (`geocompy.apps.terminal`)
- Set Measurement CLI application (`geocompy.apps.setmeasurement`)

## v0.5.1

### Added

- Missing GeoCom `abort` command
- Discovered GeoCom RPC 11009 (unknown true function name, implemented as
  `switch_display`)

### Fixed

- GeoCom `get_internal_temperature` returned `int` instead of `float`
- GeoCom `get_user_prism_definition` had incorrect return param parsers

## v0.5.0

Initial release on PyPI.

Notable features:

- Serial communication handler
- Utility data types
- GeoCom commands from TPS1000, 1100, 1200 and VivaTPS instruments
  (and any other with overlapping command set)
- GSI Online commands for DNA instruments
