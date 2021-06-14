import serial
import struct
import time


BEGIN_TONE = 2
END_TONE = 3
HALT = 255


class OutputChannel:
    def __init__(self):
        self._serial = serial.Serial(
            port='/dev/serial0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1,
        )

    def send_byte(self, b):
        self.send_bytes(struct.pack('B', b))

    def send_bytes(self, byte_string):
        self._serial.write(byte_string)

    def close(self):
        self._serial.close()
        self._serial = None

    def begin_tone(self, frequency):
        self.send_byte(BEGIN_TONE)
        self.send_bytes(struct.pack('<H', frequency))

    def end_tone(self):
        self.send_byte(END_TONE)


channel = OutputChannel()


# Send it the OK.
channel.send_bytes(b'OK!')


time.sleep(1)
channel.begin_tone(200)
time.sleep(0.3)
channel.begin_tone(100)
time.sleep(0.8)
channel.end_tone()
time.sleep(1)
channel.send_byte(HALT)


channel.close()
print('done.')
