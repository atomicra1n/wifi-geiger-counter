from machine import Pin, Timer
import time
import config
import geiger
import hv_control
import buzzer
import wifi_manager

print("starting up...")

led = Pin(config.LED_PIN, Pin.OUT)
led.on()

# setup buzzer
buzzer.setup(config.BUZZER_PIN)
buzzer.beep(2700, 100)

# setup geiger counter
geiger.setup(config.PULSE_PIN)
geiger.set_click_callback(buzzer.click)

# setup hv
hv_control.setup(config.HV_PWM_PIN, config.HV_FB_PIN)
hv_control.start()

# run pid at 100hz
tim = Timer(0)
tim.init(freq=100, mode=Timer.PERIODIC, callback=hv_control.update)

# wifi
if wifi_manager.connect(config.WIFI_SSID, config.WIFI_PASS):
    led.off()
    wifi_manager.start(geiger, hv_control)
    print("ready")
else:
    print("no wifi, running offline")

while True:
    wifi_manager.check()
    
    # debug
    cpm = geiger.get_cpm()
    usvh = geiger.get_usvh()
    hv = hv_control.get_voltage()
    print("cpm:", round(cpm), ", usvh:", round(usvh, 4), ", hv:", round(hv), "V")
    
    time.sleep(5)