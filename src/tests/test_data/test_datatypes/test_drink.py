from __future__ import annotations

import unittest

from libs.data.datatypes.drink import Drink


class TestDrink(unittest.TestCase):
    __drink_id: int = 1
    __ingredients: list[(int, int)] = [(1, 40), (2, 60)]
    __ingredients2: list[(int, int)] = [(1, 20), (2, 20), (3, 60)]
    __ingredients3: list[(int, int)] = [(1, 14), (2, 25), (3, 61)]
    __ingredients4: list[(int, int)] = [(3, 12), (7, 27), (12, 32), (33, 29)]
    name: str = "Tequila Sunrise"

    __drink: Drink = None
    __drink2: Drink = None
    __drink3: Drink = None
    __drink4: Drink = None
    def setUp(self):
        self.__drink = Drink(drink_id=self.__drink_id, name=self.name,
                             ingredients=self.__ingredients)
        self.__drink2 = Drink(drink_id=self.__drink_id, name=self.name,
                             ingredients=self.__ingredients2)
        self.__drink3 = Drink(drink_id=self.__drink_id, name=self.name,
                             ingredients=self.__ingredients3)
        self.__drink4 = Drink(drink_id=self.__drink_id, name=self.name,
                             ingredients=self.__ingredients4)

    def test_get_id_function(self):
        self.assertEqual(1, self.__drink.get_id())

    def test_get_ingredients_function(self):
        self.assertEqual([(1, 40), (2, 60)], self.__drink.get_ingredients())

    def test_remove_ingredient_function(self):
        self.__drink.remove_ingredient(2)
        self.assertEqual([(1, 100)], self.__drink.get_ingredients())

        self.__drink2.remove_ingredient(2)
        self.assertEqual([(1, 25), (3, 75)], self.__drink2.get_ingredients())

        self.__drink3.remove_ingredient(2)
        self.assertEqual([(1, 19), (3, 81)], self.__drink3.get_ingredients())

        self.__drink4.remove_ingredient(12)
        self.assertEqual([(3, 18), (7, 40), (33, 42)], self.__drink4.get_ingredients())

if __name__ == '__main__':
    unittest.main()
