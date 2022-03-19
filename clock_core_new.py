#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import datetime
import logging
import time
import traceback
import requests

imgdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'img')
#picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')

if os.path.exists(libdir):
  sys.path.append(libdir)
  
from pprint import pprint
from PIL import Image,ImageDraw,ImageFont
from waveshare_epd import epd7in5_V2

WEATHER_API_KEY = 'f49bdc5ac4d80d694096358ec9976c24'
weather_base_url = "http://api.openweathermap.org/data/2.5/weather?"
zip_code = '80521'
weather_url = weather_base_url + "appid=" + WEATHER_API_KEY + "&zip=" + zip_code
weather = None

def update_weather():
  try:
    global weather
    weather = requests.get(weather_url).json()
  except:
    logging.info('weather could not be retrieved')

def temp():
  f = float(weather['main']['temp']) * 1.8 - 459.67
  t = str(int(f))
  return t

def description():
  return weather['weather'][0]['main']

def icon():
  icon = weather['weather'][0]['icon'] + '.bmp'
  icon = os.path.join(imgdir, icon)
  if os.path.isfile(icon):
    return icon
  else:
    os.path.join(imgdir, '01n.bmp')
  return icon

#def sprite():
#  return os.path.join(imgdir, 'weather_icons.jpg')

def update_time():
  d = datetime.datetime.now()
  t = d.strftime('%-I:%M')
  return t
  
#def drawSprite(x,y):
#  epd = epd2in7.EPD()
#  epd.init()
#  Himage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
#  draw = ImageDraw.Draw(Himage)
#  newimage = Image.open(sprite())
#  Himage.paste(newimage, (0,0))
#  epd.display(epd.getbuffer(Himage))
#  epd.sleep()
  

def update(t):
  epd = epd7in5_V2.EPD()
  epd.init()
#  epd.Clear(0xFF)

  Himage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
  draw = ImageDraw.Draw(Himage)
  x = 10
  if len(t) == 4:
    x = x + 10
  draw.text((x, 48), t, font = font128, fill = 0)
  if weather is not None:
    draw.text((210, 8), temp(), font = font32, fill = 0)
    draw.text((248, 14), 'f', font = font24, fill = 0)
    draw.text((50, 14), description(), font = font24, fill = 0)
    newimage = Image.open(icon())
    Himage.paste(newimage, (0,0))
  epd.display(epd.getbuffer(Himage))
  epd.sleep()

try:
  logging.basicConfig(level=logging.INFO)
  logging.info(imgdir)
  font128 = ImageFont.truetype(os.path.join(imgdir, 'code_bold.otf'), 120)  
  font32 = ImageFont.truetype(os.path.join(imgdir, 'code_bold.otf'), 32)
  font24 = ImageFont.truetype(os.path.join(imgdir, 'code_bold.otf'), 24)
  tp = ''
  
  while True:
    t = update_time()
    if tp != t:
      tp = t
      update_weather()
      update(tp)
    time.sleep(5)
  
#  drawSprite()
    
except IOError as e:
  logging.info(e)
    
except KeyboardInterrupt:    
  logging.info("ctrl + c:")
  epd2in7.epdconfig.module_exit()
  exit()

