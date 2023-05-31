from flask import Flask, render_template, Response, request
import cv2
import psycopg2
import datetime
import os
from threading import Thread
import image
import d_transfert as df
import speech_recognition as sr
from queue import Queue
import serial
from flask_serial import Serial

app=Flask(__name__, template_folder="./templates")
# Tentative avec flask_serial
"""app.config['SERIAL_PORT']='COM4'
app.config['SERIAL_BAUDRATE']=12900
app.config['SERIAL_BYTESIZE']=8
app.config['SERIAL_PARITY']='N'
app.config['SERIAL_STOPBITS']=1
"""
#ser_ordi = Serial(app)

#ser_ordi=serial.Serial('COM4',baudrate=19200)

global capture, rec_frame, out, switch
global mode
global name


global mode_connu
capture=0
switch=1
def whatmod():
    global mode
    fichier = open('User_Interface\mod.txt', 'r')
    mode = fichier.read()
    fichier.close()
    print(mode)
    return mode

def changemod(info):
    global mode
    fichier = open('User_Interface\mod.txt', 'w')
    fichier.write(info)
    fichier.close()
    print(mode)
    whatmod()
    return mode


try:
    os.mkdir('User_Interface\shots')
except OSError as error:
    pass

camera = cv2.VideoCapture(0)

#requetes sql
"""fonction DATABASE """
con = psycopg2.connect(
    database="ptc",
    user="postgres",
    password="0000"
)


cur = con.cursor()

def ex_com(q):
    cur.execute(q)
    con.commit()


def upload(info):
    
    req ="INSERT INTO image (image_name,image_url) VALUES ('"+str(info[0])+"', '"+ str(info[1]) + "');"
    ex_com(req)
    return 


def uploadstep(info):
     
    req ="INSERT INTO list_of_step (id_image,distance_step,angle_step,index_step,name_step,url_step) VALUES ("+str(info[0])+", "+str(info[1])+", "+str(info[2])+", "+str(info[3])+", 't"+"', '"+str(info[4])+  "');"
    print(req)
    ex_com(req)
    return


def getid(info):
    new="'%"+str(info)+"%'"
    req ="select i.id_image from image as i where i.image_name LIKE "+new
    ex_com(req)

    return cur.fetchall()




def requeteALLSTEP(info):
    new="'%"+str(info)+"%'"
    req="select i.id_image,s.index_step,i.image_name,s.distance_step,s.angle_step,s.name_step from list_of_step as s INNER JOIN image as i on s.id_image = i.id_image where i.image_name LIKE "+new +" order by s.index_step"
    
    ex_com(req)
    return cur.fetchall()

def requeteGenerale():
    req = "select image_name from image"
    ex_com(req)
    return cur.fetchall()

def requete(info):
    new="'%"+str(info)+"%'"
    #req=" select i.id_image,i.image_name,s.distance_step,s.angle_step,s.index_step,s.name_step from list_of_step as s INNER JOIN image as i on s.id_image = i.id_image where s.index_step = 1 and i.image_name LIKE" +new
    req = "select i.image_name,count(s.index_step),sum(s.distance_step) from list_of_step as s INNER JOIN image as i on s.id_image = i.id_image where i.image_name LIKE" +new +"group by i.image_name, i.id_image order by i.id_image"

    ex_com(req)
    return cur.fetchall()

def requeteUrl(info):
    new="'%"+str(info)+"%'"
    req = "select image_url from image where image_name LIKE "+new +"order by id_image"
    ex_com(req)
    return cur.fetchall()


def requeteUrlstep(info):
    new="'%"+str(info)+"%'"
    req = "select s.url_step from list_of_step as s INNER JOIN image as i on s.id_image = i.id_image where i.image_name LIKE" +new +"group by s.url_step, s.index_step order by s.index_step;"

    ex_com(req)
    return cur.fetchall()




"""
def ecriture(info):
    global ser_ordi
    if not ser_ordi.isOpen():
        ser_ordi.open()

    if type(info) == str:
            info = info.encode()
    
    ser_ordi.write(info)
    
    
    pass
"""
def changementmode(info):
    
    global mode
    
    df.envoyer_donnees_serial("stop<")
    text=info+"<"
    df.envoyer_donnees_serial(text)

    return 0
"""
def init():
    global mode_connu
    global mode
    global ser_ordi

    
   
    mode_connu=False
    print("wow")
    #va = str(ser_ordi.read_until(b"<"))
    #print(va)
    mode = "dessin"
    envoi(mode)
    mode_connu=True
"""


def gen_frames():  # generate frame by frame from camera
    global out, capture,rec_frame
    global ser_ordi
    global name

    while True:
        success, frame = camera.read() 
        if success: 
            if(capture):
                capture=0
                now = datetime.datetime.now()
                
                p = os.path.sep.join(['User_Interface/static', str(name)+".png"])
                cv2.imwrite(p, frame)
                upload([name,"/static/"+str(name)+".png"])
                print(p)
                image.anaimage(p,name)
                out = df.traitement_transfert()
                df.envoyer_donnees_serial(out)
                name=""

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

def input_listening2():
    try:
        # Creation queue
        result_queue = Queue()
        # Démarrage thread
        t = Thread(target=lambda q: q.put(listen_timeout2()), args=(result_queue,))
        t.start()

        # Fin du thread
        t.join()
        # Recup resultat de listen_timeout
        result = result_queue.get()
    except:
        result = "Error"
    return result

def listen_timeout2():
    r = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:

        print("calibration du microphone")
        r.adjust_for_ambient_noise(source)
        print("ECOUTE (Francais)")

        audio = r.listen(source, phrase_time_limit=3)
        try:
            instruction = (testfr2(r, audio))
            print(instruction)
            return instruction
        except sr.UnknownValueError:
            print("Impossible de comprendre la parole.")
        except sr.RequestError as e:
            print("Erreur de service de reconnaissance vocale : {}".format(e))
    return "Error"


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

