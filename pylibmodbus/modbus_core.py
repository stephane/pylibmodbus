# Copyright (c) Stéphane Raimbault <stephane.raimbault@gmail.com>
#
# SPDX-License-Identifier: BSD-3-Clause

from cffi import FFI

ffi = FFI()
ffi.cdef(
	"""
	typedef struct _modbus modbus_t;

	typedef struct _modbus_mapping_t {
		int nb_bits;
		int start_bits;
		int nb_input_bits;
		int start_input_bits;
		int nb_input_registers;
		int start_input_registers;
		int nb_registers;
		int start_registers;
		uint8_t *tab_bits;
		uint8_t *tab_input_bits;
		uint16_t *tab_input_registers;
		uint16_t *tab_registers;
	} modbus_mapping_t;

	typedef enum
	{
		MODBUS_ERROR_RECOVERY_NONE          = 0,
		MODBUS_ERROR_RECOVERY_LINK          = (1<<1),
		MODBUS_ERROR_RECOVERY_PROTOCOL      = (1<<2)
	} modbus_error_recovery_mode;

	int modbus_set_slave(modbus_t* ctx, int slave);
	int modbus_get_slave(modbus_t* ctx);
	int modbus_set_error_recovery(modbus_t *ctx, modbus_error_recovery_mode error_recovery);
	int modbus_set_socket(modbus_t *ctx, int s);
	int modbus_get_socket(modbus_t *ctx);

	int modbus_get_response_timeout(modbus_t *ctx, uint32_t *to_sec, uint32_t *to_usec);
	int modbus_set_response_timeout(modbus_t *ctx, uint32_t to_sec, uint32_t to_usec);

	int modbus_get_byte_timeout(modbus_t *ctx, uint32_t *to_sec, uint32_t *to_usec);
	int modbus_set_byte_timeout(modbus_t *ctx, uint32_t to_sec, uint32_t to_usec);

	int modbus_get_indication_timeout(modbus_t *ctx, uint32_t *to_sec, uint32_t *to_usec);
	int modbus_set_indication_timeout(modbus_t *ctx, uint32_t to_sec, uint32_t to_usec);

	int modbus_get_header_length(modbus_t *ctx);

	int modbus_connect(modbus_t *ctx);
	void modbus_close(modbus_t *ctx);

	void modbus_free(modbus_t *ctx);

	int modbus_flush(modbus_t *ctx);
	int modbus_set_debug(modbus_t *ctx, int flag);
	const char *modbus_strerror(int errnum);

	int modbus_read_bits(modbus_t *ctx, int addr, int nb, uint8_t *dest);
	int modbus_read_input_bits(modbus_t *ctx, int addr, int nb, uint8_t *dest);
	int modbus_read_registers(modbus_t *ctx, int addr, int nb, uint16_t *dest);
	int modbus_read_input_registers(modbus_t *ctx, int addr, int nb, uint16_t *dest);
	int modbus_write_bit(modbus_t *ctx, int coil_addr, int status, uint8_t *msg, uint8_t *req);
	int modbus_write_register(modbus_t *ctx, int reg_addr, const uint16_t value, uint8_t *msg, uint8_t *req);
	int modbus_write_bits(modbus_t *ctx, int addr, int nb, const uint8_t *data, uint8_t *msg, uint8_t *req);
	int modbus_write_registers(modbus_t *ctx, int addr, int nb, const uint16_t *data, uint8_t *msg, uint8_t *req);
	int modbus_mask_write_register(modbus_t *ctx, int addr, uint16_t and_mask, uint16_t or_mask);
	int modbus_write_and_read_registers(modbus_t *ctx, int write_addr, int write_nb,
												   const uint16_t *src, int read_addr, int read_nb,
												   uint16_t *dest);
	int modbus_report_slave_id(modbus_t *ctx, int max_dest, uint8_t *dest);

	int modbus_send_raw_request(modbus_t *ctx, const uint8_t *raw_req, int raw_req_length);

	int modbus_receive(modbus_t *ctx, uint8_t *req);

	int modbus_receive_confirmation(modbus_t *ctx, uint8_t *rsp);

	int modbus_reply(modbus_t *ctx, const uint8_t *req,
							int req_length, modbus_mapping_t *mb_mapping);

	int modbus_reply_exception(modbus_t *ctx, const uint8_t *req,
										  unsigned int exception_code);

	modbus_mapping_t* modbus_mapping_new_start_address(
	unsigned int start_bits, unsigned int nb_bits,
	unsigned int start_input_bits, unsigned int nb_input_bits,
	unsigned int start_registers, unsigned int nb_registers,
	unsigned int start_input_registers, unsigned int nb_input_registers);

	modbus_mapping_t* modbus_mapping_new(int nb_bits, int nb_input_bits,
												int nb_registers, int nb_input_registers);
	void modbus_mapping_free(modbus_mapping_t *mb_mapping);

	float modbus_get_float(const uint16_t *src);
	void modbus_set_float(float f, uint16_t *dest);

	void modbus_set_bits_from_byte(uint8_t *dest, int idx, const uint8_t value);
	void modbus_set_bits_from_bytes(uint8_t *dest, int idx, unsigned int nb_bits,
									   const uint8_t *tab_byte);
	uint8_t modbus_get_byte_from_bits(const uint8_t *src, int idx, unsigned int nb_bits);
	float modbus_get_float_abcd(const uint16_t *src);
	float modbus_get_float_dcba(const uint16_t *src);
	float modbus_get_float_badc(const uint16_t *src);
	float modbus_get_float_cdab(const uint16_t *src);
	void modbus_set_float_abcd(float f, uint16_t *dest);
	void modbus_set_float_dcba(float f, uint16_t *dest);
	void modbus_set_float_badc(float f, uint16_t *dest);
	void modbus_set_float_cdab(float f, uint16_t *dest);

	modbus_t* modbus_new_tcp(const char *ip_address, int port);
	int modbus_tcp_listen(modbus_t *ctx, int nb_connection);
	int modbus_tcp_accept(modbus_t *ctx, int *s);

	modbus_t* modbus_new_tcp_pi(const char *node, const char *service);
	int modbus_tcp_pi_listen(modbus_t *ctx, int nb_connection);
	int modbus_tcp_pi_accept(modbus_t *ctx, int *s);

	modbus_t* modbus_new_rtu(const char *device, int baud, char parity, int data_bit, int stop_bit);
	int modbus_rtu_set_serial_mode(modbus_t *ctx, int mode);
	int modbus_rtu_get_serial_mode(modbus_t *ctx);

	int modbus_rtu_set_rts(modbus_t *ctx, int mode);
	int modbus_rtu_get_rts(modbus_t *ctx);

	int modbus_rtu_set_custom_rts(modbus_t *ctx, void (*set_rts) (modbus_t *ctx, int on));

	int modbus_rtu_set_rts_delay(modbus_t *ctx, int us);
	int modbus_rtu_get_rts_delay(modbus_t *ctx);
"""
)
C = ffi.dlopen("modbus")

