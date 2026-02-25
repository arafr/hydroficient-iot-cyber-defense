# docs: https://pypi.org/project/paho-mqtt/
import paho.mqtt.client as mqtt
import json

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(json.loads(msg.payload))

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.tls_set('../certs/ca.pem', 'certs/expired-device-cert.pem','certs/test4-device-key.pem')

try:
    mqttc.connect("localhost", 8883)
except Exception as e:
    print(e)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
try:
    mqttc.loop_forever()
except KeyboardInterrupt:
    mqttc.disconnect()