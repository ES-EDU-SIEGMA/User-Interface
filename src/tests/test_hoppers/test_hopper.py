from libs.hopper import hopper as Hopper_module
import unittest


class TestHopper(unittest.TestCase):
    __mock_communication: bool = True
    __ms_per_ml: int = 150
    __hopper_sizes: list[int | None] = [40, 40, 40, 40,
                                        40, None, None, 40,
                                        40, None, 40, 40]
    __pico_identifier: list[str] = []
    __serial_connections: list[str] = []
    __max_serial_identifier_attempt: int = 0

    __hopper_object = Hopper_module.Hopper(__mock_communication,
                                           __ms_per_ml,
                                           __hopper_sizes,
                                           __pico_identifier,
                                           __serial_connections,
                                           __max_serial_identifier_attempt)

    def test_get_expected_weight_after_initialization(self):
        __expected_result: int = 0
        __received_result: int = self.__hopper_object.get_expected_weight()
        self.assertEqual(__expected_result, __received_result)

    def test_get_expected_weight_after_weight_calculations(self):
        __data: dict = {
            "0": {"fill_amount": 100, "flow_speed": 1},
            "1": {"fill_amount": 40, "flow_speed": 10},
            "4": {"fill_amount": 39, "flow_speed": 2},
            "5": {"fill_amount": 0, "flow_speed": 1}
        }
        self.__hopper_object.dispense_drink(__data)

        __expected_result: int = 100+40+39+0
        __received_result: int = self.__hopper_object.get_expected_weight()

        self.assertEqual(__expected_result, __received_result)


if __name__ == '__main__':
    unittest.main()
