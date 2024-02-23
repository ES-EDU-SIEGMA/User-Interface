from __future__ import annotations

from libs.hardware.dispenserGroupController.dispenserGroupController import (
    PicoException,
)
from libs.hardware.dispenserGroupController.iDispenserGroupController import (
    IDispenserGroupController,
)
from libs.hardware.timingCalculator.calculator import (
    IngredientNotAvailableException,
    Calculator,
)


class DispenseMechanism:
    __calculator: Calculator = None
    __controller: list[IDispenserGroupController] = None
    __expected_weight: int = -1

    def __init__(
        self,
        controller: list[IDispenserGroupController],
        timing_calculator: Calculator,
    ):
        """
        :param controller: list of controller to use
        :param timing_calculator: instance of TimingCalculator to compute timings
        """
        self.__controller = controller
        self.__calculator = timing_calculator

    def dispense_drink(
        self, ingredients_to_dispense: list[(int, int, int)], volume: int = 250
    ) -> None:
        """
        :param ingredients_to_dispense: list of Ingredients in format:
                                        triple (<hopper_for_ingredient>,
                                                <percentage_of_ingredient>,
                                                <flow_speed_of_ingredient>)
        :param volume: the total amount of the drink in millilitre
                       (default: 250ml)
        """
        try:
            self.__expected_weight, timings = self.__calculator.calculate_timing(
                ingredients=ingredients_to_dispense, volume=volume
            )
            for dispense_cycle in timings:
                for index in range(1, len(self.__controller)):
                    # FIXME: Optimization -> Parallelize send and then wait for ready to send new timings
                    self.__controller[index].send_timings(dispense_cycle[index])
                    self.__controller[index].wait_for_ready_signal()
        except PicoException as e:
            # TODO: add proper logging!
            print(e)
        except IngredientNotAvailableException as e:
            # TODO: add proper logging!
            print(e)

    def get_expected_weight(self) -> int:
        return self.__expected_weight
