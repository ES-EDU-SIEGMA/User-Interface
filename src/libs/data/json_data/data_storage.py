import json


class DataStorage:
    __json_drink_dict: dict = None

    def __init__(self):
        self.__update_drink_dict()

    def __update_drink_dict(self):
        try:
            with open("drink_list.json", "r") as jsonFile:
                self.__json_drink_dict = json.load(jsonFile)
        except Exception as error:
            print(error)
            return {}

    ########################################################################################################################
    #       The following methods are used to return data to the caller
    ########################################################################################################################
    def get_beverages(self) -> list[list[str]]:
        __result_list: list[list[str]] = []
        for __drink_id in self.__json_drink_dict:
            if self.__json_drink_dict[__drink_id]["mix_drink"] is False:
                __beverage_as_list = self.__create_beverage_as_list(__drink_id)
                __result_list.append(__beverage_as_list)
        return __result_list

    def get_recipe_names(self) -> list[list[str]]:
        __result_list: list[list[str]] = []
        for __drink_id in self.__json_drink_dict:
            if self.__json_drink_dict[__drink_id]["mix_drink"]:
                __recipe_as_list = self.__create_recipe_as_list(__drink_id)
                __result_list.append(__recipe_as_list)
        return __result_list

    def get_beverages_on_hopper(self) -> list[list[str]]:
        __result_list: list[list[str]] = []
        for __drink_id in self.__json_drink_dict:
            if self.__json_drink_dict[__drink_id]["hopper_id"] is not None:
                __beverage_as_list = self.__create_beverage_as_list(__drink_id)
                __result_list.append(__beverage_as_list)
        return __result_list

    def get_beverages_dispensable(self) -> list[list[str]]:
        __result_list: list[list[str]] = []
        for __drink_id in self.__json_drink_dict:
            if self.__json_drink_dict[__drink_id]["dispensable"]:
                __beverage_as_list = self.__create_beverage_as_list(__drink_id)
                __result_list.append(__beverage_as_list)
        return __result_list

    def get_recipes_dispensable(self) -> list[list[str]]:
        __result_list: list[list[str]] = []
        for __drink_id in self.__json_drink_dict:
            if self.__json_drink_dict[__drink_id]["dispensable"]:
                __recipe_as_list = self.__create_recipe_as_list(__drink_id)
                __result_list.append(__recipe_as_list)
        return __result_list

    def __create_beverage_as_list(self, __drink_id: str) -> list[str]:
        __result_beverage: list[str] = [
            self.__json_drink_dict[__drink_id]["id"],
            self.__json_drink_dict[__drink_id]["name"],
            self.__json_drink_dict[__drink_id]["hopper_id"],
            self.__json_drink_dict[__drink_id]["flow_speed"],
        ]
        return __result_beverage

    def __create_recipe_as_list(self, __drink_id: str) -> list[str]:
        __result_recipe: list[str] = [
            self.__json_drink_dict[__drink_id]["id"],
            self.__json_drink_dict[__drink_id]["name"],
            self.__needed_beverages_id_to_string(
                self.__json_drink_dict[__drink_id]["needed_beverages"]
            ),
            self.__fill_perc_beverages_to_string(
                self.__json_drink_dict[__drink_id]["fill_perc"]
            ),
        ]
        return __result_recipe

    @staticmethod
    def __needed_beverages_id_to_string(__list: list[list[int]]) -> str:
        __result_string_list = []
        for __item in __list:
            __result_string_list.append(str(__item[0]))
        return ";".join(__result_string_list)

    @staticmethod
    def __fill_perc_beverages_to_string(__list: list[list[int]]) -> str:
        __result_string_list = []
        for __item in __list:
            __result_string_list.append(str(__item[0]))
            __result_string_list.append(str(__item[1]))
        return ";".join(__result_string_list)


########################################################################################################################
#       the following methods are used to change data
########################################################################################################################


def write_drink_list(new_drink_list: dict):
    try:
        with open("drink_list", "w") as jsonFile:
            json.dump(new_drink_list, jsonFile, indent=4)
    except Exception as error:
        print(error)
