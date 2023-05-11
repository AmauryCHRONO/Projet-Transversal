#!/usr/bin/env python
# coding: utf-8
"""
author : Amaury CHRONOWSKI
"""
# Bibliotheque
from rplidar import RPLidar
from serial import Serial
import numpy as np
import math



def detectionObstacle(ser):
    """
    Fonction de détéction et d'ésquive d'obstacle pour base roulante équipé de Lidar.

    Args:
        ser(Serial object): Liaison série entre l'ordinateur de commande et la carte d'execution.
    """
    # Connection au Lidar
    lidar = RPLidar('dev/ttyUSB0')

    #Variables
    tour = [] # Stock les données d'un tour du Lidar
    res = 0 # Stock le résultat de la fonction de traitement des données

    envoiInstruction("z", ser)

    try:
        print('Début du programme de détection.... Appuyer sur Crl+C pour arréter.')

        for mesure in lidar.iter_scans(): # Recupération des données
          for scan in mesure: # Lecture de chaque mesure
                angle = scan[1]
                distance = scan[2]

                if np.floor(angle)<=2: # Envoi des données au traitement et remise du tour à zéro
                    res = traitement(tour, res, ser)    
                    tour = []

                if distance<=300 and (angle<90 or angle>270): # Selection des mesures selon les critaire de détection (en face du robot et a moins de 30 cm du Lidar)
                    tour.append((angle, distance))
                    
    except KeyboardInterrupt: # Arrêt du programme
        envoiInstruction("f", ser)
        print('Arrêt du programme de détection.')
        lidar.stop()
        lidar.disconnect()


def traitement(tour, not_move, ser):
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
        envoiInstruction("q", ser)
        return 0
    
    if droite and not gauche: # Si l'obstacle se trouve à droite de la base roulante il tourne à gauche
        envoiInstruction("q", ser)
        return 0
    
    if not droite and gauche: # Si l'obstacle se trouve à gauche de la base roulante il tourne à droite
        envoiInstruction("d", ser)
        return 0
    
    if not gauche and not droite and not_move == 4: # S'il n'y a pas d'obstacle apres 4 passage dans la fonction on indique au robot de se déplacer tout droit(a changer)
        print("en avant\n")
        envoiInstruction("z", ser)
        return 0
    
    elif not gauche and not droite and not_move<4: # Compte de passage dans la fonction sans instruction de déplacement
        return not_move+1

def envoiInstruction(direction, ser):
    """
    Fonction d'envoie d'instruction à la liasion serie

    Args:
        direction(str): Direction que la base roulante doit prendre.
        ser(Serial object): Liaison série entre l'ordinateur de commande et la carte d'execution.
    """
    if direction=='z':
        ser.write(b'z0000')
    if direction=='s':
        ser.write(b's0000')
    if direction=='q':
        ser.write(b'q0000')
    if direction=='d':
        ser.write(b'd0000')
    if direction=='f':
        ser.write(b'f0000')


ser = Serial(port="COM5", baudrate=19200)