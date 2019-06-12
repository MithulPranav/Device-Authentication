import json
import paho.mqtt.client as mqtt
import time
import Registration.py

SID = 12
XGWNS=25

def hash(a,b,c=None):
    if c is None:
        t=int(str(a)+str(b))
        t^=10
        return t
    else:
        t=int(str(a)+str(b)+str(c))
        t^=10
        return t

def publish_data(topic,data):
    client.publish(topic,data)

def smartLogin(data):
    T1=data["T"]
    T2=2
    e=data["e"]
    f=data["f"]
    x=e^f
    print(x)
    A=hash(XGWNS,T1,T2)^x
    print(A)
    sdata = {	
		"MI" : data["MI"] ,
       	"e1" : data["e"] ,
       	"N" : data["N"] ,
       	"T1" : data["T"] ,
       	"T2" : data["T2"] ,
       	"SID" : SID ,
       	"A" : A,
		"e2" : Registration.e
    }

    publish_data("SAuth",data)

def authGateway(data):
	Z1=5019
	K1=8
	K2=7
	T4=4
	HASH1=hash(data["f2"],XGWNS,int(str(data["T1"])+str(data["T2"])+str(data["T3"])))
	print(HASH1)
	#Check HASH1==H2
	F11=data["F"]^hash(data["f1"],XGWNS)
	print(F11)
	K1_=Z1^F11
	print(K1_)
	SK=hash(0,K1^K2)
	print(SK)
	R12=hash(F11,SID,int(str(data["T1"])+str(data["T2"])+str(data["T3"])+str(T4)))^K2
	print(R12)
	sdata = {
		"S" : data["S"],
		"R12" : R12,
		"T1" : data["T1"],
		"T2" : data["T2"],
		"T3" : data["T3"],
		"T4" : data["T4"]
	}
	publish_data("UAuth",sdata)

def on_connect(client, userdata, flags, rc):
    print ("Connected")

def on_message(client, userdata, message):
    data=json.loads(message.payload.decode("utf-8"))
    print (data)
    if message.topic == "SmartLogin":
        smartLogin(data)
	if message.topic == "AuthGateway":
		authGateway(data)

client = mqtt.Client("PSA")
client.username_pw_set("clnyrexp","s8WgWnydSOzB")
client.on_connect=on_connect
client.on_message=on_message
client.subscribe("SmartLogin")
client.subscribe("AuthGateway")
client.loop_forever()

