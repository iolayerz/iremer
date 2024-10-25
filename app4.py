from flask import Flask, render_template, Response, request, redirect, url_for, jsonify
import cv2
import serial
import time
from pathlib import Path
import random

global ser, fdetect
fdetect = 0

#ser = serial.Serial('/dev/ttyUSB0',9600)
#ser = serial.Serial('COM3',9600)
time.sleep(2)

iremer = Flask(__name__)

face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

@iremer.route('/fd')
def fd():
    the_answer = random.randint(25, 60)
    return str(the_answer)

def detect_bounding_box(vid):
    global fdetect
    gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))

    if len(faces) != 0:
        fdetect = 1
        #print(fdetect)
    else:
        fdetect = 0
        #print(fdetect)

    for (x, y, w, h) in faces:
        cv2.rectangle(vid, (x, y), (x + w, y + h), (0, 255, 0), 4)
    return faces

def gen_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()  # read the camera frame

        if not success:
            break
        else:
            faces = detect_bounding_box(frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

def gen_frames2():
    camera = cv2.VideoCapture(1)  
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
             
@iremer.route('/', methods=['POST','GET'])
def index():
    global ser,fdetect
    if request.method == 'POST':
        print(request.form['moveCmd'])
        if request.form['moveCmd'] == 'FORWARD':
            print("Move Forward")
            #ser.write(bytes('f','utf-8'))
            time.sleep(0.5)
            #data = ser.readline()
            #print(data)
            #del(ser)
        elif request.form['moveCmd'] == 'LEFT':
            print("Move Left")
            #ser.write(bytes('l','utf-8'))
            time.sleep(0.5)
            #data = ser.readline()
            #print(data)
        elif request.form['moveCmd'] == 'RIGHT':
            print("Move Right")
            #ser.write(bytes('r','utf-8'))
            time.sleep(0.5)
            #data = ser.readline()
            #print(data)
        elif request.form['moveCmd'] == 'BACKWARD':
            print("Move Backward")
            #ser.write(bytes('b','utf-8'))
            time.sleep(0.5)
            #data = ser.readline()
            #print(data)
        elif request.form['moveCmd'] == 'STOP':
            print("Stop Movement")
            #ser.write(bytes('s','utf-8'))
            time.sleep(0.5)
            #data = ser.readline()
            #print(data)
        else:
            pass
        
    return render_template('index.html')

@iremer.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@iremer.route('/video_feed2')
def video_feed2():
    return Response(gen_frames2(), mimetype='multipart/x-mixed-replace; boundary=frame')

@iremer.route('/_refresh')
def refresh():
    global fdetect
    response =  { 
        'status' : 'Success', 
        'data': fdetect,
    }
    print(f'DEBUG: Sending response {response}')
    return jsonify(response)

if __name__ == '__main__':
    iremer.run(debug=True,host='0.0.0.0')