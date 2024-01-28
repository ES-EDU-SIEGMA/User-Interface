from libs.hardware.controller.dispenser_array_controller import PicoException
from libs.hardware.timing_calculator.calculator import Calculator
from libs.hardware.controller.idispenser_array_controller import (
    IDispenserArrayController,
)


class DispenserMechanism:
    __calculation: Calculator = None
    __controller: list[IDispenserArrayController] = None
    __expected_weight: int = -1

    def __init__(
        self, controller: list[IDispenserArrayController], timing_calculator: Calculator
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
