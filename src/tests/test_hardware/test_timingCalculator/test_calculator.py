from __future__ import annotations
import unittest

from libs.hardware.timingCalculator.calculator import Calculator
from libs.hardware.timingCalculator.calculator import IngredientNotAvailableException


class TestCalculation(unittest.TestCase):
    __hopper_sizes: list[int | None] = [
        40,
        40,
        40,
        40,
        None,
        None,
        None,
        40,
        None,
        None,
        None,
        None,
    ]
    __ms_per_ml: int = 150
    __calculation: Calculator = None

    def setUp(self):
        self.__calculation = Calculator(
            ms_per_ml=self.__ms_per_ml, hopper_sizes=self.__hopper_sizes
        )

    def test_raises_exception_if_hopper_not_available(self):
        data = [(0, 10, 1), (5, 90, 1)]

        self.assertRaises(
            IngredientNotAvailableException,
            self.__calculation.calculate_timing,
            ingredients=data,
            volume=250,
        )

    def test_raises_exception_if_hopper_not_associated(self):
        data = [(None, 10, 1), (7, 90, 1)]

        self.assertRaises(
            IngredientNotAvailableException,
            self.__calculation.calculate_timing,
            ingredients=data,
            volume=250,
        )

    def test_calculation_for_one_run_required(self):
        data = [(0, 50, 1), (7, 50, 1)]
        weight, timings = self.__calculation.calculate_timing(
            ingredients=data, volume=80
        )

        self.assertEqual(1, len(timings))
        self.assertListEqual(
            [
                [
                    [self.__ms_per_ml * self.__hopper_sizes[0], 0, 0, 0],
                    [0, 0, 0, self.__ms_per_ml * self.__hopper_sizes[7]],
                    [0, 0, 0, 0],
                ]
            ],
            timings,
        )
        self.assertEqual(self.__hopper_sizes[0] + self.__hopper_sizes[7], weight)

    def test_calculation_for_multiple_run_required(self):
        data = [(0, 50, 1), (7, 50, 1)]
        weight, timings = self.__calculation.calculate_timing(
            ingredients=data, volume=160
        )

        self.assertEqual(2, len(timings))
        self.assertListEqual(
            [
                [
                    [self.__ms_per_ml * self.__hopper_sizes[0], 0, 0, 0],
                    [0, 0, 0, self.__ms_per_ml * self.__hopper_sizes[7]],
                    [0, 0, 0, 0],
                ],
                [
                    [self.__ms_per_ml * self.__hopper_sizes[0], 0, 0, 0],
                    [0, 0, 0, self.__ms_per_ml * self.__hopper_sizes[7]],
                    [0, 0, 0, 0],
                ],
            ],
            timings,
        )
        self.assertEqual((self.__hopper_sizes[0] + self.__hopper_sizes[7]) * 2, weight)


if __name__ == "__main__":
    unittest.main()
