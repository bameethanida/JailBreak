from machine import Pin, PWM, ADC
from time import sleep
import urequests as requests

GATESTATUS = False
DOORAPI = "https://abc.def/efg/door"
WIFISTATUS = False

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


def serverMon():
    global GATESTATUS
    while True:
        r = requests.get(DOORAPI)
        json = r.json()
        GATESTATUS = json.status
        sleep(0.0001)
