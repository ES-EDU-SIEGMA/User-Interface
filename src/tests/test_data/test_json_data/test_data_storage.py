import unittest

import pytest

from libs.data.data_json import data_storage as Json_data_module


@pytest.fixture
def __data_storage_object() -> Json_data_module.DataStorage:
    __configuration_ingredients: dict = {
        "test_ingredient_1": {"hopper_position": 0, "amount": 100},
        "test_ingredient_2": {"hopper_position": 1, "amount": 0},
        "test_ingredient_3": {"hopper_position": None, "amount": 300},
        "test_ingredient_4": {"hopper_position": None, "amount": 0},
    }
    __configuration_ingredient_file_path: str = "libs/tests/test_data/test_json_data/ingredients.json"
    __configuration_recipe_file_path: str = "libs/tests/test_data/test_json_data/recipes.json"
    __return: Json_data_module.DataStorage = Json_data_module.DataStorage(__configuration_ingredients,
                                                                                       __configuration_ingredient_file_path,
                                                                                       __configuration_recipe_file_path)
    return __return


class DataStorageGetMethods(unittest.TestCase):

    """def test_get_ingredient_name(self, __data_storage_object):
        __received_result: list[str] = __data_storage_object.get_ingredient_names()
        __expected_result: list[str] = ["test_ingredient_1", "test_ingredient_2", "test_ingredient_3",
                                        "test_ingredient_4",
                                        "test_ingredient_5"]
        self.assertEqual(__received_result, __expected_result)

    def test_get_recipe_names(self, __data_storage_object):
        __received_result: list[str] = __data_storage_object.get_recipe_names()
        __expected_result: list[str] = ["test_recipe_1", "test_recipe_2"]
        self.assertEqual(__received_result, __expected_result)"""

    def test


if __name__ == '__main__':
    unittest.main()
