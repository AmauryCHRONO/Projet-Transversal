from flask import Flask, render_template, Response, request
import cv2
import datetime, time
import os, sys
import numpy as np
from threading import Thread
import sr


app=Flask(__name__, template_folder="./templates")

@app.route('/video_feed')
def video_feed():
    return Response(sr.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

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