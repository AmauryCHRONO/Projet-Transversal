from rplidar import RPLidar
from serial import Serial
import numpy as np
import math


ser = Serial(port="COM5", baudrate=19200)

def run():
    lidar = RPLidar('COM4')
    tour = []
    temp = True
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

    for scan in tour:
        distance = scan[1]
        angle = scan[0]

        if  abs(distance*math.sin(np.deg2rad(angle)))<100:
            if angle<90 :
                gauche = True
                                
            if angle-360>-90:
                droite = True

    if gauche and droite:
        print("centre")
        Envoi_instruction("q")
        return False
    if gauche and not droite:
        print("gauche")
        Envoi_instruction("q")
        return False
    if not gauche and droite:
        print("droite")
        Envoi_instruction("d")
        return False
    if not gauche and not droite and move:
        print("en avant")
        Envoi_instruction("z")
        return True
    elif not gauche and not droite and not move:
        return True
        
                            



def Envoi_instruction(direction):
    #Fonction qui envoie par liaison série les informations de direction 
    if direction=='z':
        ser.write(b'z')
    if direction=='s':
        ser.write(b's')
    if direction=='q':
        ser.write(b'q')
    if direction=='d':
        ser.write(b'd')
    if direction=='f':
        ser.write(b'f')

run()
if __name__=="__name__":
    #Envoi_instruction("z")
    run()