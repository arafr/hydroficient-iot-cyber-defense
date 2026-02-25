# TEST 3: Generate a New CA (not trusted by our broker) and a device certificate signed by it.
```
openssl genrsa -out different-ca-key.pem 2048
openssl req -x509 -new -nodes -key different-ca-key.pem -subj "/CN=RootCA" -days 3650 -out different-ca.pem

openssl genrsa -out "different-device-key.pem" 2048
openssl req -new -key "different-device-key.pem" -out "different-req.pem" -subj "/CN=$i"
openssl x509 -req -days 365 -in "different-req.pem" -CA different-ca.pem -CAkey different-ca-key.pem -CAcreateserial -out "different-ca-device-cert.pem" -extfile <(echo -e "subjectAltName=DNS:test\nextendedKeyUsage=clientAuth")
```

# TEST 4: Expired device certificate (0 days)
```
openssl genrsa -out "test4-device-key.pem" 2048
openssl req -new -key "test4-device-key.pem" -out "test4-req.pem" -subj "/CN=test4"
openssl x509 -req -days 0 -in "test4-req.pem" -CA ../../certs/ca.pem -CAkey ../../certs/ca-key.pem -CAcreateserial -out "expired-device-cert.pem" -extfile <(echo -e "subjectAltName=DNS:localhost\nextendedKeyUsage=clientAuth")
```