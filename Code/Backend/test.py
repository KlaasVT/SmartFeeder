import sys
import adafruit_dht
from RPi import GPIO
import time
import spidev
from helpers.Mcp import Mcp



GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
motor = [6,13,19,26]
GPIO.setup(motor[0],GPIO.OUT)
GPIO.setup(motor[1],GPIO.OUT)
GPIO.setup(motor[2],GPIO.OUT)
GPIO.setup(motor[3],GPIO.OUT)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)

output = [[0,0,0,1],[0,0,1,1],[0,0,1,0],[0,1,1,0],[0,1,0,0],[1,1,0,0],[1,0,0,0],[1,0,0,1]]

dhtDevice = adafruit_dht.DHT11(21)

humidity = dhtDevice.humidity
temp = dhtDevice.temperature
print(humidity)
print(temp)

# while True:
#     time.sleep(0.0002)
#     n = 0
#     while n<7:
#         i = 0
#         time.sleep(0.0002)
#         while i< 4:
#             GPIO.output(motor[i], output[n][i])
#             i += 1
#             time.sleep(0.0002)
#         n+=1
#     waarde = GPIO.input(12)
#     print(waarde)

def read_spi(channel):
  spidata = spi.xfer2([1,(8+channel)<<4,0])
  return ((spidata[1] & 3) << 8) + spidata[2]


spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 10 ** 5
channeldata = read_spi(0)
channeldata = 5/1023 * channeldata
channeldata = (channeldata - 0.5) * 100
print("Waarde = {}".format(channeldata))

spi.close()
# while True:
#     mcp = Mcp(0,0)
#     waarde = mcp.read_channel(0)
#     volt = (waarde / 1024.0) * 5

#     graden = (volt - 0.5) * 100 
#     print(volt)
#     mcp.closespi()
#     time.sleep(0.1)
