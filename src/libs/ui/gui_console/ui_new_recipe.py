import re as RegularExpression


def print_help_commands():
    print("input options: \n"
          "input <help>                           to see a list of available commands\n\n"
          "new recipe cmds:\n"
          "input <recipes>                        to see a list of all recipes\n"
          "input <beverage>                       to see a list of all available beverages\n"
          "input <my_recipe>                      to see the drinks you have selected for your recipe\n"
          "input [<beverage-name>;<ml>]           to put a beverage onto the hopper-position\n"
          "      example:  coca_cola;100\n"
          "input [<create>;<recipe-name>]         to create your recipe with the given name\n"
          "      example:  create;cool_name\n\n"
          "change ui cmds:\n"
          "input <select>                         to dispense a drink\n"
          "input <edit>                           to edit the hopper-layout\n"
          "input <exit>                           to exit the application")


class NewRecipe:
    __data_beverage_names: list[str] = None
    __data_recipe_names: list[str] = None
    __commands: list[str] = ["help", "recipes", "beverage", "my-recipe", "select", "new", "exit"]
    __return_value: str = None
    __new_recipe_process: bool = None

    __selected_drinks_and_fill_amounts: list[str] = None
    __sum_fill_amounts: int = None
    MAX_FILL_AMOUNT: int = 350

    def __init__(self):
        pass

    def activate(self, __data_beverage_names: list[str], __data_drink_names: list[str]) -> str:
        self.__data_beverage_names = __data_beverage_names
        self.__data_recipe_names = __data_drink_names
        self.__return_value = ""
        self.__new_recipe_process = True

        self.__selected_drinks_and_fill_amounts = []
        self.__sum_fill_amounts = 0

        print("you are currently in the new-recipe window")
        print("enter <help> to see the available commands")
        return self.__new_recipe_loop()

    def reactivate(self) -> str:
        self.__return_value = ""
        self.__new_recipe_process = True
        self.__selected_drinks_and_fill_amounts = []
        self.__sum_fill_amounts = 0
        print("enter <help> to see the available commands")
        return self.__new_recipe_loop()

    def deactivate(self):
        pass

    def __new_recipe_loop(self) -> str:
        while self.__new_recipe_process:
            __input: str = input()
            self.__case_distinction(__input)
        return self.__return_value

    def __print_recipe_names(self):
        print("recipe names:")
        for __recipe in self.__data_recipe_names:
            print(__recipe)

    def __print_beverage_names(self):
        print("all beverages:")
        for __beverage in self.__data_beverage_names:
            print(__beverage)

    def __print_new_recipe_progress(self):
        print("your recipe:")
        if not self.__selected_drinks_and_fill_amounts:
            print("nothing selected so far")
        for __list_item in self.__selected_drinks_and_fill_amounts:
            print(f"beverage  {__list_item[0]}   fill amount {__list_item[1]}ml")

    def __try_split_string_command(self, __input: str) -> bool:
        # there are two commands with a split input
        # 1.command is [<beverage-name>;<ml>]
        # 2.command is [<create>;<recipe-name>]

        try:  # try to split the input
            __split_input = __input.split(";")
            if len(__split_input) == 2:  # the input should consist of exactly two values
                if __split_input[0] == "create":
                    return self.__create_beverage(__split_input[1])
                else:
                    return self.__try_add_beverage(__split_input)
        except ValueError:
            return False

    def __create_beverage(self, __recipe_name: str) -> bool:
        if (__recipe_name not in self.__data_recipe_names and
                __recipe_name not in self.__data_beverage_names and
                not RegularExpression.search(";", __recipe_name) and
                not RegularExpression.search("hopper_", __recipe_name)):
            self.__return_value = f"command;new;{__recipe_name},{self.__selected_drinks_and_fill_amounts}"
            print(f"recipe {__recipe_name} added with the following ingredients:")
            self.__print_new_recipe_progress()
            self.__new_recipe_process = False
            return True
        else:
            print(f"failed to create your drink. The name: {__recipe_name} is already used")
            return False

    def __try_add_beverage(self, __split_input: list[str]) -> bool:
        try:
            __beverage_name: str = __split_input[0]
            __fill_amount: int = int(__split_input[1])  # try to cast into int
            if ((self.__sum_fill_amounts + __fill_amount) < self.MAX_FILL_AMOUNT
                    and __beverage_name in self.__data_beverage_names):
                self.__selected_drinks_and_fill_amounts.append(__split_input[0])  # appending beverage name
                self.__selected_drinks_and_fill_amounts.append(__split_input[1])  # appending fill amount ml
                return True
            else:
                return False
        except ValueError:
            pass
            return False

    def __case_distinction(self, __input: str):
        match __input:
            case "help":
                print_help_commands()
            case "recipes":
                self.__print_recipe_names()
            case "beverage":
                self.__print_beverage_names()
            case "my_recipe":
                self.__print_new_recipe_progress()
            case "select":
                self.__return_value = "change_window;select"
                self.__new_recipe_process = False
            case "edit":
                self.__return_value = "change_window;edit"
                self.__new_recipe_process = False
            case "exit":
                self.__return_value = "exit;pseudo_string"
                self.__new_recipe_process = False
            case _:
                if self.__try_split_string_command(__input):
                    pass
                else:
                    print("please enter a valid input")
