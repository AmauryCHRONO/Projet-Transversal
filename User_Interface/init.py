import serial

def envoyer_donnees_serial(donnees):
    """_summary_ : envoie donnees par port serie, donnees étant une string contenant tout les points/donnée du tracé

    Args:
        donnees (str): _description_
        port (str): port de connexion du module Xbee
        vitesse_baud (int, optional): vitesse de communication. Defaults to 19200.
        timeout (int, optional): Defaults to 1.
    """
    try:
        ser = serial.Serial("COM3", 19200)
        print("Port série ouvert :", ser.name)

        if type(donnees) == str:
            donnees = donnees.encode()

        ser.write(b"%s",donnees)
        print("Données envoyées :", donnees)

        ser.close()
        print("Port série fermé.")
        
    except Exception as e:
        print("Erreu", e)

if __name__=="__main__":
    envoyer_donnees_serial("telecomande<")