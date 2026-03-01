import paho.mqtt.client as mqtt
import json
# hmac docs: https://docs.python.org/3/library/hmac.html
import hashlib
import hmac
from datetime import datetime, timezone

import os
from dotenv import load_dotenv
load_dotenv()
shared_secret = os.environ.get("SHARED_SECRET")

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # subscribe to both main-building and east wing readings
    client.subscribe("hydroficient/grandmarina/+/readings")

def validate_hmac(message,hmac_signature):
    # we need to take out the hmac signature out from the message first.
    message.pop('hmac')
    # recompute hash
    # convert message dictionary to json
    message = json.dumps(message,sort_keys=True)
    # Create a new HMAC object using the secret key and SHA256 hash function
    hmac_object = hmac.new(shared_secret.encode(), message.encode(), hashlib.sha256)
    # the hexadecimal representation of the HMAC
    computed_signature =  hmac_object.hexdigest()
    # compare sent and recomputed hmac signature
    return hmac.compare_digest(computed_signature,hmac_signature)

def validate_timestamp(message_time):
    msg_time = datetime.fromisoformat(message_time.replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)
    age = (now - msg_time).total_seconds()
    # 30 second limit
    if age > 30:
        return False
    else:
        return True

# dictionary of seen devices:last sequence number
# example: seen = {'device-1':5, 'device-2':10}
seen = {}
def validate_sequence(device,counter):
    # if new device
    if not device in seen.keys():
        # update seen
        seen[device] = counter
        return True
    # if device exists in seen dictionary.
    # sequence number counter must be greater than last seen sequence number
    if counter > seen[device]:
        seen[device] = counter
        return True
    return False

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # load up python dictionary
    message = json.loads(msg.payload)

    # HMAC validation
    hmac_signature = message['hmac']
    if not validate_hmac(message,hmac_signature):
        message["status"]="rejected"
        message["reason"]="HMAC validation failed."
        write_to_file(message)
        return print(f"{message['status']} HMAC validation failed. {message}")
    
    # timestamp validation
    if not validate_timestamp(message['timestamp']):
        message["status"]="rejected"
        message["reason"]="Message too old."
        write_to_file(message)
        return print(f"{message['status']} Timestamp validation failed. {message}")

    # sequence number validation
    if not validate_sequence(message['device_id'],message['counter']):
        message["status"]="rejected"
        message["reason"]="Sequence validation failed."
        write_to_file(message)
        return print(f"{message['status']} Sequence validation failed. {message}")

    # finally since all validations passed, print the message.
    message["status"]="accepted"
    print(f"{message['status']} {message}")
    write_to_file(message)

def write_to_file(message):
    # append messages to messages.json for splunk ingestion
    with open('messages.json','a') as json_file:
        json.dump(message,json_file)
        json_file.write('\n')

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

# Provide path to CA certificate, device certificate, device private key. 
mqttc.tls_set('certs/ca.pem','certs/dashboard1.pem','certs/dashboard1-key.pem')

# change port to 8883
mqttc.connect("localhost", 8883)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
try:
    mqttc.loop_forever()
except KeyboardInterrupt:
    mqttc.disconnect()