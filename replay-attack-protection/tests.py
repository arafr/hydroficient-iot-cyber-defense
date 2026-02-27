from sensor import WaterSensor
import time
import paho.mqtt.client as mqtt
import json

def on_publish(client, userdata, mid, reason_code, properties):
    # reason_code and properties will only be present in MQTTv5. It's always unset in MQTTv3
    try:
        userdata.remove(mid)
    except KeyError:
        print("on_publish() is called with a mid not present in unacked_publish")
        print("This is due to an unavoidable race-condition:")
        print("* publish() return the mid of the message sent.")
        print("* mid from publish() is added to unacked_publish by the main thread")
        print("* on_publish() is called by the loop_start thread")
        print("While unlikely (because on_publish() will be called after a network round-trip),")
        print(" this is a race-condition that COULD happen")
        print("")
        print("The best solution to avoid race-condition is using the msg_info from publish()")
        print("We could also try using a list of acknowledged mid rather than removing from pending list,")
        print("but remember that mid could be re-used !")

unacked_publish = set()
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_publish = on_publish

mqttc.user_data_set(unacked_publish)
mqttc.connect("localhost",8883)
mqttc.tls_set('certs/ca.pem','certs/sensor1.pem','certs/sensor1-key.pem')
mqttc.loop_start()
# Wait for all message to be published
while len(unacked_publish):
    time.sleep(0.1)
\
from sensor import WaterSensor
test_sensor = WaterSensor('test-sensor-1')
# MODIFIED MESSAGE TEST
print('-'*50)
print("TEST 1: Replaying Modified Message")
reading=test_sensor.generate_reading()
# editing flow_rate, this changes the hmac signature of the message.
reading['flow_rate']=90
msg_info = mqttc.publish("hydroficient/grandmarina/building-1/readings", json.dumps(reading), qos=1)
unacked_publish.add(msg_info.mid)
print("published: " + json.dumps(reading))
print('-'*50)

# AGED MESSAGE TEST
print('-'*50)
print("TEST 2: Replaying Aged Message")
reading=test_sensor.generate_reading()
print("Waiting 30 seconds for message to age, then it will be published.")
time.sleep(31)
msg_info = mqttc.publish("hydroficient/grandmarina/building-1/readings", json.dumps(reading), qos=1)
unacked_publish.add(msg_info.mid)
print("published: " + json.dumps(reading))
print('-'*50)

# SEQUENCE VALIDATION TEST
print('-'*50)
print("TEST 3: Replaying Same Message")
# we generate and publish an acceptable message
reading=test_sensor.generate_reading()
msg_info = mqttc.publish("hydroficient/grandmarina/building-1/readings", json.dumps(reading), qos=1)
unacked_publish.add(msg_info.mid)
print("published: " + json.dumps(reading))
# now we try to replay the same message again (same counter)
msg_info = mqttc.publish("hydroficient/grandmarina/building-1/readings", json.dumps(reading), qos=1)
unacked_publish.add(msg_info.mid)
print("published: " + json.dumps(reading))
print('-'*50)


# Due to race-condition described above, the following way to wait for all publish is safer
msg_info.wait_for_publish()

mqttc.disconnect()
mqttc.loop_stop()


