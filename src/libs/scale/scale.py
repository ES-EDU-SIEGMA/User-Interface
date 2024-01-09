class Scale:
    """
    IMPORTANT: Requires HX711 and associated GPIOs to be initialized!
    """

    __hardware = None
    __number_of_measurements: int

    def __init__(self, hardware, number_of_measurements: int = 3):
        __hardware = hardware
        __number_of_measurements = number_of_measurements

    def get_weight(self) -> int:
        """
        :return: measured weight in gramm
        """
        if self.__hardware is None:
            return -1
        measurement = self.__hardware.get_weight(self.__number_of_measurements)
        measurement = int(round(measurement * 1000))  # convert from _mg_ to _g_
        return measurement
