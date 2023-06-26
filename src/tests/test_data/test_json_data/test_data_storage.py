from __future__ import annotations

from os.path import abspath as absolute_path, join, dirname, realpath
from libs.data.data_json import data_storage as json_data_module
import unittest


########################################################################################################################
# test methods to get data
########################################################################################################################


class TestDataStorageGetMethods(unittest.TestCase):
    __configuration_ingredients: dict = {
        "test_ingredient_1": {"hopper_position": None, "amount": 100},
        "test_ingredient_2": {"hopper_position": 0, "amount": 200},
        "test_ingredient_3": {"hopper_position": 1, "amount": 300},
        "test_ingredient_4": {"hopper_position": None, "amount": 0},
    }

    __configuration_ingredient_file_path: str = absolute_path(
        join(dirname(realpath(__file__)), "test_ingredients.json")
    )

    __configuration_recipe_file_path: str = absolute_path(
        join(dirname(realpath(__file__)), "test_recipes.json")
    )

    __data_storage_object: json_data_module.DataStorage = json_data_module.DataStorage(
        __configuration_ingredients,
        __configuration_ingredient_file_path,
        __configuration_recipe_file_path,
    )

    def test_get_ingredient_names(self):
        __expected_result: list[str] = [
            "test_ingredient_1",
            "test_ingredient_2",
            "test_ingredient_3",
            "test_ingredient_4",
            "test_ingredient_5",
        ]
        __received_result: list[str] = self.__data_storage_object.get_ingredient_names()

        self.assertEqual(__expected_result, __received_result)

    def test_get_recipe_names(self):
        __expected_result: list[str] = ["test_recipe_1", "test_recipe_2"]
        __received_result: list[str] = self.__data_storage_object.get_recipe_names()

        self.assertEqual(__expected_result, __received_result)

    def test_get_ingredients_on_hopper_names(self):
        __expected_result: list[str | None] = [None] * 12
        __expected_result[0] = "test_ingredient_2"
        __expected_result[1] = "test_ingredient_3"
        __received_result: list[
            str
        ] = self.__data_storage_object.get_ingredient_on_hopper_names()

        self.assertEqual(__expected_result, __received_result)

    def test_get_recipe_dispensable_names(self):
        __expected_result: list[str] = ["test_recipe_2"]
        __received_result: list[
            str
        ] = self.__data_storage_object.get_recipe_dispensable_names()

        self.assertEqual(__expected_result, __received_result)

    def test_get_dispense_data(self):
        __expected_result: dict = {
            "0": {"fill_amount": 20, "flow_speed": 2},
            "1": {"fill_amount": 100, "flow_speed": 1},
        }
        __received_result: dict = self.__data_storage_object.get_dispense_data(
            "test_recipe_2"
        )

        self.assertEqual(__expected_result, __received_result)


########################################################################################################################
# test method to set the hopper
########################################################################################################################


class TestDataStorageSetMethod(unittest.TestCase):
    __configuration_ingredients: dict = {
        "test_ingredient_1": {"hopper_position": None, "amount": 100},
        "test_ingredient_2": {"hopper_position": 0, "amount": 200},
        "test_ingredient_3": {"hopper_position": 1, "amount": 300},
        "test_ingredient_4": {"hopper_position": None, "amount": 0},
    }

    __configuration_ingredient_file_path: str = absolute_path(
        join(dirname(realpath(__file__)), "test_ingredients.json")
    )

    __configuration_recipe_file_path: str = absolute_path(
        join(dirname(realpath(__file__)), "test_recipes.json")
    )

    __data_storage_object: json_data_module.DataStorage = json_data_module.DataStorage(
        __configuration_ingredients,
        __configuration_ingredient_file_path,
        __configuration_recipe_file_path,
    )

    def test_set_hopper(self):
        self.__data_storage_object.set_hopper(0, "test_ingredient_1")

        __expected_result_ingredient_on_hopper_names: list[str | None] = [None] * 12
        __expected_result_ingredient_on_hopper_names[0] = "test_ingredient_1"
        __expected_result_ingredient_on_hopper_names[1] = "test_ingredient_3"
        __received_result_ingredient_on_hopper_names: list[
            str
        ] = self.__data_storage_object.get_ingredient_on_hopper_names()

        __expected_result_dispensable_recipe_names: list[str] = []
        __received_result_dispensable_recipe_names: list[
            str
        ] = self.__data_storage_object.get_recipe_dispensable_names()

        self.assertEqual(
            __expected_result_ingredient_on_hopper_names,
            __received_result_ingredient_on_hopper_names,
        )
        self.assertEqual(
            __expected_result_dispensable_recipe_names,
            __received_result_dispensable_recipe_names,
        )


########################################################################################################################
# test method to create a recipe
########################################################################################################################


class TestDataStorageCreateMethod(unittest.TestCase):
    __configuration_ingredients: dict = {
        "test_ingredient_1": {"hopper_position": None, "amount": 100},
        "test_ingredient_2": {"hopper_position": 0, "amount": 200},
        "test_ingredient_3": {"hopper_position": 1, "amount": 300},
        "test_ingredient_4": {"hopper_position": None, "amount": 0},
    }

    __configuration_ingredient_file_path: str = absolute_path(
        join(dirname(realpath(__file__)), "test_ingredients.json")
    )

    __configuration_recipe_file_path: str = absolute_path(
        join(dirname(realpath(__file__)), "test_recipes.json")
    )

    __data_storage_object: json_data_module.DataStorage = json_data_module.DataStorage(
        __configuration_ingredients,
        __configuration_ingredient_file_path,
        __configuration_recipe_file_path,
    )

    def test_create_recipe(self):
        __data: dict = {
            "test_recipe_3": {
                "test_ingredient_1": {"fill_amount": 100},
                "test_ingredient_3": {"fill_amount": 30},
            }
        }
        self.__data_storage_object.create_recipe(__data)

        __expected_result_recipes: list[str] = [
            "test_recipe_1",
            "test_recipe_2",
            "test_recipe_3",
        ]
        __received_result_recipes: list[
            str
        ] = self.__data_storage_object.get_recipe_names()

        __expected_result_dispensable_recipe_names: list[str] = ["test_recipe_2"]
        __received_result_dispensable_recipe_names: list[
            str
        ] = self.__data_storage_object.get_recipe_dispensable_names()

        self.assertEqual(__expected_result_recipes, __received_result_recipes)
        self.assertEqual(
            __expected_result_dispensable_recipe_names,
            __received_result_dispensable_recipe_names,
        )


if __name__ == "__main__":
    unittest.main()
