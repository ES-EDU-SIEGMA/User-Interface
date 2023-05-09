import os
import time


USE_MOCK_HX711 = os.environ.get("USE_MOCK_HX711", False)
USE_MOCK_GPIO = os.environ.get("USE_MOCK_GPIO", False)

if USE_MOCK_HX711:
	from MockHX711 import MockHX711
	hx = MockHX711(5,6)
else:
	from hx711 import HX711
	hx = None

if USE_MOCK_GPIO:
	import MOCKGPIO
	GPIO = MOCKGPIO()
else:
	import RPi.GPIO as GPIO 


referenceUnit = 870298



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


if __name__ == "__main__":
    __init__()
    print("now")
    time.sleep(3)
    # 356825889
    print(getCurrentWeight())
    print(getCurrentWeight())
    close()
