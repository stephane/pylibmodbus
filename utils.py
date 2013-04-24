"""
    Libmodbus utility's mapper

"""
from cffi import FFI

ffi = FFI()
ffi.cdef("""
    float modbus_get_float(const uint16_t *src);
""")

C = ffi.verify("""
#include <modbus.h>
""", libraries=['modbus'], include_dirs=['/usr/local/include/modbus'])

def modbus_get_float(array):
    """Convert two unsigned short to a float"""
    return C.modbus_get_float(array)
