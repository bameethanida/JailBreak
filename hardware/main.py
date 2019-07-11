from machine import Pin, PWM, ADC
from time import sleep
import json
import urequests as requests
from _thread import start_new_thread as thread

GATESTATUS = False
DOORAPI = "https://exceed.superposition.pknn.dev/data/5"
WIFISTATUS = False
ALERTSTATUS = False


def escape_check():
    global ALERTSTATUS
    pin_lazer = Pin(25)
    while(True):
        pin_lazer.value(1)
        if (pin_ldr.read() >= 2500):
            ALERTSTATUS = True
        sleep(0.01)


def alert_mode():
    global ALERTSTATUS, GATESTATUS
    pin_buzzer = Pin(26, Pin.OUT)
    pin_led = Pin(21, Pin.OUT)
    while(True):
        if ALERTSTATUS:
            GATESTATUS = True
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
                    r = requests.get(DOORAPI)
                    json_data = r.json()
                    data = json.dumps({
                        'door': GATESTATUS,
                        'buzzer': json_data.buzzer,
                        'LED': json_data.LED
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
    global GATESTATUS
    while True:
        r = requests.get(DOORAPI)
        json = r.json()
        GATESTATUS = json['door']
        sleep(2)


def lightMon():
    global led, ldr, laser
    while True:
        laser.value(0)
        if ldr.read() < 1000:
            led[0].value(1)
            led[1].value(1)
            led[2].value(1)
        else:
            led[0].value(0)
            led[1].value(0)
            led[2].value(0)
        laser.value(1)
        sleep(0.1)


thread(WIFIConnect, [])
thread(btnMon, [])
thread(serverMon, [])
#thread(escape_check, [])
#thread(alert_mode, [])