def modbus_set_bits_from_byte(data, index, value):
	return libmodbus.modbus_set_bits_from_byte(data, index, value)


def modbus_set_bits_from_bytes(data, index, nb_bits, tab_byte):
	libmodbus.modbus_set_bits_from_bytes(data, index, nb_bits, tab_byte)


def modbus_get_byte_from_bits(data, index, nb_bits):
	return libmodbus.modbus_get_byte_from_bits(data, index, nb_bits)


def modbus_get_float_abcd(data):
	return libmodbus.modbus_get_float_abcd(data)


def modbus_get_float_dcba(data):
	return libmodbus.modbus_get_float_dcba(data)


def modbus_get_float_badc(data):
	return libmodbus.modbus_get_float_badc(data)


def modbus_get_float_cdab(data):
	return libmodbus.modbus_get_float_cdab(data)


def modbus_set_float_abcd(value, data):
	libmodbus.modbus_modbus_set_float_abcd(value, data)


def modbus_set_float_dcba(value, data):
	libmodbus.modbus_modbus_set_float_dcba(value, data)


def modbus_set_float_badc(value, data):
	libmodbus.modbus_modbus_set_float_badc(value, data)


def modbus_set_float_cdab(value, data):
	libmodbus.modbus_modbus_set_float_cdab(value, data)


def get_float(data):
	return C.modbus_get_float(data)


def set_float(value, data):
	C.modbus_set_float(value, data)


