import six
from cffi import FFI

ffi = FFI()
ffi.cdef("""
    typedef struct _modbus modbus_t;

    int modbus_connect(modbus_t *ctx);
    void modbus_close(modbus_t *ctx);
    const char *modbus_strerror(int errnum);

    modbus_t* modbus_new_tcp(const char *ip_address, int port);

    int modbus_read_bits(modbus_t *ctx, int addr, int nb, uint8_t *dest);
    int modbus_read_input_bits(modbus_t *ctx, int addr, int nb, uint8_t *dest);
    int modbus_read_registers(modbus_t *ctx, int addr, int nb, uint16_t *dest);
    int modbus_read_input_registers(modbus_t *ctx, int addr, int nb, uint16_t *dest);
    int modbus_write_bit(modbus_t *ctx, int coil_addr, int status);
    int modbus_write_register(modbus_t *ctx, int reg_addr, int value);
    int modbus_write_bits(modbus_t *ctx, int addr, int nb, const uint8_t *data);
    int modbus_write_registers(modbus_t *ctx, int addr, int nb, const uint16_t *data);
""")
C = ffi.verify("""
#include <modbus.h>
""", libraries=['modbus'], include_dirs=['/usr/local/include/modbus'])


class ModbusException(Exception):
    pass


class ModbusTcp(object):
    def __init__(self, ip=six.b("127.0.0.1"), port=502):
        self.ctx = C.modbus_new_tcp(ip, port)

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
