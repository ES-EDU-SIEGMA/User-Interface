from __future__ import annotations

from libs.data.data_handler.IDatahandler import IDatahandler
from libs.data.datatypes.drink import Drink
from libs.data.datatypes.ingredient import Ingredient


class DataException(Exception):
    pass


class DataExceptionID(DataException):
    pass


class DataExceptionName(DataException):
    pass


class Data:
    __data_handler: IDatahandler = None
    __ingredients: list[Ingredient] = None
    __drinks: list[Drink] = None

    def __init__(self, data_handler: IDatahandler):
        self.__data_handler = data_handler
        self.__ingredients = self.__data_handler.read_ingredients()
        self.__drinks = self.__data_handler.read_drinks()

    def get_ingredients(self) -> list[Ingredient]:
        """
        :return: list of ingredients
        """
        return self.__ingredients

    def add_ingredient(self, ingredient: Ingredient) -> None:
        """
        :param ingredient: ingredient to be added

        :raises DataException: if ingredient already exists
        """
        for element in self.__ingredients:
            if ingredient.get_id() == element.get_id():
                raise DataExceptionID("Ingredient-ID or Name exists already!")
            if ingredient.name == element.name:
                raise DataExceptionName("Ingredient-Name exists already!")

        self.__ingredients.append(ingredient)
        self.__data_handler.write_ingredients(self.__ingredients)

    def update_ingredient(self, ingredient: Ingredient) -> None:
        """
        :param ingredient: ingredient to with updated data

        :raises DataException: if ingredient does not exist
        """
        for index, element in enumerate(self.__ingredients):
            if element.get_id() == ingredient.get_id():
                self.__ingredients[index] = ingredient
                break
        else:
            # only executed if no matching ingredient were found
            raise DataException("Ingredient does not exist!")

    def get_drinks(self) -> list[Drink]:
        """
        return: list of drinks
        """
        return self.__drinks

    def get_drink(self, drink_id: int) -> Drink | None:
        """
        :param drink_id: ID of drink to get data from

        :return: Drink or None if drink does not exist
        """
        for drink in self.__drinks:
            if drink.get_id() == drink_id:
                return drink
        return None

    def add_drink(self, drink: Drink) -> None:
        """
        :param drink: Drink to be added

        :raises DataException: if drink already exists
        """
        for element in self.__drinks:
            if drink.get_id() == element.get_id():
                raise DataExceptionID("Drink-ID exists already!")
            if drink.name == element.name:
                raise DataExceptionName("Drink-Name exists already!")

        self.__drinks.append(drink)
        self.__data_handler.write_drinks(self.__drinks)

    def update_drink(self, drink: Drink) -> None:
        """
        :param drink: Drink to be updated

        :raises DataException: if drink does not exist
        """
        for index, element in enumerate(self.__drinks):
            if element.get_id() == drink.get_id():
                self.__drinks[index] = drink
                break
        else:
            # only executed if no matching drink were found
            raise DataException("Drink does not exist!")
