#!/usr/bin/python3
# -*- coding: utf-8 -*-
 
#smartremocon.py
 
import paho.mqtt.client as mqtt
import subprocess
import json
import datetime
import time
import RPi.GPIO as GPIO
#from time import sleep
 
HOST = 'mqtt.beebotte.com'
PORT = 8883
CA_CERTS = 'mqtt.beebotte.com.pem'
TOKEN = 'token_3fUjQbGecQ6GBrPk'    #Beebotteで作成したチャンネルのトークンを入力
TOPIC = 'RaspberryPi/RoomLightController'    #Beebotteで作成したトピック名を入力
date = datetime.datetime.now()


MORNING_TH_HOUR = 7
NIGHT_TH_HOUR = 21
is_daytime = True
 
def on_connect(client, userdata, flags, respons_code):
    print('status {0}'.format(respons_code))
 
def on_disconnect(client, userdata, flags, respons_code):
    print("Unexpected disconnection.")
    client.loop_stop()
    
def light_on():
    #date = datetime.datetime.now()
    GPIO.output(4, 1)
    subprocess.call(["python3", "irrp.py", "-p", "-g17", "-f", "codes", "light_on", "--freq", "33"])
    print("Light on at ", date)
    GPIO.output(4, 0)
       
def light_off():
    #date = datetime.datetime.now()
    GPIO.output(4, 1)
    subprocess.call(["python3", "irrp.py", "-p", "-g17", "-f", "codes", "light_off", "--freq", "33"])
    print("Light off at",date)
    GPIO.output(4, 0)


'''
def default_command(data):
    subprocess.call(["python3", "irrp.py", "-p", "-g17", "-f", "codes", data["device"]+":"+data["action"]])
    print("excuted command: " + data["device"]+":"+data["action"])
'''
 
def on_message(client, userdata, msg):
    #print(msg.topic + ' ' + str(msg.payload))
    data = json.loads(msg.payload.decode("utf-8"))["data"]
    #print(msg.payload.decode("utf-8"))
    #print(data)
    
    if (data == 'light_on'):
        light_on()
        
    elif (data == 'light_off'):
        light_off()

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.username_pw_set('token:%s' % TOKEN)
    client.tls_set(CA_CERTS)
    client.connect(HOST, PORT)
    client.subscribe(TOPIC)
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.OUT)
 
# GPIO21番ピンを3.3Vに設定
    GPIO.output(4, 0)
    
    while 1:
        date = datetime.datetime.now()
        if((is_daytime == False) and (date.hour == MORNING_TH_HOUR)):
            light_on()#Turn the light on once in the morning.

        if((MORNING_TH_HOUR <= date.hour) and (date.hour < NIGHT_TH_HOUR)):
            is_daytime = True
        else:
            is_daytime = False
        
        client.loop()
        GPIO.output(4, 0)
        time.sleep(1)
    
    GPIO.cleanup()
    #client.loop_forever()