from machine import Pin, PWM, ADC
from time import sleep

GATESTATUS = False


def btnMon():
    global GATESTATUS
    p_mon = Pin(34, Pin.IN)
    btnstatus = False
    while True:
        if p_mon.value() == 0:  # BTN-Down
            if not btnstatus:
                GATESTATUS = not GATESTATUS
            btnstatus = True
        else:
            btnstatus = False
        sleep(0.0001)


def WIFIConnect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    while not wlan.isconnected():
        print('connecting...')
        wlan.connect('exceed16_8', '12345678')
        while not wlan.isconnected():
            pass
        print('connected')

def servo_spin(GATESTATUS)
  global GATESTATUS
  SERVO_PIN = 32
  if (GATESTATUS):
    servo1 = pyb.Servo(1)
    #SERVO=Pin(LED_PIN,Pin.IN)
    #SERVO.value()
    #servo1.angle(angle from -90 to 90,time(milli.sec) for move)
    servo1.angle(50, 1000)
