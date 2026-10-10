from machine import Pin, PWM
import time

buz_pin = None

def setup(pin):
    global buz_pin
    buz_pin = pin

def click():
    p = PWM(Pin(buz_pin), freq=2700, duty=512)
    time.sleep_ms(1)
    p.deinit()

def beep(freq=2700, ms=100):
    p = PWM(Pin(buz_pin), freq=freq, duty=512)
    time.sleep_ms(ms)
    p.deinit()

def alarm():
    for f in range(1000, 3000, 100):
        beep(f, 30)