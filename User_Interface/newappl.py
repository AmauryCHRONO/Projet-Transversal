from flask import Flask, render_template, Response, request
import cv2
import psycopg2
import datetime
import os
from threading import Thread

global capture, rec_frame, out, switch
capture=0
switch=1


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
    database="drawbot_db",
    user="postgres",
    password="0000"
)

cur = con.cursor()

def ex_com(q):
    cur.execute(q)
    con.commit()

def requeteALLSTEP(info):
    new="'%"+str(info)+"%'"
    req="select i.id_image,i.image_name,s.distance_step,s.angle_step,s.index_step,s.name_step from list_of_step as s INNER JOIN image as i on s.id_image = i.id_image where i.image_name LIKE "+new
    
    ex_com(req)
    return cur.fetchall()

def requete(info):
    new="'%"+str(info)+"%'"
    req=" select i.id_image,i.image_name,s.distance_step,s.angle_step,s.index_step,s.name_step from list_of_step as s INNER JOIN image as i on s.id_image = i.id_image where s.index_step = 1 and i.image_name LIKE" +new
    
    ex_com(req)
    return cur.fetchall()


@app.route("/", methods=['GET','POST'])
def index():
    if request.method == 'POST':
        if request.form['method'] == 'post1':
            model = request.form['cmd']
            res=requete(model)
            length=len(res)
            print(res)
            messages="Le modèle n'est pas présent"
            return render_template("info.html",res=res,length=length)
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
                return render_template("info.html",res=res,length=length)
    else:
        return render_template("home.html")

@app.route("/voix", methods=['GET','POST'])
def voice():
    if request.method=='POST':
        return render_template("voix.html")
    #
    #TODO --> le bordel sur le bouton de voix
    #
    elif request.method=='GET':
        return render_template("voix.html")

@app.route("/control", methods=['GET','POST'])
def control():
    if request.method=='GET':
        return render_template("control.html")


if __name__=="__main__":
    app.run(debug=True)

    
camera.release()
cv2.destroyAllWindows()  