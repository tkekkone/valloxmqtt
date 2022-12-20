FROM python:3-alpine

RUN python -m pip install --upgrade pip

RUN apk add git

RUN pip3 install wget &&\
pip3 install paho-mqtt &&\
pip3 install asyncio  &&\
pip3 install git+https://github.com/yozik04/vallox_websocket_api &&\
rm -rf /var/cache/apk/*

COPY valloxtomqtt.py /valloxtomqtt.py

CMD ["python3","/valloxtomqtt.py"]
