import time

from libs.ui import userinterface as ui_module
from libs.hardware import hopper as hopper_module
from libs.scale.scale import Scale


class StateProgress:
    __ui_object = ui_module.UserInterface
    __hopper_object = hopper_module.DispenserMechanism
    __scale_object = Scale

    __max_waiting_time: int
    __time_waited: int

    __expected_weight: int
    __TOLERANCE_WEIGHT_MULTIPLIER: float = 0.95  # chosen arbitrarily
    __progress_percentage: int

    __PROGRAM_STATE: str = "progress"

    def __init__(
        self,
        ui_object: ui_module.UserInterface,
        hopper_object: hopper_module.DispenserMechanism,
        scale_object: Scale,
        max_waiting_time: int,
    ):
        self.__ui_object = ui_object
        self.__hopper_object = hopper_object
        self.__scale_object = scale_object
        self.__max_waiting_time = max_waiting_time + 1
        self.__time_waited = 0
        self.__expected_weight = 0
        self.__progress_percentage = 0

    def call_ui(self) -> dict:
        self.__time_waited = self.__time_waited % self.__max_waiting_time
        self.__time_waited += 1
        if self.__time_waited < self.__max_waiting_time:
            time.sleep(1)
            return self.__ui_object.select_view(
                self.__PROGRAM_STATE, self.__progress_percentage
            )
        else:
            # waited to long for the drink to finish. aborting progress display
            return self.__ui_object.select_view(self.__PROGRAM_STATE, -1)

    def execute_command(self, recipe_name: str):
        if self.__expected_weight == 0:
            self.__expected_weight = int(
                self.__hopper_object.get_expected_weight()
                * self.__TOLERANCE_WEIGHT_MULTIPLIER
            )

        current_weight: int = self.__scale_object.get_weight()
        self.__progress_percentage: int = int(
            (current_weight / self.__expected_weight) * 100
        )

        if self.__progress_percentage >= 100:
            self.__expected_weight = 0
