from .new_data_json import data_storage as Data


class DataInterface:
    __data_storage: Data.DataStorage

    def __init__(self, __hopper_position_and_amount: dict):
        self.__data_storage = Data.DataStorage(__hopper_position_and_amount)
        print("initializing DataInterface")

    ####################################################################################################################
    # Methods to access data
    ####################################################################################################################

    def get_ingredient_names(self) -> list[str]:
        """ returns list[<ingredient-name>]"""
        return self.__data_storage.get_ingredient_names()

    def get_recipe_names(self) -> list[str]:
        """ returns list[<recipe-name>]"""
        return self.__data_storage.get_recipe_names()

    def get_ingredient_on_hopper_names(self) -> list[str]:
        """ returns list[<ingredient-name>]
            the individual hopper position is encoded into the list position of the name"""
        return self.__data_storage.get_ingredient_on_hopper_names()

    def get_recipe_dispensable_names(self) -> list[str]:
        """ returns list[<recipe-name>]"""
        return self.__data_storage.get_recipe_dispensable_names()

    # todo create the get_data_ui method
    def get_data_ui(self, __program_state: str):
        pass

    def get_data_logic(self, __program_state: str, __cmd: str):
        pass

    # todo we need ingredient data for calculating timings. But what kind of data should be returned

    ####################################################################################################################
    # Methods to change data
    ####################################################################################################################

    # todo transform input to the correct input
    def set_hopper(self, __hopper_position: int, __new_beverage_on_hopper_name: str):
        self.__data_storage.set_hopper(__hopper_position, __new_beverage_on_hopper_name)

    # todo change create_recipe input
    def create_recipe(self, __new_recipe_input: dict):
        """ <new-recipe-input>:= list[<recipe-name>,<beverage-name>,<fill-amount>,<beverage-name>,<fill-amount>,...]"""
        self.__data_storage.create_recipe(__new_recipe_input)
