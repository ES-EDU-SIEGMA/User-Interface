from __future__ import annotations


class Selection:
    """__return_value:= {
            "cmd": "exit" | "change_ui" | "dispense",
            "data": None | "edit" | "new" | <recipe-name>
    }"""

    __dispensable_recipe_names: list[str]

    __is_running: bool
    __return_value: dict

    def __init__(self):
        __progress_dispense_drink = False

    def activate(self, __data: list[str]) -> dict:

        if __data:
            # check if __data is not None
            self.__dispensable_recipe_names = __data
        else:
            # __data is None
            self.__dispensable_recipe_names = []

        self.__print_recipe_names()

        self.__return_value = {"cmd": "", "data": None}

        self.__is_running = True
        return self.__drink_selection_loop()

    ####################################################################################################################
    #
    ####################################################################################################################

    def __drink_selection_loop(self) -> dict:
        while self.__is_running:
            __input: str = input()
            self.__case_distinction(__input)

        return self.__return_value

    def __case_distinction(self, __input: str):

        if __input == "exit":
            self.__return_value["cmd"] = "exit"
            self.__is_running = False
        else:
            if not self.__try_valid_selection_input(__input):
                print("please enter a valid input")

    def __try_valid_selection_input(self, __input: str) -> bool:

        if __input.isdigit() and 0 <= int(__input) < len(
            self.__dispensable_recipe_names
        ):
            # check if __input is an int that represents a recipe_name that the machine knows

            __recipe_name: str = self.__dispensable_recipe_names[int(__input)]
            self.__return_value["cmd"] = "dispense"
            self.__return_value["data"] = __recipe_name
            self.__is_running = False

            print(f"your {__recipe_name} is being dispensed")
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
            # check if there are recipes available

            __drink_number = 0
            for __recipe_name in self.__dispensable_recipe_names:
                print(f"{__drink_number}: {__recipe_name}")
                __drink_number += 1

        else:
            # no recipes are available
            print("There are no recipes available currently")
