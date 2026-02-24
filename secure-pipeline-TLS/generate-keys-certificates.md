docs: https://learn.microsoft.com/en-us/azure/vpn-gateway/point-to-site-certificates-linux-openssl

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