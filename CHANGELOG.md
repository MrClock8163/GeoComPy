# Changelog

All notable changes in the GeoComPy project will be documented in this
file.

The project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added

- Added support for checksums in GeoCOM transactions
- Added `SocketConnection` to allow socket based communication
- Added `open_socket` function to create TCP and RFCOMM socket connections

## Changed

- Changed the `Connection` interface definition to require `send_binary`,
  `receive_binary` and `exchange_binary` methods
- Changed `open_serial` to raise `ConnectionRefusedError` instead of the
  original exception when the connection could not be opened
- Changed all methods of `SerialConnection` to raise the general
  `ConnectionEror` and `TimeoutError` instead of serial specific
  `SerialException` and`SerialTimeoutException`
- Changed `GeoCom` init to raise `ConnectionRefusedError` instead of
  `ConnectionError` when the connection could not be verified
- Changed `GsiOnlineDNA` init to raise `ConnectionRefusedError` instead of
  `ConnectionError` when the connection could not be verified
- Updated GeoCOM response parsing to raise exception when the number of
  received paramters does not match the number of parsers specified
- Updated `GeoCom` init signature to require keyword arguments
- Updated `GsiOnlineDNA` init signature to require keyword arguments
- Updated `Angle` init signature to require keyword arguments
- Updated `GsiWord` and subclass init signatures to require keyword arguments
- Updated `GsiBlock` `.parse` and `.serialize` signatures to require keyword
  arguments
- Updated `parse_gsi_word` signature to require keyword arguments
- Updated `parse_gsi_blocks_from_file` signature to require keyword arguments
- Updated `write_gsi_blocks_to_file` signature to require keyword arguments
- Renamed `retry` option of `open_serial` to `attempts`
- Renamed `retry` option of `GeoCom` to `attempts`
- Renamed `retry` option of `GsiOnlineDNA` to `attempts`

## v0.13.0 (2025-09-29)

### Added

- Added `dot` product to `Vector`
- Added `cross` product to `Vector`
- Added `device` option to GeoCOM CSV `setup_listing`

### Changed

- Reworked arithmetic operations supported by `Angle`
- Reworked arithmetic operations supported by `Vector`
- Renamed `parsestr` to `parse_string`
- Renamed `parsebool` to `parse_bool`
- Renamed `toenum` to `get_enum`
- Renamed `enumparser` to `get_enum_parser`
- Updated GeoCOM FTR `download` to return `bytes` instead of `str`
- Updated GeoCOM FTR `download_large` to return `bytes` instead of `str`

### Fixed

- GeoCOM IMG `set_telescopic_configuration` was missing the `prefix` parameter
- GeoCOM CSV `get_voltage_memory` was calling the wrong GeoCOM commmand
- `Angle.to_dms` was sometimes returning incorrect value due to rounding
- Package could not be installed from ZIP due to a missing version fallback

### Removed

- Removed `normalize_rad` classmethod from `Angle`

## v0.12.0 (2025-08-26)

### Added

- Added Leica GSI format module
  - Container types for words
  - Container type for blocks
  - Parsing
  - Serialization

### Changed

- GSI Online DNA commands now use the new GSI format module for GSI parsing
  and serialization

### Fixed

- Fixed DMS angle formatting where leading zeroes were missing from seconds

### Removed

- Removed the obsolete `gsiword` utility function from the `data` module

## v0.11.0 (2025-08-14)

### Added

- Added discovered GeoCOM RPC 5074 (unknown true function name, implemented as
  `abort_listing` in CSV subsystem)
- Added `logger` optional parameter to `open_serial`
- Added `logger` optional parameter to `SerialConnection`

### Changed

- Renamed GeoCOM FTR `abort_list` to `abort_listing`

### Fixed

- GeoCOM CSV `list` command did not properly parse returned string parameters

### Removed

- Removed `get_logger` utility function

## v0.10.0 (2025-08-08)

### Added

- Added `relative_to` method to the `Angle` type
- Added precision option to DMS angle formatting

### Changed

- Renamed GeoCOM TMC `set_orientation` to `set_azimuth` to make its purpose more
  obvious
- Changed input parameter type of `set_azimuth` to be more permissive

## v0.9.0 (2025-08-01)

Starting with this version, the package is in beta stage. The public API is
not going to drastically change from this point. Small changes, and
developments are still to come.

### Changed

- GeoCOM CSV `get_laserlot_status` was renamed to `get_laserplummet_status`
- GeoCOM CSV `switch_laserlot` was renamed to `switch_laserplummet`
- GeoCOM CSV `get_laserlot_intensity` was renamed to
`get_laserplummet_intensity`
- GeoCOM CSV `set_laserlot_intensity` was renamed to
`set_laserplummet_intensity`

## v0.8.1 (2025-07-30)

### Added

- new methods for `SerialConnection` wrapper:
  - `send_binary`
  - `receive_binary`
  - `exchange_binary`
- `precision` property for the GeoCOM definition

### Changed

- GeoCOM TMC `get_angle_correction_status` was renamed to
  `get_angle_correction`
- GeoCOM TMC `switch_angle_correction` was renamed to `set_angle_correction`
- GeoCOM `get_double_precision` was moved to COM
- GeoCOM `set_double_precision` was moved to COM

### Fixed

- method docstrings were rendered wrong in some cases due to missing new lines
- GSI Online DNA settings commands were parsing boolean value incorrectly
- GeoCOM AUT `set_search_area` command would not execute due to incorrect
  parameter serialization when sending the request to the instrument

## v0.8.0 (2025-07-24)

All CLI applications were migrated to a new package called
[Instrumentman](https://github.com/MrClock8163/Instrumentman). Further
development happens there.

### Added

- Component swizzling in vectors and coordinates

### Changed

- Wait/delay times are now expected in seconds instead of milliseconds,
  where possible

## v0.7.0 (2025-06-29)

### Added

- `retry` option to `open_serial`
- Morse CLI application (`geocompy.apps.morse`)
- Interactive Terminal CLI application (`geocompy.apps.terminal`)
- Set Measurement CLI applications (`geocompy.apps.setmeasurement...`)

## v0.6.0 (2025-06-12)

### Added

- GeoCOM
  - Digital Level
    - LS10/15 GeoCOM support through new `dna` subsytem (LS10/15 also responds
      to GSI Online DNA commands)
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
- GeoCOM File Transfer subsystem commmands were missing from the command name
  lookup table

## v0.5.1 (2025-05-16)

### Added

- Missing GeoCOM `abort` command
- Discovered GeoCOM RPC 11009 (unknown true function name, implemented as
  `switch_display`)

### Fixed

- GeoCOM `get_internal_temperature` returned `int` instead of `float`
- GeoCOM `get_user_prism_definition` had incorrect return param parsers

## v0.5.0 (2025-05-15)

Initial release on PyPI.

Notable features:

- Serial communication handler
- Utility data types
- GeoCOM commands from TPS1000, 1100, 1200 and VivaTPS instruments
  (and any other with overlapping command set)
- GSI Online commands for DNA instruments
