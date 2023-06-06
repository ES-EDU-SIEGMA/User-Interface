from . import data_objects as Data


class DataInterface:
    __runtime_data: Data.RuntimeData  # object to get drink_data from

    def __init__(self):
        self.__runtime_data = Data.RuntimeData()

    def get_beverage_names(self) -> list[str]:
        """ returns a list of all beverage names (beverage names are unique)"""
        return self.__runtime_data.get_beverage_names()

    def get_recipe_names(self) -> list[str]:
        """ returns a list of all recipe names (recipe names are unique)"""
        return self.__runtime_data.get_recipe_names()

    def get_dispensable_beverage_names(self) -> list[str]:
        """ returns a list of all recipe names (beverage names are unique)"""
        return self.__runtime_data.get_dispensable_beverage_names()

    def get_dispensable_recipe_names(self) -> list[str]:
        """ returns a list of the names of all recipes that can be dispensed (recipe names are unique)"""
        return self.__runtime_data.get_dispensable_recipe_names()

    def get_beverage_hopper_names(self) -> list[str]:
        """ returns a list of the names of all ingredients that can be dispensed (beverage names are unique)"""
        return self.__runtime_data.get_beverage_hopper_names()

    # todo maybe return bool on set cmds
    def create_recipe(self, __name: str, __name_and_amount: str):
        self.__runtime_data.create_recipe(__name, __name_and_amount)

    # currently create_beverage is not supported
    def create_beverage(self):
        pass

    # todo don't know whether this name1,2 thing is good
    def set_beverage_hopper(self, __old_beverage_name: str, __new_beverage_name: str):
        pass

    # idea for this is to create functionality that allows to manipulate already existing ingredients
    def change_beverage(self):
        pass

    # idea for this is to create functionality that allows to manipulate already existing recipes
    def change_recipe(self):
        pass
