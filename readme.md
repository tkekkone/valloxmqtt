Build the image

`docker build -t valloxmqtt .`

Run the program image with config from env

`docker run -e VALLOX_ADDRESS='vallox.home' -e MQTT_ADDRESS='mqtt.home' -ti valloxmqtt`

Other env variables 
* MQTT_PORT - Mqtt broker port
* METRICS - Comma separated list, includes all if not defined
* MQTT_USERNAME
* MQTT_PASSWORD
* WAIT_TIME_SECONDS - interval between metric fetch, default 30
