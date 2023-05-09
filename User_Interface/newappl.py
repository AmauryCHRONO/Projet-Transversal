from flask import Flask, render_template, Response, request
import cv2
import datetime, time
import os, sys
import numpy as np
from threading import Thread

global capture, rec_frame, out, switch
capture=0
switch=1


try:
    os.mkdir('User_Interface\shots')
except OSError as error:
    pass


net = cv2.dnn.readNetFromCaffe('User_Interface\saved_model\deploy.prototxt.txt', 'User_Interface/saved_model/res10_300x300_ssd_iter_140000.caffemodel')
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


@app.route("/", methods=['GET','POST'])
def index():
    return render_template("home.html")

@app.route("/voix")
def voice():
    return render_template("voix.html")


if __name__=="__main__":
    app.run(debug=True)

    
camera.release()
cv2.destroyAllWindows()  