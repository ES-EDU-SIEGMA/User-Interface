def print_help_commands():
    print("input options: \n"
          "input <help>                             to see a list of available commands\n\n"
          "new recipe cmds:\n"
          "input <recipes>                          to see a list of all recipes\n"
          "input <ingredient>                       to see a list of all available ingredients\n"
          "input <my_recipe>                        to see the drinks you have selected for your recipe\n"
          "input [<ingredient-name>;<ml>]           to put a ingredient onto the hopper-position\n"
          "      example:  coca_cola;100\n"
          "input [<create>;<recipe-name>]           to create your recipe with the given name\n"
          "      example:  create;cool_name\n\n"
          "change ui cmds:\n"
          "input <select>                         to dispense a drink\n"
          "input <edit>                           to edit the hopper-layout\n"
          "input <exit>                           to exit the application")


class NewRecipe:
    __ingredient_names: list[str]
    __recipe_names: list[str]
    __commands: list[str] = ["drinks", "help", "recipes", "ingredient", "my_recipe", "edit", "select", "new", "exit"]
    __return_value: str
    __is_running: bool

    __new_recipe: list[str]
    __sum_fill_amounts: int
    MAX_FILL_AMOUNT: int = 350

    def __init__(self):
        pass

    def activate(self, __ingredient_names: list[str], __recipe_names: list[str]) -> str:
        self.__ingredient_names = __ingredient_names
        self.__recipe_names = __recipe_names
        self.__return_value = ""
        self.__is_running = True
        self.__new_recipe = []
        self.__sum_fill_amounts = 0
        print("you are currently in the new-recipe window")
        print("enter <help> to see the available commands")
        return self.__new_recipe_loop()

    def deactivate(self):
        pass

    def __new_recipe_loop(self) -> str:
        while self.__is_running:
            __input: str = input()
            self.__case_distinction(__input)
        return self.__return_value

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
            for __list_item in self.__new_recipe:
                print(f"ingredient  {__list_item[0]}   fill amount {__list_item[1]}ml")
        else:
            print("nothing selected so far")

    def __case_distinction(self, __input: str):
        match __input:
            case "help":
                print_help_commands()
            case "recipes":
                self.__print_recipe_names()
            case "ingredients":
                self.__print_ingredient_names()
            case "my_recipe":
                self.__print_new_recipe_progress()
            case "select":
                self.__return_value = "change_window;select"
                self.__is_running = False
            case "edit":
                self.__return_value = "change_window;edit"
                self.__is_running = False
            case "exit":
                self.__return_value = "exit;pseudo_string"
                self.__is_running = False
            case _:
                self.__try_split_string_command(__input)

    def __try_split_string_command(self, __input: str):
        # there are two commands with a split input
        # 1.command is [<create>;<recipe-name>]
        # 2.command is [<ingredient-name>;<ml>]
        __split_input = __input.split(";")
        if __split_input[0] == "create":
            self.__create_recipe(__split_input[1])
        else:
            self.__try_add_ingredient(__split_input)

    def __create_recipe(self, __recipe_name: str):
        if (__recipe_name not in self.__recipe_names and
                __recipe_name not in self.__commands):
            self.__return_value = f"command;new;{__recipe_name};{self.__new_recipe}"
            self.__is_running = False
            print(f"recipe {__recipe_name} added with the following ingredients:")
            self.__print_new_recipe_progress()
        else:
            print(f"failed to create your drink. The name: {__recipe_name} is not valid")

    def __try_add_ingredient(self, __split_input: list[str]):
        __ingredient_name: str = __split_input[0]
        if __split_input[1].isdigit():
            __fill_amount: int = int(__split_input[1])
            if ((self.__sum_fill_amounts + __fill_amount) < self.MAX_FILL_AMOUNT
                    and __ingredient_name in self.__ingredient_names):
                self.__new_recipe.append(__split_input[0])  # appending ingredient name
                self.__new_recipe.append(__split_input[1])  # appending fill amount ml
                print(f"{__ingredient_name} with {__fill_amount}ml added to your recipe")
            else:
                print(f"The glass is only {self.MAX_FILL_AMOUNT}ml large.\n"
                      f"Your new addition would overflow the glass by"
                      f"{self.__sum_fill_amounts + __fill_amount - self.MAX_FILL_AMOUNT}\n"
                      f"please add a lower amount")
        else:
            print("please enter a valid input")
