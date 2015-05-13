# -*- coding: utf-8 -*-
# Copyright (c) 2013, Stéphane Raimbault <stephane.raimbault@gmail.com>
#
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import division
import ctypes
import struct

C = ctypes.CDLL( '/usr/local/lib/libmodbus.so', use_errno=True )
C.modbus_strerror.restype = ctypes.c_char_p
C.modbus_get_float.restype = ctypes.c_float
C.modbus_set_float.argtypes = [ctypes.c_float, ctypes.c_void_p]


def get_float( data ):
    data = ( ctypes.c_uint16 * len( data ) )( *data )
    return C.modbus_get_float( ctypes.byref( data ) )


def set_float( value, data ):
    dest = ( ctypes.c_uint16 * 2 )()
    ctypes.cast( dest, ctypes.POINTER( ctypes.c_uint16 ) )
    C.modbus_set_float( value, dest )
    data[0] = dest[0]
    data[1] = dest[1]


def cast_to_int16( data ):
    return struct.unpack( 'h', struct.pack( 'H', data ) )[0]


def cast_to_int32( data ):
    return struct.unpack( 'l', struct.pack( 'L', data ) )[0]


class ModbusException( Exception ):
    pass


class ModbusCore( object ):
    def _run( self, func, *args ):
        rc = func( self.ctx, *args )
        if rc == -1:
            raise Exception( C.modbus_strerror( ctypes.get_errno( ) ) )

    def connect( self ):
        return self._run( C.modbus_connect )


    def set_slave( self, slave ):
        return self._run( C.modbus_set_slave, slave )


    def get_response_timeout( self ):
        sec = ctypes.c_uint32( )
        usec = ctypes.c_uint32( )
        self._run( C.modbus_get_response_timeout, ctypes.byref( sec ), ctypes.byref( usec ) )
        return float( sec.value ) + ( float( usec.value ) / 1000000 )


    def set_response_timeout( self, seconds ):
        sec = int( seconds )
        usec = int( ( seconds - sec ) * 1000000 )
        self._run( C.modbus_set_response_timeout, sec, usec )


    def close( self ):
        C.modbus_close( self.ctx )


    def read_bits( self, addr, nb ):
        dest = ( ctypes.c_uint8 * nb )()
        ctypes.cast( dest, ctypes.POINTER( ctypes.c_uint8 ) )
        self._run( C.modbus_read_bits, addr, nb, dest )
        dest = [dest[i] for i in xrange( nb )]
        return dest


    def read_input_bits( self, addr, nb ):
        dest = ( ctypes.c_uint8 * nb )()
        ctypes.cast( dest, ctypes.POINTER( ctypes.c_uint8 ) )
        self._run( C.modbus_read_input_bits, addr, nb, dest )
        dest = [dest[i] for i in xrange( nb )]
        return dest


    def read_registers( self, addr, nb ):
        dest = ( ctypes.c_uint16 * nb )()
        ctypes.cast( dest, ctypes.POINTER( ctypes.c_uint16 ) )
        self._run( C.modbus_read_registers, addr, nb, dest )
        dest = [dest[i] for i in xrange( nb )]
        return dest


    def read_input_registers( self, addr, nb ):
        dest = ( ctypes.c_uint16 * nb )()
        ctypes.cast( dest, ctypes.POINTER( ctypes.c_uint16 ) )
        self._run( C.modbus_read_input_registers, addr, nb, dest )
        dest = [dest[i] for i in xrange( nb )]
        return dest


    def write_bit( self, addr, status ):
        self._run( C.modbus_write_bit, addr, status )


    def write_register( self, addr, value ):
        self._run( C.modbus_write_register, addr, value )


    def write_bits( self, addr, nb, data ):
        nb = len( data )
        data = ( ctypes.c_uint8 * nb )( *data )
        self._run( C.modbus_write_bits, addr, nb, ctypes.byref( data ) )


    def write_registers( self, addr, data ):
        nb = len( data )
        data = ( ctypes.c_uint16 * nb )( *data )
        self._run( C.modbus_write_registers, addr, nb, ctypes.byref( data ) )


    def write_and_read_registers( self, write_addr, data, read_addr, read_nb ):
        write_nb = len( data )
        data = ( ctypes.c_uint16 * write_nb )( *data )

        dest = ( ctypes.c_uint16 * read_nb )()
        ctypes.cast( dest, ctypes.POINTER( ctypes.c_uint16 ) )

        self._run( C.modbus_write_and_read_registers, write_addr, len( data ), data, read_addr, read_nb, dest )
        dest = [dest[i] for i in xrange( read_nb )]
        return dest


