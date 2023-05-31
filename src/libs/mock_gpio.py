"""
simulates RPi.GPIO
"""

pins: [int] = {}


BCM = "BCM"


def setmode(mode: bool):
    pass


# False = Low
def setup(pin, mode, initial=None, pul_up_down=None):
    pins[pin] = False


def input(pin):
    return pins.get(pin, False)


def output(pin, state):
    pins[pin] = state


def cleanup():
    pass


def setwarnings(flag):
    pass
