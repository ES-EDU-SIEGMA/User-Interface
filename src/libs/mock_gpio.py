"""
simulates RPi.GPIO
"""

pins: [int] = {}


def setmode(self, mode):
    pass


# False = Low
def setup(self, pin, mode, initial=None, pul_up_down=None):
    self.pins[pin] = False


def input(self, pin):
    return self.pins.get(pin, False)


def output(self, pin, state):
    self.pins[pin] = state


def cleanup(self):
    pass


def setwarnings(self, flag):
    pass
