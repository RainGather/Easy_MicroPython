import urequests as requests
import time
import ujson as json
import machine
import sys
import network
import dht



num_map = [16, 5, 4, 0, 2, 14, 12, 13, 15, 3, 1]


def WAVESHARE_UART_Fingerprint_Reader(port=1, baudrate=19200):
    from machine import UART
    from .finger import Finger
    ser = UART(port, baudrate)
    ser.init(baudrate, bits=8, parity=None, stop=1)
    return Finger(ser)


class DHT22():
    def __init__(self, num):
        num = num_map[num]
        self.p = dht.DHT22(machine.Pin(num))
    
    def get(self):
        self.p.measure()
        return self.p.temperature(), self.p.humidity()


class DHT11():
    def __init__(self, num):
        num = num_map[num]
        self.p = dht.DHT11(machine.Pin(num))
    
    def get(self):
        self.p.measure()
        return self.p.temperature(), self.p.humidity()


class OUT():
    def __init__(self, num):
        num = num_map[num]
        self.p = machine.Pin(num, machine.Pin.OUT)
        self.p.value(0)
        self.value = self.p.value
    
    def on(self):
        self.p.value(1)
        
    def off(self):
        self.p.value(0)


def IN(num):
    num_map = [16, 5, 4, 0, 2, 14, 12, 13, 15, 3, 1]
    num = num_map[num]
    return machine.Pin(num, machine.Pin.IN)


class SERVO():
    def __init__(self, num, freq=50):
        self.p = PWM(num, freq)
        self.zhuan = self.turn

    def turn(self, angle):
        pwm = int(25 + angle / 180 * 100)
        self.p.duty(pwm)


def PWM(num, freq=50):
    pin = OUT(num)
    return machine.PWM(pin, freq=freq)


DUOJI = SERVO
FINGER = WAVESHARE_UART_Fingerprint_Reader