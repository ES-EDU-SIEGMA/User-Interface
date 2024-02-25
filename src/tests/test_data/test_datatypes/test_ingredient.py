from __future__ import annotations

import unittest

from libs.data.datatypes.ingredient import Ingredient

class TestIngredient(unittest.TestCase):
    __ingredient_id: int = 1
    name: str = "Sprite"
    flow_speed: int = 1
    dispenser_id: int = 1

    __ingredient: Ingredient = None

    def setUp(self):
        self.__ingredient = Ingredient(ingredient_id=self.__ingredient_id, name=self.name,
                                       flow_speed=self.flow_speed, dispenser_id=self.dispenser_id)

    def test_get_id_function(self):
        self.assertEqual(1, self.__ingredient.get_id())


if __name__ == '__main__':
    unittest.main()
