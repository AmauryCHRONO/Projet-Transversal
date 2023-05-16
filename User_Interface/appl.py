from flask import Flask, render_template, request, url_for, redirect, flash, Response
#import psycopg2
import cv2
import datetime, time
import os, sys
import numpy as np
from threading import Thread

"""con = psycopg2.connect(
    database="drawbot_db",
    user="postgres",
    password="Ud7PsJab"
)"""

cur = con.cursor()

global capture,rec_frame, grey, switch, neg, face, rec, out 
capture=0
switch=1
rec=0

#make shots directory to save pics
try:
    os.mkdir('../Analysis/shots')
except OSError as error:
    pass


def ex_com(q):
    cur.execute(q)
    con.commit()

def display_all_table(table):
    try:
        query="select * from " + table
        cur.execute(query)
        resultat = cur.fetchall()
        return resultat
    except:
        return 1

def ins_val_v2(table_colonne,values):
    try:
        query="insert into" + table_colonne + "values" + values 
        cur.execute(query)
        con.commit()

        return 0
    except:
        return 1
    
def display_element(table,element="*",characteristic=""):

    query="select "+element+ " from " + table 

    if characteristic != "":
        query = query +" "+characteristic 

    cur.execute(query)
    resultat = cur.fetchall()

    return resultat

def check(im):
    ch="select id_image from image where image_name = '"+im+"'" 
    ex_com(ch)
    return cur.fetchall()

def retrive_info(id):
    info="select * from list_of_step as los inner join image as i on los.id_image = i.id_image where i.id_image ="+id
    ex_com(info)
    return cur.fetchall()




app=Flask(__name__)

app.secret_key='123'


################################################################
# def camera

camera = cv2.VideoCapture(0)

def record(out):
    global rec_frame
    while(rec):
        time.sleep(0.05)
        out.write(rec_frame)


def detect_face(frame):
    global net
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
        (300, 300), (104.0, 177.0, 123.0))   
    net.setInput(blob)
    detections = net.forward()
    confidence = detections[0, 0, 0, 2]

    if confidence < 0.5:            
            return frame           

    box = detections[0, 0, 0, 3:7] * np.array([w, h, w, h])
    (startX, startY, endX, endY) = box.astype("int")
    try:
        frame=frame[startY:endY, startX:endX]
        (h, w) = frame.shape[:2]
        r = 480 / float(h)
        dim = ( int(w * r), 480)
        frame=cv2.resize(frame,dim)
    except Exception as e:
        pass
    return frame
 

def gen_frames():  # generate frame by frame from camera
    global out, capture,rec_frame
    while True:
        success, frame = camera.read() 
        if success:  
            if(capture):
                capture=0
                now = datetime.datetime.now()
                p = os.path.sep.join(['../Analysis/shots', "shot_{}.png".format(str(now).replace(":",''))])
                cv2.imwrite(p, frame)
            
            if(rec):
                rec_frame=frame
                frame= cv2.putText(cv2.flip(frame,1),"Recording...", (0,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),4)
                frame=cv2.flip(frame,1)
            
                
            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass
                
        else:
            pass


################################################################
# routes

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/requests',methods=['POST','GET'])
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
        elif  request.form.get('rec') == 'Start/Stop Recording':
            global rec, out
            rec= not rec
            if(rec):
                now=datetime.datetime.now() 
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter('vid_{}.avi'.format(str(now).replace(":",'')), fourcc, 20.0, (640, 480))
                #Start new thread for recording the video
                thread = Thread(target = record, args=[out,])
                thread.start()
            elif(rec==False):
                out.release()
                          
                 
    elif request.method=='GET':
        return render_template('cam.html')
    return render_template('cam.html')

@app.route('/', methods=['POST','GET'])
def acc():
    return render_template("index.html")


@app.route('/home', methods=['POST','GET'])
def index():
    messages=""
    instruct=[]
    visibility="hidden"
    if request.method == 'POST':
        model = request.form['cmd']
        res=check(model)
        if res==[]:
            messages="Le modèle n'est pas présent"
        else:
            messages="Le modèle "+model+" est présent"
            instruct=retrive_info(str(res[0][0]))
            visibility="visible"
    return render_template("index.html", messages=messages, instruct=instruct, visibility=visibility)

if __name__ == "__main__":
    app.run(debug=True) 

camera.release()
cv2.destroyAllWindows() 