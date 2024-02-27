from __future__ import annotations

from libs.data.datatypes.drink import Drink
from libs.data.datatypes.ingredient import Ingredient
from libs.data.data_handler.IDatahandler import IDatahandler


class DataException(Exception):
    pass


class Data:
    __datahandler: IDatahandler = None
    __ingredients: list[Ingredient] = None
    __drinks: list[Drink] = None

    def __init__(self, datahandler: IDatahandler):
        self.__datahandler = datahandler
        self.__ingredients = self.__datahandler.read_ingredients()
        self.__drinks = self.__datahandler.read_drinks()

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
                raise DataException("Ingredient exists already!")

        self.__ingredients.append(ingredient)
        self.__datahandler.write_ingredients(self.__ingredients)

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
            raise DataException("Ingredient does not exist!")

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
        if drink not in self.__drinks:
            raise DataException("Drink exists already!")

        self.__drinks.append(drink)
        self.__datahandler.write_drinks(self.__drinks)

    def update_drink(self, drink: Drink) -> None:
        """
        :param drink: Drink to be updated

        :raises DataException: if drink does not exist
        """
        if drink not in self.__drinks:
            raise DataException("Drink does not exist!")

        for index, element in enumerate(self.__drinks):
            if element.get_id() == drink.get_id():
                self.__drinks[index] = drink
                return
