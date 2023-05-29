from serial import Serial
import keyboard


def envoiInstruction(direction, ser):
    if direction=='z':
        ser.write(b'z<')
    if direction=='s':
        ser.write(b's<')
    if direction=='q':
        ser.write(b'q<')
    if direction=='d':
        ser.write(b'd<')
    if direction=='f':
        ser.write(b'f<')
    if direction=='a':
        ser.write(b'p<')
    if direction=='e':
        ser.write(b'u<')
        
ser_ordi= Serial(port="COM5", baudrate=19200)

boucle = True
while(boucle):
    ser_ordi.write(b"dessin<")
    instruction = ser_ordi.read_until(b"<")
    instruction = str(instruction)
    instruction = instruction[2:-1]
    if instruction == "OK<":
        boucle = False

boucle = True
while(boucle):
    msg = b"I+1046/n1000||+1046/n1000||+1046/n1000||<"
    ser_ordi.write(msg)
    instruction = ser_ordi.read_until(b"<")
    instruction = str(instruction)
    instruction = instruction[2:-1]
    if instruction == "OK<":
        boucle = False

instruction = ser_ordi.read_until(b"<")
instruction = str(instruction)
instruction = instruction[2:-1]
if instruction == "fin dessin<":
    ser_ordi.write(b"telecommande<")
    boucle = True 
    while(boucle):
        if keyboard.is_pressed("z"):
            envoiInstruction("z", ser_ordi)
        if keyboard.is_pressed("q"):
            envoiInstruction("q", ser_ordi)
        if keyboard.is_pressed("s"):
            envoiInstruction("s", ser_ordi)
        if keyboard.is_pressed("d"):
            envoiInstruction("q", ser_ordi)
        if keyboard.is_pressed("a"):
            envoiInstruction("a", ser_ordi)
        if keyboard.is_pressed("e"):
            envoiInstruction("e", ser_ordi)
        if keyboard.is_pressed("f"):
            envoiInstruction("f", ser_ordi)
            boucle = False


ser_ordi.write(b"stop<")

ser_ordi.close()