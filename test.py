#!/usr/bin/python3
# -*- coding: utf-8 -*-
 
#smartremocon.py
 
import paho.mqtt.client as mqtt
import subprocess
import json
import datetime
from time import sleep
 
HOST = 'mqtt.beebotte.com'
PORT = 8883
CA_CERTS = 'mqtt.beebotte.com.pem'
TOKEN = 'token_3fUjQbGecQ6GBrPk'    #Beebotteで作成したチャンネルのトークンを入力
TOPIC = 'RaspberryPi/RoomLightController'    #Beebotteで作成したトピック名を入力
 
def on_connect(client, userdata, flags, respons_code):
    print('status {0}'.format(respons_code))
 
def on_disconnect(client, userdata, flags, respons_code):
    print("Unexpected disconnection.")
    client.loop_stop()

'''
def default_command(data):
    subprocess.call(["python3", "irrp.py", "-p", "-g17", "-f", "codes", data["device"]+":"+data["action"]])
    print("excuted command: " + data["device"]+":"+data["action"])
'''
 
def on_message(client, userdata, msg):
    print(msg.topic + ' ' + str(msg.payload))
    data = json.loads(msg.payload.decode("utf-8"))["data"]
    print(msg.payload.decode("utf-8"))
    print(data)
    
    if (data == 'light_on'):
        date = datetime.datetime.now()
        print(date)
        
    elif (data == 'light_off'):
        date = datetime.datetime.now()
        print(date.hour)

    '''
    if (data["device"] == 'air_con'):
        if   (data["action"] == 'on'):
            date = datetime.datetime.now()
            if date.month in list_summer:
                print(date.month,"月　","冷房をつけます")
                subprocess.call(["python3", "irrp.py", "-p", "-g17", "-f", "codes", data["device"]+":"+"on"])
 
            elif date.month in list_winter:
                print(date.month,"月　","暖房をつけます")
                subprocess.call(["python3", "irrp.py", "-p", "-g17", "-f", "codes", data["device"]+":"+"on-winter"])
 
        else:
            default_command(data)
    '''


if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.username_pw_set('token:%s' % TOKEN)
    client.tls_set(CA_CERTS)
    client.connect(HOST, PORT)
    client.subscribe(TOPIC)
    client.loop_forever()