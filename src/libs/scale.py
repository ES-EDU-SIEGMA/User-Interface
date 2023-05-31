from . import globals as local_globals

if local_globals.RUN_ON_PI:
    from .hx711 import HX711
    import RPi.GPIO as GPIO
else:
    print("SCALE USING MOCK")
    from .mock_hx711 import HX711
    from . import mock_gpio as GPIO

referenceUnit = 870298
hx = HX711(5, 6)


def __init__():
    global hx
    global referenceUnit
    GPIO.setwarnings(GPIO, None)
    hx.set_reading_format("MSB", "MSB")
    hx.set_reference_unit(referenceUnit)
    hx.reset()
    hx.tare()


def get_current_weight():
    global hx

    if hx is None:
        return -1

    current = hx.get_weight(5)
    current = int(round(current * 1000))
    hx.power_down()
    hx.power_up()
    return current


def close():
    GPIO.cleanup(GPIO)


if __name__ == "__main__":
    __init__()
    print("now")
    print(get_current_weight())
    print(get_current_weight())
    close()
