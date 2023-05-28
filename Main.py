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
import time
import math
import os



# Bloque de code pour le mode télécommandé

def telecommande(ser_ordi, ser_STM):
    """
    Fonction qui permet de dessin de facon télécommander avec le robot.

    Args:
        ser_ordi(Serial object): Liaison série entre l'ordinateur de commande et l'ordinateur distant.
        ser_STM(Serial object): Liaison série entre l'ordinateur de commande et la carte d'execution.
    """

    boucle = True
    while(boucle):

        # Réception de données et traitement
        command = ser_ordi.read_until(b"<")
        command = str(command)
        command = command[2:-1]

        if command == "f<": # Fin du programme
            boucle = False
        if command == "z<": # Avancer 
            envoiInstruction("z", ser_STM)
        if command == "q<": # Tourner à gauche
            envoiInstruction("q", ser_STM)
        if command == "s<": # Reculer
            envoiInstruction("s", ser_STM)
        if command == "d<": # Tourner à droite
            envoiInstruction("d", ser_STM)
        if command == "a<": # Baisser le crayon
            envoiInstruction("a", ser_STM)
        if command == "e<": # Lever le crayon
            envoiInstruction("e", ser_STM)

    envoiInstruction("f", ser_STM)
    print('Arrêt du programme de télécommande.')

def envoiInstruction(direction, ser):
    """
    Fonction d'envoie d'instruction à la liasion serie.

    Args:
        direction(str): Direction que la base roulante doit prendre.
        ser(Serial object): Liaison série entre l'ordinateur de commande et la carte d'execution.
    """
    if direction=='z':
        ser.write(b'z00000<')
    if direction=='s':
        ser.write(b's00000<')
    if direction=='q':
        ser.write(b'q00000<')
    if direction=='d':
        ser.write(b'd00000<')
    if direction=='f':
        ser.write(b'f00000<')
    if direction=='a':
        ser.write(b'p00000<')
    if direction=='e':
        ser.write(b'u00000<')



# Bloque de code pour le dessin

def dessin(ser_STM, ser_ordi, lidar):
    """
    Fonction qui réalise un dessin a partir de données reçus.

    Args:
        ser_ordi(Serial object): Liaison série entre l'ordinateur de commande et l'ordinateur distant.
        ser_STM(Serial object): Liaison série entre l'ordinateur de commande et la carte d'execution.
        lidar(RPLidar object): Liaison avec le capteur Lidar qui nous donne la posision d'obstacle.
    """

    boucle = True
    ser_ordi.write("OK<") # Annonce d'attente de données

    while(boucle):

        # Réception de données et traitement
        donnees = ser_STM.read_until(b"<")
        donnees = str(donnees)
        donnees = donnees[2:-1]

        if donnees[0] == "I": # TRaitement et utilisation des données reçus
            ser_ordi.write("OK<")
            angles, distances = decodage(donnees)
            deplacement(ser_STM, ser_ordi, lidar, angles, distances)

        elif donnees == "stop<": # Fin du programme
            boucle = False
        
        else:
            ser_ordi.write(b"NO<")

    envoiInstruction("f", ser_STM)
    print('Arrêt du programme de dessin.')
    
def deplacement(ser_STM, ser_ordi, lidar, angles, distances):
    """
    Fonction qui réalise le dessin par étapes: 1) Rotaition, 2) Recule de la distance entre le centre des roue et le crayon, 3) Baisse le crayon,
    4) Avance de la distance voulue, 5) Leve le crayon, 6) Avance de la distance entre le centre des roue et le crayon.

    Args:
        ser_ordi(Serial object): Liaison série entre l'ordinateur de commande et l'ordinateur distant.
        ser_STM(Serial object): Liaison série entre l'ordinateur de commande et la carte d'execution.
        lidar(RPLidar object): Liaison avec le capteur Lidar qui nous donne la posision d'obstacle.
        angles(tuple): Enssemble des angles à réaliser pour le dessin.
        distances(tuple): Enssemble des distance à parcourir pour le dessin.
    """

    # Distance entre le centre des roue et le crayon
    msgra = "in0110" # Avancer
    msgrr = "hn0110" #Reculer

    for i in range(len(angles)): # Parcoure l'ensemble des points du dessin
        k = 0
        for j in range(6): # Réalisation de toute les étapes pour chaque ségement

            if k == 0: # Rotaition
                msg = "t" + angles[i]
                erreur = envoieMsgDessin(msg, ser_STM, ser_ordi)

            elif k == 1: # Recule de la distance entre le centre des roue et le crayon
                erreur = envoieMsgDessin(msgrr, ser_STM, ser_ordi)

            elif k == 2: # Baisse le crayon
                ser_STM.write(b'p00000')
                time.sleep(2)
                erreur = ""

            elif k == 3: # Avance de la distance voulue
                # La detection d'obstacle ne fonctionne pas, pas eu le temps de debugger
                """
                obstacle = True
                while(obstacle):
                    ret = detectionObstacleDessin(lidar, distances[i])
                    if not ret:
                        obstacle = False
                    else:
                        ser_ordi.write(b"erreur obstacle<")
                        ser_ordi.read_until(b"<")
                """
                msg = "i" + distances[i]
                erreur = envoieMsgDessin(msg, ser_STM, ser_ordi)

            elif k == 4: # Leve le crayon
                ser_STM.write(b'u00000')
                time.sleep(2)
                erreur = ""
                
            elif k == 5: # Avance de la distance entre le centre des roue et le crayon
                erreur = envoieMsgDessin(msgra, ser_STM, ser_ordi)

            
            if erreur ==  "": # Pas d'erreur, étape suivante
                k+=1

            else: # Communication des erreur à l'ordinateur distant pour resoudre l'erreur et recommancer l'action automatiquement
                msg = "Erreur a l'etape " + str(k) + "<" 
                msg = msg.encode()
                ser_ordi.write(msg)
                ser_ordi.read_until(b"<")
    
    ser_ordi.write(b"fin dessin")

