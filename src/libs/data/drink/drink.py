from src.libs.data.drink.ingredient import Ingredient


class Drink:
    __id_: int
    __ingredients: list[Ingredient]

    def __init__(self, id_, ingredients):
        self.__id_ = id_
        self.__ingredients = ingredients
        self.__base_value = 0

    def get_id(self) -> int:
        """
        :return: Drink-ID
        """
        return self.__id_
