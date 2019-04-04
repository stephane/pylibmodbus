#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) Stéphane Raimbault <stephane.raimbault@gmail.com>

"""
Launch the tests/bandwidth-server-many-up program of libmodbus before running the
test suite with: python -m tests
"""
from __future__ import division

import unittest
import pylibmodbus


class ModbusTcpTest(unittest.TestCase):
    def setUp(self):
        self.mb = pylibmodbus.ModbusTcp("127.0.0.1", 1502)
        self.mb.connect()

    def tearDown(self):
        self.mb.close()

    def test_get_set_timeout(self):
        old_response_timeout = self.mb.get_response_timeout()
        self.mb.set_response_timeout(old_response_timeout + 1)

        new_response_timeout = self.mb.get_response_timeout()
        self.assertEqual(new_response_timeout, old_response_timeout + 1)

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

    def test_write_and_read_registers(self):
        write_data = list(range(5))
        # Write 5 registers and read 3 from address 2
        read_data = self.mb.write_and_read_registers(0, write_data, 2, 3)
        self.assertListEqual(list(read_data), write_data[2:])


class ModbusDataTest(unittest.TestCase):
    def test_set_get_float(self):
        UT_REAL = 916.540649
        data = [0x229A, 0x4465]
        self.assertAlmostEqual(pylibmodbus.get_float(data), UT_REAL, places=6)

        pylibmodbus.set_float(UT_REAL, data)
        self.assertAlmostEqual(pylibmodbus.get_float(data), UT_REAL, places=6)

    def test_cast_signed_integers(self):
        MAX_UINT16 = 65535
        MAX_UINT32 = 4294967295

        # 0 to 32767 -32768 to - 1
        self.assertEqual(pylibmodbus.cast_to_int16(0), 0)
        self.assertEqual(pylibmodbus.cast_to_int16(MAX_UINT16), -1)
        self.assertEqual(pylibmodbus.cast_to_int16(MAX_UINT16 / 2), 32767)
        self.assertEqual(pylibmodbus.cast_to_int16((MAX_UINT16 / 2) + 1), -32768)

        # Idem for 32 bits
        self.assertEqual(pylibmodbus.cast_to_int32(0), 0)
        self.assertEqual(pylibmodbus.cast_to_int32(MAX_UINT32), -1)
        self.assertEqual(pylibmodbus.cast_to_int32(MAX_UINT32 / 2), MAX_UINT32 // 2)
        self.assertEqual(
            pylibmodbus.cast_to_int32((MAX_UINT32 / 2) + 1), -((MAX_UINT32 // 2) + 1)
        )


if __name__ == "__main__":
    unittest.main()