def cast_to_int16(data):
	return int(ffi.cast("int16_t", data))


def cast_to_int32(data):
	return int(ffi.cast("int32_t", data))


class ModbusException(Exception):
	pass


class ModbusCore(object):
	def _run(self, func, *args):
		rc = func(self.ctx, *args)
		if rc == -1:
			raise Exception(ffi.string(C.modbus_strerror(ffi.errno)).decode())

	def connect(self):
		return self._run(C.modbus_connect)

	def set_slave(self, slave):
		return self._run(C.modbus_set_slave, slave)

	def set_debug(self, debug):
		return self._run(libmodbus.modbus_set_debug, debug)

	def get_response_timeout(self):
		sec = ffi.new("uint32_t*")
		usec = ffi.new("uint32_t*")
		self._run(libmodbus.modbus_get_response_timeout, sec, usec)
		return sec[0] + (usec[0] / 1000000)

	def set_response_timeout(self, seconds):
		sec = int(seconds)
		usec = int((seconds - sec) * 1000000)
		self._run(libmodbus.modbus_set_response_timeout, sec, usec)

	def get_byte_timeout(self):
		sec = ffi.new("uint32_t*")
		usec = ffi.new("uint32_t*")
		self._run(libmodbus.modbus_get_byte_timeout, sec, usec)
		return sec[0] + (usec[0] / 1000000)

	def set_byte_timeout(self, seconds):
		sec = int(seconds)
		usec = int((seconds - sec) * 1000000)
		self._run(libmodbus.modbus_set_byte_timeout, sec, usec)

	def get_indication_timeout(self):
		sec = ffi.new("uint32_t*")
		usec = ffi.new("uint32_t*")
		self._run(libmodbus.modbus_get_indication_timeout, sec, usec)
		return sec[0] + (usec[0] / 1000000)

	def set_indication_timeout(self, seconds):
		sec = int(seconds)
		usec = int((seconds - sec) * 1000000)
		self._run(libmodbus.modbus_set_indication_timeout, sec, usec)

	def close(self):
		C.modbus_close(self.ctx)
		
	def flush(self):
		C.modbus_flush(self.ctx)

	def read_bits(self, addr, nb):
		dest = ffi.new("uint8_t[]", nb)
		self._run(C.modbus_read_bits, addr, nb, dest)
		return dest

	def read_input_bits(self, addr, nb):
		dest = ffi.new("uint8_t[]", nb)
		self._run(C.modbus_read_input_bits, addr, nb, dest)
		return dest

	def read_registers(self, addr, nb):
		dest = ffi.new("uint16_t[]", nb)
		self._run(C.modbus_read_registers, addr, nb, dest)
		return dest

	def read_input_registers(self, addr, nb):
		dest = ffi.new("uint16_t[]", nb)
		self._run(C.modbus_read_input_registers, addr, nb, dest)
		return dest

	def write_bit(self, addr, status):
		# int
		msg = ffi.new("uint8_t[]", 260)
		req = ffi.new("uint8_t[]", 260)
		self._run(libmodbus.modbus_write_bit, addr, status, msg, req)
		return msg, req

	def write_register(self, addr, value):
		# int
		msg = ffi.new("uint8_t[]", 260)
		req = ffi.new("uint8_t[]", 260)
		self._run(libmodbus.modbus_write_register, addr, value, msg, req)
		return msg, req

	def write_bits(self, addr, nb, data):
		# const uint8_t*
		msg = ffi.new("uint8_t[]", 260)
		req = ffi.new("uint8_t[]", 260)
		nb = len(data)
		self._run(libmodbus.modbus_write_bits, addr, nb, data, msg, req)
		return msg, req

	def write_registers(self, addr, data):
		# const uint16_t*
		nb = len(data)
		msg = ffi.new("uint8_t[]", 260)
		req = ffi.new("uint8_t[]", 260)
		self._run(libmodbus.modbus_write_registers, addr, nb, data, msg, req)
		return msg, req

	def write_and_read_registers(self, write_addr, data, read_addr, read_nb):
		# const uint16_t*
		dest = ffi.new("uint16_t[]", read_nb)
		self._run(
			C.modbus_write_and_read_registers,
			write_addr,
			len(data),
			data,
			read_addr,
			read_nb,
			dest,
		)
		return dest
