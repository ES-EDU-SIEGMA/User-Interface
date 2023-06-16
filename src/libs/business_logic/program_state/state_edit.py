from src.libs.ui import userinterface as ui_module
from src.libs.data import data_interface as data_module


class StateEdit:
    __ui_object: ui_module.UserInterface
    __data_object: data_module.DataInterface

    __PROGRAM_STATE: str = "edit"

    def __init__(
        self,
        __ui_object: ui_module.UserInterface,
        __data_object: data_module.DataInterface,
    ):
        self.__ui_object = __ui_object
        self.__data_object = __data_object

    def call_ui(self) -> dict:
        __data = self.__data_object.get_data_ui(self.__PROGRAM_STATE)
        return self.__ui_object.select_view(self.__PROGRAM_STATE, __data)

    def execute_command(self, __data: dict):
        self.__data_object.set_hopper(__data)
