# Copyright (c) Stéphane Raimbault <stephane.raimbault@gmail.com>
#
# SPDX-License-Identifier: BSD-3-Clause

from .modbus_core import C, ModbusCore


class ModbusRtu(ModbusCore):
    def __init__(
        self, device="/dev/ttyS0", baud=19200, parity="N", data_bit=8, stop_bit=1
    ):
        self.ctx = C.modbus_new_rtu(device, baud, parity, data_bit, stop_bit)
