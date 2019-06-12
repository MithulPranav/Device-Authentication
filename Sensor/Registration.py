import paho.mqtt.client as mqtt
import json
import time

def hash(a,b,c):
    t=int(str(a)+str(b)+str(c))
    t=t^10
    return t

s={}
e=0
f=0
def on_connect():
    print ("Connected")

def on_message(client, userdata, message):
	data=json.loads(message.payload.decode("utf-8"))
	print(data)
	t2=int(data["T"])
	Tc=time.gmtime()
	Tc=int(time.strftime("%H%M%S", Tc))

	if Tc-t2 > 5:
		print ("Time delay is higher")
		return

	e=data["E"]
	print (e)
	f=data["F"]
	print (f)
	print ("Sensor Registration Completed Successfully")

def on_publish(client, userdata, mid):
	print("Published data to Gateway")

# MQTT Connection establishment
client=mqtt.Client("P1")
client.on_connect=on_connect
client.on_message=on_message
client.on_publish=on_publish

ip="m15.cloudmqtt.com"
client.username_pw_set("clnyrexp","s8WgWnydSOzB")
client.connect(ip,12861)


# Registration Phase
# 1. Publishing Part
r=3
XGWNS=25
SID=12
MP=hash(XGWNS,r,SID)
print("MP: "+str(MP))
MN=r^XGWNS
print("MN: "+str(MN))
RMP=MP^MN
print("RMP: "+str(RMP))
t1=time.gmtime()
#t1=time.strftime("%H%M%S", t1)
t1=1
d={ "Id":SID , "RMP":RMP , "MN":MN , "T":t1 }
data=json.dumps(d)
client.publish("SReg",data)

# 2. Subscribing Part
client.loop_start()
client.subscribe("G2SReg")
time.sleep(10)
client.loop_stop()
