class Selection:
    __dispensable_recipe_names: list[str]
    __return_value: list[str]
    __is_running: bool
    __recipe_names_is_empty: bool

    def __init__(self):
        pass

    def activate(self, __data: list[str]) -> list[str]:

        if __data:
            # check if __data is not None
            self.__dispensable_recipe_names = __data
        else:
            # __data is None
            self.__dispensable_recipe_names = []

        self.__return_value = []

        print("You are currently in the drink-selection window.\n"
              "Enter <help> to see the available commands.")
        self.__print_recipe_names()

        self.__is_running = True
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
                if not self.__find_recipe_name(__input):
                    print("please enter a valid input")

    def __find_recipe_name(self, __input: str) -> bool:

        if __input in self.__dispensable_recipe_names:
            # check if __input is a recipe_name that the machine knows

            self.__return_value = ["dispense_drink", __input]
            self.__is_running = False

            print("your drink is being dispensed")
            return True

        # sends the select cmd if a number that represents a recipe is the input
        elif __input.isdigit() and 0 <= int(__input) < len(self.__dispensable_recipe_names):
            # check if __input is an int that represents a recipe_name that the machine knows

            self.__return_value = ["dispense_drink", self.__dispensable_recipe_names[int(__input)]]
            self.__is_running = False

            print("your drink is being dispensed")
            return True

        else:
            # __input is not a valid recipe_name
            return False

    ####################################################################################################################
    # Print methods
    ####################################################################################################################

    def __print_recipe_names(self):

        print("The following drinks are available for selection:")

        if self.__dispensable_recipe_names:
            # check if self.__dispensable_recipe_names is not []

            __index = 0
            for __drink_name in self.__dispensable_recipe_names:
                print(f"{__index}: {__drink_name}")

        else:
            # self.__dispensable_recipe_names is []
            print("There are no recipes available currently")

    def __print_help_commands(self):

        if self.__dispensable_recipe_names:
            # check if self.__dispensable_recipe_names is not []

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

        else:
            # self.__dispensable_recipe_names is []

            print("input options: \n"
                  "input <help>                           to see a list of commands\n\n"
                  "drink selection cmds:\n"
                  "input <drinks>                         to see a list of all available drinks\n"
                  "input <drink-name> or <drink-index>    to dispense the drink\n\n"
                  "change UI_module cmds:\n"
                  "input <edit>                           to edit the hopper-layout\n"
                  "input <new>                            to enter a new recipe\n"
                  "input <exit>                           to exit the application")
