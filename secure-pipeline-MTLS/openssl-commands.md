Note: Instead of the cryptography library, I used openSSL to generate keys and certificates. I found it easier to learn and write commands.

# Create CA Certificate
```
openssl genrsa -out ca-key.pem 2048
openssl req -x509 -new -nodes -key ca-key.pem -subj "/CN=RootCA" -days 3650 -out ca.pem
```

# Create Server Certificate Signed by CA
```
openssl genrsa -out "server-key.pem" 2048

openssl req -new -key "server-key.pem" -out "server-req.pem" -subj "/CN=localhost"

openssl x509 -req -days 365 -in "server-req.pem" -CA ca.pem -CAkey ca-key.pem -CAcreateserial -out "server.pem" -extfile <(echo -e "subjectAltName=DNS:localhost\nextendedKeyUsage=serverAuth")
```

# Create Certificates for Devices, Signed by CA
```
for i in sensor1 sensor2 dashboard1
do
    openssl genrsa -out "$i-key.pem" 2048

    openssl req -new -key "$i-key.pem" -out "$i-req.pem" -subj "/CN=$i"

    openssl x509 -req -days 365 -in "$i-req.pem" -CA ca.pem -CAkey ca-key.pem -CAcreateserial -out "$i.pem" -extfile <(echo -e "subjectAltName=DNS:$i\nextendedKeyUsage=clientAuth")
done
```

docs: https://learn.microsoft.com/en-us/azure/vpn-gateway/point-to-site-certificates-linux-openssl