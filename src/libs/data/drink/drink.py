from src.libs.data.drink.ingredient import Ingredient


class Drink:

    __ID: int
    __ingredients: list[Ingredient]

    def __init__(self, ID, ingredients):
        self.__ID = ID
        self.__ingredients = ingredients
        self.__base_value = 0
