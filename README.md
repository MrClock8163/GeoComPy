<h1 align="center">
<img src="https://raw.githubusercontent.com/mrclock8163/geocompy/main/docs/geocompy_logo.png" alt="GeoComPy logo" width="300">
</h1><br>

[![PyPI - Version](https://img.shields.io/pypi/v/geocompy)](https://pypi.org/project/geocompy/)
[![Python Version](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2FMrClock8163%2FGeoComPy%2Frefs%2Fheads%2Fmain%2Fpyproject.toml)](https://pypi.org/project/geocompy/)
[![GPLv3](https://img.shields.io/github/license/mrclock8163/geocompy)](https://www.gnu.org/licenses/gpl-3.0.html)
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
