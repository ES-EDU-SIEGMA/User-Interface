from libs.ui import ui as UserInterface
from libs.drink_data import new_data_interface as Data
import json

if __name__ == "__main__":

    __standard_input_hopper_positions: dict
    __data_object: Data.DataInterface
    try:
        with open("libs/drink_data/standard_input_initialization", "r") as __json_ingredients:
            __standard_input_hopper_positions = json.load(__json_ingredients)
    except Exception as e:
        print(e)
        __standard_input_hopper_positions = {}
    __data_object = Data.DataInterface(__standard_input_hopper_positions)
    UserInterface.Ui("gui_console", __data_object)

    print("end_call")
