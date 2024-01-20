#!/usr/bin/python3

"""
NOTE: simple script to test scale implementation on the hardware
"""

import time

from RPi.GPIO import GPIO
from libs.scale.scale_hardware.tatobari_hx711.hx711 import HX711
from libs.scale.scale import Scale

if __name__ == "__main__":
    # disable warnings for GPIO and use BCM for pin addressing
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    # init hardware library
    scale_hardware: HX711 = HX711(5, 6)
    scale_hardware.set_reading_format("MSB", "MSB")
    scale_hardware.set_reference_unit(870298)

    # reset hardware
    scale_hardware.reset()
    scale_hardware.tare()

    # init scale library
    scale = Scale(scale_hardware, 5)

    while True:
        try:
            print(scale.get_weight())
            time.sleep(5)
        except KeyboardInterrupt:
            scale_hardware.power_down()
            GPIO.cleanup()
