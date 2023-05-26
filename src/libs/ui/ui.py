import PyQt5.QtWidgets as PyQtWidgets
from .gui_console import ui_drink_selection as UiDrinkSelection
from .gui_console import ui_edit_hoppers as UiEditHoppers
from .gui_console import ui_new_recipe as UiNewRecipe
"""from .gui_windows import ui_drink_selection as UiDrinkSelection
from .gui_windows import ui_edit_hoppers as UiEditHoppers
from .gui_windows import ui_new_recipe as UiNewRecipe"""
from . import controller_mock as Controller
from ..drink_data import data_interface as Data
import sys


# todo change gui to ui in the code

class Ui:
    """ the class Ui creates view objects and activates each view with the command activate()"""
    __ui_drink_selection: UiDrinkSelection.Selection
    __ui_edit_hoppers: UiEditHoppers.EditHopper
    __ui_new_recipe: UiNewRecipe.NewRecipe
    __ui_current: (
            UiDrinkSelection.Selection |
            UiEditHoppers.EditHopper |
            UiNewRecipe.NewRecipe)
    __ui_running: bool
    __ui_menu_string: str
    __ui_menu_string_list: list[str]
    __data: Data.DataInterface

    def __init__(self, __ui_type: "str"):
        # todo add __parent to class __init__ call and create console __parent mock
        if __ui_type == "gui_console":
            self.__ui_drink_selection = UiDrinkSelection.Selection()
            self.__ui_edit_hoppers = UiEditHoppers.EditHopper()
            self.__ui_new_recipe = UiNewRecipe.NewRecipe()
            self.__data = Data.DataInterface()
            self.__ui_running = True
            self.__ui_loop_console()

        """elif __ui_type == "gui_windows":
            __app = PyQtWidgets.QApplication(sys.argv)
            self.__ui_drink_selection = UiDrinkSelection.ui_drink_selection.Selection(__app)
            self.__ui_edit_hoppers = UiEditHoppers.ui_edit_hoppers.EditHoppers(__app)
            self.__ui_new_recipe = UiNewRecipe.ui_new_recipe.NewRecipe(__app)
            sys.exit(__app.exec())"""

    def __call_gui_selection(self) -> str:
        """ calls the ui-view that represents the selection process"""
        __data_drink_names: list[str] = self.__get_data_dispensable_drink_names()
        self.__ui_current.deactivate()
        self.__ui_current = self.__ui_drink_selection
        return self.__ui_drink_selection.activate(__data_drink_names)

    def __call_gui_edit_hoppers(self) -> str:
        """ calls the ui-view that represents the edit hopper process"""
        __data_hopper_names: list[str] = self.__get_data_beverage_on_hopper_names()
        __data_beverage_names: list[str] = self.__get_data_beverage_names()
        self.__ui_current.deactivate()
        self.__ui_current = self.__ui_edit_hoppers
        return self.__ui_edit_hoppers.activate(__data_hopper_names, __data_beverage_names)

    def __call_gui_new_recipe(self) -> str:
        """ calls the ui-view that represents the new recipe process"""
        __data_beverage_names: list[str] = self.__get_data_beverage_names()
        __data_recipe_names: list[str] = self.__get_data_recipe_names()
        self.__ui_current.deactivate()
        self.__ui_current = self.__ui_new_recipe
        return self.__ui_new_recipe.activate(__data_beverage_names, __data_recipe_names)

    def __reactivate(self) -> str:
        """ this method is used to come back to a previous view after executing a command"""
        match self.__ui_current:
            case self.__ui_drink_selection:
                return self.__call_gui_selection()
            case self.__ui_edit_hoppers:
                return self.__call_gui_edit_hoppers()
            case self.__ui_new_recipe:
                return self.__call_gui_new_recipe()

    def call_back_pyqt(self, __ui_menu_string):
        """ this case distinction manages the pyqt window flow.
            pyqt works with string distinctions like the console, but it doesn't receive them as
            a function return value but rather through a function callback"""
        self.__ui_menu_string = __ui_menu_string
        self.__ui_menu_string_list = self.__ui_menu_string.split(";")
        match self.__ui_menu_string_list[0]:
            case "change_window":
                match self.__ui_menu_string_list[1]:
                    case "select":
                        self.__call_gui_selection()
                    case "edit":
                        self.__call_gui_edit_hoppers()
                    case "new":
                        self.__call_gui_new_recipe()
            case "command":
                self.__execute_command()
                self.__ui_menu_string: str = self.__reactivate()
            case "exit":
                sys.exit(print("Program ended"))

    def __ui_loop_console(self):
        """ main loop that switches between the different ui-views for the console version and executes commands.
            Distinctions are made depending upon the string return value it receives from method calls"""
        __data_drink_names: list[str] = self.__get_data_dispensable_drink_names()
        self.__ui_menu_string = f"{self.__ui_drink_selection.activate(__data_drink_names)};pseudo_string"
        self.__ui_current = self.__ui_drink_selection

        while self.__ui_running:
            self.__ui_menu_string_list = self.__ui_menu_string.split(";")

            match self.__ui_menu_string_list[0]:
                case "change_window":
                    match self.__ui_menu_string_list[1]:
                        case "select":
                            self.__ui_menu_string: str = self.__call_gui_selection()
                        case "edit":
                            self.__ui_menu_string: str = self.__call_gui_edit_hoppers()
                        case "new":
                            self.__ui_menu_string: str = self.__call_gui_new_recipe()
                case "command":
                    self.__execute_command()
                    self.__ui_menu_string: str = self.__reactivate()
                case "exit":
                    sys.exit(print("Program ended"))

    def __execute_command(self):
        """ selects the cmd that the ui-view wishes to execute"""
        self.__ui_menu_string_list = self.__ui_menu_string.split(";")
        match self.__ui_menu_string_list[1]:
            case "selection":
                self.__select_drink_command()
            case "edit":
                self.__edit_hopper_command()
            case "new":
                self.__create_recipe_command()

    def __select_drink_command(self):
        """ calls a cmd to dispense a drink"""
        __drink_name: str = self.__ui_menu_string_list[2]
        Controller.select_drink(__drink_name)

    def __edit_hopper_command(self):
        """ calls a cmd to edit the hopper"""
        __hopper = int(self.__ui_menu_string_list[2])  # hopper
        __drink_on_hopper_name: str = self.__ui_menu_string_list[3]  # beverage
        Controller.edit_hopper(__hopper, __drink_on_hopper_name)

    def __create_recipe_command(self):
        """ calls a cmd to create a new recipe"""
        __new_recipe_name: str = self.__ui_menu_string_list[2]
        __selected_drinks_and_fill_amounts: list[str] = self.__ui_menu_string_list[3:]
        Controller.create_recipe(__new_recipe_name, __selected_drinks_and_fill_amounts)

    def __get_data_dispensable_drink_names(self) -> list[str]:
        __result: list[str]
        __result = self.__data.get_dispensable_beverage_names()
        __result + self.__data.get_dispensable_recipe_names()
        return __result

    def __get_data_beverage_on_hopper_names(self) -> list[str]:
        __result: list[str]
        __result = self.__data.get_beverage_hopper_names()
        return __result

    def __get_data_beverage_names(self) -> list[str]:
        __result: list[str]
        __result = self.__data.get_beverage_names()
        return __result

    def __get_data_recipe_names(self) -> list[str]:
        __result: list[str]
        __result = self.__data.get_recipe_names()
        return __result
