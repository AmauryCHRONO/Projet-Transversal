import speech_recognition as sr
import threading
from serial import Serial

ser = Serial(port="COM3",baudrate=19200)

def input_listening():
    test = True
    while test:
        inp = input("Press Enter to start listening and anything else to stop the program...\
                \nMode d'emploi : 'action' 'distance' (distance en cm par défaut 50 cm pas sup a 9m)")
        retour = ''
        if inp == '':
            retour = listen_timeout()
        else:
            print("Program Finished")
            test = False
        if retour == "shutdown":
            test = False
    ser.close()
    return None

def findNumber(str):
    try:
        nombre = str(10*int(str))
        long = len(nombre)

        if long<5:
            return str((5-long)*"0"+nombre)
        else:
            return str(500)
    except:
        print("pas de nombre après")
        return str(500)

def testeng(r, audio):
    text = r.recognize_google(audio, language='en-US')
    print("Vous avez dit : {}".format(text))

    textMots = text.split() #chercher mot exact

    for i,mot in enumerate(textMots):
        if mot == ("off") or mot == ("shut"):
            return"shutdown"
        elif mot == ("start"):
            # ser.write(b"STAR")
            return"START"
        elif mot == ("stop"):
            maVar = ("f" + findNumber(textMots[i + 1]))
            maVar_b = maVar.encode()
            ser.write(maVar_b)
            # ser.write(b"STOP")
            return"STOP"
        elif mot == ("straight"):
            maVar = ("v" + findNumber(textMots[i + 1]))
            maVar_b = maVar.encode()
            ser.write(maVar_b)
            ser.write(b"v")
            # ser.write(b"DEVA")
            return"DEVANT"
        elif mot == ("forward"):
            maVar = ("z" + findNumber(textMots[i + 1]))
            maVar_b = maVar.encode()
            ser.write(maVar_b)
            # ser.write(b"AVAN")
            return"AVANCE"
        elif mot == ("back"):
            maVar = ("s" + findNumber(textMots[i + 1]))
            maVar_b = maVar.encode()
            ser.write(maVar_b)
            # ser.write(b"RECU")
            return"RECULE"
        elif mot == ("left"):
            maVar = ("q" + findNumber(textMots[i + 1]))
            maVar_b = maVar.encode()
            ser.write(maVar_b)
            # ser.write(b"GAUC")
            return"GAUCHE"
        elif mot == ("right"):
            maVar = ("d" + findNumber(textMots[i + 1]))
            maVar_b = maVar.encode()
            ser.write(maVar_b)
            # ser.write(b"DROI")
            return"DROITE"
        return"Aucun mot clef trouve"


def testfr(r, audio):
    text = r.recognize_google(audio, language='fr-FR')
    print("Vous avez dit : {}".format(text))

    textMots = text.split()  # chercher mot exact

    for i, mot in enumerate(textMots):
        if mot == ("off") or mot == ("arrêt") or mot == ("arrête"):
            return"shutdown"
        elif mot == ("start"):
            # ser.write(b"STAR")
            return"START"
        elif mot == ("stop"):  # stopper marche aussi
            maVar = ("f" + findNumber(textMots[i + 1]))
            maVar_b = maVar.encode()
            ser.write(maVar_b)
            # ser.write(b"STOP")
            return"STOP"
        elif mot == ("devant"):
            maVar = ("v" + findNumber(textMots[i + 1]))
            maVar_b = maVar.encode()
            ser.write(maVar_b)
            # ser.write(b"DEVAN")
            return"DEVANT"
        elif mot == ("avance"):
            maVar = ("z" + findNumber(textMots[i+1]))
            maVar_b = maVar.encode()
            ser.write(maVar_b)
            # ser.write(b"AVAN")
            return"AVANCE"
        elif mot == ("recule"):
            maVar = ("s" + findNumber(textMots[i + 1]))
            maVar_b = maVar.encode()
            ser.write(maVar_b)
            # ser.write(b"RECU")
            return"RECULE"
        elif mot == ("gauche"):
            maVar = ("q" + findNumber(textMots[i + 1]))
            maVar_b = maVar.encode()
            ser.write(maVar_b)
            # ser.write(b"GAUC")
            return"GAUCHE"
        elif mot == ("droite"):
            maVar = ("d" + findNumber(textMots[i + 1]))
            maVar_b = maVar.encode()
            ser.write(maVar_b)
            # ser.write(b"DROI")
            return"DROITE"
    return"Aucun mot clef trouvé"


def listen_timeout():
    r = sr.Recognizer()
    mic = sr.Microphone()
    langue = "fr"

    with mic as source:
        print("calibration du microphone")
        r.adjust_for_ambient_noise(source)
        print("ECOUTE ("+langue+")")
        audio = r.listen(source, phrase_time_limit=3)
        try:
            if langue == "fr":
                instruction = (testfr(r, audio))
            else:
                instruction = (testeng(r, audio))
            print(instruction)
            # envoie du resultat a input qui teste si besoin de shutdown
            return instruction
        except sr.UnknownValueError:
            print("Impossible de comprendre la parole.")
        except sr.RequestError as e:
            print("Erreur de service de reconnaissance vocale : {}".format(e))
    return "Error"


if __name__ == "__main__":
    # Démarrage thread
    t = threading.Thread(target=input_listening(), name="speechRe")
    t.start()

    # Fin du thread
    t.join()
