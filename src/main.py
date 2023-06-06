from libs.ui import ui as UserInterface
from libs.drink_data import new_data_interface as Data

__beverage_fill_amount: dict
# __ingredient_fill_amount:= {<beverage-name>: list[<flow-speed>, <bottle-current-amount>]}
__hopper_beverage_name_list: list[str]
# __ingredients_on_hopper:= list[<beverage-name>]

__beverage_fill_amount = {}

if __name__ == "__main__":
    UserInterface.Ui("gui_console", Data.DataInterface())
