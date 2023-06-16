class Scale:
    def __init__(
        self,
        __mock_scale: bool,
        __calculation_method: str,
        __number_of_measurements: int,
    ):
        if __mock_scale:
            from libs.scale.scale_hardware import mock_hx711 as mock_hx711_module

            self.__scale_object = mock_hx711_module.MockHX711()
        else:
            from libs.scale.scale_hardware.hx711 import HX711 as HX711

            self.__scale_object = HX711(
                __calculation_method, __number_of_measurements
            )

    def get_weight(self) -> int:
        return self.__scale_object.get_weight()

    def close(self):
        self.__scale_object.close_hx711()
