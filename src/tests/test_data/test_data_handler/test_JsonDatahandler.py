from __future__ import annotations

import unittest

from os.path import abspath as absolute_path, join, dirname, realpath
from libs.data.data_handler import JsonDatahandler as json_data_module
from libs.data.datatypes.drink import Drink
from libs.data.datatypes.ingredient import Ingredient

class TestJsonDatahandler(unittest.TestCase):

    __configuration_ingredient_file_path: str = absolute_path(
        join(dirname(realpath(__file__)), "test_ingredients.json")
    )

    __configuration_recipe_file_path: str = absolute_path(
        join(dirname(realpath(__file__)), "test_drinks.json")
    )

    __data_storage_object: json_data_module.JSONDatahandler = json_data_module.JSONDatahandler(
        __configuration_ingredient_file_path,
        __configuration_recipe_file_path,
    )

    def test_read_ingredients(self):
        __expected_result_list: list[Ingredient] = [(Ingredient(1, "Cola", 1, 2)),
                                      (Ingredient(2, "Sprite", 1, 1)),
                                      (Ingredient(3, "Fanta", 1, 1))]
        __expected_result = []

        for i in range(len(__expected_result_list)):
            __expected_result.append(dict(vars(__expected_result_list[i])))

        __received_result_list: list[Ingredient] = self.__data_storage_object.read_ingredients()

        __received_result = []

        for i in range(len(__received_result_list)):
            __received_result.append(dict(vars(__received_result_list[i])))

        self.assertEqual(__expected_result, __received_result)

    def test_read_drinks(self):
        __expected_result: list[Drink] = [(Drink(drink_id=1, name="Cherry_banana_juice", ingredients=list[(24, 50), (29, 50)])),
                                          (Drink(drink_id=2, name="Apple_spritzer", ingredients=list[(0, 60), (2, 40)]))]

        __received_result: list[Drink] = self.__data_storage_object.read_drinks()

        self.assertEqual(__expected_result, __received_result)

    def test_write_ingredients(self):

        __expected_result: list[Ingredient] = [(Ingredient(1, "Cola", 1, 2)),
                                      (Ingredient(2, "Sprite", 1, 1)),
                                      (Ingredient(3, "Fanta", 1, 1))]

        self.__data_storage_object.write_ingredients(__expected_result)

        __received_result: list[Ingredient] = self.__data_storage_object.read_ingredients()

        self.assertEqual(__expected_result, __received_result)

    def test_write_drinks(self):

        __expected_result: list[Drink] = [(Drink(drink_id=1, name="Cherry_banana_juice", ingredients=list[(24, 50), (29, 50)])),
                                          (Drink(drink_id=2, name="Apple_spritzer", ingredients=list[(0, 60), (2, 40)]))]

        self.__data_storage_object.write_drinks(__expected_result)

        __received_result: list[Drink] = self.__data_storage_object.read_drinks()

        self.assertEqual(__expected_result, __received_result)


if __name__ == '__main__':
    unittest.main()
