# Overview
This project secures the Grand Marina hotel’s HYDROLOGIC water monitoring system by implementing a hardened IoT security pipeline.

It includes:

* TLS and Mutual TLS (mTLS) for encrypted and authenticated communication between sensors, server, and dashboard.

* Replay attack protection using timestamp validation, counters, and HMAC message signing.

* Real-time monitoring dashboard for water flow, pressure, and remote shutoff controls.

| Links |
| ------------- |
| [Threat Model with STRIDE Analysis](threat-model-stride.pdf/) |
| [Insecure Pipeline](insecure-pipeline/) |
| [Secure Pipeline with TLS](secure-pipeline-TLS/) |