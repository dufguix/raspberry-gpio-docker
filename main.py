import time
import board
import adafruit_dht
import paho.mqtt.client as mqtt
import yaml

with open('config.yml', 'r') as file:
   config = yaml.safe_load(file)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    if config['debug'] == True :
        print(f"Connected with result code {reason_code}")


def publish(temperature, humidity):
    mqttc.publish(config['mqtt_temp_topic'], temperature)
    mqttc.publish(config['mqtt_hum_topic'], humidity)

read_period =  config['read_period'] #seconds
max_reporting_period = config['max_reporting_period'] #seconds
count = 0
old_temperature = 0
old_humidity = 0

#sensor = adafruit_dht.DHT22(board.D4)
sensor = adafruit_dht.DHT11(board.D4)

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
if config['mqtt_tls'] == True :
  mqttc.tls_set()
mqttc.username_pw_set(username=config['mqtt_user'],password=config['mqtt_password'])
mqttc.connect(config['mqtt_host'], config['mqtt_port'], 60)

mqttc.loop_start()

while True:
    try:
        temperature = sensor.temperature
        humidity = sensor.humidity
        count = count + read_period
        if count > max_reporting_period or old_temperature != temperature or old_humidity != humidity:
            count = 0
            publish(temperature, humidity)
        old_temperature = temperature
        old_humidity = humidity
        if config['debug'] == True :
            print("Temp={0:0.1f}ºC, Humidity={1:0.1f}%".format(temperature, humidity))
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        if config['debug'] == True :
            print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        sensor.exit()
        raise error

    time.sleep(read_period)


mqttc.loop_stop()
