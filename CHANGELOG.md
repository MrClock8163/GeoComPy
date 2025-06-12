# Changelog

## v0.7.0 (in development)

### Added

- `retry` option to `open_serial`
- Interactive Terminal CLI application (`geocompy.apps.terminal`)
- Set Measurement CLI application (`geocompy.apps.setmeasurement`)

## v0.6.0

### Added

- GeoCom
  - Digital Level
    - LS10/15 GeoCom support through new `dna` subsytem (LS10/15 also responds to GSI Online DNA commands)
  - Central Services
    - `get_firmware_creation_date` command (RPC 5038)
    - `get_datetime_new` command (RPC 5051)
    - `set_datetime_new` command (RPC 5050)
    - `setup_listing` command (RPC 5072)
    - `get_maintenance_end` command (RPC 5114)
  - Theodolite Measurement and Calculation
    - `get_complete_measurement` command (RPC 2167)

### Fixed

- `morse.py` example script was not using the most up-to-date methods
- GeoCom File Transfer subsystem commmands were missing from the command name lookup table

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
