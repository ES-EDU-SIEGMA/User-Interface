class Scale:
    """
    IMPORTANT: Requires HX711 and associated GPIOs to be initialized!
    """

    __hardware = None
    __number_of_measurements: int = None
    __base_value: int = None

    def __init__(self, hardware, number_of_measurements: int = 3):
        self.__hardware = hardware
        self.__number_of_measurements = number_of_measurements
        self.__base_value = 0

    def tare(self):
        current = self.get_weight()
        self.__base_value = current

    def get_weight(self) -> int:
        """
        :return: measured weight in gramm
        """
        if self.__hardware is None:
            return -1
        measurement = self.__hardware.get_weight(self.__number_of_measurements)
        measurement = int(round(measurement * 1000))  # convert from _mg_ to _g_
        measurement = measurement - self.__base_value
        return measurement
