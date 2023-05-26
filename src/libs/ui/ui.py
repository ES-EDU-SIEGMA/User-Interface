import gui_console as GuiComponent
import controller as Controller


# todo change gui to ui in the code

class Ui:
    """ the class Ui creates view objects and activates each view with the command activate()"""
    __ui_drink_selection: GuiComponent.ui_drink_selection = None
    __ui_edit_hoppers: GuiComponent.ui_edit_hoppers = None
    __ui_new_recipe: GuiComponent.ui_new_recipe = None
    __ui_current: (GuiComponent.ui_drink_selection |
                   GuiComponent.ui_edit_hoppers |
                   GuiComponent.ui_new_recipe) = None
    __ui_running: bool = None
    __ui_menu_string: (str | list[str]) = None

    def __init__(self):
        # todo add __parent to class __init__ call and create console __parent mock
        self.__ui_drink_selection = GuiComponent.ui_drink_selection.Selection()
        self.__ui_edit_hoppers = GuiComponent.ui_edit_hoppers.EditHoppers()
        self.__ui_new_recipe = GuiComponent.ui_new_recipe.NewRecipe()

        self.__ui_loop()

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

    def __ui_loop(self):
        """ main loop that switches between the different ui-views"""
        __data_drink_names: list[str] = self.__get_data_dispensable_drink_names()
        self.__ui_menu_string = self.__ui_drink_selection.activate(__data_drink_names)

        while self.__ui_running:
            self.__ui_menu_string = self.__ui_menu_string.split(";")

            match self.__ui_menu_string[0]:
                case "selection":
                    self.__ui_menu_string = self.__call_gui_selection()
                case "edit":
                    self.__ui_menu_string = self.__call_gui_edit_hoppers()
                case "new":
                    self.__ui_menu_string = self.__call_gui_new_recipe()
                case "command":
                    self.__execute_command()
                    self.__ui_menu_string = self.__ui_current.reactivate()
                case "exit":
                    __running_ui = False

    def __execute_command(self):
        """ selects the cmd from the ui-view"""
        match self.__ui_menu_string[1]:
            case "selection":
                self.__select_drink_command()
            case "edit":
                self.__edit_hopper_command()
            case "new":
                self.__create_recipe_command()

    def __select_drink_command(self):
        """ calls a cmd to dispense a drink"""
        __drink_name: str = self.__ui_menu_string[2]
        Controller.select_drink(__drink_name)

    def __edit_hopper_command(self):
        """ calls a cmd to edit the hopper"""
        __hopper = int(self.__ui_menu_string[2])
        __drink_on_hopper_name: str = self.__ui_menu_string[3]
        Controller.edit_hopper(__hopper, __drink_on_hopper_name)

    def __create_recipe_command(self):
        """ calls a cmd to create a new recipe"""
        __new_recipe_name: str = self.__ui_menu_string[2]
        __selected_drinks_and_fill_amounts: list[str] = self.__ui_menu_string[3:]
        Controller.create_recipe(__new_recipe_name, __selected_drinks_and_fill_amounts)

    def __get_data_dispensable_drink_names(self) -> list[str]:
        pass

    def __get_data_beverage_on_hopper_names(self) -> list[str]:
        pass

    def __get_data_beverage_names(self) -> list[str]:
        pass

    def __get_data_recipe_names(self) -> list[str]:
        pass


if __name__ == "main":
    pass
