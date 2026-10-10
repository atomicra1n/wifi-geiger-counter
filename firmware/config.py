# pin assignments
HV_PWM_PIN = 4
HV_FB_PIN = 0 
PULSE_PIN = 1
BUZZER_PIN = 5
LED_PIN = 2

# the feedback divider is 100M/220k so ratio is like 454.5
# 400v / 454.5 = 0.88v = 880mv on the adc
HV_TARGET = 880

# m4011 tube conversion factor
CPM_TO_USVH = 0.0057

WIFI_SSID = ""
WIFI_PASS = ""