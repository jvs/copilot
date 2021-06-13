import board
import busio
from digitalio import DigitalInOut, Direction


led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = True

channel = busio.UART(
    tx=board.GP0,
    rx=board.GP1,
    baudrate=9600,
    bits=8,
    parity=None,
    stop=1,
    timeout=10,
)

print('reading...')
message = channel.read(1)
print('received:', repr(message))
