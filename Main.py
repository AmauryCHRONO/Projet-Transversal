#!/usr/bin/env python
# coding: utf-8
"""
author : Amaury CHRONOWSKI
         Mathieu ZEMAN 
"""
# Bibliotheque
from rplidar import RPLidar
from serial import Serial
import numpy as np
import math
import os
import time
import multiprocessing as mp

# Bloque de code pour le mode télécommandé

def telecomander(ser_ordi, ser_STM, obstacle, process_obstacle):

    boucle = True
    ser_ordi.write(b'OK<')
    while(boucle):
        obstacle.acquire()
        command = ser_ordi.read_until(b"<")
        if command == "fin<":
            process_obstacle.kill()
            boucle = False
        if command == "z<":
            envoiInstruction("z", ser_STM)
        if command == "q<":
            envoiInstruction("q", ser_STM)
        if command == "s<":
            envoiInstruction("s", ser_STM)
        if command == "d<":
            envoiInstruction("d", ser_STM)

    envoiInstruction("f", ser_STM)
    print('Arrêt du programme de télécommande.')

def detectionObstacle(ser_STM, lidar, obstacle):
    """
    Fonction de détéction et d'ésquive d'obstacle pour base roulante équipé de Lidar.

    Args:
        ser(Serial object): Liaison série entre l'ordinateur de commande et la carte d'execution.
    """

    #Variables
    tour = [] # Stock les données d'un tour du Lidar
    res = 0 # Stock le résultat de la fonction de traitement des données

    try:
        print('Début du programme de détection.... Appuyer sur Crl+C pour arréter.')

        for mesure in lidar.iter_scans(): # Recupération des données
          for scan in mesure: # Lecture de chaque mesure
                angle = scan[1]
                distance = scan[2]

                if np.floor(angle)<=2: # Envoi des données au traitement et remise du tour à zéro
                    res = traitement(tour, res, ser_STM, obstacle)    
                    tour = []

                if distance<=300 and (angle<90 or angle>270): # Selection des mesures selon les critaire de détection (en face du robot et a moins de 30 cm du Lidar)
                    tour.append((angle, distance))
                    
    except KeyboardInterrupt: # Arrêt du programme
        envoiInstruction("f", ser_STM)
        print('Arrêt du programme de détection.')
        
def traitement(tour, not_move, ser, obstacle):
    """
    Fonction de traitement des mesures d'un tour du Lidar.

    Args:
        tour(list of tuples): Liste des mesures d'un tour, les données sont sous formme de tuples (angle, distance).
        not_move(int): Variables qui comptabilise le nombre de fois qu'il n'y a pas eu d'instruction de mouvement.
        ser(Serial object): Liaison série entre l'ordinateur de commande et la carte d'execution.
    
    Return:
        not_move(int): Variables qui comptabilise le nombre de fois qu'il n'y a pas eu d'instruction de mouvement.
    """

    # Varibles indiquant la presence d'obstacle
    gauche = False
    droite = False

    for scan in tour: # Lecture des données
        distance = scan[1]
        angle = scan[0]

        if  abs(distance*math.sin(np.deg2rad(angle)))<100: # Obstacle considéré que l'osqu'il se situe sur le trajet de la base roulante.
            if angle<90 :
                droite = True
                                
            if angle-360>-90:
                gauche = True

    if gauche and droite: # Si l'obstacle se trouve devant la base roulante il tourne à gauche
        try:
            obstacle.acquire()
        except:
            pass
        envoiInstruction("q", ser)
        return 0
    
    if droite and not gauche: # Si l'obstacle se trouve à droite de la base roulante il tourne à gauche
        try:
            obstacle.acquire()
        except:
            pass
        envoiInstruction("q", ser)
        return 0
    
    if not droite and gauche: # Si l'obstacle se trouve à gauche de la base roulante il tourne à droite
        try:
            obstacle.acquire()
        except:
            pass
        envoiInstruction("d", ser)
        return 0
    
    if not gauche and not droite and not_move == 4: # S'il n'y a pas d'obstacle apres 4 passage dans la fonction on indique au robot de se déplacer tout droit(a changer)
        if obstacle.get_value()==0:
            obstacle.release()
        return 0
    
    elif not gauche and not droite and not_move<4: # Compte de passage dans la fonction sans instruction de déplacement
        return not_move+1

def envoiInstruction(direction, ser):
    """
    Fonction d'envoie d'instruction à la liasion serie.

    Args:
        direction(str): Direction que la base roulante doit prendre.
        ser(Serial object): Liaison série entre l'ordinateur de commande et la carte d'execution.
    """
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

# Bloque de code pour le dessin

def dessin(ser_STM, ser_ordi,lidar):
    boucle = True
    while(boucle):
        ser_ordi.write("OK<")
        donnees = ser_STM.read_until(b"<")
        if donnees != "stop<":
            angles, distances = decodage(donnees)
            deplacement(ser_STM, ser_ordi, lidar, angles, distances)
        else:
            boucle = False


    


