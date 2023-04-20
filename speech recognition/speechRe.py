import speech_recognition as sr
import threading
from serial import Serial

ser = Serial(port="COM3",baudrate=19200)

def testEng(r,audio):
    text = r.recognize_google(audio, language='en-US')
    print("Vous avez dit : {}".format(text))
    if text.find("off") != -1 or text.find("shut") != -1:
        return("shutdown")
    elif text.find("start") != -1:
        #ser.write(b"STAR")
        return("START")
    elif text.find("stop") != -1:  # stopper marche aussi
        ser.write(b"f")
        #ser.write(b"STOP")
        return("STOP")
    elif text.find("forward") != -1:
        ser.write(b"z")
        #ser.write(b"AVAN")
        return("AVANCE")
    elif text.find("back") != -1:
        ser.write(b"s")
        #ser.write(b"RECU")
        return("RECULE")
    elif text.find("left") != -1:
        ser.write(b"q")
        #ser.write(b"GAUC")
        return("GAUCHE")
    elif text.find("right") != -1:
        ser.write(b"d")
        #ser.write(b"DROI")
        return("DROITE")

def testFr(r,audio):
    text = r.recognize_google(audio, language='fr-FR')
    print("Vous avez dit : {}".format(text))
    if text.find("off") != -1 or text.find("arrêt") != -1:
        return("shutdown")
    elif text.find("start") != -1:
        #ser.write(b"STAR")
        return("START")
    elif text.find("stop") != -1:  # stopper marche aussi
        ser.write(b"f")
        #ser.write(b"STOP")
        return("STOP")
    elif text.find("avance") != -1:
        ser.write(b"z")
        # ser.write(b"AVAN")
        return("AVANCE")
    elif text.find("recule") != -1:
        ser.write(b"s")
        # ser.write(b"RECU")
        return("RECULE")
    elif text.find("gauche") != -1:
        ser.write(b"q")
        # ser.write(b"GAUC")
        return("GAUCHE")
    elif text.find("droite") != -1:
        ser.write(b"d")
        # ser.write(b"DROI")
        return("DROITE")

def listen_timeout():
    r = sr.Recognizer()
    mic = sr.Microphone()
    langue="fr"

    with mic as source:
        print("calibration du microphone")
        r.adjust_for_ambient_noise(source)
        booleen=True
        while booleen:
            print("ECOUTE ("+langue+")")
            audio=r.listen(source, phrase_time_limit=4)
            try:
                if langue=="fr":
                    instruction=(testFr(r,audio))
                else:
                    instruction=(testEng(r,audio))
                print(instruction)
                if instruction=="shutdown":
                    booleen = False
                #ici envoie des instructions pour GUS
            except sr.UnknownValueError:
                print("Impossible de comprendre la parole.")
            except sr.RequestError as e:
                print("Erreur de service de reconnaissance vocale : {}".format(e))
    return "done"
if __name__ == "__main__":
    # Démarrage thread
    t = threading.Thread(target=listen_timeout,name="speechRe")
    t.start()

    # Fin du thread
    t.join()