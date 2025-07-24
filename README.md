<h1 align="center">
<img src="https://raw.githubusercontent.com/mrclock8163/geocompy/main/docs/geocompy_logo.png" alt="GeoComPy logo" width="300">
</h1><br>

[![PyPI - Version](https://img.shields.io/pypi/v/geocompy)](https://pypi.org/project/geocompy/)
[![Python Version](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2FMrClock8163%2FGeoComPy%2Frefs%2Fheads%2Fmain%2Fpyproject.toml)](https://pypi.org/project/geocompy/)
[![MIT](https://img.shields.io/github/license/mrclock8163/geocompy)](https://opensource.org/license/mit)
[![Tests status](https://img.shields.io/github/actions/workflow/status/mrclock8163/geocompy/run-tests.yml?label=tests)](https://github.com/MrClock8163/GeoComPy)
[![Docs status](https://app.readthedocs.org/projects/geocompy/badge/?version=latest)](https://geocompy.readthedocs.io/latest/)
[![Typed](https://img.shields.io/pypi/types/geocompy)](https://pypi.org/project/geocompy/)

GeoComPy is a Python library providing wrapper functions for serial
communication protocols of Leica surveying instruments.

The package is mainly built around the GeoCom ASCII protocol, supported by
a number of total stations and other instruments running TPS1000, 1100, 1200
and other firmware. For some older instruments that do not support GeoCom,
the GSI Online command set is used for communication.

- **Download:** https://pypi.org/project/geocompy/
- **Documentation:** https://geocompy.readthedocs.io/
- **Source:** https://github.com/MrClock8163/GeoComPy
- **Bug reports:** https://github.com/MrClock8163/GeoComPy/issues

>[!TIP]
>Command line applications using GeoComPy are available as a separate
>complimentary package called
>[Instrumentman](https://github.com/MrClock8163/Instrumentman).

## Main features

- Pure Python implementation
- Support for type checkers
- Primitives for relevant data
- Command building and parsing through function calls
- Multiple supported protocols (e.g. GeoCom, GSI Online)

## Requirements

To use the package, Python 3.11 or higher is required.

For the platform independent serial communication, GeoComPy relies on the
[pySerial](https://pypi.org/project/pyserial/) package to provide the
necessary abstractions.

## Installation

The preferred method to install GeoComPy is through PyPI, where both wheel
and source distributions are made available.

```shell
python -m pip install geocompy
```

If not yet published changes/fixes are needed, that are only available in
source, GeoComPy can also be installed locally from source, without any
external tools. Once the repository is cloned to a directory, it can be
installed with pip.

```shell
git clone https://github.com/MrClock8163/GeoComPy.git
cd GeoComPy
python -m pip install .
```

## Short example

The below example demonstrates how to connect to a GeoCom capable instrument
through a serial connection. Once the connection is up and running, the
total station is instructed to turn to horizontal 0, and position the
telescope parallel to the ground.

```py
from geocompy import (
    Angle,
    open_serial,
    GeoCom
)


with open_serial("COM1") as comm:
    tps = GeoCom(comm)
    tps.aut.turn_to(Angle(0), Angle(90, 'DEG'))
```

## License

GeoComPy is free and open source software, and it is distributed under the terms of the
[MIT License](https://opensource.org/license/mit).