def deplacement(ser_STM, ser_ordi, lidar, angles, distances):
    msgra = "an0080"
    msgrr = "rn0080"

    for i in range(len(angles)):
        k = 0
        for j in range(6):
            match k:
                case 0:
                    erreur = envoieMsgDessin(msgrr, ser_STM, ser_ordi)
                case 1:
                    ser_STM.write(b"cD0000")
                    time.sleep(2)
                    erreur = ""
                case 2:
                    obstacle = True
                    while(obstacle):
                        ret = detectionObstacleDessin(lidar, distances[i])
                        if ret == 0:
                            obstacle = False
                        else:
                            ser_ordi.write(b"erreur obstacle<")
                            ser_ordi.read_until(b"<")
                    msg = "a" + distances[i]
                    erreur = envoieMsgDessin(msg, ser_STM, ser_ordi)
                case 3:
                    ser_STM.write(b"cU0000")
                    time.sleep(2)
                    erreur = ""
                case 4:
                    erreur = envoieMsgDessin(msgra, ser_STM, ser_ordi)
                case 5:
                    msg = "t" + angles[i]
                    erreur = envoieMsgDessin(msgra, ser_STM, ser_ordi)
            if erreur ==  "":
                k+=1
            else:
                ser_ordi.write(b"erreur a l'etape %i<", k)
                ser_ordi.read_until(b"<")

def detectionObstacleDessin(lidar,distance_test):
    for mesure in lidar.iter_scans(): # Recupération des données
        if len(mesure)!=0:
            for scan in mesure: # Lecture de chaque mesure
                angle = scan[1]
                distance = scan[2]

                if np.floor(angle)<=2: # Envoi des données au traitement et remise du tour à zéro
                    res = traitementdessin(tour,distance_test)    
                    tour = []

                if distance<=300 and (angle<90 or angle>270): # Selection des mesures selon les critaire de détection (en face du robot et a moins de 30 cm du Lidar)
                    tour.append((angle, distance))
            break
    return res

def  traitementdessin(tour,distance):
    # Varibles indiquant la presence d'obstacle
    gauche = False
    droite = False

    for scan in tour: # Lecture des données
        distance = scan[1]
        angle = scan[0]

        if  abs(distance*math.sin(np.deg2rad(angle)))<distance+20: # Obstacle considéré que l'osqu'il se situe sur le trajet de la base roulante.
            if angle<90 :
                droite = True
                                
            if angle-360>-90:
                gauche = True

    if gauche or droite: # Si l'obstacle se trouve devant la base roulante il tourne à gauche
        return 1
    
    if not gauche and not droite: 
        return 0






def envoieMsgDessin(msg, ser_STM, ser_ordi):
    ser_STM.write(b"%s",msg)
    ret = ser_STM.read_until(b"K")
    if ret == "NACK":
        erreur = msg[:2]
        ser_ordi.write(b"erreur robot<")
    else:
        erreur = ""
    return erreur

def decodage(donnees):
    # Initialisation des listes angle et distance
    angle = []
    distance = []
    
    # Recherche des sous-chaînes correspondant à chaque paire angle-distance
    substrings = donnees.split("||")
    
    # Boucle sur chaque sous-chaîne pour extraire les valeurs d'angle et de distance
    for substring in substrings:
        if substring.startswith("I+"):
            angle.append(substring[1:6])
            distance.append(substring[7:11])
        elif substring.startswith("+"):
            angle.append(substring[0:5])
            distance.append(substring[6:10])
        elif substring.startswith("-"):
            angle.append(substring[0:5])
            distance.append(substring[7:11])
    
    # Retourne les listes d'angles et de distances
    return angle, distance

def main():
    # Connection
    ser_STM = Serial(port="dev/ttyACM0", baudrate=19200)
    ser_ordi= Serial(port="COM5", baudrate=19200)
    lidar = RPLidar('dev/ttyUSB0')

    # Premiere communication avec l'ordinateur
    ser_ordi.write(b'OK<') # Indique que la communication peut etre commencer
    instruction = ser_ordi.read_until('<')

    
    if instruction == "telecomander<":
        obstacle = mp.Semaphore(1)
        process_obstacle = mp.Process(target = detectionObstacle, args = (ser_STM, lidar, obstacle,))
        process_obstacle.start()
        process_obstacle.join()

        process_telecomander = mp.Process(target = telecomander, args=(ser_ordi, ser_STM, obstacle, process_obstacle,))
        process_telecomander.start()
        process_telecomander.join()

    if instruction == "dessin<":
        process_dessin = mp.Process(target = dessin, args = (ser_STM, ser_ordi, lidar,))
        
        process_dessin.start()
        process_dessin.join()

    envoiInstruction("f", ser_STM)
    lidar.stop()
    lidar.disconnect()
    ser_STM.close()
    ser_ordi.close()

if __name__ == "__main__":
    main()
