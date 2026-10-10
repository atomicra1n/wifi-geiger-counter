from machine import Pin, PWM, ADC

pwm = None
adc = None
duty = 0
running = False

# pid
kp = 0.5
ki = 0.1
kd = 0.05
integral = 0
last_err = 0

def setup(pwm_pin, fb_pin):
    global pwm, adc
    pwm = PWM(Pin(pwm_pin), freq=20000, duty=0)
    adc = ADC(Pin(fb_pin))
    adc.atten(ADC.ATTN_11DB)

def read_mv():
    raw = adc.read()
    return int(raw / 4095 * 3300)

def get_voltage():
    # multiply by divider ratio to get actual hv
    return read_mv() * 455 / 1000

def update(timer=None):
    global duty, integral, last_err
    if not running:
        return
    
    from config import HV_TARGET
    
    mv = read_mv()
    err = HV_TARGET - mv
    
    integral += err
    # clamp
    if integral > 1000:
        integral = 1000
    if integral < -1000:
        integral = -1000
    
    d = err - last_err
    last_err = err
    
    out = kp * err + ki * integral + kd * d
    duty = int(duty + out)
    
    if duty < 0:
        duty = 0
    if duty > 1023:
        duty = 1023
    
    pwm.duty(duty)

def start():
    global running, integral, duty
    running = True
    integral = 0
    duty = 0

def stop():
    global running, duty
    running = False
    duty = 0
    pwm.duty(0)