from digitalio import DigitalInOut, Direction
import board
import busio
import pwmio
import struct
import time

# Prepare the LED.
led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = True


class Buzzer:
    def __init__(self, pin, duty_cycle=2 ** 8):
        self._pin = pin
        self._out = None
        self._duty_cycle = duty_cycle

    def buzz(self, frequency):
        if self._out is not None:
            if frequency > 0:
                self._out.frequency = frequency
            else:
                self._out.duty_cycle = 0
            return

        if frequency <= 0:
            return

        self._out = pwmio.PWMOut(
            pin=self._pin,
            duty_cycle=self._duty_cycle,
            frequency=frequency,
            variable_frequency=True,
        )

    def stop(self):
        if self._out is not None:
            self._out.duty_cycle = 0
            self._out.deinit()
            self._out = None

    def play_tune(self, *frequencies):
        for frequency in frequencies:
            self.buzz(frequency)
            time.sleep(0.1)
        self.stop()


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


buzzer = Buzzer(pin=board.GP15)

# Play the warm up tune.
buzzer.play_tune(40, 100)

# Create our input channel.
channel = InputChannel()


# Wait until we receive the OK.
while True:
    message = channel.read_bytes(3)
    if message == b'OK!':
        break


# Play the ready sound.
buzzer.play_tune(300, 600, 800)


def nop():
    return


def press_keys():
    num_keys = channel.read_byte()
    keycodes = list(self.read_bytes(num_keys))
    pass


def begin_tone():
    frequency = channel.read_uint16()
    buzzer.buzz(frequency)


def end_tone():
    buzzer.stop()


handlers = [
    nop,
    press_keys,
    begin_tone,
    end_tone,
]

# Loop forever, reading commands from the channel.
while True:
    command_code = channel.read_byte()
    if command_code == 255:
        break
    try:
        handlers[command_code]()
    except Exception:
        buzzer.play_tune(100, 50)
        raise
        continue

# Play the shutdown sound.
buzzer.play_tune(600, 300, 200, 200)
