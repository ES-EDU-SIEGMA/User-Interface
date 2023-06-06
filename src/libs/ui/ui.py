from .gui_console import ui_drink_selection as UiDrinkSelection
from .gui_console import ui_edit_hoppers as UiEditHoppers
from .gui_console import ui_new_recipe as UiNewRecipe
from . import controller_mock as Controller
from ..drink_data import new_data_interface as Data
import sys


class Ui:
    """ the class Ui creates view objects and activates each view with the command activate()"""
    __ui_view_drink_selection: UiDrinkSelection.Selection
    __ui_view_edit_hoppers: UiEditHoppers.EditHopper
    __ui_view_new_recipe: UiNewRecipe.NewRecipe
    __ui_view_current: (
            UiDrinkSelection.Selection |
            UiEditHoppers.EditHopper |
            UiNewRecipe.NewRecipe)

    __ui_menu_string: str
    __ui_menu_string_list: list[str]

    __data: Data.DataInterface

    def __init__(self, __ui_type: "str", __data_interface: Data.DataInterface):
        if __ui_type == "gui_console":
            self.__ui_view_drink_selection = UiDrinkSelection.Selection()
            self.__ui_view_edit_hoppers = UiEditHoppers.EditHopper()
            self.__ui_view_new_recipe = UiNewRecipe.NewRecipe()
            self.__data = __data_interface
            self.__ui_loop_console()

    def __call_gui_selection(self) -> str:
        """ calls the selection ui-view"""
        __data_drink_names: list[str] = self.__data.get_recipe_dispensable_names()
        self.__ui_view_current.deactivate()
        self.__ui_view_current = self.__ui_view_drink_selection
        return self.__ui_view_drink_selection.activate(__data_drink_names)

    def __call_gui_edit_hopper(self) -> str:
        """ calls the edit hopper ui-view"""
        __hopper_names: list[str] = self.__data.get_ingredient_on_hopper_names()
        __ingredient_names: list[str] = self.__data.get_ingredient_names()
        self.__ui_view_current.deactivate()
        self.__ui_view_current = self.__ui_view_edit_hoppers
        return self.__ui_view_edit_hoppers.activate(__hopper_names, __ingredient_names)

    def __call_gui_new_recipe(self) -> str:
        """ calls the new recipe ui-view"""
        __ingredient_names: list[str] = self.__data.get_ingredient_names()
        __recipe_names: list[str] = self.__data.get_recipe_names()
        self.__ui_view_current.deactivate()
        self.__ui_view_current = self.__ui_view_new_recipe
        return self.__ui_view_new_recipe.activate(__ingredient_names, __recipe_names)

    def __ui_loop_console(self):
        """ Main loop that switches between the different ui-views for the console version and executes commands.
            Distinctions are made depending upon the string return value it receives from method calls."""
        # the following three lines are used to set up the loop for the first iteration
        __recipe_names: list[str] = self.__data.get_recipe_dispensable_names()
        self.__ui_menu_string = f"{self.__ui_view_drink_selection.activate(__recipe_names)}"
        self.__ui_view_current = self.__ui_view_drink_selection

        while True:
            self.__ui_menu_string_list = self.__ui_menu_string.split(";")

            match self.__ui_menu_string_list.pop(0):
                case "change_window":
                    match self.__ui_menu_string_list.pop(0):
                        case "select":
                            self.__ui_menu_string: str = self.__call_gui_selection()
                        case "edit":
                            self.__ui_menu_string: str = self.__call_gui_edit_hopper()
                        case "new":
                            self.__ui_menu_string: str = self.__call_gui_new_recipe()
                case "command":
                    self.__execute_command()
                    self.__ui_menu_string: str = self.__activate()
                case "exit":
                    sys.exit(print("Program ended"))

    def __execute_command(self):
        """ selects the cmd that the ui-view wishes to execute"""
        match self.__ui_menu_string_list.pop(0):
            case "select":
                Controller.select_drink(self.__ui_menu_string_list)
            case "edit":
                self.__data.set_hopper(self.__ui_menu_string_list[0], self.__ui_menu_string_list[1])
            case "new":
                self.__data.create_recipe(self.__ui_menu_string_list)

    # todo change inputs for execute commands to fit to data or do that in the data_interface

    def __activate(self) -> str:
        """ This method is used to come back to the previous view after finishing a command"""
        match self.__ui_view_current:
            case self.__ui_view_drink_selection:
                return self.__call_gui_selection()
            case self.__ui_view_edit_hoppers:
                return self.__call_gui_edit_hopper()
            case self.__ui_view_new_recipe:
                return self.__call_gui_new_recipe()
