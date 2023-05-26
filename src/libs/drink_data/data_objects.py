from .json_data import data_storage as Data
import re as RegularExpression


# todo add remaining amount to beverage and remember those changes

class Beverage:
    """ Beverage represents a drink that can be put on the hopper. Recipe is only used by RuntimeData"""
    __id: int
    __name: str
    __hopper_id: int | None
    __flow_speed: int

    def __init__(self, __id: int, __name: str, __hopper_id: int, __flow_speed: int):
        self.__id = __id
        self.__hopper_id = __hopper_id
        self.__name = __name
        self.__flow_speed = __flow_speed

    def __str__(self):
        return f"[{self.__name}, {self.__id}]"

    def get_id(self) -> int:
        return self.__id

    def get_name(self) -> str:
        return self.__name

    def get_hopper_id(self) -> int:
        return self.__hopper_id

    def get_flow_speed(self) -> int:
        return self.__flow_speed


class Recipe:
    """ Recipe represents a drink that is mixed with multiple beverages. Recipe is only used by RuntimeData """
    __id: int
    __name: str
    __needed_beverages_id: list[Beverage]
    __fill_perc_beverages: list[list[int]]  # list[list[<beverage-id>,<fill-amount(ml)>]]

    def __init__(self, __id: int, __name: str, __needed_beverages: list[Beverage], __fill_perc_beverages: list[[int]]):
        self.__id = __id
        self.__name = __name
        self.__needed_beverages_id = __needed_beverages
        self.__fill_perc_beverages = __fill_perc_beverages

    def __str__(self):
        return f"{self.__name}, {self.__id}"

    def get_id(self) -> int:
        return self.__id

    def get_name(self) -> str:
        return self.__name

    def get_needed_beverages_recipe(self) -> list[Beverage]:
        return self.__needed_beverages_id

    def get_fill_perc_recipe(self) -> list[list[int]]:
        return self.__fill_perc_beverages

    def get_fill_perc_beverage(self, __beverage_id: int) -> int:
        for __id_and_fill_amount in self.__fill_perc_beverages[0:]:
            if __id_and_fill_amount[0] == __beverage_id:
                return __id_and_fill_amount[1]


