from rplidar import RPLidar
from serial import Serial
import numpy as np
import math

def run():
    lidar = RPLidar('COM4')

    try:
        print('Recording measurments... Press Crl+C to stop.')

        for mesure in lidar.iter_scans():
          for scan in mesure: 
                angle = scan[1]
                distance = scan[2]
                
                if distance<=300:
                    if  distance*math.sin(np.deg2rad(angle))<60 and (angle<=90 or angle>=270):

                        if angle<90:
                            print("A droite")    

                        if angle>270:
                            print("A gauche")
                            
                    else:
                        print("Tout droit")
                
    except KeyboardInterrupt:
        print('Stoping.')
        lidar.stop()
        lidar.disconnect()