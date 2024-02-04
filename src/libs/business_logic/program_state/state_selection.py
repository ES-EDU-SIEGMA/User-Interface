from libs.ui import userinterface as ui_module
from libs.data import data_interface as data_module
from libs.hardware import hopper as hopper_module


class StateSelection:
    __ui_object: ui_module.UserInterface
    __data_object: data_module.DataInterface
    __hopper_object: hopper_module.DispenseMechanism

    __PROGRAM_STATE: str = "selection"

    def __init__(
        self,
        __ui_object: ui_module.UserInterface,
        __data_object: data_module.DataInterface,
        __hopper_object: hopper_module.DispenseMechanism,
    ):
        self.__ui_object = __ui_object
        self.__data_object = __data_object
        self.__hopper_object = __hopper_object

    def call_ui(self) -> dict:
        __data = self.__data_object.get_data_ui(self.__PROGRAM_STATE)
        return self.__ui_object.select_view(self.__PROGRAM_STATE, __data)

    def execute_command(self, __recipe_name: str):
        __data: dict = self.__data_object.get_data_dispense(__recipe_name)
        self.__hopper_object.dispense_drink(__data)