class RuntimeData:
    """RuntimeData is an aggregation of beverages and recipes."""
    __beverages: list[Beverage]
    __recipes: list[Recipe]
    __beverages_on_hopper: list[Beverage]
    __beverages_dispensable: list[Beverage]
    __recipes_dispensable: list[Recipe]
    __data_storage: Data  # object that provides drink_data to RuntimeData

    def __init__(self):
        self.__data_storage = Data.DataStorage()
        self.__update_beverages()
        self.__update_recipes()
        self.__update_beverages_on_hopper()
        self.__update_beverages_dispensable()
        self.__update_recipes_dispensable()

    ####################################################################################################################
    # the following methods are used to update the runtime drink_data
    ####################################################################################################################

    def __update_beverages(self):
        """ __update_beverages() is """
        __return_list: list[Beverage] = []
        __beverage_data: list[list[str]] = self.__data_storage.get_beverages()
        for __beverage in __beverage_data:
            __id = int(__beverage[0])
            __name = __beverage[1]
            if __beverage[2]:
                __hopper_id = int(__beverage[2])
            else:
                __hopper_id = None
            __flow_speed = int(__beverage[3])
            __return_list.append(Beverage(__id, __name, __hopper_id, __flow_speed))
        self.__beverages = __return_list

    def __update_recipes(self):
        __return_list: list[Recipe] = []
        __recipe_data: list[list[str]] = self.__data_storage.get_recipes()
        for __recipe in __recipe_data:
            __id = int(__recipe[0])
            __name = __recipe[1]
            __needed_beverages_str = __recipe[2]
            __fill_perc_beverages_str = __recipe[3]
            __needed_beverages = self.__transform_needed_beverages_str(__needed_beverages_str)
            __fill_perc_beverages = self.__transform_fill_perc_str(__fill_perc_beverages_str)
            __return_list.append(Recipe(__id, __name, __needed_beverages, __fill_perc_beverages))
        self.__recipes = __return_list

    def __update_beverages_on_hopper(self):
        __return_list: list[Beverage] = []
        __beverage_data: list[list[str]] = self.__data_storage.get_beverages_on_hopper()
        for __beverage in __beverage_data:
            __id = int(__beverage[0])
            __name = __beverage[1]
            __hopper_id = int(__beverage[2])
            __flow_speed = int(__beverage[3])
            __return_list.append(Beverage(__id, __name, __hopper_id, __flow_speed))
        self.__beverages_on_hopper = __return_list

    def __update_beverages_dispensable(self):
        __return_list: list[Beverage] = []
        __beverage_data: list[list[str]] = self.__data_storage.get_beverages_dispensable()
        for __beverage in __beverage_data:
            __id = int(__beverage[0])
            __name = __beverage[1]
            __hopper_id = int(__beverage[2])
            __flow_speed = int(__beverage[3])
            __return_list.append(Beverage(__id, __name, __hopper_id, __flow_speed))
        self.__beverages_dispensable = __return_list

    def __update_recipes_dispensable(self):
        __return_list: list[Recipe] = []
        __recipe_data: list[list[str]] = self.__data_storage.get_recipes_dispensable()
        for __recipe in __recipe_data:
            __id = int(__recipe[0])
            __name = __recipe[1]
            __needed_beverages_str = __recipe[2]
            __fill_perc_beverages_str = __recipe[3]
            __needed_beverages = self.__transform_needed_beverages_str(__needed_beverages_str)
            __fill_perc_beverages = self.__transform_fill_perc_str(__fill_perc_beverages_str)
            __return_list.append(Recipe(__id, __name, __needed_beverages, __fill_perc_beverages))
        self.__recipes_dispensable = __return_list

    def __transform_needed_beverages_str(self, __beverage_ids_str: str) -> list[Beverage]:
        __beverage_ids_list_str: list[str] = __beverage_ids_str.split(";")
        __beverage_ids_int: list[int] = [eval(__id) for __id in __beverage_ids_list_str]
        __result: list[Beverage] = []
        for __beverage_id_int in __beverage_ids_int:
            for __beverage in self.__beverages:
                if __beverage_id_int == __beverage.get_id():
                    __result.append(__beverage)
        return __result

    @staticmethod
    def __transform_fill_perc_str(__fill_perc_beverages_str: str):
        """ transforms the fill_perc str form data_storage to a fill_perc list[list[int]]"""
        __fill_perc_list_str: list[str] = __fill_perc_beverages_str.split(";")
        __fill_perc_list_int: list[int] = [eval(__string_element) for __string_element in __fill_perc_list_str]
        __result: list[list[int]] = []
        while len(__fill_perc_list_int) != 0:
            __id: int = __fill_perc_list_int.pop(0)
            __fill_amount: int = __fill_perc_list_int.pop(0)
            __result.append([__id, __fill_amount])
        return __result

    ####################################################################################################################
    #
    ####################################################################################################################

    ####################################################################################################################
    # The following methods are used by data_functions to provide drink_data
    # to the class DataInterface in data_functions
    ####################################################################################################################

    def get_beverage_names(self) -> list[str]:
        """ returns a list of all beverage names (beverage names are unique)"""
        __result: list[str] = []
        for __beverage in self.__beverages:
            __result.append(__beverage.get_name())
        return __result

    def get_recipe_names(self) -> list[str]:
        """ returns a list of all recipe names (recipe names are unique)"""
        __result: list[str] = []
        for __recipe in self.__recipes:
            __result.append(__recipe.get_name())
        return __result

    def get_dispensable_beverage_names(self) -> list[str]:
        """ returns a list of all recipe names (beverage names are unique)"""
        __result: list[str] = []
        for __dispensable_beverage in self.__beverages_dispensable:
            __result.append(__dispensable_beverage.get_name())
        return __result

    def get_dispensable_recipe_names(self) -> list[str]:
        """ returns a list of the names of all recipes that can be dispensed (recipe names are unique)"""
        __result: list[str] = []
        for __dispensable_recipe in self.__recipes_dispensable:
            __result.append(__dispensable_recipe.get_name())
        return __result

    def get_beverage_hopper_names(self) -> list[str]:
        """ returns a list of the names of all beverages that can be dispensed (beverage names are unique)"""
        __result: list[str] = ["not_used" for i in range(0, 12)]
        for __beverage_on_hopper in self.__beverages_on_hopper:
            __hopper_position: int = __beverage_on_hopper.get_hopper_id()
            __result[__hopper_position] = __beverage_on_hopper.get_name()
        return __result

    def create_recipe(self, __name: str, __name_and_amount: str):
        """ transforms the string input into int and list[list[int]] input and calls create_recipe"""
        __name_and_amount_list_str: list[str] = __name_and_amount.split(";")
        __needed_beverages: list[list[int]] = []
        while len(__name_and_amount_list_str) != 0:
            __id = int(__name_and_amount_list_str.pop(0))
            __amount = int(__name_and_amount_list_str.pop(0))
            __needed_beverages.append([__id, __amount])
        self.__data_storage.create_recipe(__name, __needed_beverages)
        self.__update_recipes()
        self.__update_recipes_dispensable()

    def set_beverage_hopper(self, __old_beverage_name: str, __new_beverage_name: str):
        self.__data_storage.set_beverage_hopper(__old_beverage_name, __new_beverage_name)
        self.__update_recipes_dispensable()
        self.__update_beverages()
        self.__update_beverages_on_hopper()
        self.__update_beverages_dispensable()
