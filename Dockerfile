FROM python:3.9 
#FROM arm32v7/python:3.9
RUN apt update && apt install -y libgpiod2
RUN pip install RPi-GPIO adafruit-circuitpython-dht paho-mqtt pyyaml
ADD main.py .
CMD ["python", "./main.py"] 
