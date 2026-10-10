from machine import Pin
import time

pulse_count = 0
pulse_times = []
click_func = None

def pulse_handler(pin):
    global pulse_count
    pulse_count += 1
    pulse_times.append(time.ticks_ms())
    if click_func:
        click_func()

def setup(pin_num):
    p = Pin(pin_num, Pin.IN)
    p.irq(trigger=Pin.IRQ_FALLING, handler=pulse_handler)
    return p

def get_cpm():
    global pulse_times
    now = time.ticks_ms()
    # keep only last 60 seconds
    pulse_times = [t for t in pulse_times if now - t < 60000]
    return len(pulse_times)

def get_usvh():
    from config import CPM_TO_USVH
    return get_cpm() * CPM_TO_USVH

def set_click_callback(func):
    global click_func
    click_func = func