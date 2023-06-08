class NewRecipe:
    __ingredient_names: list[str]
    __recipe_names: list[str]
    __commands: list[str] = ["drinks", "help", "recipes", "ingredient", "my_recipe", "edit", "select", "new", "exit"]
    __return_value: list[str]
    __is_running: bool

    __new_recipe: list[str]
    __sum_fill_amounts: int
    MAX_FILL_AMOUNT: int = 350

    def __init__(self):
        pass

    def activate(self, __data: list[list[str]]) -> list[str]:

        if __data:
            # check if __data is not None
            self.__ingredient_names = __data[0]
            self.__recipe_names = __data[1]
        else:
            # __data is None
            self.__ingredient_names = []
            self.__recipe_names = []

        self.__return_value = []
        self.__new_recipe = []
        self.__sum_fill_amounts = 0

        print("You are currently in the new-recipe window."
              "Enter <help> to see the available commands.")

        self.__is_running = True
        return self.__new_recipe_loop()

    ####################################################################################################################
    #
    ####################################################################################################################

    def __new_recipe_loop(self) -> list[str]:

        while self.__is_running:
            __input: str = input()
            self.__case_distinction(__input)

        return self.__return_value

    def __case_distinction(self, __input: str):

        match __input:
            case "help":
                self.__print_help_commands()
            case "recipes":
                self.__print_recipe_names()
            case "ingredients":
                self.__print_ingredient_names()
            case "my_recipe":
                self.__print_new_recipe_progress()
            case "select":
                self.__return_value = ["change_view", "selection"]
                self.__is_running = False
            case "edit":
                self.__return_value = ["change_view", "edit"]
                self.__is_running = False
            case "exit":
                self.__return_value = []
                self.__is_running = False
            case _:
                if not self.__try_split_string_command(__input):
                    print("please enter a valid input")

    def __try_split_string_command(self, __input: str) -> bool:
        # there are two commands with a split input
        # 1.command is str create;<recipe-name>
        # 2.command is str <ingredient-name>;<ml-amount>

        __split_input = __input.split(";")
        if __split_input[0] == "create":
            self.__create_recipe(__split_input[1])
            return True

        else:
            return self.__try_add_ingredient(__split_input)

    def __create_recipe(self, __recipe_name: str):
        if not self.__new_recipe:
            # check if self.__new_recipe is []
            print("Can't create an empty recipe. You didn't add any ingredients to your recipe.")

        elif (__recipe_name not in self.__recipe_names and
                __recipe_name not in self.__commands):
            # make sure the new recipe names doesn't conflict with already existing recipe names or command names

            self.__return_value = ["new_recipe", __recipe_name, self.__new_recipe]
            self.__is_running = False

            print(f"recipe {__recipe_name} added with the following ingredients:")
            self.__print_new_recipe_progress()

        else:
            # the new recipe name is not valid
            print(f"failed to create your drink. The name: {__recipe_name} is not valid")

    def __try_add_ingredient(self, __split_input: list[str]) -> bool:

        if __split_input[0] in self.__ingredient_names and __split_input[1].isdigit():
            # confirm that input has the form of str <ingredient-name>;<ml-amount>
            # we currently ignore __split_input[n] n>1 if such an input exists

            __ingredient_name: str = __split_input[0]
            __fill_amount: int = int(__split_input[1])

            if (self.__sum_fill_amounts + __fill_amount) < self.MAX_FILL_AMOUNT:
                # Test whether the ml-amount fits into the glass with the rest of the recipes ingredient.

                self.__new_recipe.append(__ingredient_name)
                self.__new_recipe.append(str(__fill_amount))
                print(f"{__ingredient_name} with {__fill_amount}ml added to your recipe")

            else:
                # test to check whether ingredient fits into the glass failed.
                print(f"The glass is {self.MAX_FILL_AMOUNT}ml large.\n"
                      f"The new ingredient doesn't fit into the glass with the rest of the ingredients.\n"
                      f"The glass would overflow by"
                      f"{self.__sum_fill_amounts + __fill_amount - self.MAX_FILL_AMOUNT}\n"
                      f"please add a lower ingredient fill amount")

            return True

        else:
            # no valid input found
            return False

    ####################################################################################################################
    # Print methods
    ####################################################################################################################

    def __print_recipe_names(self):

        print("Recipe names:")
        for __recipe in self.__recipe_names:
            print(__recipe)

    def __print_ingredient_names(self):

        print("All ingredients:")
        for __ingredient_name in self.__ingredient_names:
            print(__ingredient_name)

    def __print_new_recipe_progress(self):

        print("Your recipe:")
        if self.__new_recipe:
            # check if self.__new_recipe is not []
            for __list_item in self.__new_recipe:
                print(f"ingredient  {__list_item[0]}   fill amount {__list_item[1]}ml")

        else:
            # self.__new_recipe is []
            print("nothing selected so far")

    @staticmethod
    def __print_help_commands():
        print("input options: \n"
              "input <help>                             to see a list of available commands\n\n"
              "new recipe cmds:\n"
              "input <recipes>                          to see a list of all recipes\n"
              "input <ingredient>                       to see a list of all available ingredients\n"
              "input <my_recipe>                        to see the drinks you have selected for your recipe\n"
              "input [<ingredient-name>;<ml>]           to put a ingredient onto the hopper-position\n"
              "      example:  coca_cola;100\n"
              "input [<create>;<recipe-name>]           to create your recipe with the given name\n"
              "      example:  create;example_name\n\n"
              "change UI_module cmds:\n"
              "input <select>                         to dispense a drink\n"
              "input <edit>                           to edit the hopper-layout\n"
              "input <exit>                           to exit the application")
