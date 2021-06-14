import board
import busio
import struct


class InputChannel:
    def __init__(self):
        self._uart = busio.UART(
            tx=board.GP0,
            rx=board.GP1,
            baudrate=9600,
            bits=8,
            parity=None,
            stop=1,
            timeout=60,
        )

    def read_byte(self):
        while True:
            received = self._uart.read(1)
            if received is not None:
                return received[0]

    def read_bytes(self, num_bytes):
        if num_bytes == 0:
            return b''

        while True:
            received = self._uart.read(num_bytes)
            if received is not None:
                return received

    def read_uint16(self):
        while True:
            received = self._uart.read(2)
            if received is not None:
                return struct.unpack('<H', received)[0]

    def read_float(self):
        while True:
            received = self._uart.read(4)
            if received is not None:
                return struct.unpack('<f', received)[0]
