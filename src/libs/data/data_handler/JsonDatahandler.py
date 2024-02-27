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
        ingredients_dict = (self.__read(self.__path_to_ingredients))["ingredients"]

        ingredients: list[Ingredient] = []
        for item in ingredients_dict:
            ingredients.append(
                Ingredient(
                    ingredient_id=item["id"],
                    name=item["name"],
                    flow_speed=item["flow_speed"],
                    dispenser_id=item["dispenser_id"],
                )
            )

        return ingredients

    def write_ingredients(self, ingredients: list[Ingredient]) -> None:
        ingredients_dict = {"ingredients": []}

        for ingredient in ingredients:
            item: dict = {
                "id": ingredient.get_id(),
                "name": ingredient.name,
                "flow_speed": ingredient.flow_speed,
                "dispenser_id": ingredient.dispenser_id,
            }
            ingredients_dict["ingredients"].append(item)

        self.__write(self.__path_to_ingredients, ingredients_dict)

    def read_drinks(self) -> list[Drink]:
        drinks_dict = (self.__read(self.__path_to_drinks))["drinks"]

        drinks: list[Drink] = []
        for item in drinks_dict:
            drinks.append(
                Drink(
                    drink_id=item["id"],
                    name=item["name"],
                    ingredients=self.__unmarshal_drink_ingredients(
                        ingredients=item["ingredients"]
                    ),
                )
            )

        return drinks

    def write_drinks(self, drinks: list[Drink]) -> None:
        drink_list = {"drinks": []}

        for drink in drinks:
            item: dict = {
                "id": drink.get_id(),
                "name": drink.name,
                "ingredients": self.__marshal_drink_ingredients(
                    drink.get_ingredients()
                ),
            }
            drink_list["drinks"].append(item)

        self.__write(self.__path_to_drinks, drink_list)

    @staticmethod
    def __unmarshal_drink_ingredients(
        ingredients: list[dict[str, int]]
    ) -> list[(int, int)]:
        ingredients_list: list[(int, int)] = []
        for item in ingredients:
            ingredients_list.append((int(item["id"]), int(item["percentage"])))

        return ingredients_list

    @staticmethod
    def __marshal_drink_ingredients(
        ingredients: list[(int, int)]
    ) -> list[dict[str, int]]:
        ingredients_dict: list[dict[str, int]] = []
        for item in ingredients:
            ingredients_dict.append({"id": item[0], "percentage": item[1]})

        return ingredients_dict

    @staticmethod
    def __write(path_to_file: str, data: dict) -> None:
        with open(path_to_file, "w") as out_file:
            json.dump(data, out_file, indent=4)

    @staticmethod
    def __read(path_to_file: str) -> dict:
        with open(path_to_file, "r") as in_file:
            data = json.load(in_file)
        return data
