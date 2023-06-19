class Scale:
    __scale_object = None
    __git_code: bool = False
    __reference_unit: int = 870298

    def __init__(
            self,
            __mock_scale: bool,
            __calculation_method: str,
            __number_of_measurements: int,
    ):
        if __mock_scale:
            from libs.scale.scale_hardware import mock_hx711 as mock_hx711_module

            self.__scale_object = mock_hx711_module.MockHX711()

        elif self.__git_code:

            from scale_hardware import hx711_git_code as hx711_git
            import RPI.GPIO as GPIO

            GPIO.setwarnings(False)
            self.__scale_object = hx711_git.HX711(5, 6)
            self.__scale_object.set_reading_format("MSB", "MSB")
            self.__scale_object.set_reference_unit(self.__reference_unit)
            self.__scale_object.reset()
            self.__scale_object.tare()

        else:
            from libs.scale.scale_hardware.hx711 import HX711 as HX711

            self.__scale_object = HX711(
                __calculation_method, __number_of_measurements
            )

    def get_weight(self) -> int:

        if self.__git_code:
            if self.__scale_object is None:
                return -1

            current = self.__scale_object.get_weight(5)
            current = int(round(current * 1000))
            self.__scale_object.power_down()
            self.__scale_object.power_up()
            return current

        else:
            return self.__scale_object.get_weight()

    def close(self):
        self.__scale_object.close_hx711()
