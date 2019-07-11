from machine import Pin, PWM, ADC
from time import sleep
import json
import urequests as requests
from _thread import start_new_thread as thread
import pyb

GATESTATUS = False
DOORAPI = "https://exceed.superposition.pknn.dev/data/:5"
WIFISTATUS = False
ALERTSTATUS = False


def escape_check():
    while(True):
        global alert
        pin_lazer.value(1)
        print(pin_ldr.read())
        sleep(0.01)


def alert_mode():
    global alert
    while(True):
        if alert:
            pin_buzzer.value(1)
            pin_led.value(1)
            sleep(0.5)
            pin_buzzer.value(0)
            pin_led.value(0)
            sleep(0.5)
        sleep(0.01)


def btnMon():
    global GATESTATUS, WIFISTATUS
    p_mon = Pin(34, Pin.IN)
    btnstatus = False
    while True:
        if p_mon.value() == 0:  # BTN-Down
            if not btnstatus:
                GATESTATUS = not GATESTATUS
                if WIFISTATUS:
                    data = json.dumps({
                        'gate_status': GATESTATUS
                    })
                    headers = {'Content-type': 'application/json'}
                    requests.post(DOORAPI, data=data, headers=headers)
            btnstatus = True
        else:
            btnstatus = False
        sleep(0.0001)


def WIFIConnect():
    global WIFISTATUS
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    while not wlan.isconnected():
        WIFISTATUS = False
        print('connecting...')
        wlan.connect('exceed16_8', '12345678')
        while not wlan.isconnected():
            pass
        WIFISTATUS = True
        print('connected')


def servo_spin(GATESTATUS):
    global GATESTATUS
    SERVO_PIN = 32
    if (GATESTATUS):
        servo1 = pyb.Servo(1)
        # SERVO=Pin(LED_PIN,Pin.IN)
        # SERVO.value()
        # servo1.angle(angle from -90 to 90,time(milli.sec) for move)
        servo1.angle(50, 1000)


def servo_spin_test(GATESTATUS):
    global GATESTATUS
    SERVO_PIN = 32
    if (GATESTATUS):
        servo = PWM(Pin(22), freq=50, duty=77)
        servo.duty(30)
        sleep(0.5)
        servo.deinit()
        print('rolling in the deep')


def serverMon():
    global GATESTATUS
    while True:
        r = requests.get(DOORAPI)
        json = r.json()
        GATESTATUS = json['gate_status']
        sleep(2)


thread(WIFIConnect, None)
thread(btnMon, None)
thread(serverMon, None)
thread(escape_check, None)
thread(alert_mode, None)
