from json_data import data_storage as Data


class Beverage:
    __id: int
    __name: str
    __hopper_id: int
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
    __beverages: list[Beverage] = None
    __recipes: list[Recipe] = None
    __beverages_on_hopper: list[Beverage] = None
    __beverages_dispensable: list[Beverage] = None
    __recipes_dispensable: list[Recipe] = None
    __data_storage: Data = None

    def __init__(self):
        self.__data_storage = Data.DataStorage()
        self.__update_beverages()
        self.__update_recipes()
        self.__update_beverages_on_hopper()
        self.__update_beverages_dispensable()
        self.__update_recipes_dispensable()

    def __update_beverages(self):
        __return_list: list[Beverage] = []
        __beverage_data: list[list[str]] = self.__data_storage.get_beverages()
        for __beverage in __beverage_data:
            __id = int(__beverage[0])
            __name = __beverage[1]
            __hopper_id = int(__beverage[2])
            __flow_speed = int(__beverage[3])
            __return_list.append(Beverage(__id, __name, __hopper_id, __flow_speed))
        self.__beverages = __return_list

    def __update_recipes(self):
        __return_list: list[Recipe] = []
        __recipe_data: list[list[str]] = self.__data_storage.get_recipe_names()
        for __recipe in __recipe_data:
            __id = int(__recipe[0])
            __name = __recipe[1]
            __needed_beverages = __recipe[2]
            __fill_perc_beverages = __recipe[3]  # Todo think about whether the data is right here
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
        __recipe_data = self.__data_storage.get_recipes_dispensable()
        for __recipe in __recipe_data:
            __id = int(__recipe[0])
            __name = __recipe[1]
            __needed_beverages = __recipe[2]
            __fill_perc_beverages = __recipe[3]  # Todo think about whether the data is right here
            __return_list.append(Recipe(__id, __name, __needed_beverages, __fill_perc_beverages))
        self.__recipes_dispensable = __return_list

    def __create_beverages(self, __beverage_ids: list[str]):
        __int_id_list = [eval(__id) for __id in __beverage_ids]
        __result = []
        for __beverage_id in __int_id_list:
            __id = self.__beverages[__beverage_id]

            __reult.append(Beverage())
            # todo fix that


    def get_recipes(self) -> list[Recipe]:
        return self.__recipes

    def get_beverages(self) -> list[Beverage]:
        return self.__beverages

    def get_beverages_on_hopper(self) -> list[Beverage]:
        return self.__beverages_on_hopper

    def get_beverages_dispensable(self) -> list[Beverage]:
        return self.__beverages_dispensable

    def get_recipes_dispensable(self) -> list[Recipe]:
        return self.__recipes_dispensable
