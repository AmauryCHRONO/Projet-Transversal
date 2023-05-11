import speech_recognition as sr
import threading
import psycopg2
from flask import Flask, render_template, Response, request
from queue import Queue

def input_listening():
    # Creation queue
    result_queue = Queue()
    # Démarrage thread
    t = threading.Thread(target=lambda q: q.put(listen_timeout()), args=(result_queue,))
    t.start()

    # Fin du thread
    t.join()

    # Recup resultat de listen_timeout 
    result = result_queue.get()
    if result != "Error":
        new="'%"+str(result)+"%'"
        req=" select i.id_image,i.image_name,s.distance_step,s.angle_step,s.index_step,s.name_step from list_of_step as s INNER JOIN image as i on s.id_image = i.id_image where s.index_step = 1 and i.image_name LIKE" +new
        
        ex_com(req)
        return cur.fetchall()

def ex_com(q):
    cur.execute(q)
    con.commit()

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

    with mic as source:
        print("calibration du microphone")
        r.adjust_for_ambient_noise(source)
        print("ECOUTE (Francais)")
        audio = r.listen(source, phrase_time_limit=3)
        try:
            instruction = (testfr(r, audio))
            print(instruction)
            # envoie du resultat a input qui teste si besoin de shutdown
            return instruction
        except sr.UnknownValueError:
            print("Impossible de comprendre la parole.")
        except sr.RequestError as e:
            print("Erreur de service de reconnaissance vocale : {}".format(e))
    return "Error"
    

if __name__ == "__main__":
    # FLASK
    app = Flask(__name__, template_folder="./templates")

    # DATABASE
    con = psycopg2.connect(
        database="jalon1",
        user="postgres",
        password="CRONOS3317"
        )
    cur = con.cursor()


@app.route("/voix", methods=['GET','POST'])
def index():
    if request.method == 'POST':
        res = input_listening()
        length = len(res)
        print(res)
        messages = "le modele n'est pas present"
        return render_template("info.html",res=res,length=length)
    else:
        return render_template("voix.html")