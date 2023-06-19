import RPi.GPIO as GPIO

# the module RPi.GPIO is only available for the raspberry pi
import time
import threading


class HX711:
    """__PD_SCK refers to the pin on the pi to which the hx 711 PD_SCK pin is connected.
    the PD_SCK pin on the hx711 is used to control the hx711 converter.
    __DOUT refers to the pin on the pi to which the hx711 DOUT pin is connected.
    the DOUT pin on the hx711 returns an int encoded as 24 bit 2's complement.

    to read data from the hx711 DOUT pin the PD_SCK pin on the hx711 must be activated and deactivated.
    the hx711 then returns one bit of data.

    __GAIN # todo add explanation. We are using GAIN=128 on Channel A

    __calculation_method:= str "median" | "average"
    __number_of_measurements determines how many measurement values used to calculate a weight value.
    __offset is a weight value that is used to tare the scale."""

    __calculation_method: str
    __number_of_measurements: int
    __number_of_measurements_is_odd: bool
    __offset: int
    __reference_unit: int = 870298

    __read_lock = threading.Lock()
    # todo check whether a read lock is necessary.

    __PD_SCK: int = 6
    __DOUT: int = 5
    __GAIN: int = 128

    def __init__(self, __calculation_method: str, __number_of_measurements: int):
        self.__calculation_method = __calculation_method
        self.__number_of_measurements = __number_of_measurements

        if __number_of_measurements % 2:
            # __number_of_calculations is odd
            __number_of_measurements_is_odd = True

        else:
            # __number_of_calculations is even
            __number_of_measurements_is_odd = False

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__PD_SCK, GPIO.OUT)
        GPIO.setup(self.__DOUT, GPIO.IN)

        time.sleep(1)
        # todo not sure if waiting 1 sec is necessary. Included this one because it was in the previous code.

        self.__offset = 0
        self.__get_value()
        # reading from the hx711 to set the GAIN value

        self.__determine_offset()

    ####################################################################################################################
    # Methods that can be called
    ####################################################################################################################

    def get_weight(self) -> int:
        __value: int = self.__get_value()
        __return_value = int(__value / self.__reference_unit)
        # todo check this: i don't know why we divide by a reference unit here.
        return int(round(__return_value * 1000))
        # multiply with 1000 to get the correct unit

    @staticmethod
    def close_hx711():
        GPIO.cleanup()

    ####################################################################################################################
    # Methods to approximate the weight
    ####################################################################################################################

    def __get_value(self) -> int:
        self.__new_reading_cycle()
        __scale_value: int = 0

        if self.__calculation_method == "median":
            __scale_value = self.__get_median_weight()
        elif self.__calculation_method == "average":
            __scale_value = self.__get_average_weight()

        return __scale_value

    # todo: think about if the first half of __get_median_weight and __get_average_weight should be its own method

    def __get_median_weight(self) -> int:
        __measuring_values: list[int] = []
        __current_number_of_measurements: int = 0

        while __current_number_of_measurements < self.__number_of_measurements:
            __current_number_of_measurements += 1
            __measured_value = self.__get_scale_values()
            __measuring_values.append(__measured_value - self.__offset)
            # deduct the scale offset from every __measured_value

        __measuring_values.sort()
        # we need sorted data to calculate the median value.

        if self.__number_of_measurements_is_odd:
            # check if the self.__number_of_calculations is odd.
            return __measuring_values[len(__measuring_values) // 2]
            # return the middle value of __values

        else:
            # self.__number_of_calculations is even
            __middle_of_values = len(__measuring_values) / 2
            return int(
                sum(__measuring_values[__middle_of_values : __middle_of_values + 2]) / 2
            )
            # because there is no middle value for an even number of values,
            # we return the average of the two values around the middle

    def __get_average_weight(self) -> int:
        __measuring_values: list[int] = []
        __current_number_of_measurements: int = 0

        while __current_number_of_measurements < self.__number_of_measurements:
            __current_number_of_measurements += 1
            __measured_value = self.__get_scale_values()
            __measuring_values.append(__measured_value - self.__offset)
            # deduct the scale offset from every __measured_value

        __measuring_values.sort()
        # we need sorted data to calculate the __trimmed_data.

        __trim_percentage: float = 0.1
        __trim_amount: int = int(len(__measuring_values) * __trim_percentage)
        __trimmed_data: list[int] = __measuring_values[__trim_amount: -__trim_amount]
        # we are trimming the edges of the data to remove potentially large outlier values.
        # the __trim_percentage is set arbitrarily.

        if len(__trimmed_data) == 0:
            return 0
        else:
            return int(sum(__trimmed_data) / len(__trimmed_data))

    ####################################################################################################################
    # Method to tare the scale
    ####################################################################################################################

    def __determine_offset(self):
        # this method uses a different self.__number_of_calculations value,
        # as the value defined during initialization might be to low to get a reliable offset result.
        # using a custom self.__number_of_calculations value is more of a preference than an actual requirement.

        __tmp = self.__number_of_measurements
        self.__number_of_measurements = 15
        # the value that self.__number_of_calculations is set to is arbitrary.

        self.__offset = self.__get_average_weight()

        self.__number_of_measurements = __tmp

    ####################################################################################################################
    # Methods to read data
    ####################################################################################################################

    def __get_scale_values(self) -> int:
        # one read cycle consists of reading 3 bytes and 1 bit (25 bits)

        self.__read_lock.acquire()

        while GPIO.input(self.__DOUT) != 0:
            # wait until the DOUT pin has finished the transmission of the last bit.
            # not sure if this is necessary, but it was part of the previous code.
            pass

        __msb_byte: int = self.__read_byte()
        __middle_byte: int = self.__read_byte()
        __lsb_byte: int = self.__read_byte()

        self.__read_next_bit()
        # we need to read one bit after every three bytes to set the GAIN value on the hx711.

        self.__read_lock.release()

        __return_value: int = self.__convert_to_signed_int(
            [__msb_byte, __middle_byte, __lsb_byte]
        )

        return __return_value

    def __read_byte(self):
        __byte_value: int = 0

        for __bit in range(8):
            __byte_value <<= 1
            __byte_value |= self.__read_next_bit()

        return __byte_value

    def __read_next_bit(self):
        # Clock HX711 Digital Serial Clock (PD_SCK).  DOUT will be
        # ready 1µs after PD_SCK rising edge, so we sample after
        # lowering PD_SCL, when we know DOUT will be stable.

        GPIO.output(self.__PD_SCK, True)
        GPIO.output(self.__PD_SCK, False)
        # activate and deactivate the __PD_SCK pin to generate a response from the hx711 on the __DOUT pin.

        __bit_value: bool = GPIO.input(self.__DOUT)
        # one bit response from the hx711 on the __DOUT pin

        return int(__bit_value)
        # return int converted from bool.

    @staticmethod
    def __convert_to_signed_int(__three_bytes: list[int]) -> int:
        # the hx711 sends a number that is encoded in two complement.
        # convert the number from two's complement to signed int value

        __two_complement_value: int = (
            (__three_bytes[0] << 16) | (__three_bytes[1] << 8) | __three_bytes[2]
        )

        __signed_int_value: int = -(__two_complement_value & 0x800000) + (
            __two_complement_value & 0x7FFFFF
        )

        return __signed_int_value

    ####################################################################################################################
    # Methods for hx711
    ####################################################################################################################

    def __new_reading_cycle(self):
        # each cycle in which we read from the hx711 is initiated by turning the hx711 on and off.

        self.__power_down()
        self.__power_up()

    def __power_down(self):
        self.__read_lock.acquire()

        GPIO.output(self.__PD_SCK, False)
        GPIO.output(self.__PD_SCK, True)
        # cause a rising edge on the HX711 Digital Serial Clock (PD_SCK).
        # we then leave it held up and wait for 100µs.
        # after 60µs the HX711 should be powered down.

        time.sleep(0.0001)

        self.__read_lock.release()

    def __power_up(self):
        self.__read_lock.acquire()

        GPIO.output(self.__PD_SCK, False)
        # Lower the HX711 Digital Serial Clock (PD_SCK) line.

        time.sleep(0.0001)
        # Wait 100 us for the HX711 to power back up.

        self.__read_lock.release()
