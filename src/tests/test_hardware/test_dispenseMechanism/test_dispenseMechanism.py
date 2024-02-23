from __future__ import annotations

import unittest
from unittest.mock import MagicMock, Mock

from libs.hardware.dispenseMechanism.dispenseMechanism import DispenseMechanism
from libs.hardware.dispenserGroupController.iDispenserGroupController import (
    IDispenserGroupController,
)
from libs.hardware.timingCalculator.calculator import Calculator


class TestDispenseMechanism(unittest.TestCase):
    __calculation: Calculator = None
    __controller: list[IDispenserGroupController] = None
    __dispenseMechanism: DispenseMechanism = None

    def setUp(self):
        self.__calculation = MagicMock()

        self.__controller = []
        for index in range(1, 3):
            self.__controller.append(MagicMock())

        self.__dispenseMechanism = DispenseMechanism(
            controller=self.__controller, timing_calculator=self.__calculation
        )

    def test_controller_is_initialized(self):
        self.assertTrue(self.__dispenseMechanism)

    def test_get_expected_weight_after_initialization(self):
        self.assertEqual(-1, self.__dispenseMechanism.get_expected_weight())

    def test_get_expected_weight_after_calculations(self):
        expected_sum: int = 150
        self.__calculation.calculate_timing = Mock(
            return_value=(expected_sum, [[[], [], []]])
        )
        self.__dispenseMechanism.dispense_drink([])
        self.assertEqual(expected_sum, self.__dispenseMechanism.get_expected_weight())


if __name__ == "__main__":
    unittest.main()
