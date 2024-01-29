from __future__ import annotations
import unittest
from unittest.mock import MagicMock, Mock

from libs.hardware.dispenserMechanism import DispenserMechanism
from libs.hardware.timing_calculator.calculator import Calculator
from libs.hardware.controller.idispenser_array_controller import (
    IDispenserArrayController,
)


class TestHopper(unittest.TestCase):
    __calculation: Calculator = None
    __controller: list[IDispenserArrayController] = None
    __hopper: DispenserMechanism = None

    def setUp(self):
        self.__calculation = MagicMock()

        self.__controller = []
        for index in range(1, 3):
            self.__controller.append(MagicMock())

        self.__hopper = DispenserMechanism(
            controller=self.__controller, timing_calculator=self.__calculation
        )

    def test_controller_is_initialized(self):
        self.assertTrue(self.__hopper)

    def test_get_expected_weight_after_initialization(self):
        self.assertEqual(-1, self.__hopper.get_expected_weight())

    def test_get_expected_weight_after_calculations(self):
        expected_sum: int = 150
        self.__calculation.calculate_timing = Mock(
            return_value=(expected_sum, [[], [], []])
        )
        self.__hopper.dispense_drink({})
        self.assertEqual(expected_sum, self.__hopper.get_expected_weight())


if __name__ == "__main__":
    unittest.main()
