import time

# import RPi.GPIO as GPIO
import mock_gpio as GPIO
import mock_hx711 as HX711

referenceUnit: int = 870298
hx: HX711


def close():
    GPIO.cleanup()


def __init__():
    global hx
    global referenceUnit
    hx = HX711.HX711(5, 6)
    hx.set_reading_format("MSB", "MSB")
    hx.set_reference_unit(referenceUnit)
    hx.reset()
    hx.tare(hx, times=15)


def get_current_weight() -> int:
    global hx

    if HX711 is None:
        return -1

    current: int = int(round(hx.get_weight(5) * 1000))
    hx.reset()
    return current


if __name__ == "__main__":
    __init__()
    print("now")
    time.sleep(3)
    # 356825889
    print(get_current_weight())
    print(get_current_weight())
    close()
