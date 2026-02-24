from datetime import datetime, timezone
import random
class WaterSensor:
  def __init__(self,device_id):
    self.device_id=device_id
    self.counter=0
    # baseline for realistic variation
    self.pressure_up = 82
    self.pressure_down = 80
    self.flow_rate = 40
  def generate_reading(self):
    self.counter+=1
    return {
        "device_id":self.device_id,
        "timestamp":datetime.now(timezone.utc).isoformat(),
        "counter":self.counter,
        # realistic variation
        "pressure_up":self.pressure_up + round(random.uniform(-2,2),1),
        "pressure_down":self.pressure_down + round(random.uniform(-2,2),1),
        "flow_rate":self.flow_rate + round(random.uniform(-2,2),1)
    }
  # introduce anomalies
  # leak means high flow rate
  def simulate_leak(self):
    reading = self.generate_reading()
    reading['flow_rate'] = round(random.uniform(80,120),1)
    reading['anomaly']='leak'
    return reading
  # blockage (high upstream, low downstream pressure)
  def simulate_blockage(self):
    reading = self.generate_reading()
    reading['pressure_up'] = round(random.uniform(100,120),1)
    reading['pressure_down'] = round(random.uniform(40,70),1)
    reading['anomaly']='blockage'
    return reading
  # stuck sensor (same values)
  def simulate_stuck(self):
    reading = self.generate_reading()
    stuck_value = round(random.uniform(70,90),1) # generate random stuck value
    reading['pressure_up'] = stuck_value
    reading['pressure_down'] = stuck_value
    reading['flow_rate']=stuck_value
    reading['anomaly']='stuck'
    return reading