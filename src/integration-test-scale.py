"""
simple script to test scale implementation on the hardware

"""

from libs.scale.scale_interface import Scale

__scale: Scale = None

if __name__ == "__main__":
    __scale = Scale(True, "average", 5)

    for measurement_index in range(1, 10):
        print(__scale.get_weight())

    __scale.close()
