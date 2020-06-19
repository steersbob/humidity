"""
Code example for publishing data to the Brewblox eventbus

Dependencies:
- paho-mqtt
- adafruit-dht
"""

import json
import logging
from os import getenv
from ssl import CERT_NONE
from time import sleep

import Adafruit_DHT
from paho.mqtt import client as mqtt

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y/%m/%d %H:%M:%S')
LOGGER = logging.getLogger()

TOPIC = 'brewcast/history'
SENSOR = Adafruit_DHT.DHT22
PIN = 4

host = getenv('HOST', 'eventbus')
transport = getenv('TRANSPORT', 'tcp')
port = getenv('PORT', 1883 if transport == 'tcp' else '443')


# Create an MQTT client
client = mqtt.Client(transport=transport)

if transport == 'websockets':
    client.ws_set_options(path='/eventbus')
    client.tls_set(cert_reqs=CERT_NONE)
    client.tls_insecure_set(True)

try:
    client.connect_async(host=host, port=port)
    client.loop_start()

    while True:
        sleep(5)

        humidity, temperature = Adafruit_DHT.read_retry(SENSOR, PIN)
        if None in (humidity, temperature):
            LOGGER.warning('Discarding values')
            continue

        if not 0 <= humidity <= 100:
            LOGGER.warning(f'Discarding invalid humidity of {humidity}')
            continue

        if not 0 <= temperature <= 50:
            LOGGER.warning(f'Discarding invalid temperature of {temperature}')
            continue

        message = {
            'key': 'humidity',
            'data': {
                'humidity[%]': humidity,
                'temperature[degC]': temperature,
            },
        }

        client.publish(TOPIC, json.dumps(message))
        LOGGER.info(f'{temperature:.2f}°C | {humidity:.2f}%')


finally:
    client.loop_stop()
