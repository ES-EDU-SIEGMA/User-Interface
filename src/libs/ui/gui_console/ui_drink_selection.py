def print_help_commands():
    print("input options: \n"
          "input <help>                           to see a list of commands\n\n"
          "drink selection cmds:\n"
          "input <drinks>                         to see a list of all available drinks\n"
          "input <drink-name> or <drink-index>    to dispense the drink\n\n"

          "change ui cmds:\n"
          "input <edit>                           to edit the hopper-layout\n"
          "input <new>                            to enter a new recipe\n"
          "input <exit>                           to exit the application")


class Selection:
    __recipe_names: list[str]
    __return_value: str
    __is_running: bool
    __recipe_names_is_empty: bool

    def __init__(self):
        pass

    def activate(self, __recipe_names: list[str]) -> str:
        self.__recipe_names = __recipe_names
        self.__return_value = ""
        self.__is_running = True
        self.__recipe_names_is_empty = len(self.__recipe_names) == 0
        print(f"You are currently in the drink-selection window.\n"
              "Enter <help> to see the available commands")
        self.__print_recipe_names()
        return self.__drink_selection_loop()

    def deactivate(self):
        pass

    def __drink_selection_loop(self) -> str:
        while self.__is_running:
            __input: str = input()
            self.__case_distinction(__input)
        return self.__return_value

    def __print_recipe_names(self):
        print("The following drinks are available for selection:")
        if self.__recipe_names_is_empty:
            print("There are no recipes available currently")
        else:
            __index = 0
            for __drink_name in self.__recipe_names:
                print(f"{__index}: {__drink_name}")

    def print_help_commands(self):
        if self.__recipe_names_is_empty:
            print("input options: \n"
                  "input <help>                           to see a list of commands\n\n"
                  "drink selection cmds:\n"
                  "input <drinks>                         to see a list of all available drinks\n"
                  "input <drink-name> or <drink-index>    to dispense the drink\n\n"
                  "change ui cmds:\n"
                  "input <edit>                           to edit the hopper-layout\n"
                  "input <new>                            to enter a new recipe\n"
                  "input <exit>                           to exit the application")
        else:
            print("input options: \n"
                  "input <help>                           to see a list of commands\n\n"
                  "drink selection cmds:\n"
                  "input <drinks>                         to see a list of all available drinks\n"
                  "input <drink-name> or <drink-index>    to dispense the drink\n\n"
                  f"      Example: {self.__recipe_names[0]}  or  0"
                  "change ui cmds:\n"
                  "input <edit>                           to edit the hopper-layout\n"
                  "input <new>                            to enter a new recipe\n"
                  "input <exit>                           to exit the application")

    def __case_distinction(self, __input: str):
        # sends the select cmd if a recipe name is the input
        if __input in self.__recipe_names:
            self.__return_value = f"command;select;{__input}"
            self.__is_running = False
            print("your drink is being dispensed")

        # sends the select cmd if a number that represents a recipe is the input
        elif __input.isdigit() and 0 <= int(__input) < len(self.__recipe_names):
            self.__return_value = f"command;select;{self.__recipe_names[int(__input)]}"
            self.__is_running = False
            print("your drink is being dispensed")

        else:
            match __input:
                case "help":
                    print_help_commands()
                case "drinks":
                    self.__print_recipe_names()
                case "edit":
                    self.__return_value = "change_window;edit"
                    self.__is_running = False
                case "new":
                    self.__return_value = "change_window;new"
                    self.__is_running = False
                case "exit":
                    self.__return_value = "exit;pseudo_string"
                    self.__is_running = False
                case _:
                    print("please enter a valid input")
