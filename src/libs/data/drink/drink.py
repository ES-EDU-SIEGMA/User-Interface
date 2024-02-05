from src.libs.data.drink.ingredient import Ingredient


class Drink:
    __id_: int
    __ingredients: list[Ingredient, int]

    def __init__(self, id_, ingredients):
        self.__id_ = id_
        self.__ingredients = ingredients
        self.__base_value = 0

    def get_id(self) -> int:
        return self.__id_

    def get_ingredients(self) -> list:
        """
        :return: Ingredient list from the selected drink
        """
        return self.__ingredients

    def add_ingredient(self, ingredient_id: int, percentage: int):
        """
        :param ingredient_id:
        :param percentage:
        """
        if percentage > 100:
            percentage = 100

        self.__ingredients.append([ingredient_id, percentage])

    def remove_ingredient(self, ingredient_id: int):
        """
        :param ingredient_id:
        """
        self.__ingredients.remove([ingredient_id])

    def adjust_amount(self, ingredient_id: int, percentage: int):
        """
        :param ingredient_id:
        :param percentage:
        """