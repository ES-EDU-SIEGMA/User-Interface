from __future__ import annotations

import unittest
from os.path import abspath as absolute_path, join, dirname, realpath

from libs.data.data import Data, DataException
from libs.data.datatypes.drink import Drink
from libs.data.datatypes.ingredient import Ingredient
from libs.data.data_handler.IDatahandler import IDatahandler
from libs.data.data_handler.JsonDatahandler import JSONDatahandler

class TestData(unittest.TestCase):
    __ingredient_read_sources: str = absolute_path(
        join(dirname(realpath(__file__)), "../json_data/test_ingredients_data.json")
    )
    __ingredient_read_sources_empty: str = absolute_path(
        join(dirname(realpath(__file__)), "../json_data/test_ingredients_empty.json")
    )
    __ingredient_write_sources: str = absolute_path(
        join(dirname(realpath(__file__)), "../json_data/test_ingredients_write.json")
    )

    __drinks_read_sources: str = absolute_path(
        join(dirname(realpath(__file__)), "../json_data/test_drinks_data.json")
    )
    __drinks_read_sources_empty: str = absolute_path(
        join(dirname(realpath(__file__)), "../json_data/test_drinks_empty.json")
    )
    __drinks_write_sources: str = absolute_path(
        join(dirname(realpath(__file__)), "../json_data/test_drinks_write.json")
    )

    __data_handler: IDatahandler = JSONDatahandler(
        path_to_ingredients=__ingredient_read_sources, path_to_drinks=__drinks_read_sources
    )

    __expected_ingredients_empty: list[Ingredient] = [
    ]
    __expected_ingredients: list[Ingredient] = [
        Ingredient(1, "Cola", 1, 2),
        Ingredient(2, "Sprite", 1, 1),
        Ingredient(3, "Fanta", 1, None)
    ]
    __expected_ingredient_added: list[Ingredient] = [
        Ingredient(1, "Cola", 1, 2),
        Ingredient(2, "Sprite", 1, 1),
        Ingredient(3, "Fanta", 1, None),
        Ingredient(5, "Cola", 1, 2)
    ]
    __expected_ingredient_updated: list[Ingredient] = [
        Ingredient(1, "Vodka", 1, 2),
        Ingredient(2, "Sprite", 1, 1),
        Ingredient(3, "Fanta", 1, None)
    ]

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
    __expected_drinks_empty: list[Drink] = [
    ]
    data: Data = None
    ingredient_new: Ingredient = None
    ingredient_exists: Ingredient = None
    ingredient_update: Ingredient = None

    def setUp(self):
        self.data = Data(datahandler=self.__data_handler)
        self.ingredient_new = Ingredient(5, "Cola", 1, 2)
        self.ingredient_exists = Ingredient(1, "Cola", 1, 2)
        self.ingredient_update = Ingredient(1, "Vodka", 1, 2)

    def test_get_ingredients_for_empty_list(self):
        datahandler = JSONDatahandler(
            path_to_ingredients=self.__ingredient_read_sources_empty,
            path_to_drinks=self.__drinks_read_sources_empty,
        )
        data_empty = Data(datahandler=datahandler)

        self.assertEqual(len(self.__expected_ingredients_empty), len(data_empty.get_ingredients()))

    def test_get_ingredients_successful(self):
        for index, item in enumerate(self.data.get_ingredients()):
            self.assertEqual(item.get_id(), self.__expected_ingredients[index].get_id())
            self.assertEqual(item.name, self.__expected_ingredients[index].name)
            self.assertEqual(
                item.flow_speed, self.__expected_ingredients[index].flow_speed
            )
            self.assertEqual(
                item.dispenser_id, self.__expected_ingredients[index].dispenser_id
            )

    def test_add_ingredient_raises_exception(self):
        #todo Exception also if name exists?
        self.assertRaises(
            DataException,
            self.data.add_ingredient,
            ingredient=self.ingredient_exists,
        )
        self.__data_handler.write_ingredients(self.__expected_ingredients)

    def test_add_ingredient_successful(self):
        self.data.add_ingredient(self.ingredient_new)

        for index, item in enumerate(self.data.get_ingredients()):
            self.assertEqual(item.get_id(), self.__expected_ingredient_added[index].get_id())
            self.assertEqual(item.name, self.__expected_ingredient_added[index].name)
            self.assertEqual(
                item.flow_speed, self.__expected_ingredient_added[index].flow_speed
            )
            self.assertEqual(
                item.dispenser_id, self.__expected_ingredient_added[index].dispenser_id
            )

        self.__data_handler.write_ingredients(self.__expected_ingredients)


    def test_update_ingredients_raises_exception(self):
        self.assertRaises(
            DataException,
            self.data.update_ingredient,
            ingredient=self.ingredient_new,
        )
        self.__data_handler.write_ingredients(self.__expected_ingredients)

    def test_update_ingredients_successful(self):
        self.data.update_ingredient(self.ingredient_update)

        for index, item in enumerate(self.data.get_ingredients()):
            self.assertEqual(item.get_id(), self.__expected_ingredient_updated[index].get_id())
            self.assertEqual(item.name, self.__expected_ingredient_updated[index].name)
            self.assertEqual(
                item.flow_speed, self.__expected_ingredient_updated[index].flow_speed
            )
            self.assertEqual(
                item.dispenser_id, self.__expected_ingredient_updated[index].dispenser_id
            )

        self.__data_handler.write_ingredients(self.__expected_ingredients)


    def test_get_drinks_for_empty_list(self):
        pass

    def test_get_drinks_successful(self):
        pass

    def test_get_drink_successful(self):
        pass

    def test_add_drink_raises_exception(self):
        pass

    def test_add_drink_successful(self):
        pass

    def test_update_drinks_raises_exception(self):
        pass

    def test_update_drinks_successful(self):
        pass


if __name__ == "__main__":
    unittest.main()
