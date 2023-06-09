from .scale_hardware import hx711 as Hx711_module
# import is commented out because import RPi.GPIO in hx711 creates problems when running the code outside the pi.
# to run the code on the pi remove the comment symbol from the import line for Hx711_module.
from .scale_hardware import mock_hx711 as Mock_hx711_module


class Scale:
    __scale_object: Hx711_module.HX711 | Mock_hx711_module.MockHX711

    def __init__(self, __mock_scale: bool, __calculation_method: str, __number_of_measurements: int):
        if __mock_scale:
            self.__scale_object = Mock_hx711_module.MockHX711()
        else:
            self.__scale_object = Hx711_module.HX711(__calculation_method, __number_of_measurements)

    def get_weight(self) -> int:
        return self.__scale_object.get_weight()

    def close_connection(self):
        self.__scale_object.close_hx711()
