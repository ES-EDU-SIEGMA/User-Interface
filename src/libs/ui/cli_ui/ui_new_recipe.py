from __future__ import annotations


class NewRecipe:
    """__return_value:= {
            "cmd": "exit" | "change_ui" | "new",
            "data": None | "selection" | "edit" |
            {<recipe-name>: {<ingredient-name>: {"fill_amount": <fill-amount>}}}
    }"""

    __ingredient_names: list[str]
    __recipe_names: list[str]
    __commands: list[str] = [
        "drinks",
        "help",
        "recipes",
        "ingredient",
        "my_recipe",
        "edit",
        "select",
        "new",
        "exit",
    ]

    __new_recipe_progress: list[list[str | int]]
    __sum_fill_amount: int
    MAX_FILL_AMOUNT: int = 350

    __is_running: bool
    __return_value: dict

    def __init__(self):
        pass

    def activate(self, __data: list[list[str]]) -> dict:
        if __data:
            # check if __data is not None
            self.__ingredient_names = __data[0]
            self.__recipe_names = __data[1]
        else:
            # __data is None
            self.__ingredient_names = []
            self.__recipe_names = []

        self.__new_recipe_progress = []
        self.__sum_fill_amount = 0

        print(
            "You are currently in the new-recipe window.\n"
            "Enter <help> to see the available commands."
        )

        self.__return_value = {"cmd": "", "data": None}

        self.__is_running = True
        return self.__new_recipe_loop()

    ####################################################################################################################
    #
    ####################################################################################################################

    def __new_recipe_loop(self) -> dict:
        while self.__is_running:
            __input: str = input()
            self.__case_distinction(__input)

        return self.__return_value

    def __case_distinction(self, __input: str):
        if __input == "help":
            self.__print_help_commands()
        elif __input == "recipes":
            self.__print_recipe_names()
        elif __input == "ingredients":
            self.__print_ingredient_names()
        elif __input == "my_recipe":
            self.__print_new_recipe_progress()
        elif __input == "select":
            self.__return_value["cmd"] = "change_ui"
            self.__return_value["data"] = "selection"
            self.__is_running = False
        elif __input == "edit":
            self.__return_value["cmd"] = "change_ui"
            self.__return_value["data"] = "edit"
            self.__is_running = False
        elif __input == "exit":
            self.__return_value["cmd"] = "exit"
            self.__is_running = False
        else:
            if not self.__rey_valid_recipe_input(__input):
                print("please enter a valid input")

    def __rey_valid_recipe_input(self, __input: str) -> bool:
        # there are two commands with a split input
        # 1.command is str create;<recipe-name>
        # 2.command is str <ingredient-name>;<ml-amount>

        __split_input = __input.split(";")

        if __split_input[0] == "create":
            self.__try_create_recipe(__split_input[1])
            return True

        else:
            return self.__try_add_ingredient(__split_input)

    def __try_create_recipe(self, __recipe_name: str):
        if not self.__new_recipe_progress:
            # check if we got an empty recipe
            print(
                "Can't create an empty recipe. You didn't add any ingredients to your recipe."
            )

        elif (
            __recipe_name not in self.__recipe_names
            and __recipe_name not in self.__commands
        ):
            # check if new recipe-name conflicts with existing recipe-names or console-commands

            self.__return_value["cmd"] = "new"
            self.__return_value["data"] = {}
            self.__return_value["data"][__recipe_name] = {}
            for __ingredient_list in self.__new_recipe_progress:
                __ingredient_name = __ingredient_list[0]
                __fill_amount = __ingredient_list[1]
                self.__return_value["data"][__recipe_name][__ingredient_name] = {}
                self.__return_value["data"][__recipe_name][__ingredient_name][
                    "fill_amount"
                ] = __fill_amount

            print(f"recipe {__recipe_name} added with the following ingredients:")
            self.__print_new_recipe_progress()
            self.__is_running = False

        else:
            # the new recipe name is not valid
            print(
                f"failed to create your drink. The name: {__recipe_name} is not valid"
            )

    def __try_add_ingredient(self, __split_input: list[str]) -> bool:
        # todo prevent adding two times the same ingredient or overwrite ingredient

        if (
            __split_input[0] in self.__ingredient_names
            and __split_input[1].isdigit()
            and len(__split_input) == 2
        ):
            # confirm that input has the form <ingredient-name>;<ml-amount>

            __ingredient_name: str = __split_input[0]
            __fill_amount: int = int(__split_input[1])

            if (self.__sum_fill_amount + __fill_amount) < self.MAX_FILL_AMOUNT:
                # check if the newly added ingredient fits into the glass with the other ingredients

                self.__new_recipe_progress.append([__ingredient_name, __fill_amount])

                print(
                    f"added new ingredient {__ingredient_name} with {__fill_amount}ml"
                )

            else:
                # newly added ingredient doesn't fit into the glass
                print(
                    f"The glass is {self.MAX_FILL_AMOUNT}ml large.\n"
                    f"The new ingredient doesn't fit into the glass with the rest of the ingredients.\n"
                    f"The glass would overflow by"
                    f"{self.__sum_fill_amount + __fill_amount - self.MAX_FILL_AMOUNT}\n"
                    f"please add a lower ingredient fill amount"
                )

            return True

        else:
            # no valid input found
            return False

    ####################################################################################################################
    # Print methods
    ####################################################################################################################

    def __print_recipe_names(self):
        print("Recipe names:")
        for __recipe_name in self.__recipe_names:
            print(__recipe_name)

    def __print_ingredient_names(self):
        print("All ingredients:")
        for __ingredient_name in self.__ingredient_names:
            print(__ingredient_name)

    def __print_new_recipe_progress(self):
        print("Your recipe:")
        if self.__new_recipe_progress:
            # check if ingredients were added to the new recipe

            for __ingredient_list in self.__new_recipe_progress:
                print(
                    f"ingredient:{__ingredient_list[0]}   fill amount:{__ingredient_list[1]}ml"
                )

        else:
            # the new recipe is empty
            print("nothing selected so far")

    def __print_help_commands(self):
        if self.__ingredient_names:
            # check if there are any ingredients

            print(
                "input options: \n"
                "input <help>                             to see a list of available commands\n\n"
                "new recipe cmds:\n"
                "input <recipes>                          to see a list of all recipes\n"
                "input <ingredient>                       to see a list of all available ingredients\n"
                "input <my_recipe>                        to see the drinks you have selected for your recipe\n"
                "input [<ingredient-name>;<ml>]           to put a ingredient onto the hopper-position\n"
                f"      example:  {self.__ingredient_names[0]};100\n"
                "input [<create>;<recipe-name>]           to create your recipe with the given name\n"
                "      example:  create;example_new_recipe_name\n\n"
                "change UI_module cmds:\n"
                "input <select>                         to dispense a drink\n"
                "input <edit>                           to edit the hopper-layout\n"
                "input <exit>                           to exit the application"
            )

        else:
            # no ingredients available

            print(
                "input options: \n"
                "input <help>                             to see a list of available commands\n\n"
                "new recipe cmds:\n"
                "input <recipes>                          to see a list of all recipes\n"
                "input <ingredient>                       to see a list of all available ingredients\n"
                "input <my_recipe>                        to see the drinks you have selected for your recipe\n"
                "input [<ingredient-name>;<ml>]           to put a ingredient onto the hopper-position\n"
                "input [<create>;<recipe-name>]           to create your recipe with the given name\n"
                "      example:  create;example_new_recipe_name\n\n"
                "change UI_module cmds:\n"
                "input <select>                         to dispense a drink\n"
                "input <edit>                           to edit the hopper-layout\n"
                "input <exit>                           to exit the application"
            )
