Build the image

`docker build -t valloxmqtt .`

Run the program image with config from env

`docker run -e VALLOX_ADDRESS='vallox.home' -e MQTT_ADDRESS='mqtt.home' -e MQTT_PORT='1883' -ti valloxmqtt`
