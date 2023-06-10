from libs.ui import userinterface as UI_module
from libs.data import data_interface as Data_module


class StateNew:
    __ui_object: UI_module.UserInterface
    __data_object: Data_module.DataInterface

    __program_state: str = "new"

    def __init__(self, __ui_object, __data_object):
        self.__ui_object = __ui_object
        self.__data_object = __data_object

    def call_ui(self) -> dict:
        __data = self.__data_object.get_data_ui(self.__program_state)
        return self.__ui_object.select_view(self.__program_state, __data)

    def execute_command(self, __cmd: dict):
        self.__data_object.create_recipe(__cmd["cmd_create_recipe"])
