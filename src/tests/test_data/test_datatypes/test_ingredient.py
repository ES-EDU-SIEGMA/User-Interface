from __future__ import annotations

import unittest

from libs.data.datatypes.ingredient import Ingredient


class TestIngredient(unittest.TestCase):
    __id: int = 178
    __flow_speed: int = 1
    __name: str = "Test Ingredient"
    __dispenser_id: int = 1

    ingredient: Ingredient = None

    def setUp(self):
        self.ingredient = Ingredient(
            ingredient_id=self.__id,
            name=self.__name,
            flow_speed=self.__flow_speed,
            dispenser_id=self.__dispenser_id,
        )

    def test_get_id(self):
        self.assertEqual(self.__id, self.ingredient.get_id())

    def test_get_name(self):
        self.assertEqual(self.__name, self.ingredient.name)

    def test_update_name(self):
        self.ingredient.name = "Updated Ingredient"
        self.assertEqual("Updated Ingredient", self.ingredient.name)

    def test_get_flow_speed(self):
        self.assertEqual(self.__flow_speed, self.ingredient.flow_speed)

    def test_update_flow_speed(self):
        self.ingredient.flow_speed += 10
        self.assertEqual(self.__flow_speed + 10, self.ingredient.flow_speed)

    def test_get_dispenser_id(self):
        self.assertEqual(self.__dispenser_id, self.ingredient.dispenser_id)

    def test_update_dispenser_id(self):
        self.ingredient.dispenser_id += 8
        self.assertEqual(self.__dispenser_id + 8, self.ingredient.dispenser_id)


if __name__ == "__main__":
    unittest.main()
