from __future__ import annotations

import unittest
from os.path import abspath as absolute_path, join, dirname, realpath
from os import remove

from libs.data.data_handler.JsonDatahandler import JSONDatahandler
from libs.data.datatypes.drink import Drink
from libs.data.datatypes.ingredient import Ingredient


class TestJsonDatahandler(unittest.TestCase):
    __ingredient_read_sources: str = absolute_path(
        join(dirname(realpath(__file__)), "../json_data/test_ingredients_data_handler.json")
    )
    __ingredient_write_sources: str = absolute_path(
        join(dirname(realpath(__file__)), "../json_data/test_ingredients_write.json")
    )
    __expected_ingredients: list[Ingredient] = [
        Ingredient(1, "Cola", 1, 2),
        Ingredient(2, "Sprite", 1, 1),
        Ingredient(3, "Fanta", 1, None),
    ]

    __drinks_read_sources: str = absolute_path(
        join(dirname(realpath(__file__)), "../json_data/test_drinks_data_handler.json")
    )
    __drinks_write_sources: str = absolute_path(
        join(dirname(realpath(__file__)), "../json_data/test_drinks_write.json")
    )
    __expected_drinks: list[Drink] = [
        Drink(
            drink_id=1,
            name="Cherry Banana Juice",
            ingredients=[(24, 50), (29, 50)],
        ),
        Drink(
            drink_id=2,
            name="Apple Spritzer",
            ingredients=[],
        ),
    ]

    data_storage_object: JSONDatahandler = None

    def setUp(self):
        self.data_storage_object = JSONDatahandler(
            path_to_ingredients=self.__ingredient_read_sources,
            path_to_drinks=self.__drinks_read_sources,
        )

    def test_read_ingredients(self):
        for index, item in enumerate(self.data_storage_object.read_ingredients()):
            self.assertEqual(item.get_id(), self.__expected_ingredients[index].get_id())
            self.assertEqual(item.name, self.__expected_ingredients[index].name)
            self.assertEqual(
                item.flow_speed, self.__expected_ingredients[index].flow_speed
            )
            self.assertEqual(
                item.dispenser_id, self.__expected_ingredients[index].dispenser_id
            )

    def test_write_ingredients(self):
        datahandler = JSONDatahandler(
            path_to_ingredients=self.__ingredient_write_sources,
            path_to_drinks=self.__drinks_write_sources,
        )
        datahandler.write_ingredients(ingredients=self.__expected_ingredients)
        with open(self.__ingredient_read_sources, "r") as expected, open(
            self.__ingredient_write_sources, "r"
        ) as result:
            expected_data = expected.read()
            result_data = result.read()
            self.assertMultiLineEqual(expected_data, result_data)

        remove(self.__ingredient_write_sources)

    def test_read_drinks(self):
        for index, item in enumerate(self.data_storage_object.read_drinks()):
            self.assertEqual(item.get_id(), self.__expected_drinks[index].get_id())
            self.assertEqual(item.name, self.__expected_drinks[index].name)
            self.assertListEqual(
                item.get_ingredients(), self.__expected_drinks[index].get_ingredients()
            )

    def test_write_drinks(self):
        datahandler = JSONDatahandler(
            path_to_ingredients=self.__ingredient_write_sources,
            path_to_drinks=self.__drinks_write_sources,
        )
        datahandler.write_drinks(drinks=self.__expected_drinks)
        with open(self.__drinks_read_sources, "r") as expected, open(
            self.__drinks_write_sources, "r"
        ) as result:
            expected_data = expected.read()
            result_data = result.read()
            self.assertMultiLineEqual(expected_data, result_data)

        remove(self.__drinks_write_sources)


if __name__ == "__main__":
    unittest.main()
