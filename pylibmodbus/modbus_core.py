# -*- coding: utf-8 -*-
# Copyright (c) 2013, Stéphane Raimbault <stephane.raimbault@gmail.com>

from cffi import FFI

ffi = FFI()
ffi.cdef("""
    typedef struct _modbus modbus_t;

    int modbus_connect(modbus_t *ctx);
    void modbus_close(modbus_t *ctx);
    const char *modbus_strerror(int errnum);

    int modbus_read_bits(modbus_t *ctx, int addr, int nb, uint8_t *dest);
    int modbus_read_input_bits(modbus_t *ctx, int addr, int nb, uint8_t *dest);
    int modbus_read_registers(modbus_t *ctx, int addr, int nb, uint16_t *dest);
    int modbus_read_input_registers(modbus_t *ctx, int addr, int nb, uint16_t *dest);
    int modbus_write_bit(modbus_t *ctx, int coil_addr, int status);
    int modbus_write_register(modbus_t *ctx, int reg_addr, int value);
    int modbus_write_bits(modbus_t *ctx, int addr, int nb, const uint8_t *data);
    int modbus_write_registers(modbus_t *ctx, int addr, int nb, const uint16_t *data);

    float modbus_get_float(const uint16_t *src);
    void modbus_set_float(float f, uint16_t *dest);

    modbus_t* modbus_new_tcp(const char *ip_address, int port);
""")
C = ffi.dlopen('modbus')


def get_float(data):
    return C.modbus_get_float(data)

def set_float(value, data):
    C.modbus_set_float(value, data)

def cast_to_int16(data):
    return int(ffi.cast('int16_t', data))

def cast_to_int32(data):
    return int(ffi.cast('int32_t', data))


class ModbusException(Exception):
    pass


class ModbusCore(object):
    def _run(self, func, *args):
        rc = func(self.ctx, *args)
        if rc == -1:
            raise Exception(ffi.string(C.modbus_strerror(ffi.errno)))

    def connect(self):
        return self._run(C.modbus_connect)

    def close(self):
        C.modbus_close(self.ctx)

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
        self._run(C.modbus_write_bit, addr, status)

    def write_register(self, addr, value):
        # int
        self._run(C.modbus_write_register, addr, value)

    def write_bits(self, addr, nb, data):
        # const uint8_t*
        nb = len(data)
        self._run(C.modbus_write_bits, addr, nb, data)

    def write_registers(self, addr, data):
        nb = len(data)
        self._run(C.modbus_write_registers, addr, nb, data)
