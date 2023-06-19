"""
simple script to test scale implementation on the hardware

"""
import time

from libs.scale.scale_interface import Scale

__scale: Scale = None

if __name__ == "__main__":
    __scale = Scale(__mock_scale=True, __number_of_measurements=5)

    for measurement_index in range(1, 10):
        print(__scale.get_weight())
        time.sleep(3)

    __scale.close()
