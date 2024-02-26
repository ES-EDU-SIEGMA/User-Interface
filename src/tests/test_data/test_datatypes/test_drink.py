from __future__ import annotations

import unittest

from libs.data.datatypes.drink import Drink, DrinkException


class TestDrink(unittest.TestCase):
    __id: int = 178
    __name: str = "Test Drink"
    __ingredients: list[(int, int)] = [(1, 25), (3, 50), (2, 25)]
    drink: Drink = None

    def setUp(self):
        self.drink = Drink(
            drink_id=self.__id, name=self.__name, ingredients=self.__ingredients
        )

    def test_get_id(self):
        self.assertEqual(self.__id, self.drink.get_id())

    def test_get_name(self):
        self.assertEqual(self.__name, self.drink.name)

    def test_update_name(self):
        self.drink.name = "Updated Drink"
        self.assertEqual("Updated Drink", self.drink.name)

    def test_get_ingredients(self):
        self.assertEqual(self.__ingredients, self.drink.get_ingredients())

    def test_add_ingredient_drink_already_exists(self):
        self.assertRaises(
            DrinkException,
            self.drink.add_ingredient,
            ingredient_id=self.__ingredients[1][0],
            percentage=self.__ingredients[1][1],
        )

    def test_add_ingredient_on_empty_ingredients(self):
        drink = Drink(drink_id=self.__id, name=self.__name, ingredients=[])
        drink.add_ingredient(ingredient_id=5, percentage=90)
        self.assertListEqual([(5, 100)], drink.get_ingredients())

    def test_add_ingredient_without_rounding(self):
        self.drink.add_ingredient(20, 40)
        expected_list = [(1, 15), (3, 30), (2, 15), (20, 40)]
        self.assertListEqual(expected_list, self.drink.get_ingredients())

    def test_add_ingredient_with_rounding(self):
        self.drink.add_ingredient(20, 33)
        expected_list = [(1, 16), (3, 33), (2, 16), (20, 35)]
        self.assertListEqual(expected_list, self.drink.get_ingredients())

    def test_remove_ingredient_drink_not_existing(self):
        self.assertRaises(
            DrinkException, self.drink.remove_ingredient, ingredient_id=25
        )

    def test_remove_ingredient_from_empty_list(self):
        drink = Drink(drink_id=self.__id, name=self.__name, ingredients=[])
        self.assertRaises(DrinkException, drink.remove_ingredient, ingredient_id=25)

    def test_remove_ingredient_without_rounding(self):
        self.drink.remove_ingredient(ingredient_id=3)
        self.assertListEqual([(1, 50), (2, 50)], self.drink.get_ingredients())

    def test_remove_ingredient_with_rounding(self):
        self.drink.remove_ingredient(1)
        self.assertListEqual([(3, 66), (2, 34)], self.drink.get_ingredients())

    def test_remove_ingredient_empty_list_remaining(self):
        for ingredient in self.__ingredients:
            self.drink.remove_ingredient(ingredient_id=ingredient[0])
        self.defaultTestResult()


if __name__ == "__main__":
    unittest.main()
