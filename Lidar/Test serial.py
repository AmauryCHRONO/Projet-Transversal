from serial import Serial

ser = Serial(port="COM6", baudrate=19200)
ser.write(b'q')
print(ser.read(7))
ser.close()
