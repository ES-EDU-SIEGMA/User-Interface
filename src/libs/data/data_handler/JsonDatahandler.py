from __future__ import annotations

import json

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
        return list(self.__read(self.__path_to_ingredients).values())

    def write_ingredients(self, ingredients: list[Ingredient]) -> None:
        self.__write(self.__path_to_ingredients, ingredients)

    def read_drinks(self) -> list[Drink]:
        return list(self.__read(self.__path_to_drinks).values())

    def write_drinks(self, drinks: list[Drink]) -> None:
        self.__write(self.__path_to_drinks, dict(drinks))

    def __write(self, path_to_file: str, data: dict) -> None:
        try:
            with open(
                    file=path_to_file, mode="w"
            ) as __json_recipes:
                return json.dump(data)

        except Exception as __error:
            print(
                f"produced an error while reading in the recipe file.\nerror: {__error}"
            )
            return {}

    def __read(self, path_to_file: str) -> dict:
        try:
            with open(
                file=path_to_file, mode="r"
            ) as __json_recipes:
                return json.load(__json_recipes)

        except Exception as __error:
            print(
                f"produced an error while reading in the recipe file.\nerror: {__error}"
            )
            return {}
