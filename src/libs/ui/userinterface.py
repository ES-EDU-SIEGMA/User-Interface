from .gui_console import ui_drink_selection as Ui_selection_module
from .gui_console import ui_edit_hoppers as Ui_edit_module
from .gui_console import ui_new_recipe as Ui_new_module
from ..drink_data import data_interface as Data_module


class UserInterface:
    """ the class UserInterface creates view objects and activates each view with the method activate()"""
    __ui_view_selection: Ui_selection_module.Selection
    __ui_view_edit_hopper: Ui_edit_module.EditHopper
    __ui_view_new_recipe: Ui_new_module.NewRecipe
    __data_object: Data_module.DataInterface

    def __init__(self,
                 __ui_console: bool,
                 __data_object: Data_module.DataInterface):

        self.__data_object = __data_object

        if __ui_console:
            self.__ui_view_selection = Ui_selection_module.Selection()
            self.__ui_view_edit_hopper = Ui_edit_module.EditHopper()
            self.__ui_view_new_recipe = Ui_new_module.NewRecipe()

    def select_view(self, __program_state: str) -> list[str]:
        __data: list[str] | list[list[str]] = self.__data_object.get_data_ui(__program_state)
        # __data might need multiple types depending on the different view implementations
        match __program_state:
            case "selection":
                return self.__ui_view_selection.activate(__data)
            case "edit":
                return self.__ui_view_edit_hopper.activate(__data)
            case "new":
                return self.__ui_view_new_recipe.activate(__data)
