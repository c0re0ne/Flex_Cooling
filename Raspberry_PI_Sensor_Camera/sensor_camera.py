#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

import Adafruit_DHT
from picamera import PiCamera
from time import sleep
from PIL import Image, ImageDraw, ImageFont

camera = PiCamera()
camera.resolution = (2592, 1944)
camera.framerate = 15
camera.start_preview()
sleep(2)
camera.capture('/var/www/html/sensor/picture.jpg')
camera.stop_preview()
sleep(1)

img = Image.open("picture.jpg")
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("arial.ttf", 50)

local_encoding = 'cp850'
deg = u'\xb0'.encode(local_encoding)

# Parse command line parameters.
sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }
if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
    sensor = sensor_args[sys.argv[1]]
    pin = sys.argv[2]
else:
    print('Usage: sudo ./Adafruit_DHT.py [11|22|2302] <GPIO pin number>')
    print('Example: sudo ./Adafruit_DHT.py 2302 4 - Read from an AM2302 connected to GPIO pin #4')
    sys.exit(1)


humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)


if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}°C  Humidity={1:0.1f}%'.format(temperature, humidity))
    str='Temp={0:0.1f} deg,  Humidity={1:0.1f}%'.format(temperature, humidity)
    draw.text((70, 250), str, fill='yellow', font = font)
    img.save('drawn_image.jpg')
else:
    print('Failed to get reading. Try again!')
    sys.exit(1)
