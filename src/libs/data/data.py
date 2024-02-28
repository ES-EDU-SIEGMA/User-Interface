from __future__ import annotations

from libs.data.datatypes.drink import Drink
from libs.data.datatypes.ingredient import Ingredient
from libs.data.data_handler.IDatahandler import IDatahandler


class DataExceptionID(Exception):
    pass


class DataExceptionName(Exception):
    pass


class Data:
    __data_handler: IDatahandler = None
    __ingredients: list[Ingredient] = None
    __drinks: list[Drink] = None

    def __init__(self, datahandler: IDatahandler):
        self.__data_handler = datahandler
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
        for index in range(len(self.__ingredients)):
            if ingredient.get_id() == self.__ingredients[index].get_id():
                raise DataExceptionID("Ingredient-ID or Name exists already!")
            if ingredient.name == self.__ingredients[index].name:
                raise DataExceptionName("Ingredient-Name exists already!")

        self.__ingredients.append(ingredient)
        self.__data_handler.write_ingredients(self.__ingredients)

    def update_ingredient(self, ingredient: Ingredient) -> None:
        """
        :param ingredient: ingredient to be updated

        :raises DataException: if ingredient does not exist
        """
        counter: int = 0
        for index in range(len(self.__ingredients)):
            if ingredient.get_id() != self.__ingredients[index].get_id():
                counter += 1
        if counter == len(self.__ingredients):
            raise DataExceptionID("Ingredient does not exist!")

        for index, element in enumerate(self.__ingredients):
            if element.get_id() == ingredient.get_id():
                self.__ingredients[index] = ingredient
                return

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
        for index in range(len(self.__drinks)):
            if drink.get_id() == self.__drinks[index].get_id():
                raise DataExceptionID("Drink-ID exists already!")
            if drink.name == self.__drinks[index].name:
                raise DataExceptionName("Drink-Name exists already!")

        self.__drinks.append(drink)
        self.__data_handler.write_drinks(self.__drinks)

    def update_drink(self, drink: Drink) -> None:
        """
        :param drink: Drink to be updated

        :raises DataException: if drink does not exist
        """
        counter: int = 0
        for index in range(len(self.__drinks)):
            if drink.get_id() != self.__drinks[index].get_id():
                counter += 1
        if counter == len(self.__drinks):
            raise DataExceptionID("Drink does not exist!")

        for index, element in enumerate(self.__drinks):
            if element.get_id() == drink.get_id():
                self.__drinks[index] = drink
                return
