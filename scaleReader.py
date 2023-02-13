import time
import sys
import RPi.GPIO as GPIO
from hx711 import HX711

referenceUnit = 870298
hx = None

def close():
    GPIO.cleanup()
    
def __init__():
    global hx
    global referenceUnit
    GPIO.setwarnings(False)
    hx = HX711(5, 6)
    hx.set_reading_format("MSB", "MSB")
    hx.set_reference_unit(referenceUnit)
    hx.reset()
    hx.tare()
    
def getCurrentWeight():
    global hx
    
    if hx == None:
        return -1
    
    current = hx.get_weight(5)
    current = int(round(current * 1000))
    hx.power_down()
    hx.power_up()
    return current
    
if __name__ == '__main__':
    __init__()
    print("now")
    time.sleep(3)
    #356825889
    print(getCurrentWeight())
    print(getCurrentWeight())
    close()
    