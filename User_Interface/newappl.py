from flask import Flask, render_template, Response, request
import cv2
import psycopg2
import datetime
import os
from threading import Thread

import speech_recognition as sr
from queue import Queue

global capture, rec_frame, out, switch,mode
capture=0
switch=1

mode = "manuelle"
try:
    os.mkdir('User_Interface\shots')
except OSError as error:
    pass

camera = cv2.VideoCapture(0)

def gen_frames():  # generate frame by frame from camera
    global out, capture,rec_frame
    while True:
        success, frame = camera.read() 
        if success: 
            if(capture):
                capture=0
                now = datetime.datetime.now()
                p = os.path.sep.join(['User_Interface/shots', "shot_{}.png".format(str(now).replace(":",''))])
                cv2.imwrite(p, frame)
            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass
                
        else:
            pass


def input_listening():
    try:
        # Creation queue
        result_queue = Queue()
        # Démarrage thread
        t = Thread(target=lambda q: q.put(listen_timeout()), args=(result_queue,))
        t.start()

        # Fin du thread
        t.join()
        # Recup resultat de listen_timeout
        result = result_queue.get()
    except:
        result = "Error"
    return result

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
            return instruction
        except sr.UnknownValueError:
            print("Impossible de comprendre la parole.")
        except sr.RequestError as e:
            print("Erreur de service de reconnaissance vocale : {}".format(e))
    return "Error"

def testfr(r, audio):
    text = r.recognize_google(audio, language='fr-FR')
    print("Vous avez dit : {}".format(text))

    listeMot = requeteGenerale()

    textMots = text.split()  # chercher mot exact

    for mot in textMots:
        for i in listeMot:
            if i[0] == mot:
                return mot
            
    return "Aucun mot clef trouvé"

app=Flask(__name__, template_folder="./templates")

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture',methods=['POST','GET'])
def tasks():
    global switch,camera
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            global capture
            capture=1

        elif  request.form.get('stop') == 'Stop/Start':
            
            if(switch==1):
                switch=0
                camera.release()
                cv2.destroyAllWindows()
                
            else:
                camera = cv2.VideoCapture(0)
                switch=1
                          
                 
    elif request.method=='GET':
        return render_template('camera.html')
    return render_template('camera.html')


"""fonction DATABASE """
con = psycopg2.connect(
    database="ptc",
    user="postgres",
    password="0000"
)
def envoi(info):
    print(info)
    return 0

cur = con.cursor()

def ex_com(q):
    cur.execute(q)
    con.commit()

def requeteALLSTEP(info):
    new="'%"+str(info)+"%'"
    req="select i.id_image,i.image_name,s.distance_step,s.angle_step,s.index_step,s.name_step from list_of_step as s INNER JOIN image as i on s.id_image = i.id_image where i.image_name LIKE "+new
    
    ex_com(req)
    return cur.fetchall()

def requeteGenerale():
    req = "select image_name from image"
    ex_com(req)
    return cur.fetchall()

def requete(info):
    new="'%"+str(info)+"%'"
    #req=" select i.id_image,i.image_name,s.distance_step,s.angle_step,s.index_step,s.name_step from list_of_step as s INNER JOIN image as i on s.id_image = i.id_image where s.index_step = 1 and i.image_name LIKE" +new
    req = "select i.image_name,count(s.index_step),sum(s.distance_step) from list_of_step as s INNER JOIN image as i on s.id_image = i.id_image where i.image_name LIKE" +new +"group by i.image_name"

    ex_com(req)
    return cur.fetchall()

def requeteUrl(info):
    new="'%"+str(info)+"%'"
    req = "select image_url from image where image_name LIKE "+new
    ex_com(req)
    return cur.fetchall()



@app.route("/", methods=['GET','POST'])
def index():
    global mode 
    mode = "dessin"
    if request.method == 'POST':
        envoi(mode)
        if request.form['method'] == 'post1':
            model = request.form['cmd']
            res=requete(model)
            length=len(res)
            print(res)
            return render_template("info.html",res=res,length=length,typeSub="submit",typeName="text",typeIndex="hidden")
        for i in range(100):
            if request.form['method'] == str(i):
                name = request.form['name'+str(i)]
                distance = request.form['distance'+str(i)]
                angle = request.form['angle'+str(i)]
                print(f"Nom: {name} Distance: {distance} Angle: {angle}")
                print("ok step")
                res=requeteALLSTEP(name)
                length=len(res)
                print(res)
                return render_template("info.html",res=res,length=length, typeSub="hidden",typeName="hidden",typeIndex="text")
    else:
        envoi(mode)
        return render_template("home.html")

@app.route("/voix", methods=['GET','POST'])
def speechReco():
    if request.method == 'POST':
        resultat = input_listening()
        res=requete(resultat)
        print(res)
        if res!=[]:
            length = len(res)
            img = requeteUrl(resultat)
            print(img[0][0])
            return render_template("info.html",res=res,length=length,typeSub="submit",typeName="text",typeIndex="hidden",urlImage=img[0][0])
        else:
            return render_template("voix.html",message = "Mot non trouvé")
    return render_template("voix.html")

@app.route("/manuelle", methods=['GET','POST'])
def manuelle():
    global mode 
    mode = "manuelle"
    if request.method=='POST':
        if request.form['method'] == 'post2':
            envoi(mode)
            return render_template("manuelle.html")
    #
    #TODO --> le bordel sur le bouton de voix
    #
    elif request.method=='GET':
        envoi(mode)
        return render_template("manuelle.html")

@app.route("/control", methods=['GET','POST'])
def control():
    if request.method=='GET':
        return render_template("control.html")


if __name__=="__main__":
    app.run(debug=True)

    
camera.release()
cv2.destroyAllWindows()  