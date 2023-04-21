from serial import Serial

ser = Serial(port="COM5", baudrate=19200)
ser.write(b'z')

input()
ser.write(b"f")