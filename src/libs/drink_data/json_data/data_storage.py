import json
import re as RegularExpression


class DataStorage:
    __json_drink_dict: dict
    __free_ids: list[int]

    def __init__(self):
        self.__get_drink_dict()
        self.__determine_if_dispensable()
        self.__determine_free_ids()

    def __get_drink_dict(self):
        try:
            with open(file="libs/drink_data/json_data/drink_list.json", mode="r") as jsonFile:
                self.__json_drink_dict = json.load(jsonFile)
        except Exception as error:
            print(error)
            return {}

    def __determine_if_dispensable(self):
        pass

    def __determine_free_ids(self):
        __list_int: list[int] = [i for i in range(0, (len(self.__json_drink_dict) + 20))]
        __used_ids: list[int] = [int(__drink_id_str) for __drink_id_str in self.__json_drink_dict]
        self.__free_ids: list[int] = [__id for __id in __list_int if __id not in __used_ids]

    ####################################################################################################################
    # the following methods are used to return drink_data to the class RuntimeData
    ####################################################################################################################
    def get_beverages(self) -> list[list[str]]:
        """ returns a list of ingredients. Each beverage is a list of strings"""
        __result_list: list[list[str]] = []
        for __drink_id_str in self.__json_drink_dict:
            if self.__json_drink_dict[__drink_id_str]["mix_drink"] is False:
                __beverage_as_list = self.__create_beverage_as_list(__drink_id_str)
                __result_list.append(__beverage_as_list)
        return __result_list

    def get_recipes(self) -> list[list[str]]:
        """ returns a list of recipes. Each recipe is a list of strings"""
        __result_list: list[list[str]] = []
        for __drink_id_str in self.__json_drink_dict:
            if self.__json_drink_dict[__drink_id_str]["mix_drink"]:
                __recipe_as_list = self.__create_recipe_as_list(__drink_id_str)
                __result_list.append(__recipe_as_list)
        return __result_list

    def get_beverages_on_hopper(self) -> list[list[str]]:
        """ returns a list of ingredients that are on the hopper. Each beverage is a list of strings"""
        __result_list: list[list[str]] = []
        for __drink_id_str in self.__json_drink_dict:
            if self.__json_drink_dict[__drink_id_str]["hopper_id"] is not None:
                __beverage_as_list = self.__create_beverage_as_list(__drink_id_str)
                __result_list.append(__beverage_as_list)
        return __result_list

    def get_beverages_dispensable(self) -> list[list[str]]:
        """ returns a list of ingredients that are dispensable. Each beverage is a list of strings"""
        __result_list: list[list[str]] = []
        for __drink_id_str in self.__json_drink_dict:
            if self.__json_drink_dict[__drink_id_str]["dispensable"]:
                __beverage_as_list = self.__create_beverage_as_list(__drink_id_str)
                __result_list.append(__beverage_as_list)
        return __result_list

    def get_recipes_dispensable(self) -> list[list[str]]:
        """ returns a list of recipes that are dispensable. Each recipe is a list of strings"""
        __result_list: list[list[str]] = []
        for __drink_id_str in self.__json_drink_dict:
            if (self.__json_drink_dict[__drink_id_str]["dispensable"] and
                    self.__json_drink_dict[__drink_id_str]["mix_drink"]):
                __recipe_as_list = self.__create_recipe_as_list(__drink_id_str)
                __result_list.append(__recipe_as_list)
        return __result_list

    ####################################################################################################################
    #
    ####################################################################################################################

    def __create_beverage_as_list(self, __beverage_id_str: str) -> list[str]:
        """ returns a beverage as a list to the given beverage id"""
        __result_beverage_as_list: list[str] = [
            self.__json_drink_dict[__beverage_id_str]["id"],
            self.__json_drink_dict[__beverage_id_str]["name"],
            self.__json_drink_dict[__beverage_id_str]["hopper_id"],
            self.__json_drink_dict[__beverage_id_str]["flow_speed"],
        ]
        return __result_beverage_as_list

    def __create_recipe_as_list(self, __recipe_id_str: str) -> list[str]:
        """ returns a recipe as a list to the given recipe id"""
        __result_recipe_as_list: list[str] = [
            self.__json_drink_dict[__recipe_id_str]["id"],
            self.__json_drink_dict[__recipe_id_str]["name"],
            self.__needed_beverages_id_to_string(
                self.__json_drink_dict[__recipe_id_str]["needed_beverages"]
            ),
            self.__fill_perc_beverages_to_string(
                self.__json_drink_dict[__recipe_id_str]["needed_beverages"]
            ),
        ]
        return __result_recipe_as_list

    @staticmethod
    def __needed_beverages_id_to_string(__list: list[list[int]]) -> str:
        __result_string_list = []
        for __item in __list:
            __result_string_list.append(str(__item[0]))
        __result = ";".join(__result_string_list)
        return __result

    @staticmethod
    def __fill_perc_beverages_to_string(__list: list[list[int]]) -> str:
        __result_string_list = []
        for __item in __list:
            __result_string_list.append(str(__item[0]))  # id
            __result_string_list.append(str(__item[1]))  # amount
        __result: str = ";".join(__result_string_list)
        return __result

    ####################################################################################################################
    #       the following methods are used to change drink_data
    ####################################################################################################################

    def __update_drink_dict(self):
        try:
            with open("drink_list.json", "w") as jsonFile:
                json.dump(self.__json_drink_dict, jsonFile, indent=4)
                self.__determine_if_dispensable()
        except Exception as error:
            print(error)

    def create_recipe(self, __name: str, __needed_beverages: list[list[int]]):
        __id: int = self.__find_free_id()
        __new_recipe: dict = {
            "id": __id,
            "name": __name,
            "hopper_id": None,
            "dispensable": False,
            "flow_speed": None,
            "mix_drink": True,
            "needed_beverages": __needed_beverages}
        self.__json_drink_dict[str(__id)]: dict = __new_recipe
        self.__update_drink_dict()

    # todo we might want to make the assumption that a new drink on the hopper is full
    def set_beverage_hopper(self, __old_beverage_name: str, __new_beverage_name: str):
        """ __old_beverage_id and __new_beverage_id can refer to the same drink.
            receives either a beverage name or a string of the form hopper_<int>"""
        if RegularExpression.search("^hopper_", __old_beverage_name):
            for __drink_id_str in self.__json_drink_dict:
                if self.__json_drink_dict[__drink_id_str]["name"] == __new_beverage_name:
                    self.__json_drink_dict[__drink_id_str]["hopper_id"] = __old_beverage_name.split("_")[1]

        elif RegularExpression.search("^hopper_", __new_beverage_name):
            for __drink_id_str in self.__json_drink_dict:
                if self.__json_drink_dict[__drink_id_str]["name"] == __new_beverage_name:
                    self.__json_drink_dict[__drink_id_str]["hopper_id"] = None

        else:
            __hopper_id_to_change = None  # int
            for __drink_id_str in self.__json_drink_dict:
                if self.__json_drink_dict[__drink_id_str]["name"] == __old_beverage_name:
                    __hopper_id_to_change = self.__json_drink_dict[__drink_id_str]["hopper_id"]
                    self.__json_drink_dict[__drink_id_str]["hopper_id"] = None
                if self.__json_drink_dict[__drink_id_str]["name"] == __old_beverage_name:
                    self.__json_drink_dict[__drink_id_str]["hopper_id"] = __hopper_id_to_change

    def __find_free_id(self) -> int:
        if len(self.__free_ids) == 0:
            self.__determine_free_ids()
        return self.__free_ids.pop(0)
