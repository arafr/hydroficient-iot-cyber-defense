# Overview
This project secures the Grand Marina hotel’s HYDROLOGIC water monitoring system by implementing a secure IoT pipeline.

It includes:

* TLS and Mutual TLS (mTLS) for encrypted and authenticated communication between sensors, server, and dashboard.

* Replay attack protection using timestamp validation, counters, and HMAC message signing.

* Real-time monitoring dashboard for water flow, pressure, and remote shutoff controls.

# Set up
### 1. Clone or download repo
```
https://github.com/arafr/hydroficient-iot-cyber-defense.git
```

### 2. Install mosquitto: 
[https://mosquitto.org/download/](https://mosquitto.org/download/)


### 3. Create & activate virtual environment

```
python3 -m venv venv
source venv/bin/activate
```
### 4. Install dependencies
```
pip install -r requirements.txt
```

# Links
| Project |
| ------------- |
| [Threat Model with STRIDE Analysis](threat-model-stride.pdf/) |
| [Insecure Pipeline](insecure-pipeline/) |
| [Secure Pipeline with TLS](secure-pipeline-TLS/) |
| [Secure Pipeline with mTLS](secure-pipeline-MTLS/) |
| [Defeating Replay Attacks ](replay-attack-protection/) |