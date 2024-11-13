
# Trying to access raspberry GPIO from a docker container.

Simple python script which reads temperature and humidity sensors and send it to a MQTT broker.
- DHT sensor on D4
- build with `sudo docker compose build`

For the container, challenge are:
- access to the GPIO
- pretend to be a raspberry board

# Access to the GPIO
According to this [SO answer](https://stackoverflow.com/questions/30059784/docker-access-to-raspberry-pi-gpio-pins#48234752),
Running the container in privileged mode works.
I didn't succeed by mapping `--device /dev/gpiomem`.

# Pretend to be a raspberry board
Adafruit_dht lib depends on adafruit_platformdetect lib and RPi.GPIO.
These try to determine the board model through config files which are usually present with Raspbian.

It is up to you to find the right infos for your board thanks to lib examples below.

## adafruit_platformdetect
Lib example:
```python
from adafruit_platformdetect import Detector
detector = Detector()
print("Chip id: ", detector.chip.id)   # Chip id:  BCM2XXX
print("Board id: ", detector.board.id) # Board id:  RASPBERRY_PI_3A_PLUS
```

[Source code](https://github.com/adafruit/Adafruit_Python_PlatformDetect/blob/main/adafruit_platformdetect/chip.py)

It tries to read env vars before analyzing config files.
So simply add this to the compose file:
```yaml
    environment:
      - BLINKA_FORCECHIP=BCM2XXX
      - BLINKA_FORCEBOARD=RASPBERRY_PI_3A_PLUS
```

## RPi.GPIO
Lib example:
```python
import RPi.GPIO as GPIO
print(GPIO.RPI_INFO)
```

[Source code](https://sourceforge.net/p/raspberry-gpio-python/code/ci/default/tree/source/cpuinfo.c#l52)

It reads the following config files:
- /proc/device-tree/system/linux,revision
- /proc/cpuinfo

Focus on `/proc/cpuinfo` only.
The lib tries to find a line beginning with `Hardware        : BCMxxxx`.
On my raspbian installation, the line doesn't exist. So I copy-paste and edit the file.
```
cp /proc/cpuinfo proc-cpuinfo  #copy paste
chmod 644 proc-cpuinfo         #change permission for writing
nano proc-cpuinfo              #edit the file and add , for example, `Hardware        : BCM2837`
```
Then bind the file to the container. So in compose file:
```yaml
    volumes:
      - ./proc-cpuinfo:/proc/cpuinfo:ro
```






