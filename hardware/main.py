from machine import Pin, PWM, ADC
from time import sleep
import json
import urequests as requests
from _thread import start_new_thread as thread

GATESTATUS = False
API = "https://exceed.superposition.pknn.dev/data/5"
WIFISTATUS = False
ALERTSTATUS = False
LIGHTSTATUS = False
AUTOLIGHTSTATUS = False

laser = Pin(25, Pin.OUT)
ldr = ADC(Pin(33))
buzzer = Pin(26, Pin.OUT)
led = [
    Pin(18, Pin.OUT),
    Pin(19, Pin.OUT),
    Pin(21, Pin.OUT),
]


def escape_check():
    global ALERTSTATUS, AUTOLIGHTSTATUS, laser, ldr
    laser.value(1)
    while(True):
        if (ldr.read() >= 2500):
            ALERTSTATUS = True
        laser.value(1)
        if (ldr.read() >= 2500):
            AUTOLIGHTSTATUS = True
        laser.value(0)
        sleep(0.01)


def alert_mode():
    global ALERTSTATUS, GATESTATUS, led
    led = Pin(18, Pin.OUT)
    while(True):
        if ALERTSTATUS:
            led[1].value(0)
            led[2].value(0)
            GATESTATUS = False
            buzzer.value(1)
            led[0].value(1)
            sleep(0.5)
            buzzer.value(0)
            led[0].value(0)
            sleep(0.5)
        sleep(0.01)


def btnMon():
    global GATESTATUS, WIFISTATUS, API
    p_mon = Pin(34, Pin.IN)
    btnstatus = False
    while True:
        if p_mon.value() == 0:  # BTN-Down
            if not btnstatus:
                GATESTATUS = not GATESTATUS
                if WIFISTATUS:
                    r = requests.get(API)
                    json_data = r.json()
                    data = json.dumps({
                        'door': GATESTATUS,
                        'buzzer': json_data.buzzer,
                        'LED': json_data.LED
                    })
                    headers = {'Content-type': 'application/json'}
                    requests.post(API, data=data, headers=headers)
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


def servo_spin_test():
    global GATESTATUS
    SERVO_PIN = 32
    if (GATESTATUS):
        servo = PWM(Pin(SERVO_PIN), freq=50, duty=77)
        servo.duty(30)
        sleep(0.5)
        servo.deinit()
        print('rolling in the deep')


def serverMon():
    global GATESTATUS, ALERTSTATUS, LIGHTSTATUS, API
    while True:
        r = requests.get(API)
        json = r.json()
        GATESTATUS = json['door']
        ALERTSTATUS = json['buzzer']
        LIGHTSTATUS = json['LED']
        sleep(2)


def lightMon():
    global led
    while True:
        if (AUTOLIGHTSTATUS or LIGHTSTATUS) and not ALERTSTATUS:
            led[0].value(1)
            led[1].value(1)
            led[2].value(1)
        elif not LIGHTSTATUS and not AUTOLIGHTSTATUS and not ALERTSTATUS:
            led[0].value(0)
            led[1].value(0)
            led[2].value(0)
        sleep(0.1)


def doorMon():
    global GATESTATUS
    SERVO_PIN = 32
    servo = PWM(Pin(SERVO_PIN), freq=50, duty=30)
    while True:
        if GATESTATUS:
            servo.duty(77)
        else:
            servo.duty(30)
        sleep(0.1)


thread(WIFIConnect, [])
thread(btnMon, [])
thread(serverMon, [])
thread(lightMon, [])
thread(doorMon, [])
thread(escape_check, [])
thread(alert_mode, [])
