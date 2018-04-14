__author__ = 'Qiu Cheng(Rain Gather)'
__email__ = 'raingather@outlook.com'
__project__ = 'https://github.com/RainGather/Easy_MicroPython'
__licence__ = 'GPL 3.0 https://github.com/RainGather/Easy_MicroPython/blob/release/LICENSE'

import urequests as requests
import time
import ujson as json
import machine
import sys
import network
import dht

from machine import UART
from WAVESHARE import Finger
from PCF8591 import PCF8591
from HCSR04 import HCSR04


def num_map(num):
    if 'esp32' in sys.platform.lower():
        return num
    else:
        nums = [16, 5, 4, 0, 2, 14, 12, 13, 15]
        return nums[num]


def ULTRASONIC(trig_Pin, echo_Pin):
    trig_Pin = num_map(trig_Pin)
    echo_Pin = num_map(echo_Pin)
    return HCSR04(trig_Pin, echo_Pin)
    

def WIFI(ssid, pwd):
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.active(True)
        wlan.connect(ssid, pwd)
        while not wlan.isconnected():
            pass
        print('Network config: ', wlan.ifconfig())


def WAVESHARE_UART_Fingerprint_Reader(port=1, baudrate=19200):
    ser = UART(port, baudrate)
    ser.init(baudrate, bits=8, parity=None, stop=1)
    return Finger(ser)


class ANALOG(PCF8591):
    def __init__(self, scl, sda, freq=400000):
        scl = IN(scl)
        sda = IN(sda)
        freq = freq
        i2c = machine.I2C(freq=freq, scl=scl, sda=sda)
        PCF8591.__init__(self, i2c)
        self.channels = [self.ACHNNL0, self.ACHNNL1, self.ACHNNL2, self.ACHNNL3]
    
    def get(self, ax):
        return self.read(channel=self.channels[ax])
    

class DHT22():
    def __init__(self, num):
        num = num_map(num)
        self.p = dht.DHT22(machine.Pin(num))
    
    def get(self):
        self.p.measure()
        return self.p.temperature(), self.p.humidity()


class DHT11():
    def __init__(self, num):
        num = num_map(num)
        self.p = dht.DHT11(machine.Pin(num))
    
    def get(self):
        self.p.measure()
        return self.p.temperature(), self.p.humidity()


class OUT():
    def __init__(self, num):
        num = num_map(num)
        self.p = machine.Pin(num, machine.Pin.OUT)
        self.p.value(0)
        self.value = self.p.value
    
    def on(self):
        self.p.value(1)
        
    def off(self):
        self.p.value(0)


def IN(num):
    num = num_map(num)
    return machine.Pin(num, machine.Pin.IN)


class SERVO():
    def __init__(self, num, freq=50):
        self.p = PWM(num, freq)
        self.zhuan = self.turn

    def turn(self, angle):
        pwm = int(25 + angle / 180 * 100)
        self.p.duty(pwm)


def PWM(num, freq=50):
    num = num_map(num)
    pin = machine.Pin(num, machine.Pin.OUT)
    return machine.PWM(pin, freq=freq)


DUOJI = SERVO
FINGER = WAVESHARE_UART_Fingerprint_Reader
CHAOSHENGBO = ULTRASONIC
