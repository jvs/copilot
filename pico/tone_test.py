from digitalio import DigitalInOut, Direction
import board

from buzzer import Buzzer
from input_channel import InputChannel


# Prepare the LED.
led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = True


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
