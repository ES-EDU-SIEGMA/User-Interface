class Scale:
    __scale_object = None
    __reference_unit: int = 870298
    __mock_in_use: bool = False
    __number_of_measurements: int

    def __init__(
        self,
        __mock_scale: bool,
        __number_of_measurements: int = 3,
    ):
        if __mock_scale:
            from libs.scale.scale_hardware import mock_hx711 as mock_hx711_module

            self.__mock_in_use = True
            self.__scale_object = mock_hx711_module.MockHX711()
            self.__git_code = False
        else:
            from libs.scale.scale_hardware.tatobari_hx711.hx711 import HX711 as HX711
            import RPi.GPIO as GPIO

            GPIO.setwarnings(False)
            self.__number_of_measurements = __number_of_measurements
            self.__scale_object = HX711(5, 6)
            self.__scale_object.set_reading_format("MSB", "MSB")
            self.__scale_object.set_reference_unit(self.__reference_unit)
            self.__scale_object.reset()
            self.__scale_object.tare()

    def get_weight(self) -> int:
        if self.__scale_object is None:
            return -1

        if self.__mock_in_use:
            return self.__scale_object.get_weight()

        current = self.__scale_object.get_weight(self.__number_of_measurements)
        current = int(round(current * 1000))
        self.__scale_object.power_down()
        self.__scale_object.power_up()
        return current

    def close(self):
        if self.__mock_in_use:
            return

        GPIO.cleanup()
