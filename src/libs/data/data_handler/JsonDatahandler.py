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

        ingredients_dict = self.__read(self.__path_to_ingredients)

        # convert dictionary to list
        ingredients: list[Ingredient] = []
        for key, item in ingredients_dict.items():
            ingredients.append(Ingredient(ingredient_id=key, name=item, flow_speed=key, dispenser_id=key))

        return ingredients

    def write_ingredients(self, ingredients: list[Ingredient]) -> None:
        ingredient_list = []

        for i in range(len(ingredients)):
            ingredient_list.append(dict(vars(ingredients[i])))

        self.__write(self.__path_to_ingredients, {"ingridients": ingredient_list})

    def read_drinks(self) -> list[Drink]:
        drinks_dict = self.__read(self.__path_to_ingredients)

        # convert dictionary to list
        drinks: list[Drink] = []
        for key, item in drinks_dict.items():
            drinks.append(Drink(drink_id=key, name=item, ingredients=item))

        return drinks

    def write_drinks(self, drinks: list[Drink]) -> None:
        drink_list = []

        for i in range(len(drinks)):
            drink_list.append(dict(vars(drinks[i])))

        self.__write(self.__path_to_drinks, {"drinks": drink_list})


    def __write(self, path_to_file: str, data: dict) -> None:
        with open(path_to_file, "w") as out_file:
            json.dump(data, out_file, indent=4)

    def __read(self, path_to_file: str) -> dict:
        with open(path_to_file, "r") as out_file:
            return json.load(out_file)

