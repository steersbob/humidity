# humidity

A simple Brewblox humidity sensor, based on https://pimylifeup.com/raspberry-pi-humidity-sensor-dht22/.

Note that the AdaFruit_DHT package is only available on Pi-based systems.

To build:

```
docker build -t steersbob/humidity:local .
```

Docker-compose configuration, with automated building:

```yaml
version: "3.7"
services:
  humidity:
    build:
      context: /home/pi/humidity
    privileged: true
    init: true
```
