import serial
import json

def envoyer_donnees_serial(donnees, port, vitesse_baud=19200, timeout=1):

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
        print("Erreur :", e)


# lecture du fichier json
with open('donnees.json', 'r') as f:
    donnees = json.load(f)

output = "I"
for point in donnees['points']:

    angle = str(round(round(abs(point['angle'])*1000), 1)).zfill(4)

    if float(point['angle'])<0:
        angle =str('-'+angle)
    else:
        angle =str('+'+angle)

    distance = str(round(round(point['distance']*10, 1))).zfill(4)
    output = output + angle + "/" + distance + "||"

output = output + "<"


print(output)
#envoyer_donnees_serial(output, "COM3", vitesse_baud=19200)
