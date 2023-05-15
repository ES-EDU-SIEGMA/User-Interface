"""
simulates RPi.GPIO
"""


def __init__(self):
    self.pins = {}


def setmode(self, mode) -> None:
    pass


# False = Low
def setup(self, pin, mode, initial=None, pul_up_down=None) -> None:
    self.pins[pin] = False


def input(self, pin):
    return self.pins.get(pin, False)


def output(self, pin, state) -> None:
    self.pins[pin] = state


def cleanup(self) -> None:
    pass


def setwarnings(self, flag: bool) -> None:
    pass
