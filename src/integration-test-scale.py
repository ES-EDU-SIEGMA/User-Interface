#!/usr/bin/python3


"""
simple script to test scale implementation on the hardware

"""
import time

from libs.scale.scale_interface import Scale

__scale: Scale = None

if __name__ == "__main__":
    __scale = Scale(False, 5)

    while True:
        print(__scale.get_weight())
        time.sleep(3)

    __scale.close()
