===========
pylibmodbus
===========

Python Interface for libmodbus written with CFFI.
This libmodbus wrapper is compatible with Python 2 and Python 3.

This wrapper is only compatible with libmodbus v3.1.2 and above.

Required packages:

- python-dev and libffi-dev
- libmodbus and libmodbus-dev

Licensed under BSD 3-Clause (see LICENSE file for details).

Tests
-----

Before running the test suite, you need to launch a TCP server.
You can use the server provided by libmodbus in ``tests`` directory::

    $ ./tests/bandwidth-server-many-up

Once this server is running, you can launch the Python tests with::

    $ python -m tests
