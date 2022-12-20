import asyncio, os, threading, time, sys
from vallox_websocket_api import Client
from paho.mqtt import client as mqtt_client

if not 'VALLOX_ADDRESS' in os.environ:
    print("Must set VALLOX_ADRESS env")
    sys.exit()
else:
    client = Client(os.environ['VALLOX_ADDRESS'])

if not 'MQTT_ADDRESS' in os.environ:
    print("Must set MQTT_ADDRESS env")
    sys.exit()
else:
    broker = os.environ['MQTT_ADDRESS']

if not 'MQTT_PORT' in os.environ:
    port = 1883
else:
    port = int(os.environ['MQTT_PORT']) 

topicbase = 'vallox'
client_id = 'valloxmqtt'

if not 'MQTT_USERNAME' in os.environ:
    username = ''
else:
    username = os.environ['MQTT_USERNAME']

if not 'MQTT_PASSWORD' in os.environ:
    password = ''
else:
    password = os.environ['MQTT_PASSWORD']

async def run():
    metrics = await client.fetch_metrics()
    for key in metrics:
        mqttclient.publish(topicbase+"/"+key, metrics[key])

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


WAIT_TIME_SECONDS = 5
mqttclient = connect_mqtt()
ticker = threading.Event()
try:
    while not ticker.wait(WAIT_TIME_SECONDS):
        asyncio.run(run())
except KeyboardInterrupt:
	pass
