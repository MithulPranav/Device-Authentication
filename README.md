# Device-Authentication
Hardware implementation of a mathematical model on device authentication in IoT

Devices: Raspberry Pi 3B+

Files:

1. Gateway/Gateway.py - The Gateway code which authenticates both sensor and User

2. User/User.py - The registration of user with gateway which inturn provides the user a smart card

3. User/SmartCard.py - The SmartCard which when given the correct password authenticates the user and lets it communicate with the sensor

4. Sensor/PreDep.py - The Pre Deployment of the sensor in which the configuration details are stored in gateway

5. Sensor/Registration.py - The Registration of sensor with the gateway

6. Sensor/Authentication.py - The sensor is authenticated on its communication with the gateway

All communication happens between the devices using MQTT (Cloud broker)
