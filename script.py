"""
Code example for publishing data to the Brewblox eventbus

Dependencies:
- paho-mqtt
- adafruit-dht
"""

import json
from ssl import CERT_NONE
from time import sleep

import Adafruit_DHT

from paho.mqtt import client as mqtt

SENSOR = Adafruit_DHT.AM2302
PIN = 4

HOST = '172.17.0.1'
TOPIC = 'brewcast/history'

# Create a websocket MQTT client
client = mqtt.Client(transport='websockets')
client.ws_set_options(path='/eventbus')
client.tls_set(cert_reqs=CERT_NONE)
client.tls_insecure_set(True)

try:
    client.connect(host=HOST, port=443)
    client.loop_start()

    while True:
        sleep(5)

        humidity, temperature = Adafruit_DHT.read_retry(SENSOR, PIN)
        if None in (humidity, temperature):
            print('Discarding values...')
            continue

        message = {
            'key': 'dht22',
            'data': {
                'humidity[%]': humidity,
                'temperature[degC]': temperature,
            },
        }

        client.publish(TOPIC, json.dumps(message))
        print(f'sent {message}')


finally:
    client.loop_stop()
