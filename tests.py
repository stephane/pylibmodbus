#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013, Stéphane Raimbault <stephane.raimbault@gmail.com>

"""
Launch the tests/bandwidth-server-many-up of libmodbus before running the
test suite.
"""

import unittest
from pylibmodbus import ModbusTcp


class ModbusTcpTest(unittest.TestCase):

    def setUp(self):
        self.mb = ModbusTcp("127.0.0.1", 1502)
        self.mb.connect()

    def tearDown(self):
        self.mb.close()

    def test_read_and_write(self):
        nb = 5

        # Write [0, 0, 0, 0, 0]
        write_data = [0] * nb
        self.mb.write_registers(0, write_data)

        # Read
        read_data = self.mb.read_registers(0, nb)
        self.assertListEqual(write_data, list(read_data))

        # Write [0, 1, 2, 3, 4]
        write_data = list(range(nb))
        self.mb.write_registers(0, write_data)

        # Read
        read_data = self.mb.read_registers(0, nb)
        self.assertListEqual(write_data, list(read_data))


class ModbusDataTest(unittest.TestCase):

    def setUp(self):
        self.mb = ModbusTcp("127.0.0.1", 1502)

    def test_set_get_float(self):
        UT_REAL = 916.540649
        data = [0x229a, 0x4465]
        self.assertAlmostEqual(self.mb.get_float(data), UT_REAL, places=6)

        self.mb.set_float(UT_REAL, data)
        self.assertAlmostEqual(self.mb.get_float(data), UT_REAL, places=6)

    def test_cast_signed_integers(self):
        value = self.mb.cast_to_int16(65535)
        self.assertEqual(value, -1)


if __name__ == '__main__':
    unittest.main()
