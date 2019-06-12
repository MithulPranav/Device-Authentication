# Gateway

import json
import paho.mqtt.client as mqtt
#import mysql.connector
import time

XGWN=17 #Gatewayspecific

def hash(a,b,c=""):
    t=int(str(a)+str(b)+str(c))
    t=t^10
    return t

def publish_data(topic,data):
    client.publish(topic,data)

def preDeployment(data):
    SID = data["Id"]
    XGWNS = data["Pass"]
    """try:
        mydb=mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="adminmanager308",
            database="GATEWAY")
    except:
        print("Error while conn")
    cur=mydb.cursor()
    try:
        sql="INSERT INTO SENSOR (SID,XGWNS) VALUES (%s,%s)"
        val=(SID,XGWNS)
        cur.execute(sql,val)
        mydb.commit()
    except:
        print("Error while inserting data in database")
        mydb.rollback()
    cur.close()"""

def sRegistration(data):
    SID=data["Id"]
    MN=data["MN"]
    RMP=data["RMP"]
    t1=int(data["T"])
    TC=time.gmtime()
    #TC=int(time.strftime("%H%M%S", TC))
    TC=3
    if (TC-t1 > 5):
        print ("Connection Timed Out")
        return

    """try:
        mydb=mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="adminmanager308",
            database="Gateway")
        cur=mydb.cursor()
        sql="SELECT XGWNS FROM sensor WHERE SID = %s"
        val=(SID,)
        cur.execute(sql,val)
        dat=cur.fetchone()
        cur.close()
    except:
        print("Error while retrieving data from database")
        mydb.rollback()
        return

    XGWNS=dat[0]"""
    XGWNS = 25
    MP=RMP^MN
    print("MP: {0}".format(MP))
    r=MN^XGWNS
    print("r: {0}".format(r))
    MPS=hash(int(str(XGWNS)+str(r)),SID)
    print("MPS: {0}".format(MPS))

    if(MP==MPS):
        print("Equal")
    else:
        print ("MP not equal to MPS")

    f=hash(SID,XGWN)
    print("f: {0}".format(f))
    x=hash(MPS,XGWNS)
    print("x: "+ str(x))
    e=f^x
    print("e: "+str(e))
    #t2=time.gmtime()
    #t2=time.strftime("%H%M%S", t2)
    t2=3
    toSen = { "E":e , "F":f , "T":t2 }
    toSensor=json.dumps(toSen)
    topic="G2SReg"
    print (toSen)
    publish_data(topic,toSensor)

def uRegistration(data):
    MP = data["MP"]
    MI = data["MI"]
    XGWNU=15 # Random
    #database store MI and XGWNU

    f=hash(MI,XGWN)
    x=hash(MP,XGWNU)
    e=f^x
    print("f: "+str(f))
    print("x: "+str(x))
    print("e: "+str(e))
    x = { "f" : f , "e" : e }
    y=json.dumps(x)
    publish_data("SmartGate",y)

def sAuthentication(data):
    #STEP 2
    #'F2*' represented as 'F21' and likewise (*=1)

    TC=3
    if data["T2"]-TC > 5:
        print ("Connetion Timed Out")
        return
    f2=hash(data["SID"],XGWN)
    print("f2: "+str(f2))
    x21=data["e2"]^f2
    print("x21: "+str(x21))
    #database
    XGWNS = 25
    X2=data["A"]^hash(XGWNS,data["T1"],data["T2"])
    print("X2: "+str(X2))
    
    if X2==x21:
        print ("Sensor Authentication Successful")
    else:
        print ("Sensor Authentication Unsuccessful")
        return
    
    #STEP 3
    #database
    XGWNU=15
    f1=hash(data["MI"],XGWN)
    print("f1: "+str(f1))
    X11=data["e1"]^f1
    print("X11: "+str(X11))
    Q=hash(X11,XGWNU,data["T1"])
    print("Q: "+str(Q))
    if Q==data["N"]:
        print ("User Authentication Successful")
    else:
        print ("User Authentication Unsuccessful")
        return

    #STEP 4
    T3=3
    f12=f1^hash(f2,XGWNS)
    print("f12: "+str(f12))
    H=hash(f2,XGWNS,int(str(data["T1"])+str(data["T2"])+str(T3)))
    print("H: "+str(H))
    S=hash(Q,data["T1"],int(str(data["T2"])+str(T3)))
    print("S: "+str(S))
    Sen = {
        "f1" : f1,
        "f2" : f2,
        "F" : f12,
        "S" : S,
        "H" : H,
        "T1" : data["T1"],
        "T2" : data["T2"],
        "T3" : T3
    }
    dataToSen = json.dumps(Sen)
    publish_data("AuthGateway",dataToSen)


def on_connect(client,userdata,flags,rc):
    if rc == 0:
        print ("Connected")

def on_message(client, userdata, message):
    data=json.loads(message.payload.decode("utf-8"))
    print ("Data received from {0}: {1}".format(message.topic,data))
    if message.topic == "SPredep":
        print ("Starting Sensor Pre-Deployment .....")
        preDeployment(data)
        print ("Sensor Pre-Deployment completed")

    if message.topic == "SReg":
        print("Starting Sensor Registration .....")
        sRegistration(data)
        print ("Sensor Registration completed")

    if message.topic == "UReg":
        print ("Starting User Registration .....")
        uRegistration(data)
        print ("User Registration completed")

    if message.topic == "SAuth":
        print ("Authenticating Sensor and User .....")
        sAuthentication(data)
        print ("Authentication completed")

client=mqtt.Client("Ps")
client.username_pw_set("clnyrexp","s8WgWnydSOzB")
client.on_connect=on_connect
client.on_message=on_message

ip="m15.cloudmqtt.com"
print("Connecting to CloudMQTT .....")
client.connect(ip,12861)

print("Subscribing to SPredep")
print("Subscribing to SReg")
print("Subscribing to UReg")
print("Subscribing to SAuth")
client.subscribe("SPredep")
client.subscribe("SReg")
client.subscribe("UReg")
client.subscribe("SAuth")
client.loop_forever()
