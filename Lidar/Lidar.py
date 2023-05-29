from rplidar import RPLidar
from serial import Serial
import numpy as np
import math


ser = Serial(port="COM5", baudrate=19200)

def run():
    lidar = RPLidar('COM4')
    tour = []
    temp = 0
    try:
        print('Recording measurments... Press Crl+C to stop.')

        for mesure in lidar.iter_scans():
          for scan in mesure: 
                angle = scan[1]
                distance = scan[2]

                if np.floor(angle)<=2:
                    temp = traitement(tour,temp)    
                    tour = []
                if distance<=300 and (angle<90 or angle>270):
                    tour.append((angle, distance))
                    
                
    except KeyboardInterrupt:
        Envoi_instruction("f")
        print('Stoping.')
        lidar.stop()
        lidar.disconnect()
 
def traitement(tour,move):
    gauche = False
    droite = False
    print(tour)
    for scan in tour:
        distance = scan[1]
        angle = scan[0]

        if (distance*math.sin(np.deg2rad(angle)) <= 200 and angle <= 180) or (distance*math.sin(np.deg2rad(angle)) >= -80 and angle >= 180):
            if angle<180 :
                gauche = True
                                
            if angle>180:
                droite = True

    if gauche and droite:
        print("centre")
        Envoi_instruction("q")
        return 0
    if gauche and not droite:
        print("gauche")
        Envoi_instruction("q")
        return 0
    if not gauche and droite:
        print("droite\n")
        Envoi_instruction("d")
        return 0
    if not gauche and not droite and move == 4:
        print("en avant\n")
        Envoi_instruction("z")
        return 0
    elif not gauche and not droite and move<4:
        return move+1
        
                            


def Envoi_instruction(direction):
    #Fonction qui envoie par liaison série les informations de direction 
    if direction=='z':
        ser.write(b'z00000')
    if direction=='s':
        ser.write(b's00000')
    if direction=='q':
        ser.write(b'q00000')
    if direction=='d':
        ser.write(b'd00000')
    if direction=='f':
        ser.write(b'f00000')


Envoi_instruction("z")
run()