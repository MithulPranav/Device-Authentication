# Pre Deployment Phase

import json
import paho.mqtt.client as mqtt

def on_connect():
    print ("Connected")

def on_publish(client, userdata, mid):
	print("Registration Phase Completed")

client=mqtt.Client("P")
client.on_connect=on_connect
client.on_publish=on_publish

ip="m15.cloudmqtt.com"
client.username_pw_set("clnyrexp","s8WgWnydSOzB")
client.connect(ip,12861)

XGWNS=25
SID=12
d={ "Id":SID , "Pass":XGWNS }
print (d)
data=json.dumps(d)
client.publish("SPredep",data)