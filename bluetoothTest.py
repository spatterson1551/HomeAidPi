from bluetooth import *
import RPi.GPIO as gpio
import time
import threading

gpio.setmode(gpio.BCM)

gpio.setup(17, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(25, gpio.OUT)

gpio.output(25, gpio.HIGH)
enabled = True

target_device = "PATTERSONSW1\xe2\x80\x99s iPhone"
target_device_address = None

def enableMat():
    print('mat re-enabled')
    enabled = True
    return

while True:
    if enabled == True:
        if gpio.input(17) == gpio.HIGH:
            #someone has entered, ping bluetooth
            print("floor mat activated")
	    enabled = False
	    t = threading.Timer(5, enableMat)
	    t.start()
            if target_device == lookup_name('CC:78:5F:5B:57:29'):
                target_device_address = 'CC:78:5F:5B:57:29'

        if target_device_address is not None:
            print("Hello Steve, welcome to the family room")
            
        target_device_address = None
    time.sleep(.25)


