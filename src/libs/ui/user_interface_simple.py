from .cli_ui import ui_drink_selection as Ui_selection_module
from .cli_ui import ui_drink_progress as Ui_progress_module


class UserInterface:
    __ui_view_selection: Ui_selection_module.Selection
    __ui_view_progress: Ui_progress_module.Progress

    def __init__(self, __configure_ui_type: str):

        match __configure_ui_type:
            case "ui_console":
                self.__ui_view_selection = Ui_selection_module.Selection()
                self.__ui_view_progress = Ui_progress_module.Progress()

    def select_view(self, __program_state: str, __data: list[str] | list[list[str]] | int) -> dict:

        match __program_state:
            case "selection":
                return self.__ui_view_selection.activate(__data)
            case "progress":
                return self.__ui_view_progress.activate(__data)
