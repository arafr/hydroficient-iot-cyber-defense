# Overview 
We have a broker (mosquitto), publisher and subscriber. Publisher will publish MQTT messages over port 1883 to x topic. Subscriber will subscribe to x topic and receive all messages sent to x topic, including the ones sent by publisher.

This set up is insecure because anyone can publish and subscribe to topics, no authentication is done. Also, attacker can set up a fake broker and capture sensor data.

# Set up:
1. Clone or download repo

2. Install mosquitto: 
[https://mosquitto.org/download/](https://mosquitto.org/download/)


3. Create & activate virtual environment

`python3 -m venv venv
source venv/bin/activate`

4. Install libraries (cryptography and paho-mqtt)

`pip install requirements.txt`

5. Start broker
On a terminal, type 

`mosquitto`

Broker will start on port 1883 (insecure, no authentication)

![broker](/media/mosquitto-broker.png")

6. Start publisher

`cd insecure-pipeline 
python3 publisher.py`

Publisher will generate and publish messages to topic every 5 seconds.

![publisher](/media/publisher.png")

7. In another terminal, start subscriber:

`cd insecure-pipeline 
python3 subscriber.py`

Subscriber will subscribe to the same topic and receive messages from publisher.

![subscriber](/media/subscriber.png")

# Vulnerability
Keep the publisher running. In a new terminal, use a mosquitto command to subscribe to all topics.

`mosquitto_sub -t "#"`

![vulnerability](/media/vulnerability.png")

Anyone with access to our network can view all messages sent to our broker (to ANY topic).