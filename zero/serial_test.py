import serial

print('creating channel...')
channel = serial.Serial(
    port='/dev/serial0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1,
)

print('writing message...')
channel.write(b'k')

print('closing channel...')
channel.close()

print('done.')
