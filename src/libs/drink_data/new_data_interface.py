from .new_data_json import data_storage as Data


class DataInterface:
    __data_storage: Data.DataStorage

    def __init__(self, __hopper_position_and_amount: dict):
        self.__data_storage = Data.DataStorage(__hopper_position_and_amount)
        print("initializing DataInterface")

    ####################################################################################################################
    # Methods to access data
    ####################################################################################################################

    def get_data_ui(self, __program_state: str) -> list[str] | list[list[str]]:

        match __program_state:
            case "selection":
                __return_value: list[str] = self.__data_storage.get_recipe_dispensable_names()
                return __return_value
            case "edit":
                __return_value: list[list[str]] = [self.__data_storage.get_ingredient_on_hopper_names(),
                                                   self.__data_storage.get_ingredient_names()]
                return __return_value
            case "new":
                __return_value: list[list[str]] = [self.__data_storage.get_ingredient_names(),
                                                   self.__data_storage.get_recipe_names()]
                return __return_value

    def get_data_logic(self, __program_state: str, __recipe_name: str) -> list[list[int]]:

        match __program_state:
            case "selection":
                __return_value: list[list[int]] = self.__data_storage.get_required_ingredient_information(__recipe_name)
                return __return_value
    # todo we need ingredient data for calculating timings. But what kind of data should be returned

    ####################################################################################################################
    # Methods to change data
    ####################################################################################################################

    # todo transform input to the correct input
    def set_hopper(self, __hopper_position: int, __new_beverage_on_hopper_name: str):
        self.__data_storage.set_hopper(__hopper_position, __new_beverage_on_hopper_name)

    # todo change create_recipe input
    def create_recipe(self, __new_recipe_information: list[str]):

        __new_recipe_name: str = __new_recipe_information.pop(0)
        __new_recipe: dict = {__new_recipe_name: {}}
        # __new_recipe := dict{ <recipe-name>: dict{ <ingredient-name>: dict{fill_amount: int}}}
        __new_recipe_list = __new_recipe_information[0].split(";")
        # __new_recipe_list:= list[<ingredient-name>,<fill_amount>,<ingredient-name>,<fill_amount>,...]

        while __new_recipe_list:
            # check if there are still elements in __new_recipe_information

            __ingredient_name: str = __new_recipe_list.pop(0)
            __fill_amount: int = int(__new_recipe_list.pop(0))
            __new_recipe[__new_recipe_name][__ingredient_name] = {}
            __new_recipe[__new_recipe_name][__ingredient_name]["fill_amount"] = __fill_amount

        self.__data_storage.create_recipe(__new_recipe)
