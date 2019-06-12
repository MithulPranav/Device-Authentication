import json
import paho.mqtt.client as mqtt
import time

MI=0
e=0
f=0
r=5
XGWNU = 15
K=8 # Random

def hash(r,PW,c=""):
  t=int(str(r)+str(PW)+str(c))
  t=t^10
  return t

def uAuth(data):
    TC=4.5
    if TC-data["T4"] > 5:
        print ("Connection Timed out")
        return
    
    HASH2 = hash(hash((e^f),data["T1"]),str(str(data["T1"])+str(data["T2"])+str(data["T3"])+str(data["T4"])))
    print ("e: "+str(e))
    print ("f: "+str(f))
    print ("HASH2: {0}".format(HASH2))
    print ("S: {0}".format(data["S"]))
    if HASH2 == data["S"]:
        print ("Authenticated")
    else:
        print ("Not Authenticated")

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print ("Connected")

def on_message(client, userdata, message):
    data=json.loads(message.payload.decode("utf-8"))
    print ("Data received from {0}: {1}".format(message.topic,data))
    if message.topic == "SmartUser":    
        global MI
        global r
        MI = data["MI"]
        r = data["r"]
    if message.topic == "SmartGate":
        global e
        global f
        e = data["e"]
        f = data["f"]
    if message.topic == "UAuth":
        uAuth(data)

client = mqtt.Client("PS")
client.username_pw_set("clnyrexp","s8WgWnydSOzB")
client.on_connect=on_connect
client.on_message=on_message

print("Starting Registration Phase .....")
ip="m15.cloudmqtt.com"
client.connect(ip,12861)
client.loop_start()
client.subscribe("SmartUser")
client.subscribe("SmartGate")
time.sleep(5)
client.loop_stop()
print ("Registration Phase completed")

Operation = input("Start Login Phase? - Yes/No:  \n")
if Operation == "Yes":
    print("Starting Login Phase .....")
    PW = input("Enter the Password: ")
    MP=hash(r,PW)
    print("MP: "+str(MP))
    x=hash(MP,XGWNU)
    print("x: "+str(x))
    X=f^e
    print("X: "+str(X))
    if(X==x):
        print("Equal")
    else:
        print ("Not Equal")
        exit()
    T=1
    N=hash(x,int(str(XGWNU)+str(T)))
    print("N: "+str(N))
    z=K^f
    print("z: "+str(z))
    ip="m15.cloudmqtt.com"
    client.connect(ip,12861)
    x = { "MI" : MI , "e1": e , "z" : z , "N" : N , "T" : T }
    data = json.dumps(x)
    client.publish("SmartLogin",data)
    print ("Subscribing to UAuth .....")
    client.loop_start()
    client.subscribe("UAuth")
    time.sleep(5)
    client.unsubscribe("UAuth")
    client.loop_stop()
    print ("Login Phase completed")

else:
    print ("Invalid Input")