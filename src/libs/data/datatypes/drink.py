from __future__ import annotations

from math import floor

from libs.data.datatypes.ingredient import Ingredient


class DrinkException(Exception):
    pass


class Drink:
    __drink_id: int = None
    __ingredients: list[(int, int)] = None
    """tuple(<ingredient_id>, <percentage>)"""
    name: str = None

    def __init__(self, drink_id: int, name: str, ingredients: list[(int, int)]):
        """
        :param drink_id: id of the drink
        :param name: name of the drink
        :param ingredients: list of ingredients: tuple(<ingredient_id>, <percentage>)
        """
        self.__drink_id = drink_id
        self.__ingredients = ingredients
        self.name = name

    def get_id(self) -> int:
        return self.__drink_id

    def get_ingredients(self) -> list[(int, int)]:
        """
        :return: list of ingredients: tuple(<ingredient_id>, <percentage>)
        """
        return self.__ingredients

    def add_ingredient(self, ingredient_id: int, percentage: int) -> None:
        """
        :param ingredient_id: ID of ingredient to add
        :param percentage: Percentage of ingredient to add

        :raise DrinkException: if ingredient already added to drink!
        """
        if self.__ingredients is None or len(self.__ingredients) == 0:
            self.__ingredients = []

        ingredients: dict[int, int] = dict(self.__ingredients)

        if ingredient_id in ingredients:
            raise DrinkException("Drink already added!")

        # scale existing ingredients (soft max of remaining total after new ingredient added)
        scaling_factor = (100 - percentage) / 100
        for key, share in ingredients.items():
            ingredients[key] = floor(share * scaling_factor)

        # add new ingredient ; adjust percentage to compensate rounding errors
        ingredients[ingredient_id] = 100 - sum(ingredients.values())

        self.__ingredients = [(k, v) for k, v in ingredients.items()]

    def remove_ingredient(self, ingredient_id: int):
        """
        :param ingredient_id: ingredient ID to remove

        :raise DrinkException: if ingredient is not part of the drink
        """
        if self.__ingredients is None or len(self.__ingredients) == 0:
            raise DrinkException("No ingredients found!")

        if len(self.__ingredients) == 1:
            self.__ingredients = []
            return

        ingredients: dict[int, int] = dict(self.__ingredients)

        if ingredient_id not in ingredients:
            raise DrinkException("Ingredient not found!")

        # scaling factor for soft max
        scaling_factor = 100 - ingredients[ingredient_id]

        # remove ingredient
        ingredients.pop(ingredient_id)

        # scale remaining ingredients (soft max of new total)
        for key, share in ingredients.items():
            ingredients[key] = floor(share / scaling_factor * 100)

        # adjust the lowest share to compensate rounding errors
        key = min(ingredients, key=ingredients.get)
        ingredients[key] += 100 - sum(ingredients.values())

        self.__ingredients = [(k, v) for k, v in ingredients.items()]

    def adjust_amount(self, ingredient_id: int, percentage: int):
        """
        :param ingredient_id: ID of ingredient to update
        :param percentage: new percentage of ingredient
        """
        # TODO: Adjust percentage of other ingredients
        # TODO: Adjust percentage of given ingredient
        raise NotImplementedError()
