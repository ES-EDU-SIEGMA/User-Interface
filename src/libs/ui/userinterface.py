from .gui_console import ui_drink_selection as UiDrinkSelection
from .gui_console import ui_edit_hoppers as UiEditHoppers
from .gui_console import ui_new_recipe as UiNewRecipe
from ..drink_data import new_data_interface as Data_module


class UserInterface:
    """ the class UserInterface creates view objects and activates each view with the method activate()"""
    __ui_view_selection: UiDrinkSelection.Selection
    __ui_view_edit_hopper: UiEditHoppers.EditHopper
    __ui_view_new_recipe: UiNewRecipe.NewRecipe
    __data_object: Data_module.DataInterface

    def __init__(self,
                 __ui_type: "str",
                 __data_object: Data_module.DataInterface):

        self.__data_object = __data_object

        if __ui_type == "gui_console":
            self.__ui_view_selection = UiDrinkSelection.Selection()
            self.__ui_view_edit_hopper = UiEditHoppers.EditHopper()
            self.__ui_view_new_recipe = UiNewRecipe.NewRecipe()

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
