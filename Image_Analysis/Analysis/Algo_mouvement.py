import serial
import json

def deplacement(angles, distances, R, port, vitesse_baud=19200, timeout=1):
    """_summary_ : envoie 6 étapes de mouvement au robot pour la réalisation d'un trait.

    Args:
        angles (Liste): liste d'angle de rotation en radiant
        distances (Liste): liste de distance en mm
        R (int): distance en mm du crayon par rapport au centre des roues
        port (str): port de connexion du module Xbee
        vitesse_baud (int, optional): vitesse de communication. Defaults to 19200.
        timeout (int, optional): Defaults to 1.
    """
    try:
        ser = serial.Serial(port, vitesse_baud, timeout=timeout)
        print("Port série ouvert :", ser.name)

        for i in range(len(distances)):
            # Étape 1 : Recule de R (envoye "-R")
            #ser.write("-{}\n".format(R).encode())
            ser.write(b"-%s",R)
            print("Données envoyées :", "-%s",R)

            # Étape 2 : Baisser le crayon (envoye "cDOWN")
            #ser.write("cDOWN\n".encode())
            ser.write(b"cDOWN")
            print("Données envoyées : ", "cDOWN")

            # Étape 3 : Avance de D (envoie "distance[i]")
            #ser.write("{}\n".format(distances[i]).encode())
            ser.write(b"%s",distances[i])
            print("Données envoyées :", distances[i])

            # Étape 4 : Lever le crayon (envoie "cUP")
            #ser.write("cUP\n".encode())
            ser.write(b"cUP")
            print("Données envoyées :", "cUP")

            # Étape 5 : Avance de R (envoie "R")
            #ser.write("{}\n".format(R).encode())
            ser.write(b"%s",R)
            print("Données envoyées :", donnees)

            # Étape 6 : Tourne de Theta (envoie "angles[i]")
            #ser.write("{}\n".format(angles[i]).encode())
            ser.write(b"%s",angles[i])
            print("Données envoyées :", angles[i])

        ser.close()
        print("Port série fermé.")

    except Exception as e:
        print("Erreur :", e)


def decodage(donnees):
    """_summary_ : décode la chaine de caractère contenant tous les angles et les distances en 2 listes avec cchaque élément étant une orientation ou une distance.

    Args:
        donnees (str): longue string de la forme : "I+0000/2228||+0606/1519||+0891/5092||-0607/1535||-0289/3958||+0981/2117||+0858/2949||+0331/4293||+0259/2160||+0951/2191||+0549/2797||-0732/4060||+0303/1497||+0561/1422||+0575/1664||+0375/6319||+0231/0755||<"
            qui contient l'ensemble des informations du tracé

    Returns:
        angle : liste contenant tout les angles
        distance : liste contenant tout les distances
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
            distance.append(substring[7:11])
        elif substring.startswith("+"):
            angle.append(substring[0:5])
            distance.append(substring[6:10])
        elif substring.startswith("-"):
            angle.append(substring[0:5])
            distance.append(substring[7:11])
    
    # Retourne les listes d'angles et de distances
    return angle, distance



donnees = "I+0000/2228||+0606/1519||+0891/5092||-0607/1535||-0289/3958||+0981/2117||+0858/2949||+0331/4293||+0259/2160||+0951/2191||+0549/2797||-0732/4060||+0303/1497||+0561/1422||+0575/1664||+0375/6319||+0231/0755||<"

angles, distances = decodage(donnees)

print("angles =", angles)
print("distances =", distances)

deplacement(angles, distances, 150, "COM3", vitesse_baud=19200)