from __future__ import annotations

import unittest

from libs.data.data import Data, DataException, DataExceptionID, DataExceptionName
from libs.data.data_handler.IDatahandler import IDatahandler
from libs.data.datatypes.drink import Drink
from libs.data.datatypes.ingredient import Ingredient


class DatahandlerMock(IDatahandler):
    __ingredients: list[Ingredient] = None
    __drinks: list[Drink] = None

    def __init__(self, drinks: list[Drink], ingredients: list[Ingredient]):
        self.__drinks = list.copy(drinks)
        self.__ingredients = list.copy(ingredients)

    def read_ingredients(self) -> list[Ingredient]:
        return self.__ingredients

    def write_ingredients(self, ingredients: list[Ingredient]) -> None:
        pass

    def read_drinks(self) -> list[Drink]:
        return self.__drinks

    def write_drinks(self, drinks: list[Drink]) -> None:
        pass


class TestData(unittest.TestCase):
    __expected_ingredients: list[Ingredient] = [
        Ingredient(1, "Cola", 1, 2),
        Ingredient(2, "Sprite", 1, 1),
        Ingredient(3, "Fanta", 1, None),
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
    __data_handler: IDatahandler = None
    data: Data = None

    def setUp(self):
        if self.shortDescription() == "empty ingredients":
            self.__data_handler = DatahandlerMock(
                ingredients=[], drinks=self.__expected_drinks
            )
        elif self.shortDescription() == "empty drinks":
            self.__data_handler = DatahandlerMock(
                ingredients=self.__expected_ingredients, drinks=[]
            )
        elif self.shortDescription() == "empty sources":
            self.__data_handler = DatahandlerMock(ingredients=[], drinks=[])
        else:
            self.__data_handler = DatahandlerMock(
                ingredients=self.__expected_ingredients,
                drinks=self.__expected_drinks,
            )
        self.data = Data(data_handler=self.__data_handler)

    def test_get_ingredients_for_empty_list(self):
        """empty ingredients"""
        self.assertListEqual([], self.data.get_ingredients())

    def test_get_ingredients_successful(self):
        for index, element in enumerate(self.data.get_ingredients()):
            self.assertEqual(
                element.get_id(), self.__expected_ingredients[index].get_id()
            )
            self.assertEqual(element.name, self.__expected_ingredients[index].name)
            self.assertEqual(
                element.flow_speed, self.__expected_ingredients[index].flow_speed
            )
            self.assertEqual(
                element.dispenser_id, self.__expected_ingredients[index].dispenser_id
            )

    def test_add_ingredient_raises_exception_id_exists(self):
        ingredient = self.__expected_ingredients[1]
        ingredient.name += "_modified"
        self.assertRaises(
            DataExceptionID,
            self.data.add_ingredient,
            ingredient=ingredient,
        )

    def test_add_ingredient_raises_exception_name_exists(self):
        ingredient = Ingredient(
            ingredient_id=len(self.__expected_ingredients),
            name=self.__expected_ingredients[1].name,
            flow_speed=self.__expected_ingredients[1].flow_speed,
            dispenser_id=None,
        )
        self.assertRaises(
            DataExceptionName,
            self.data.add_ingredient,
            ingredient=ingredient,
        )

    def test_add_ingredient_successful(self):
        ingredient = Ingredient(
            len(self.__expected_ingredients) + 1,
            name="NEW Ingredient",
            flow_speed=1,
            dispenser_id=None,
        )
        self.data.add_ingredient(ingredient=ingredient)
        self.assertEqual(
            len(self.__expected_ingredients) + 1, len(self.data.get_ingredients())
        )
        self.assertEqual(ingredient, self.data.get_ingredients()[-1])

    def test_update_ingredients_raises_exception(self):
        ingredient = Ingredient(
            len(self.__expected_ingredients) + 1,
            name="NEW Ingredient",
            flow_speed=1,
            dispenser_id=None,
        )
        self.assertRaises(
            DataException,
            self.data.update_ingredient,
            ingredient=ingredient,
        )

    def test_update_ingredients_successful(self):
        ingredient = self.__expected_ingredients[-1]
        ingredient.name += "modified"
        self.data.update_ingredient(ingredient)
        self.assertEqual(ingredient, self.data.get_ingredients()[-1])

    def test_get_drinks_for_empty_list(self):
        """empty drinks"""
        self.assertListEqual([], self.data.get_drinks())

    def test_get_drinks_successful(self):
        for index, item in enumerate(self.data.get_drinks()):
            self.assertEqual(item.get_id(), self.__expected_drinks[index].get_id())
            self.assertEqual(item.name, self.__expected_drinks[index].name)
            self.assertEqual(
                item.get_ingredients(), self.__expected_drinks[index].get_ingredients()
            )

    def test_get_drink_successful(self):
        drink = self.data.get_drink(drink_id=self.__expected_drinks[0].get_id())
        self.assertEqual(drink.get_id(), self.__expected_drinks[0].get_id())
        self.assertEqual(drink.name, self.__expected_drinks[0].name)
        self.assertEqual(
            drink.get_ingredients(), self.__expected_drinks[0].get_ingredients()
        )

    def test_add_drink_raises_exception_id_exists(self):
        drink = self.__expected_drinks[-1]
        drink.name += "_modified"
        self.assertRaises(
            DataExceptionID,
            self.data.add_drink,
            drink=drink,
        )

    def test_add_drink_raises_exception_name_exists(self):
        drink = Drink(
            drink_id=len(self.__expected_drinks) + 1,
            name=self.__expected_drinks[0].name,
            ingredients=self.__expected_drinks[0].get_ingredients(),
        )
        self.assertRaises(
            DataExceptionName,
            self.data.add_drink,
            drink=drink,
        )

    def test_add_drink_successful(self):
        drink = Drink(
            drink_id=len(self.__expected_drinks) + 1,
            name=self.__expected_drinks[0].name + "_modified",
            ingredients=[],
        )
        print(f"{len(self.__expected_drinks)} -- {len(self.data.get_drinks())}")
        self.data.add_drink(drink=drink)
        print(f"{len(self.__expected_drinks)} -- {len(self.data.get_drinks())}")
        self.assertEqual(len(self.__expected_drinks) + 1, len(self.data.get_drinks()))
        self.assertEqual(drink, self.data.get_drinks()[-1])

    def test_update_drinks_raises_exception(self):
        drink = Drink(
            drink_id=len(self.__expected_drinks) + 1,
            name=self.__expected_drinks[0].name + "_modified",
            ingredients=[],
        )
        self.assertRaises(
            DataException,
            self.data.update_drink,
            drink=drink,
        )

    def test_update_drinks_successful(self):
        drink = self.__expected_drinks[-1]
        drink.name += "_modified"
        self.data.update_drink(drink)
        self.assertEqual(drink, self.data.get_drinks()[-1])


if __name__ == "__main__":
    unittest.main()
