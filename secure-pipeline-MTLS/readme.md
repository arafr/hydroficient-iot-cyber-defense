# Overview
On top of our TLS pipeline, we will add mTLS for device authentication. After device verifies broker's identity, broker will verify device identity before accepting readings. This prevents attackers from setting up a fake sensor and sending fake readings and dangerous commands.

# Protection added to pipeline:
1. Authentication of devices (sensors and dashboards have to prove they are not an imposter)

# mTLS Handshake Overview
1. Device will send hello to server (mosquitto broker).

2. Broker will send its server certificate.

3. Device will use CA certificate to check if the server certificate is signed by  CA.

4. Now device will send its certificate to server.

3. Now server will use CA certificate to check if the device certificate is signed by CA.

6. Encrypted data will be sent using the other entities' public key, which can only be decrypted by the other entities' private key. This makes sure only the real client/holding their private key can decrypt data.

# Set up instructions
### 1. Generate key and certificates
Generate key and certificate for CA, server and devices using openSSL:
[openssl-commands.md](openssl-commands.md)

### 2. Configure Mosquitto Broker to Use Certificates
Put [mosquitto-mtls.conf](mosquitto-mtls.conf) file in directory. This file will tell mosquitto broker to use require device authenticate and not allow anonymous users.
```
allow_anonymous false
require_certificate true
```

### 3. Upgrade subscriber.py and publisher.py to use mTLS
Add this line to provide path to CA certificate, device certificate, device private. key. 
```
mqttc.tls_set('certs/ca.pem','certs/X.pem','certs/X-key.pem')
```

I have configured sensor1 as publisher, dashboard1 as subscriber.

### 4. Test if mTLS is working
![mTLS Tests](media/mtls-test.png)

Start mosquitto broker with mTLS configuration (provide proper path to conf file):
```
mosquitto -c mosquitto-mtls.conf -v      
```

On another terminal, run publisher.py:
```
python3 publisher.py
```  
This will start publishing readings.

On another terminal, run subscriber.py:
```
python3 subscriber.py
```
We will start seeing readings from publisher. Visually, this looks same, however, now broker and devices verify each other and readings are encrypted.