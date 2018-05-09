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
from NTP import set_ntp_time
from simple_mqtt import MQTTClient


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
    
    
def wifi_ok():
    return network.WLAN(network.STA_IF).isconnected()


def ntp_ok():
    if time.time() < 252288000:
        return False
    return True


def WAVESHARE_UART_Fingerprint_Reader(port=1, baudrate=19200, timeout=False):
    ser = UART(port, baudrate)
    ser.init(baudrate, bits=8, parity=None, stop=1)
    return Finger(ser=ser, timeout=timeout)


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


class Daemon():
    def __init__(self, delay=0):
        self.fs = []
        self.delay = delay
        self.mqtt = None
 
    def wifi(self, ssid, pwd, host='www.hzasteam.org', port=1883):
        wlan = network.WLAN(network.STA_IF)
        if not wlan.isconnected():
            print('Connecting to network...')
            wlan.active(True)
            wlan.connect(ssid, pwd)
            t = time.time()
            while not wlan.isconnected():
                if time.time() - t > 15:
                    print('Network Connect Error, Please Press [RST] To Retry...')
                    wlan.active(False)
                    sys.exit()
            print('Network config: ', wlan.ifconfig())
        for i in range(5):
            try:
                set_ntp_time()
                break
            except Exception as e:
                print(e)
                if i < 4:
                    print('ntp time set error...try again...')
                else:
                    print('ntp time set error! will just use local time')
        self.mqtt = MQTTClient('default', host, port)
        self.mqtt.connect()
        assert self.mqtt is not None, 'mqtt connect error!'

    def loop(self, f):
        self.fs.append(f)
    
    def run_once(self):
        for f in self.fs:
            f()
        if self.mqtt is not None:
            self.mqtt.check_msg()
    
    def run(self):
        print('Start Running...')
        while True:
            try:
                self.run_once()
            except Exception as e:
                print(e)
            time.sleep(self.delay)
    
    def pub(self, *args, **kwargs):
        assert self.mqtt is not None, 'WiFi not connect!'
        self.mqtt.publish(*args, **kwargs)
    
    def sub(self, *args, **kwargs):
        assert self.mqtt is not None, 'WiFi not connect!'
        def _reg_f(f):
            self.mqtt.set_callback(f)
            self.mqtt.subscribe(*args, **kwargs)
        return _reg_f
    
    
daemon = Daemon()
loop = daemon.loop
sub = daemon.sub
pub = daemon.pub
run = daemon.run
wifi = daemon.wifi
WIFI = wifi

DUOJI = SERVO
FINGER = WAVESHARE_UART_Fingerprint_Reader
CHAOSHENGBO = ULTRASONIC
