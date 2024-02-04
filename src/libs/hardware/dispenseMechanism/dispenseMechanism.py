from libs.hardware.dispenserGroupController.dispenserGroupController import (
    PicoException,
)
from libs.hardware.timingCalculator.calculator import Calculator
from libs.hardware.dispenserGroupController.iDispenserGroupController import (
    IDispenserGroupController,
)


class DispenseMechanism:
    __calculation: Calculator = None
    __controller: list[IDispenserGroupController] = None
    __expected_weight: int = -1

    def __init__(
        self, controller: list[IDispenserGroupController], timing_calculator: Calculator
    ):
        self.__controller = controller
        self.__calculation = timing_calculator

    def dispense_drink(self, __data: dict):
        self.__expected_weight, timings = self.__calculation.calculate_timing(__data)
        try:
            for index in range(1, len(self.__controller)):
                self.__controller[index].send_timings(timings[index])
        except PicoException as pe:
            # TODO: add proper logging!
            print(pe)

    def get_expected_weight(self) -> int:
        return self.__expected_weight