def detectionObstacleDessin(lidar, distance_test):
    """
    Fonction qui permet de détecter les obstacles sur le trajet du robot.

    Args:
        lidar(RPLidar object): Liaison avec le capteur Lidar qui nous donne la posision d'obstacle.
        distance_test(str): Distance que doit parcourir le robot lors d'une étape.

    Returns:
        res(boolan): Indique s'il y a un obstacle (True) ou non (False) 
    """
    # Mise à l'echelle du dessin
    if distance_test[0] == "n": # Milimètre
        ordre = 1
    if distance_test[0] == "c": # Centimètre
        ordre = 10
    if distance_test[0] == "m": # Mètre
        ordre = 1000
    distance_test = int(distance_test) * ordre

    for mesure in lidar.iter_scans(): # Recupération des données du Lidar
        if len(mesure)!=0:
            for scan in mesure: # Lecture de chaque mesure
                angle = scan[1]
                distance = scan[2]

                if np.floor(angle)<=2: # Envoi des données au traitement et remise du tour à zéro
                    res = traitementdessin(tour)    
                    tour = []
                    break

                if distance <= distance_test and (angle >= 90 and angle <= 290): # Sélection des mesures selon les critaires de détections
                    tour.append((angle, distance))
        break
    return res

def  traitementdessin(tour):
    """
    Fonction qui permet de détécter les obstacle dans les donnée retenus du Lidar.

    Args:
        tour(tuple): Ensemble des données du Lidar sur un tour.

    Returns:
        obstacle(boolan): Indique s'il y a un obstacle sur la route du robot.
    """
    # Varibles indiquant la presence d'obstacle
    obstacle = False

    for scan in tour: # Lecture des données
        distance = scan[1]
        angle = scan[0]

        if  (distance*math.sin(np.deg2rad(angle)) <= 200 and angle <= 180) or (distance*math.sin(np.deg2rad(angle)) >= -80 and angle >= 180): # Obstacle considéré que losqu'il se situe sur le trajet de la base roulante.
            obstacle = True

    return obstacle

def envoieMsgDessin(msg, ser_STM, ser_ordi):
    """
    Fonction d'envoie d'instruction au robot.

    Args:
        msg(str): Message a envoyé.
        ser_ordi(Serial object): Liaison série entre l'ordinateur de commande et l'ordinateur distant.
        ser_STM(Serial object): Liaison série entre l'ordinateur de commande et la carte d'execution.
    
    Returns:
        erreur: Indique s'il y a une erreur
    """
    
    msg_temp = msg

    # Envoie de la commande à la STM32
    msg = msg.encode()
    ser_STM.write(msg)

    # Reception de réponce de la STM32 en cas d'erreur
    ret = ser_STM.read_until(b"K")
    if ret == "NACK":
        erreur = msg
    else:
        erreur = ""
        if msg_temp[1] == "+" or msg_temp[1] == "-": # Laisse le temps à la rotation de se faire
            ang = int(msg_temp[2]) + (int(msg_temp[3:]) / 1000)
            temps = ang/0.107 # 0.107 rad/s (vitesse de rotation)
            time.sleep(temps)
    return erreur

def decodage(donnees):
    """
    Décode le chemin du dessin reçu.

    Args:
        donnees(str): Données reçus à décoder

    Returns:
        aangles(tuple): Enssemble des angles à réaliser pour le dessin.
        distances(tuple): Enssemble des distance à parcourir pour le dessin.
    """

    # Initialisation des listes angle et distance
    angle = []
    distance = []
    
    # Recherche des sous-chaînes correspondant à chaque paire angle-distance
    substrings = donnees.split("||")
    
    # Boucle sur chaque sous-chaîne pour extraire les valeurs d'angle et de distance
    for substring in substrings:
        if substring.startswith("I+"):
            angle.append(substring[1:6])
            distance.append(substring[7:12])
        elif substring.startswith("+"):
            angle.append(substring[0:5])
            distance.append(substring[6:11])
        elif substring.startswith("-"):
            angle.append(substring[0:5])
            distance.append(substring[7:12])
    
    # Retourne les listes d'angles et de distances
    return angle, distance



# Fonction principal

def main():
    """
    Fonction principal qui permet de choisir dans quel mode on va se mettre.
    """

    # Connection
    ser_STM = Serial(port="dev/ttyACM0", baudrate=19200)
    ser_ordi= Serial(port="dev/ttyUSB1", baudrate=19200)
    lidar = RPLidar('dev/ttyUSB0')

    boucle = True
    while(boucle):

        # Réception de données et traitement
        instruction = ser_ordi.read_until(b"<")
        instruction = str(instruction)
        instruction = instruction[2:-1]

        # Séléction du mode
        if instruction == "telecommande<":
            telecommande(ser_ordi, ser_STM)

        elif instruction == "dessin<":
            dessin(ser_STM, ser_ordi, lidar)

        elif instruction == "stop<":
            boucle = False
        
        else:
            ser_ordi.write(b"NO<")


    # Arrêt du robot
    print("Arrêt du robot")
    envoiInstruction("f", ser_STM)
    lidar.stop()
    lidar.disconnect()
    ser_STM.close()
    ser_ordi.close()

if __name__ == "__main__":
    main()
