from libs.ui import userinterface as User_interface_module
from libs.drink_data import data_interface as Data_module
from libs.business_logic import business_logic as Business_logic_module
import json


class Main:
    __business_logic: Business_logic_module.BusinessLogic
    __data_object: Data_module.DataInterface
    __ui_object: User_interface_module.UserInterface

    __configuration_dict = {
        "mock_communication": True,
        "mock_scale": True,
        "ui_console": True
    }

    def __init__(self):
        __hopper_configuration = self.__get_hopper_configuration()
        __hopper_sizes = self.__get_hopper_sizes()
        print("hello")

        self.__business_logic = Business_logic_module.BusinessLogic(
            self.__configuration_dict,
            __hopper_configuration,
            __hopper_sizes)

    @staticmethod
    def __get_hopper_configuration() -> dict:
        try:
            with open(file="libs/drink_data/standard_input_initialization", mode="r") as __json_file:
                return json.load(__json_file)
        except Exception as error:
            print(error)
            return {}

    @staticmethod
    def __get_hopper_sizes() -> list[int]:
        pass


if __name__ == "__main__":
    Main()
