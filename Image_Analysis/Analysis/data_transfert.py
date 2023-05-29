import serial
import json

def envoyer_donnees_serial(donnees, port, vitesse_baud=19200, timeout=1):
    """_summary_ : envoie donnees par port serie, donnees étant une string contenant tout les points/donnée du tracé

    Args:
        donnees (str): _description_
        port (str): port de connexion du module Xbee
        vitesse_baud (int, optional): vitesse de communication. Defaults to 19200.
        timeout (int, optional): Defaults to 1.
    """
    try:
        ser = serial.Serial(port, vitesse_baud, timeout=timeout)
        print("Port série ouvert :", ser.name)

        #if type(donnees) == str:
        #    donnees = donnees.encode()

        ser.write(b"%s",donnees)
        print("Données envoyées :", donnees)

        ser.close()
        print("Port série fermé.")
        
    except Exception as e:
        print("Erreu", e)

def traitement_transfert():
    # lecture du fichier json
    with open('donnees.json', 'r') as f:
        donnees = json.load(f)

    status = True
    while status == True:
        grandeur = input("entrer une unitée de grandeur : n = millimètre | c = centimètre | m = mètres : \n")
        if grandeur == 'n':
            print("n choisi")
            status = False
        elif grandeur == 'c':
            print("c choisi")
            status = False
        elif grandeur == 'm':
            print("m choisi")
            status = False
        else:
            print('Aïe')

    output = "I"
    for point in donnees['points']:

        angle = str(round(round(abs(point['angle'])*1000), 1)).zfill(4)

        if float(point['angle'])<0:
            angle =str('-'+angle)
        else:
            angle =str('+'+angle)

        distance = str(round(round(point['distance']*10, 1))).zfill(4)

        distance = grandeur + distance
        output = output + angle + "/" + distance + "||"

    output = output + "<"


    print(output)
    return output

traitement_transfert()