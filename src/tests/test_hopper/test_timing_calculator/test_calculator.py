from __future__ import annotations
import unittest

from libs.hardware.timing_calculator.calculator import Calculator


class TestCalculation(unittest.TestCase):
    __hopper_sizes: list[int | None] = [
        40,
        40,
        40,
        40,
        40,
        None,
        None,
        40,
        40,
        None,
        40,
        40,
    ]
    __ms_per_ml: int = 150
    __calculation: Calculator = None

    def setUp(self):
        self.__calculation = Calculator(
            ms_per_ml=self.__ms_per_ml, hopper_sizes=self.__hopper_sizes
        )

    def test_calculate_timing(self):
        data: dict = {
            "0": {"fill_amount": 100, "flow_speed": 1},
            "1": {"fill_amount": 40, "flow_speed": 10},
            "4": {"fill_amount": 39, "flow_speed": 2},
            "5": {"fill_amount": 0, "flow_speed": 1},
        }
        expected_result = (
            179,
            [
                [2, 6000],
                [1, 60000],
                [0, 0],
                [0, 0],
                [1, 12000],
                [0, 0],
                [0, 0],
                [0, 0],
                [0, 0],
                [0, 0],
                [0, 0],
                [0, 0],
            ],
        )
        received_result = self.__calculation.calculate_timing(data)
        self.assertEqual(expected_result, received_result)


if __name__ == "__main__":
    unittest.main()
