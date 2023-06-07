class Selection:
    __dispensable_recipe_names: list[str]
    __return_value: list[str]
    __is_running: bool
    __recipe_names_is_empty: bool

    def __init__(self):
        pass

    def activate(self, __recipe_names: list[str]) -> list[str]:
        self.__dispensable_recipe_names = __recipe_names
        self.__return_value = []
        self.__is_running = True
        self.__recipe_names_is_empty = len(self.__dispensable_recipe_names) == 0
        print("You are currently in the drink-selection window.\n"
              "Enter <help> to see the available commands.")
        self.__print_recipe_names()
        return self.__drink_selection_loop()

    ####################################################################################################################
    #
    ####################################################################################################################

    def __drink_selection_loop(self) -> list[str]:
        while self.__is_running:
            __input: str = input()
            self.__case_distinction(__input)
        return self.__return_value

    def __case_distinction(self, __input: str):
        if __input in self.__dispensable_recipe_names:
            self.__return_value = ["dispense_drink", __input]
            self.__is_running = False
            print("your drink is being dispensed")

        # sends the select cmd if a number that represents a recipe is the input
        elif __input.isdigit() and 0 <= int(__input) < len(self.__dispensable_recipe_names):
            self.__return_value = ["dispense_drink", self.__dispensable_recipe_names[int(__input)]]
            self.__is_running = False
            print("your drink is being dispensed")

        else:
            match __input:
                case "help":
                    self.__print_help_commands()
                case "drinks":
                    self.__print_recipe_names()
                case "edit":
                    self.__return_value = ["change_view", "edit"]
                    self.__is_running = False
                case "new":
                    self.__return_value = ["change_view", "new"]
                    self.__is_running = False
                case "exit":
                    self.__return_value = []
                    self.__is_running = False
                case _:
                    print("please enter a valid input")

    ####################################################################################################################
    # Print methods
    ####################################################################################################################

    def __print_recipe_names(self):
        print("The following drinks are available for selection:")
        if self.__recipe_names_is_empty:
            print("There are no recipes available currently")
        else:
            __index = 0
            for __drink_name in self.__dispensable_recipe_names:
                print(f"{__index}: {__drink_name}")

    def __print_help_commands(self):
        if self.__recipe_names_is_empty:
            print("input options: \n"
                  "input <help>                           to see a list of commands\n\n"
                  "drink selection cmds:\n"
                  "input <drinks>                         to see a list of all available drinks\n"
                  "input <drink-name> or <drink-index>    to dispense the drink\n\n"
                  "change UI_module cmds:\n"
                  "input <edit>                           to edit the hopper-layout\n"
                  "input <new>                            to enter a new recipe\n"
                  "input <exit>                           to exit the application")
        else:
            print("input options: \n"
                  "input <help>                           to see a list of commands\n\n"
                  "drink selection cmds:\n"
                  "input <drinks>                         to see a list of all available drinks\n"
                  "input <drink-name> or <drink-index>    to dispense the drink\n\n"
                  f"      Example: {self.__dispensable_recipe_names[0]}  or  0"
                  "change UI_module cmds:\n"
                  "input <edit>                           to edit the hopper-layout\n"
                  "input <new>                            to enter a new recipe\n"
                  "input <exit>                           to exit the application")