def testfr2(r, audio):
    text = r.recognize_google(audio, language='fr-FR')
    print("Vous avez dit : {}".format(text))
    

    listeMot = ["Avance","avance","recule","Recule","droite","Droite","Gauche","gauche","Stop","stop"]

    textMots = text.split()  # chercher mot exact

    for mot in textMots:
        for i in listeMot:
            if i[0] == mot:
                return mot
            
    return text


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










@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture',methods=['POST','GET'])
def tasks():
    global switch,camera
    global mode
    global name
    mode_new="dessin"
    if mode_new!=whatmod(): 
        changemod(mode_new)      
        changementmode(mode_new)
        pass
    if request.method == 'POST':
        name = request.form['cmd']
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






@app.route("/", methods=['GET','POST'])
def index():
    global mode 
    mode_new="dessin"
    if mode_new!=whatmod(): 
        changemod(mode_new)      
        changementmode(mode_new)
        pass

    if request.method == 'POST':
        if request.form['method'] == 'post1':
            model = request.form['cmd']
            res=requete(model)
            length=len(res)
            print(res)
            
            img = requeteUrl(model)
            return render_template("info.html",res=res,length=length,typeSub="submit",typeName="text",typeIndex="hidden",urlImage = img)
        for i in range(100):
            if request.form['method'] == str(i):
                name = request.form['name'+str(i)]
                distance = request.form['distance'+str(i)]
                angle = request.form['angle'+str(i)]
                print(f"Nom: {name} Distance: {distance} Angle: {angle}")
                print("ok step")

                img = requeteUrl(name)
                res=requeteALLSTEP(name)
                length=len(res)
                print(res)
                img = requeteUrlstep(name)
                print(img)
                if img[0][0]==None:
                    print("ok")
                    img = requeteUrl(name)*100

                print(img)
                
                return render_template("info.html",res=res,length=length, typeSub="hidden",typeName="hidden",typeIndex="text",urlImage = img)
    else:
        return render_template("home.html")

@app.route("/voix", methods=['GET','POST'])
def speechReco(): 
    global mode
    mode_new="dessin"
    if mode_new!=whatmod(): 
        changemod(mode_new)      
        changementmode(mode_new)
        pass

    if request.method == 'POST':
        resultat = input_listening()
        res=requete(resultat)
        print(res)
        if res!=[]:
            length = len(res)
            img = requeteUrl(resultat)
            print(img[0][0])
            return render_template("info.html",res=res,length=length,typeSub="submit",typeName="text",typeIndex="hidden",urlImage=img)
        else:
            return render_template("voix.html",message = "Mot non trouvé")
    return render_template("voix.html")

@app.route("/commandevoix", methods=['GET','POST'])
def speechReco2(): 
    global mode
    mode_new="telecomande"
    if mode_new!=whatmod(): 
        changemod(mode_new)      
        changementmode(mode_new)
        pass
    print("2")
    if request.method == 'POST':
        resultat = input_listening2()
        print("3")
        if resultat!=[]:
            if resultat == "avance":
                df.envoyer_donnees_serial("z")
                print("4")
            elif resultat == "recule":
                df.envoyer_donnees_serial("z")
                print("4")
                pass
            elif resultat == "droite":
                df.envoyer_donnees_serial("d")
                print("4")
                pass
            elif resultat == "gauche":
                df.envoyer_donnees_serial("q")
                print("4")
                pass
            elif resultat == "stop":
                df.envoyer_donnees_serial("f")
                print("4")
                pass
            return render_template("voix2.html",message = str(resultat))
        else:
            return render_template("voix2.html",message = "Mot non trouvé")
        
    return render_template("voix2.html")




@app.route("/manuelle", methods=['GET','POST'])
def manuelle():
    global mode 
    mode_new="telecommande"
    if mode_new!=whatmod(): 
        changemod(mode_new)      
        changementmode(mode_new)
        pass
    if request.method=='POST':
        if request.form['method'] == 'post2':
           
            return render_template("manuelle.html")
    #
    #TODO --> le bordel sur le bouton de voix
    #
    elif request.method=='GET':
        return render_template("manuelle.html")
    
@app.route('/light_up', methods=['POST'])
def light_up():
    key_pressed = request.form.get('key')
    if key_pressed == 'Z' or key_pressed == 'z':
        df.envoyer_donnees_serial("z")
        return 'success'  # You can return any response you want here
    if key_pressed == 'Q' or key_pressed == 'q':
        df.envoyer_donnees_serial("q")
        return 'success'  # You can return any response you want here
    if key_pressed == 'S' or key_pressed == 's':
        df.envoyer_donnees_serial("s")
        return 'success'  # You can return any response you want here
    if key_pressed == 'D' or key_pressed == 'd':
        df.envoyer_donnees_serial("d")
        return 'success'  # You can return any response you want here
    if key_pressed == 'E' or key_pressed == 'e':
        df.envoyer_donnees_serial("e")
        return 'success'  # You can return any response you want here
    if key_pressed == 'A' or key_pressed == 'a':
        df.envoyer_donnees_serial("a")
        return 'success'  # You can return any response you want here
    if key_pressed == ' ':
        df.envoyer_donnees_serial("fx")
        return 'success'  # You can return any response you want here
    return 'failure'  #Sinon on renvoie failure

@app.route("/control", methods=['GET','POST'])
def control():
    if request.method=='GET':
        return render_template("control.html")


if __name__=="__main__":
    
    #init()
        
    app.run(debug=True)

camera.release()
cv2.destroyAllWindows()