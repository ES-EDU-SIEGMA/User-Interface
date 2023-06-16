from __future__ import annotations

from src.libs.hopper.timing_calculation import timing_calculation as calculation_module
import unittest


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
    __calculation_object = calculation_module.Calculation(__ms_per_ml, __hopper_sizes)

    def test_calculate_timing(self):
        __data: dict = {
            "0": {"fill_amount": 100, "flow_speed": 1},
            "1": {"fill_amount": 40, "flow_speed": 10},
            "4": {"fill_amount": 39, "flow_speed": 2},
            "5": {"fill_amount": 0, "flow_speed": 1},
        }
        __expected_result = {
            "expected_weight": 179,
            "timings": [
                [2, 6000],
                [1, 60000],
                [],
                [],
                [1, 12000],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
            ],
        }
        __received_result = self.__calculation_object.calculate_timing(__data)
        self.assertEqual(__expected_result, __received_result)


if __name__ == "__main__":
    unittest.main()
