class EditHopper:
    __ingredient_hopper_names: list[str]
    __ingredient_names: list[str]
    __max_hopper: int
    __return_value: list[str]
    __is_running: bool

    def __init__(self):
        pass

    def activate(self, __data: list[list[str]]) -> list[str]:
        self.__ingredient_hopper_names = __data[0]
        self.__ingredient_names = __data[1]
        self.__return_value = []
        self.__max_hopper = len(self.__ingredient_hopper_names)
        self.__is_running = True
        print("You are currently in the edit-hopper window.\n"
              "Enter <help> to see the available commands.")
        return self.__edit_hopper_loop()

    ####################################################################################################################
    #
    ####################################################################################################################

    def __edit_hopper_loop(self) -> list[str]:
        while self.__is_running:
            __input: str = input()
            self.__case_distinction(__input)
        return self.__return_value

    def __case_distinction(self, __input: str):
        match __input:
            case "help":
                self.__print_help_commands()
            case "ingredients":
                self.__print_ingredient_names()
            case "hoppers":
                self.__print_hopper_layout()
            case "select":
                self.__return_value = ["change_view", "selection"]
                self.__is_running = False
            case "new":
                self.__return_value = ["change_view", "new"]
                self.__is_running = False
            case "exit":
                self.__return_value = []
                self.__is_running = False
            case _:
                if not self.__try_change_hopper_layout(__input):
                    print("please enter a valid input")

    def __try_change_hopper_layout(self, __input: str):
        # If the input has the form <hopper>;<ingredient>;<rest> we ignore the rest and accept the input
        __split_input = __input.split(";")
        # This <if> doesn't produce errors because python evaluates <and> from left to right
        if __split_input[0].isdigit() and int(__split_input[0]) < self.__max_hopper:
            if __split_input[1] in self.__ingredient_names:
                self.__return_value = ["edit_hopper",
                                       self.__ingredient_hopper_names[int(__split_input[0])],
                                       __split_input[1]]
                self.__is_running = False
                print("hopper layout changed to:\n"
                      f"hopper-position: {__split_input[0]}   ingredient: {__split_input[1]}")

    ####################################################################################################################
    # Print methods
    ####################################################################################################################

    def __print_hopper_layout(self):
        print("The hopper layout is:")
        __hopper_position: int = 0
        for __ingredient_name in self.__ingredient_hopper_names:
            print(f"Hopper-position: {__hopper_position}   Ingredient: {__ingredient_name}")
            __hopper_position += 1

    def __print_ingredient_names(self):
        print("All ingredients:")
        for __ingredient_name in self.__ingredient_names:
            print(__ingredient_name)

    @staticmethod
    def __print_help_commands():
        print("input options: \n"
              "input <help>                             to see a list of available commands\n\n"
              "edit hopper cmds:\n"
              "input <ingredients>                      to see a list of all ingredients\n"
              "input <hoppers>                          to see a list of the current hopper layout\n"
              "input [<hopper-position>;<ingredient>]   to put an ingredient onto the hopper-position\n"
              "      example:  1;coca_cola\n\n"
              "change UI_module cmds:\n"
              "input <select>                         to dispense a drink\n"
              "input <new>                            to enter a new recipe\n"
              "input <exit>                           to exit the application")
