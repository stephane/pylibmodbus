# Copyright (c) Stéphane Raimbault <stephane.raimbault@gmail.com>
#
# SPDX-License-Identifier: BSD-3-Clause

from .modbus_core import C, ModbusCore


class ModbusTcp(ModbusCore):
    def __init__(self, ip="127.0.0.1", port=502):
        self.ctx = C.modbus_new_tcp(ip.encode(), port)

	def modbus_tcp_listen(self, nb_connection):
		self._run(libmodbus.modbus_tcp_listen, nb_connection)

	def modbus_tcp_accept(self, s):
		self._run(libmodbus.modbus_tcp_listen, s)
