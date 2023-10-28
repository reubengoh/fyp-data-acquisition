import os
import time
import RPi.GPIO as GPIO
import Adafruit_ADS1x15
from time import sleep
from datetime import datetime
import paho.mqtt.client as mqtt
import ssl
import json
import _thread

#set GPIO pins
button1 = 16
led1    = 18
button2 = 13
led2    = 15
adc = Adafruit_ADS1x15.ADS1115()

#setup GPIO direction
def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(led1,GPIO.OUT)
    GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(led2,GPIO.OUT)
    GPIO.setwarnings(False)

def on_connect(client, userdata, flags, rc):
    print("Connected to AWS IoT: " + str(rc))

client = mqtt.Client()
client.on_connect = on_connect
client.tls_set(ca_certs='./rootCA.pem', certfile='./certificate.pem.crt',
               keyfile='./private.pem.key', tls_version=ssl.PROTOCOL_SSLv23)
client.tls_insecure_set(True)
client.connect("ajs3qlih8xy22-ats.iot.us-east-1.amazonaws.com", 8883, 60)

file = open("/home/reubengoh/Documents/datalogger/data/data.csv", "w")
setup()
GAIN = 2/3 #for reading voltages from 0-6.14V


if os.stat("/home/reubengoh/Documents/datalogger/data/data.csv").st_size == 0:
    file.write("Time,Pump Run,Pump Trip,System Pressure\n")

def publishData(txt):
    print(txt)    
    while True:
        now = datetime.now()
        now_int = int(now.strftime("%Y%m%d%H%M%S"))
        #Obtain system pressure using ADC
        value = [0]
        #Read ADC channel 0
        value[0] = adc.read_adc(0,gain=GAIN)
        #Ratio of 15 bit value to max volts determines volts
        volts = value[0]/32767.0*6.144
        #Write volt as system pressure
        file.write(str(now_int)+","+str(0)+","+str(0)+","+"{0:0.3f}V".format(volts)+"\n")
        
        #Read GPIO input, Pump run or trip status
        button_state1 = GPIO.input(button1)
        button_state2 = GPIO.input(button2)
        if button_state1 == False:
            GPIO.output(led1,True)
            print('Pump Run')
            file.write(str(now_int)+","+str(1)+","+str(0)+","+"{0:0.3f}V".format(volts)+"\n")
        elif button_state1 == True:
            GPIO.output(led1, False)
            
        if button_state2 == False:
            GPIO.output(led2,True)
            print('Pump Trip')
            file.write(str(now_int)+","+str(0)+","+str(1)+","+"{0:0.3f}V".format(volts)+"\n")
        elif button_state2 == True:
            GPIO.output(led2, False)
        
        #publish volts on aws iot core
        print ("Pressure=%0.3f",volts)
        client.publish("datalogger/data", payload=json.dumps({"Pressure": volts}), qos=0, retain=False)

        file.flush()
        time.sleep(1)

_thread.start_new_thread(publishData,("Spin-up new Thread...",))

client.loop_forever()
