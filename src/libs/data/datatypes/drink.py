from __future__ import annotations


class Drink:
    __drink_id: int = None
    __ingredients: list[(int, int)] = None
    """tuple(<ingredient_id>, <percentage>)"""
    name: str = None

    def __init__(self, drink_id, name, ingredients):
        self.__drink_id = drink_id
        self.name = name
        self.__ingredients = ingredients

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
        """
        # TODO: Check sum of all ingredients to 100 !
        # TODO: update list
        raise NotImplementedError()

    def remove_ingredient(self, ingredient_id: int):
        """
        :param ingredient_id: ingredient ID to remove
        """
        # TODO: adjust percentage of other ingredients
        # TODO: update list
        raise NotImplementedError()

    def adjust_amount(self, ingredient_id: int, percentage: int):
        """
        :param ingredient_id: ID of ingredient to update
        :param percentage: new percentage of ingredient
        """
        # TODO: Adjust percentage of other ingredients
        # TODO: Adjust percentage of given ingredient
        raise NotImplementedError()
