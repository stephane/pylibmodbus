# -*- coding: utf-8 -*-
# Copyright (c) 2013, Stéphane Raimbault <stephane.raimbault@gmail.com>

from .modbus_core import C, ModbusCore


class ModbusTcp(ModbusCore):
    def __init__(self, ip="127.0.0.1", port=502):
        self.ctx = C.modbus_new_tcp(ip.encode(), port)
