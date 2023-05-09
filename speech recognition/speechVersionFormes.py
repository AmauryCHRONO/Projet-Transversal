import speech_recognition as sr
import threading

def input_listening():
    test = True
    while test:
        inp = input("Press Enter to start listening and anything else to stop the program...\
        \nMode d'emploi : 'action' 'distance' (distance en cm par défaut 50 cm)")
        retour = ''
        if inp == '':
            retour = listen_timeout()
        else:
            print("Program Finished")
            test = False
        if retour == "shutdown":
            test = False
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

'''def testeng(r, audio):
    text = r.recognize_google(audio, language='en-US')
    print("Vous avez dit : {}".format(text))

    textMots = text.split()  # chercher mot exact

    for i,mot in enumerate(textMots):
        if mot == ("off") or mot == ("shut"):
            return "shutdown"
        elif mot == ("start"):
            return "START"
        elif mot == ("stop"):
            return "STOP"
        elif mot == ("straight"):
            nbr = findNumber(textMots[i + 1])
            return "DEVANT"
        elif mot == ("forward"):
            nbr = findNumber(textMots[i + 1])
            return "AVANCE"
        elif mot == ("back"):
            nbr = findNumber(textMots[i + 1])
            return "RECULE"
        elif mot == ("left"):
            nbr = findNumber(textMots[i + 1])
            return "GAUCHE"
        elif mot == ("right"):
            nbr = findNumber(textMots[i + 1])
            return "DROITE"
        return "Aucun mot clef trouve"'''


def testfr(r, audio):
    text = r.recognize_google(audio, language='fr-FR')
    print("Vous avez dit : {}".format(text))

    textMots = text.split()  # chercher mot exact

    for i,mot in enumerate(textMots):
        if mot == ("cercle"):
            return mot
        elif mot == ("carré"):
            return mot
        elif mot == ("rectangle"):
            return mot
        elif mot == ("diagonale"):
            return mot
        elif mot == ("trait"):
            return mot
    return "Aucun mot clef trouvé"


def listen_timeout():
    r = sr.Recognizer()
    mic = sr.Microphone()
    langue = "fr"

    with mic as source:
        print("calibration du microphone")
        r.adjust_for_ambient_noise(source)
        print("ECOUTE (" + langue + ")")
        audio = r.listen(source, phrase_time_limit=3)
        try:
            if langue == "fr":
                instruction = (testfr(r, audio))
            '''else:
                instruction = (testeng(r, audio))'''
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