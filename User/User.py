import json
import paho.mqtt.client as mqtt


def hash(r,PW):
  t=int(str(r)+str(PW))
  t=t^10
  return t

def on_connect(client, userdata, flags, rc):
  if rc==0:
    print ("Connected")

client=mqtt.Client("Pu")
client.username_pw_set("clnyrexp","s8WgWnydSOzB")
client.on_connect=on_connect

ip="m15.cloudmqtt.com"

print ("Starting User Registration .....")
ID=6
PW=22
r=5 #Random
MI=hash(r,ID)
MP=hash(r,PW)
print ("MP: "+str(MP))
print ("ID: "+str(ID))
x = { "MP" : MP , "MI" : MI }
y = { "MI": MI , "r" : r }
data = json.dumps(x)
data1 = json.dumps(y)
client.connect(ip,12861)
client.publish("UReg",data)
client.publish("SmartUser",data1)
print ("User Registration completed")