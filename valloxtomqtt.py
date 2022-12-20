import asyncio, os, threading, time, sys, json
from datetime import datetime, timezone
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

if not 'METRICS' in os.environ:
    chosenmetrics = []
else:
    chosenmetrics = os.environ['METRICS'].replace(" ", "").split(',')
if not 'MQTT_USERNAME' in os.environ:
    username = ''
else:
    username = os.environ['MQTT_USERNAME']

if not 'MQTT_PASSWORD' in os.environ:
    password = ''
else:
    password = os.environ['MQTT_PASSWORD']

async def run():
    if len(chosenmetrics) == 0:
        metrics = await client.fetch_metrics()
    else:
        metrics = await client.fetch_metrics(chosenmetrics)
    metrics["TIMESTAMP"] = str(datetime.utcnow().replace(tzinfo=timezone.utc))
    mqttclient.publish(topicbase+"/sensors", json.dumps(metrics))

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

if not 'WAIT_TIME_SECONDS' in os.environ: 
    wait_time = 30
else:
    wait_time = os.environ['WAIT_TIME_SECONDS']

mqttclient = connect_mqtt()
ticker = threading.Event()
try:
    while not ticker.wait(wait_time):
        asyncio.run(run())
except KeyboardInterrupt:
	pass
