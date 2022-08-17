# pylibmodbus

[![PyPI version](https://badge.fury.io/py/pylibmodbus.svg)](https://badge.fury.io/py/pylibmodbus)

Python Interface for libmodbus written with CFFI.
This libmodbus wrapper is compatible with Python 2 and Python 3.

This wrapper is only compatible with libmodbus v3.1.2 and above.

Required packages:

- python-dev and libffi-dev
- libmodbus and libmodbus-dev

Licensed under BSD 3-Clause (see LICENSE file for details).

## Installation

The package `pylibmodbus' is available from Pypi but you must install libmodbus
before using is (see <https://libmodbus.org> for details).

Example for Debian:

```shell
apt-get install libmodbus
pip install pylibmodbus
```

## Tests

Before running the test suite, you need to launch a TCP server.
You can use the server provided by libmodbus in `tests` directory:

```shell
./tests/bandwidth-server-many-up
```

Once this server is running, you can launch the Python tests with:

```shell
python -m tests
```
