from libs.ui import userinterface as UI_module
from libs.drink_data import data_interface as Data_module
from libs.hopper import hopper as Hopper_module
from libs.scale import scale_interface as Scale_module


class StateSelection:
    __ui_object: UI_module.UserInterface
    __data_object: Data_module.DataInterface
    __hopper_object: Hopper_module.Hopper
    __scale_object: Scale_module.Scale

    __program_state: str = "selection"

    def __init__(self, __ui_object, __data_object, __hopper_object, __scale_object):
        self.__ui_object = __ui_object
        self.__data_object = __data_object
        self.__hopper_object = __hopper_object
        self.__scale_object = __scale_object

    def call_ui(self) -> dict:
        __data = self.__data_object.get_data_ui(self.__program_state)
        return self.__ui_object.select_view(self.__program_state, __data)

    def execute_command(self, __cmd: dict):
        self.__hopper_object.dispense_drink(__cmd)
