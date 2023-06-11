from libs.ui import userinterface as UI_module
from libs.data import data_interface as Data_module


class StateNew:
    __ui_object: UI_module.UserInterface
    __data_object: Data_module.DataInterface

    __PROGRAM_STATE: str = "new"

    def __init__(self,
                 __ui_object: UI_module.UserInterface,
                 __data_object: Data_module.DataInterface):

        self.__ui_object = __ui_object
        self.__data_object = __data_object

    def call_ui(self) -> dict:
        __data = self.__data_object.get_data_ui(self.__PROGRAM_STATE)
        return self.__ui_object.select_view(self.__PROGRAM_STATE, __data)

    def execute_command(self, __data: dict):
        self.__data_object.create_recipe(__data)
