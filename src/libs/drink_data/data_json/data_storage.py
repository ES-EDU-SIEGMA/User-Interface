import json


class DataStorage:
    """ <ingredient> is a liquid that can be put on the hopper
            __ingredients:= dict {<ingredient-name>: dict {flow_speed: int, amount: int, hopper_position: int/None}}
            <ingredient-name>:= a unique string that represents the ingredient
            flow_speed:= key to an integer that represents the flow speed of the ingredient
            amount:= key to an integer/None that represents the amount of liquid left in the ingredient container

        <recipe> is a combination of one or more ingredients that form a drink
            __recipes:=dict{<recipe-name>: dict {<ingredient-name>: dict {fill_amount: int}}
            <recipe-name>:= a unique string that represents the recipe
            <ingredient-name>:= a unique string that represents an ingredient
            fill_amount:= key to an integer that represents the required ml amount of an ingredient in the recipe

        -A recipe can consist of only one ingredient
        -A <recipe> can have the same name as an <ingredient>
        -An <ingredient-name> should only be used once per <recipe>
        -A recipe is dispensable if all of its <ingredient-name>'s are on the hopper"""

    ####################################################################################################################
    # Datastructures that hold all relevant data at runtime
    ####################################################################################################################

    __ingredients: dict = {}
    __recipes: dict = {}
    __ingredient_on_hopper_names: list[str] = []
    # the hopper position is encoded into the list position of __ingredient_on_hopper_names
    __dispensable_recipe_names: list[str] = []
    __hopper_count: int = 12

    ####################################################################################################################
    #
    ####################################################################################################################

    def __init__(self, __ingredient_hopper_position_and_amount: dict):
        """ __ingredient_hopper_position_and_amount:= dict {<ingredient-name>: {hopper_position: int, amount: int}}"""

        self.__initialize_data(__ingredient_hopper_position_and_amount)

    ####################################################################################################################
    # Methods that are used to access runtime data
    ####################################################################################################################

    def get_ingredient_names(self) -> list[str]:
        """ returns a list of all <ingredient-name>'s
            returns list[<ingredient-name>]"""

        __result: list[str] = []

        for __ingredient_name in self.__ingredients:
            __result.append(__ingredient_name)

        return __result

    def get_recipe_names(self) -> list[str]:
        """ returns a list of all <recipe-name>'s
            returns list[<recipe-name>]"""

        __result: list[str] = []

        for __recipe_name in self.__recipes:
            __result.append(__recipe_name)

        return __result

    def get_recipe_dispensable_names(self) -> list[str]:
        """ returns a list of <recipe-name>'s that are dispensable
            returns list[<recipe-name>]"""

        return self.__dispensable_recipe_names

    def get_ingredient_on_hopper_names(self) -> list[str]:
        """ returns a list of <ingredient-name> that are on the hopper
            returns list[<ingredient-name>]"""

        return self.__ingredient_on_hopper_names

    def get_required_ingredient_information(self, __recipe_name) -> list[list[int]]:
        """ returns a list with ingredient information for the required ingredients of a given recipe_name
            returns list[list[<fill-amount-ml>,<flow-speed>]]"""

        __return_value: list[list[int]] = []

        for __ingredient_name in self.__recipes[__recipe_name]:
            __fill_amount: int = self.__recipes[__recipe_name][__ingredient_name]["fill_amount"]
            __flow_speed: int = self.__ingredients[__ingredient_name]["flow_speed"]
            __return_value.append([__fill_amount, __flow_speed])

        return __return_value

    ####################################################################################################################
    # Methods that are used to change runtime data
    ####################################################################################################################

    def set_hopper(self, __hopper_position: int, __new_ingredient_on_hopper_name: str):
        """ Changes the hopper-layout by removing the old ingredient from the hopper
            and adding the new one to the hopper
            __new_ingredient_on_hopper_name: str or None"""
        # todo rework the set_hopper method

        if __new_ingredient_on_hopper_name:
            # todo : change this
            self.__ingredients[__new_ingredient_on_hopper_name]["hopper_position"] = __hopper_position

        if self.__ingredient_on_hopper_names[__hopper_position]:
            # if there is an ingredient on __hopper_position it gets removed and set to None
            __previous_ingredient_on_hopper_name = self.__ingredient_on_hopper_names[__hopper_position]
            self.__ingredients[__previous_ingredient_on_hopper_name]["hopper_position"] = None

        self.__update_ingredient_on_hopper_names()
        self.__update_dispensable_recipe_names()
        # __update_ingredient_on_hopper_names() should be called before __update_dispensable_recipe_names()

    def create_recipe(self, __new_recipe: dict):
        """ Adds a new recipe to the runtime data but doesn't save it persistently.
            __new_recipe_input:= dict { <recipe-name>: dict {<ingredient-name>: dict {fill_amount: int}}}"""
        # If <recipe-name> is already used the old recipe in __recipes gets overwritten.

        for __recip_name in __new_recipe:
            self.__recipes[__recip_name] = __new_recipe[__recip_name]

        self.__update_dispensable_recipe_names()

    ####################################################################################################################
    # Utility Methods
    ####################################################################################################################

    def __initialize_data(self, __ingredient_hopper_position_and_amount: dict):
        self.__read_ingredients(__ingredient_hopper_position_and_amount)
        self.__read_recipes()
        self.__update_ingredient_on_hopper_names()
        self.__update_dispensable_recipe_names()
        # __update_ingredient_on_hopper_names() should be called before __update_dispensable_recipe_names()

    def __read_ingredients(self, __ingredient_hopper_position_and_amount: dict):
        """ gets the ingredients from the corresponding json file and
            adds the fill_amounts and hopper_positions from the input to each ingredient
            __ingredient_hopper_position_and_amount:= dict {<ingredient-name>: {hopper_position: int, amount: int}}"""

        try:
            with open("libs/drink_data/data_json/ingredients.json", "r") as __json_ingredients:
                self.__ingredients = json.load(__json_ingredients)

            for __ingredient_name in self.__ingredients:
                # adds the keys hopper_position and amount to every ingredient and fills in the correct values

                if __ingredient_name in __ingredient_hopper_position_and_amount:
                    self.__ingredients[__ingredient_name]["hopper_position"] = \
                        __ingredient_hopper_position_and_amount[__ingredient_name]["hopper_position"]
                    self.__ingredients[__ingredient_name]["amount"] = \
                        __ingredient_hopper_position_and_amount[__ingredient_name]["amount"]
                else:
                    # standard value if the input doesn't specify anything for an ingredient
                    self.__ingredients[__ingredient_name]["hopper_position"] = None
                    self.__ingredients[__ingredient_name]["amount"] = None

        except Exception as error:
            print(error)
            return {}

    def __read_recipes(self):
        """ gets the recipes from the corresponding json file and determines whether a recipe is dispensable"""

        try:
            with open(file="libs/drink_data/data_json/recipes.json", mode="r") as __json_recipes:
                self.__recipes = json.load(__json_recipes)

        except Exception as error:
            print(error)
            return {}

    def __update_ingredient_on_hopper_names(self):
        """ updates __ingredient_on_hopper_names by checking if hopper_position has an int value for every ingredient.
            __ingredient_on_hopper_names[i] <=> <ingredient-name> on hopper position i
            the hopper position is encoded into the list position"""

        __result: list[str] = [None] * self.__hopper_count  # type: ignore

        for __ingredient_name in self.__ingredients:
            # in regard to the if statement: hopper_position is int or None

            if self.__ingredients[__ingredient_name]["hopper_position"] is not None:
                __hopper_position = self.__ingredients[__ingredient_name]["hopper_position"]
                __result[__hopper_position] = __ingredient_name

        self.__ingredient_on_hopper_names = __result

    def __update_dispensable_recipe_names(self):
        """ updates __dispensable_recipe_names"""

        __result: list[str] = []

        for __recipe_name in self.__recipes:

            if self.__determine_if_dispensable(__recipe_name):
                __result.append(__recipe_name)

        self.__dispensable_recipe_names = __result

    def __determine_if_dispensable(self, __recipe_name: str) -> bool:
        """ For a given <recipe-name> checks if all <ingredient-name>'s that are needed for a
            recipe are available on the hopper"""

        __required_ingredient_names: list[str] = []

        for __ingredient_name in self.__recipes[__recipe_name]:
            __required_ingredient_names.append(__ingredient_name)

        if set(__required_ingredient_names).issubset(set(self.__ingredient_on_hopper_names)):
            return True

        else:
            return False
