from __future__ import annotations

from libs.data.data_handler.IDatahandler import IDatahandler
from libs.data.datatypes.drink import Drink
from libs.data.datatypes.ingredient import Ingredient


class JSONDatahandler(IDatahandler):
    __path_to_ingredients: str = None
    __path_to_drinks: str = None

    def __init__(self, path_to_ingredients: str, path_to_drinks: str):
        """
        :param path_to_ingredients: absolute path to ingredients json file
        :param path_to_drinks: absolute path to recipes json file
        """
        self.__path_to_ingredients = path_to_ingredients
        self.__path_to_drinks = path_to_drinks

    def read_ingredients(self) -> list[Ingredient]:
        # TODO: implement
        raise NotImplementedError()

    def write_ingredients(self, ingredients: list[Ingredient]) -> None:
        # TODO: implement
        raise NotImplementedError()

    def read_drinks(self) -> list[Drink]:
        # TODO: implement
        raise NotImplementedError()

    def write_drinks(self, drinks: list[Drink]) -> None:
        # TODO: implement
        raise NotImplementedError()

    def __write(self, path_to_file: str, data: dict) -> None:
        # TODO: implement
        raise NotImplementedError()

    def __read(self, path_to_file: str) -> dict:
        # TODO: implement
        raise NotImplementedError()
