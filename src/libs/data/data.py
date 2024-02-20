from __future__ import annotations

from libs.data.datatypes.drink import Drink
from libs.data.datatypes.ingredient import Ingredient
from libs.data.data_handler.IDatahandler import IDatahandler


class Data:
    __datahandler: IDatahandler = None
    __ingredients: list[Ingredient] = None
    __drinks: list[Drink] = None

    def __init__(self, datahandler: IDatahandler):
        # TODO: load ingredients from JSON
        # TODO: load drinks from JSON
        raise NotImplementedError()

    def get_ingredients(self) -> list[Ingredient]:
        return self.__ingredients

    def add_ingredient(self, ingredient: Ingredient) -> None:
        # TODO: implement (add to list & store in JSON)
        raise NotImplementedError()

    def update_ingredient(self, ingredient: Ingredient) -> None:
        # TODO: implement (update list & store in JSON)
        raise NotImplementedError()

    def get_drinks(self) -> list[Drink]:
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
        # TODO: implement (add to list & store in JSON)
        raise NotImplementedError()

    def update_drink(self, drink: Drink) -> None:
        # TODO: implement (update list & store in JSON)
        raise NotImplementedError()
