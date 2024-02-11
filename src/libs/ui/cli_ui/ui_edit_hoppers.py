from __future__ import annotations


class EditHopper:
    """__return_value:= {
            "cmd": "exit" | "change_ui" | "edit",
            "data": None | "new" | "selection" |
            {"hopper_position": <hopper-position>,
             "ingredient_name": <ingredient-name>}
    }"""

    __ingredient_hopper_names: list[str]
    __ingredient_names: list[str]

    __max_hopper: int

    __is_running: bool
    __return_value: dict

    def __init__(self):
        pass

    def activate(self, __data: list[list[str]]) -> dict:
        if __data:
            # check if __data is not None
            self.__ingredient_hopper_names = __data[0]
            self.__ingredient_names = __data[1]
        else:
            # __data is None
            self.__ingredient_hopper_names = []
            self.__ingredient_names = []

        self.__max_hopper = len(self.__ingredient_hopper_names)

        print(
            "You are currently in the edit-hopper window.\n"
            "Enter <help> to see the available commands."
        )

        self.__return_value = {"cmd": "", "data": None}

        self.__is_running = True
        return self.__edit_hopper_loop()

    ####################################################################################################################
    #
    ####################################################################################################################

    def __edit_hopper_loop(self) -> dict:
        while self.__is_running:
            __input: str = input()
            self.__case_distinction(__input)

        return self.__return_value

    def __case_distinction(self, __input: str):
        if __input == "help":
            self.__print_help_commands()
        elif __input == "ingredients":
            self.__print_ingredient_names()
        elif __input == "hopper":
            self.__print_hopper_layout()
        elif __input == "select":
            self.__return_value["cmd"] = "change_ui"
            self.__return_value["data"] = "selection"
            self.__is_running = False
        elif __input == "new":
            self.__return_value["cmd"] = "change_ui"
            self.__return_value["data"] = "new"
            self.__is_running = False
        elif __input == "exit":
            self.__return_value["cmd"] = "exit"
            self.__is_running = False
        else:
            if not self.__try_valid_edit_input(__input):
                print("please enter a valid input")

    def __try_valid_edit_input(self, __input: str) -> bool:
        __split_input = __input.split(";")

        if (
            __split_input[0].isdigit()
            and int(__split_input[0]) in range(0, self.__max_hopper)
            and __split_input[1] in self.__ingredient_names
            and len(__split_input) == 2
        ):
            # check if __input has the form str <hopper-position>;<ingredient>
            # check if input-hopper-position < self.__max_hopper

            self.__return_value["cmd"] = "edit"
            self.__return_value["data"] = {
                "hopper_position": int(__split_input[0]),
                "ingredient_name": __split_input[1],
            }

            print(
                f"hopper layout changed to:\n"
                f"hopper-position: {__split_input[0]}   ingredient: {__split_input[1]}"
            )
            self.__is_running = False

            return True

        else:
            # no valid input received
            return False

    ####################################################################################################################
    # Print methods
    ####################################################################################################################

    def __print_hopper_layout(self):
        print("The hopper layout is:")
        __hopper_position: int = 0

        for __ingredient_name in self.__ingredient_hopper_names:
            print(
                f"Hopper-position:{__hopper_position}   Ingredient: {__ingredient_name}"
            )
            __hopper_position += 1

    def __print_ingredient_names(self):
        print("All ingredients:")

        for __ingredient_name in self.__ingredient_names:
            print(__ingredient_name)

    def __print_help_commands(self):
        if self.__ingredient_hopper_names:
            # check if there are ingredients on a hopper

            print(
                "input options: \n"
                "input <help>                             to see a list of available commands\n\n"
                "edit hopper cmds:\n"
                "input <ingredients>                      to see a list of all ingredients\n"
                "input <hopper>                          to see a list of the current hopper layout\n"
                "input [<hopper-position>;<ingredient>]   to put an ingredient onto the hopper-position\n"
                f"      Example:  0;{self.__ingredient_hopper_names[0]}\n\n"
                "change UI_module cmds:\n"
                "input <select>                         to dispense a drink\n"
                "input <new>                            to enter a new recipe\n"
                "input <exit>                           to exit the application"
            )

        else:
            # no ingredients on the hopper

            print(
                "input options: \n"
                "input <help>                             to see a list of available commands\n\n"
                "edit hopper cmds:\n"
                "input <ingredients>                      to see a list of all ingredients\n"
                "input <hopper>                          to see a list of the current hopper layout\n"
                "input [<hopper-position>;<ingredient>]   to put an ingredient onto the hopper-position\n\n"
                "change UI_module cmds:\n"
                "input <select>                         to dispense a drink\n"
                "input <new>                            to enter a new recipe\n"
                "input <exit>                           to exit the application"
            )
