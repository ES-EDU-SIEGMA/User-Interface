from .data_json import data_storage as Data


class DataInterface:
    __data_storage: Data.DataStorage

    def __init__(self, __configuration_ingredients: dict,
                 __configuration_ingredient_file_path: str,
                 __configuration_recipe_file_path: str):

        self.__data_storage = Data.DataStorage(__configuration_ingredients,
                                               __configuration_ingredient_file_path,
                                               __configuration_recipe_file_path)

    def close(self):
        pass

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

    ####################################################################################################################
    # Methods to change data
    ####################################################################################################################

    def set_hopper(self, __data: dict):
        # __data := {hopper_position: <position>, ingredient_name: <name>}

        __hopper_position: int = __data["hopper_position"]
        __ingredient_name: str = __data["ingredient_name"]
        self.__data_storage.set_hopper(__hopper_position, __ingredient_name)

    def create_recipe(self, __data: dict):
        # __data := {<recipe-name>: {<ingredient-name>: {fill_amount: <fill-amount>}}}

        self.__data_storage.create_recipe(__data)
