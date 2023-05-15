"""
simulates HX711
"""


class HX711():

    def __init__(self, dout, pd_sck, gain=128):
        self.dout = dout
        self.pd_sck = pd_sck
        self.gain = gain
        self.offset = 1
        self.offset_b = 1
        self.reference_unit = 1
        self.reference_unit_b = 1

    @staticmethod
    def is_ready(self):
        return True

    def set_gain(self, gain):
        if gain == 128:
            self.gain = 1
        elif gain == 64:
            self.gain = 3
        elif gain == 32:
            self.gain = 2

    def get_gain(self):
        if self.gain == 1:
            return 128
        if self.gain == 3:
            return 64
        if self.gain == 2:
            return 32

    @staticmethod
    def read_long(self) -> int:
        return 0

    @staticmethod
    def read_average(self, times=3) -> int:
        return 0

    @staticmethod
    def read_median(times=3) -> int:
        return 0

    @staticmethod
    def get_value(times=3) -> int:
        return 0

    @staticmethod
    def get_value_a(self, times=3) -> int:
        return 0

    @staticmethod
    def get_value_b(self, times=3) -> int:
        return 0

    @staticmethod
    def get_weight(self, times=3) -> int:
        return 0

    @staticmethod
    def get_weight_a(self, times=3) -> int:
        return 0

    @staticmethod
    def get_weight_b(self, times=3) -> int:
        return 0

    @staticmethod
    def tare(self, times=15) -> int:
        return 0

    @staticmethod
    def tare_a(self, times=15) -> int:
        return 0

    @staticmethod
    def tare_b(self, times=15) -> int:
        return 0

    def set_reading_format(self, byte_format="LSB", bit_format="MSB"):
        pass

    def set_offset(self, offset):
        self.offset = offset

    def set_offset_a(self, offset):
        self.offset = offset

    def set_offset_b(self, offset):
        self.offset = offset

    def get_offset(self):
        return self.offset

    def get_offset_a(self):
        return self.offset

    def get_offset_b(self):
        return self.offset_b

    def set_reference_unit(self, reference_unit: int):
        self.reference_unit = reference_unit

    def set_reference_unit_b(self, reference_unit: int):
        self.reference_unit_b = reference_unit

    def get_reference_unit(self) -> int:
        return self.reference_unit

    def get_reference_unit_a(self) -> int:
        return self.reference_unit

    def get_reference_unit_b(self) -> int:
        return self.reference_unit_b

    def power_down(self):
        pass

    def power_up(self):
        pass

    def reset(self):
        pass
