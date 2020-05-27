# pylint: skip-file
from repositories.DataRepository import DataRepository
from flask import Flask, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS

import datetime
import time
import threading

# Code voor led
from helpers.klasseknop import Button
from RPi import GPIO
import sys
import adafruit_dht

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
motor = [6,13,19,26]
GPIO.setup(motor[0],GPIO.OUT)
GPIO.setup(motor[1],GPIO.OUT)
GPIO.setup(motor[2],GPIO.OUT)
GPIO.setup(motor[3],GPIO.OUT)
knop1 = Button(20)

output = [[0,0,0,1],[0,0,1,1],[0,0,1,0],[0,1,1,0],[0,1,0,0],[1,1,0,0],[1,0,0,0],[1,0,0,1]]

dhtDevice = adafruit_dht.DHT11(21)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Hier mag je om het even wat schrijven, zolang het maar geheim blijft en een string is'

socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

def run_motor():
    f=0
    while f < 2000:
        time.sleep(0.0002)
        n = 0
        while n<7:
            i = 0
            time.sleep(0.0002)
            while i< 4:
                GPIO.output(motor[i], output[n][i])
                i += 1
                time.sleep(0.0002)
            n+=1
        f+=1

# API ENDPOINTS
@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."


# SOCKET IO
@socketio.on('connect')
def initial_connection():
    print('A new client connect')
    # # Send to the client!



@socketio.on("F2B_inlezen_sensor")
def inlezen_sensor(data):
    print('Sensor wordt ingelezen')
    print(data)
    sensor = data["sensor"]
    if(sensor == "DHT1"):
        value = dhtDevice.humidity
    

    res = DataRepository.insert_value_sensoren(value,sensor)
    
    data = DataRepository.read_value_sensoren(sensor)

    print(data)
    socketio.emit("B2F_inlezing_sensor",{'waarde': data})

@socketio.on("F2B_aansturen_actuator")
def aansturen_actuator(data):
    print("actuator wordt aangestuurt")
    id = data["actuator"]
    # res = DataRepository.update_status_motor(id, 1)
    thread = threading.Thread(target=run_motor)
    thread.start()









# knop1.on_press(lees_knop)


if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0')
