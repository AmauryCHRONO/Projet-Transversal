import speech_recognition as sr
import threading


def input_listening():
    test = True
    while test:
        inp = input("Press Enter to start listening and anything else to stop the program...")
        retour = ''
        if inp == '':
            retour = listen_timeout()
        else:
            print("Program Finished")
            test = False
        if retour == "shutdown":
            test = False
    return None


def testeng(r, audio):
    text = r.recognize_google(audio, language='en-US')
    print("Vous avez dit : {}".format(text))
    if text.find("off") != -1 or text.find("shut") != -1:
        return"shutdown"
    elif text.find("start") != -1:
        # ser.write(b"STAR")
        return"START"
    elif text.find("stop") != -1:  # stopper marche aussi
        # ser.write(b"STOP")
        return"STOP"
    elif text.find("forward") != -1:
        # ser.write(b"AVAN")
        return"AVANCE"
    elif text.find("back") != -1:
        # ser.write(b"RECU")
        return"RECULE"
    elif text.find("left") != -1:
        # ser.write(b"GAUC")
        return"GAUCHE"
    elif text.find("right") != -1:
        # ser.write(b"DROI")
        return"DROITE"


def testfr(r, audio):
    text = r.recognize_google(audio, language='fr-FR')
    print("Vous avez dit : {}".format(text))
    if text.find("off") != -1 or text.find("arrêt") != -1:
        return"shutdown"
    elif text.find("start") != -1:
        # ser.write(b"STAR")
        return"START"
    elif text.find("stop") != -1:  # stopper marche aussi
        # ser.write(b"STOP")
        return"STOP"
    elif text.find("avance") != -1:
        # ser.write(b"AVAN")
        return"AVANCE"
    elif text.find("recule") != -1:
        # ser.write(b"RECU")
        return"RECULE"
    elif text.find("gauche") != -1:
        # ser.write(b"GAUC")
        return"GAUCHE"
    elif text.find("droite") != -1:
        # ser.write(b"DROI")
        return"DROITE"


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
