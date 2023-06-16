from .cli_ui import ui_drink_selection as Ui_selection_module
from .cli_ui import ui_edit_hoppers as Ui_edit_module
from .cli_ui import ui_new_recipe as Ui_new_module
from .cli_ui import ui_drink_progress as Ui_progress_module


class UserInterface:
    __ui_view_selection: Ui_selection_module.Selection
    __ui_view_edit_hopper: Ui_edit_module.EditHopper
    __ui_view_new_recipe: Ui_new_module.NewRecipe
    __ui_view_progress: Ui_progress_module.Progress

    def __init__(self, __configure_ui_type: str):

        self.__ui_view_selection = Ui_selection_module.Selection()
        self.__ui_view_edit_hopper = Ui_edit_module.EditHopper()
        self.__ui_view_new_recipe = Ui_new_module.NewRecipe()
        self.__ui_view_progress = Ui_progress_module.Progress()

    def select_view(self, __program_state: str, __data: list[str] | list[list[str]] | int) -> dict:

        if __program_state == "selection":
            return self.__ui_view_selection.activate(__data)

        elif __program_state == "edit":
            return self.__ui_view_edit_hopper.activate(__data)

        elif __program_state == "new":
            return self.__ui_view_new_recipe.activate(__data)

        elif __program_state == "progress":
            return self.__ui_view_progress.activate(__data)
