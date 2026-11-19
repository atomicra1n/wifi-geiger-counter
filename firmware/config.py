# pin assignments
HV_PWM_PIN = 22
HV_FB_PIN = 26 
PULSE_PIN = 21
BUZZER_PIN = 20
LED_PIN = 19

# the feedback divider is 40M/220k so ratio is like 182.8
# 400v / 182.8 = 2.19v = 2190mv on the adc
HV_TARGET = 2190

# m4011 tube conversion factor
CPM_TO_USVH = 0.0066

WIFI_SSID = ""
WIFI_PASS = ""