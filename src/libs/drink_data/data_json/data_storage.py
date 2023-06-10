import json


class DataStorage:
    """ <ingredient> is a liquid that can be put on the hopper
        <recipe> is a combination of one or more ingredients that form a drink

        __ingredients:= dict {<ingredient-name>: dict {flow_speed: int, amount: int, hopper_position: int | None}}
        <ingredient-name>:= a unique string that represents the ingredient
        flow_speed:= key to an integer that holds the flow speed of the ingredient
        amount:= key to an integer that holds the amount of liquid left in the ingredient container
        hopper_position:= key to an integer | None that holds the hopper-position of an ingredient

        __recipes:=dict{<recipe-name>: dict {<ingredient-name>: dict {fill_amount: int}}
        <recipe-name>:= a unique string that represents the recipe
        <ingredient-name>:= a unique string that represents an ingredient
        fill_amount:= key to an integer that holds the required ml amount of an ingredient in the recipe

        __ingredient_on_hopper_names encodes the hopper position in the list position

        -A recipe can consist of only one ingredient
        -A <recipe-name> can be the same string as an <ingredient-name>
        -An <ingredient-name> should only be used once per <recipe>
        -A recipe is dispensable if all of its <ingredient-name>'s are on the hopper"""

    ####################################################################################################################
    # Datastructures that hold all relevant data at runtime
    ####################################################################################################################

    __ingredients: dict = {}
    __recipes: dict = {}
    __ingredient_on_hopper_names: list[str] = []
    __dispensable_recipe_names: list[str] = []
    __hopper_count: int = 12

    ####################################################################################################################
    #
    ####################################################################################################################

    def __init__(self, __configuration_ingredients: dict,
                 __configuration_ingredient_file_path: str,
                 __configuration_recipe_file_path: str):

        self.__initialize_data(__configuration_ingredients,
                               __configuration_ingredient_file_path,
                               __configuration_recipe_file_path)

    ####################################################################################################################
    # Methods that are used to access runtime data
    ####################################################################################################################

    def get_ingredient_names(self) -> list[str]:
        # return list[<ingredient-name>]

        __result: list[str] = []

        for __ingredient_name in self.__ingredients:
            __result.append(__ingredient_name)

        return __result

    def get_recipe_names(self) -> list[str]:
        # return list[<recipe-name>]

        __result: list[str] = []

        for __recipe_name in self.__recipes:
            __result.append(__recipe_name)

        return __result

    def get_recipe_dispensable_names(self) -> list[str]:
        # return list[<recipe-name>]

        return self.__dispensable_recipe_names

    def get_ingredient_on_hopper_names(self) -> list[str]:
        # return list[<ingredient-name>]

        return self.__ingredient_on_hopper_names

    ####################################################################################################################
    # Methods that are used to change runtime data
    ####################################################################################################################

    def set_hopper(self, __hopper_position: int, __ingredient_name: str):

        if __ingredient_name:
            # check if we got an ingredient_name and not an empty string

            self.__ingredients[__ingredient_name]["hopper_position"] = __hopper_position
            # update the hopper-position of the new ingredient

        if self.__ingredient_on_hopper_names[__hopper_position] is not None:
            # check if there is an old ingredient on the hopper

            __previous_ingredient_on_hopper_name = self.__ingredient_on_hopper_names[__hopper_position]
            self.__ingredients[__previous_ingredient_on_hopper_name]["hopper_position"] = None
            # remove the old ingredient from the hopper

        self.__update_ingredient_on_hopper_names()
        self.__update_dispensable_recipe_names()

    def create_recipe(self, __data: dict):
        # __data := {<recipe-name>: {<ingredient-name>: {fill_amount: <fill-amount>}}}
        # new recipes aren't stored persistently

        __new_recipe_name: str = list(__data.keys())[0]
        self.__recipes[__new_recipe_name] = __data[__new_recipe_name]

        self.__update_dispensable_recipe_names()

    ####################################################################################################################
    # Utility Methods
    ####################################################################################################################

    def __initialize_data(self, __configuration_ingredients: dict,
                          __configuration_ingredient_file_path: str,
                          __configuration_recipe_file_path: str):

        self.__read_ingredients(__configuration_ingredients, __configuration_ingredient_file_path)
        self.__read_recipes(__configuration_recipe_file_path)
        self.__update_ingredient_on_hopper_names()
        self.__update_dispensable_recipe_names()
        # __update_ingredient_on_hopper_names() should be called before __update_dispensable_recipe_names()

    def __read_ingredients(self, __configuration_ingredients: dict, __configuration_ingredient_file_path: str):
        # __configuration_ingredients:= dict {<ingredient-name>: {hopper_position: int | None, amount: int}}

        try:
            with open(file=__configuration_ingredient_file_path, mode="r") as __json_ingredients:
                self.__ingredients = json.load(__json_ingredients)

        except Exception as error:
            print(error)
            return {}

        for __ingredient_name in self.__ingredients:
            # configure all ingredients

            if __ingredient_name in __configuration_ingredients:
                # check if we are given ingredient-data to configure an ingredient

                self.__ingredients[__ingredient_name]["hopper_position"] = \
                    __configuration_ingredients[__ingredient_name]["hopper_position"]

                self.__ingredients[__ingredient_name]["amount"] = \
                    __configuration_ingredients[__ingredient_name]["amount"]

            else:
                # use standard values if no ingredient-data is available for an ingredient

                self.__ingredients[__ingredient_name]["hopper_position"] = None
                self.__ingredients[__ingredient_name]["amount"] = 0

    def __read_recipes(self, __configuration_recipe_file_path: str):

        try:
            with open(file=__configuration_recipe_file_path, mode="r") as __json_recipes:
                self.__recipes = json.load(__json_recipes)

        except Exception as error:
            print(error)
            return {}

    def __update_ingredient_on_hopper_names(self):

        __result: list[str | None] = [None] * self.__hopper_count

        for __ingredient_name in self.__ingredients:

            if self.__ingredients[__ingredient_name]["hopper_position"] is not None:
                # check if an ingredient is on the hopper. hopper_position: int | None

                __hopper_position = self.__ingredients[__ingredient_name]["hopper_position"]
                __result[__hopper_position] = __ingredient_name

        self.__ingredient_on_hopper_names = __result

    def __update_dispensable_recipe_names(self):

        __result: list[str] = []

        for __recipe_name in self.__recipes:

            if self.__determine_if_dispensable(__recipe_name):
                __result.append(__recipe_name)

        self.__dispensable_recipe_names = __result

    def __determine_if_dispensable(self, __recipe_name: str) -> bool:

        __required_ingredient_names: list[str] = []
        # __required_ingredient_names holds the names of all ingredients that are used in a recipe

        for __ingredient_name in self.__recipes[__recipe_name]:
            __required_ingredient_names.append(__ingredient_name)

        if set(__required_ingredient_names).issubset(set(self.__ingredient_on_hopper_names)):
            # check if the required-ingredients are all available on the hopper
            return True

        else:
            return False
