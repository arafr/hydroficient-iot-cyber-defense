from datetime import datetime, timezone
import random
import hmac
import hashlib
import json

import os
from dotenv import load_dotenv
load_dotenv()
shared_secret = os.getenv("SHARED_SECRET")

class WaterSensor:
  def __init__(self,device_id):
    self.device_id=device_id
    self.counter=0
    # baseline for realistic variation
    self.pressure_up = 82
    self.pressure_down = 80
    self.flow_rate = 40
  def generate_hmac(self,shared_secret, message):
    # convert message dictionary to json
    message = json.dumps(message,sort_keys=True)
    # Create a new HMAC object using the shared_secret and SHA256 hash function
    hmac_object = hmac.new(shared_secret.encode(), message.encode(), hashlib.sha256)
    # Return the hexadecimal representation of the HMAC
    return hmac_object.hexdigest()
  def generate_reading(self):
    self.counter+=1
    message = {
      "device_id":self.device_id,
      # replay attack protection
      "timestamp":datetime.now(timezone.utc).isoformat(),
      "counter":self.counter,
      # realistic variation
      "pressure_up":self.pressure_up + round(random.uniform(-2,2),1),
      "pressure_down":self.pressure_down + round(random.uniform(-2,2),1),
      "flow_rate":self.flow_rate + round(random.uniform(-2,2),1)
    }

    # simulate anomalies (1 in 50 chance)
    if random.randint(1,50)==1:
      random.choice([self.simulate_leak, self.simulate_blockage,self.simulate_stuck])(message)

    # generate hmac signature of the message dictionary
    hmac_signature = self.generate_hmac(shared_secret, message)
    # add hmac signature to message dictionary
    message['hmac'] = hmac_signature

    return message
  
  # anomaly functions
  # leak means high flow rate
  def simulate_leak(self,message):
    message['flow_rate'] = round(random.uniform(80,120),1)
    message['anomaly']='leak'
  # blockage (high upstream, low downstream pressure)
  def simulate_blockage(self,message):
    message['pressure_up'] = round(random.uniform(100,120),1)
    message['pressure_down'] = round(random.uniform(40,70),1)
    message['anomaly']='blockage'
  # stuck sensor (same values)
  def simulate_stuck(self,message):
    stuck_value = round(random.uniform(70,90),1) # generate random stuck value
    message['pressure_up'] = stuck_value
    message['pressure_down'] = stuck_value
    message['flow_rate']=stuck_value
    message['anomaly']='stuck'
    return message