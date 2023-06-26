from __future__ import annotations

from os.path import abspath as absolute_path, join, dirname, realpath
from libs.data import data_interface as data_interface_module
import unittest


class TestDataInterfaceGetMethods(unittest.TestCase):
    __configuration_ingredients: dict = {
        "test_ingredient_1": {"hopper_position": None, "amount": 100},
        "test_ingredient_2": {"hopper_position": 0, "amount": 200},
        "test_ingredient_3": {"hopper_position": 1, "amount": 300},
        "test_ingredient_4": {"hopper_position": None, "amount": 0},
    }
    __configuration_ingredient_file_path: str = absolute_path(
        join(dirname(realpath(__file__)), "test_json_data", "test_ingredients.json")
    )

    __configuration_recipe_file_path: str = absolute_path(
        join(dirname(realpath(__file__)), "test_json_data", "test_recipes.json")
    )

    __data_object: data_interface_module.DataInterface = (
        data_interface_module.DataInterface(
            __configuration_ingredients,
            __configuration_ingredient_file_path,
            __configuration_recipe_file_path,
        )
    )

    def test_get_data_ui_selection(self):
        __expected_result: list[str] = ["test_recipe_2"]
        __received_result: list[str] = self.__data_object.get_data_ui("selection")

        self.assertEqual(__expected_result, __received_result)

    def test_get_data_ui_edit(self):
        __expected_ingredient_on_hopper_names: list[str | None] = [None] * 12
        __expected_ingredient_on_hopper_names[0] = "test_ingredient_2"
        __expected_ingredient_on_hopper_names[1] = "test_ingredient_3"
        __expected_ingredient_names: list[str] = [
            "test_ingredient_1",
            "test_ingredient_2",
            "test_ingredient_3",
            "test_ingredient_4",
            "test_ingredient_5",
        ]

        __expected_result: list[list[str]] = [
            __expected_ingredient_on_hopper_names,
            __expected_ingredient_names,
        ]
        __received_result: list[list[str]] = self.__data_object.get_data_ui("edit")

        self.assertEqual(__expected_result, __received_result)

    def test_get_data_ui_new(self):
        __expected_ingredient_names: list[str] = [
            "test_ingredient_1",
            "test_ingredient_2",
            "test_ingredient_3",
            "test_ingredient_4",
            "test_ingredient_5",
        ]
        __expected_recipe_names: list[str] = ["test_recipe_1", "test_recipe_2"]
        __expected_result: list[list[str]] = [
            __expected_ingredient_names,
            __expected_recipe_names,
        ]
        __received_result: list[list[str]] = self.__data_object.get_data_ui("new")


class TestDataInterfaceSetMethod(unittest.TestCase):
    __configuration_ingredients: dict = {
        "test_ingredient_1": {"hopper_position": None, "amount": 100},
        "test_ingredient_2": {"hopper_position": 0, "amount": 200},
        "test_ingredient_3": {"hopper_position": 1, "amount": 300},
        "test_ingredient_4": {"hopper_position": None, "amount": 0},
    }

    __configuration_ingredient_file_path: str = absolute_path(
        join(dirname(realpath(__file__)), "test_json_data", "test_ingredients.json")
    )

    __configuration_recipe_file_path: str = absolute_path(
        join(dirname(realpath(__file__)), "test_json_data", "test_recipes.json")
    )

    __data_object: data_interface_module.DataInterface = (
        data_interface_module.DataInterface(
            __configuration_ingredients,
            __configuration_ingredient_file_path,
            __configuration_recipe_file_path,
        )
    )

    def test_set_hopper(self):
        self.__data_object.set_hopper(
            {"hopper_position": 0, "ingredient_name": "test_ingredient_1"}
        )

        __expected_ingredient_on_hopper_names: list[str | None] = [None] * 12
        __expected_ingredient_on_hopper_names[0] = "test_ingredient_1"
        __expected_ingredient_on_hopper_names[1] = "test_ingredient_3"
        __expected_ingredient_names: list[str] = [
            "test_ingredient_1",
            "test_ingredient_2",
            "test_ingredient_3",
            "test_ingredient_4",
            "test_ingredient_5",
        ]
        __expected_recipe_names: list[str] = ["test_recipe_1", "test_recipe_2"]

        __expected_get_selection: list[str] = []
        __received_get_selection: list[str] = self.__data_object.get_data_ui(
            "selection"
        )

        __expected_get_edit: list[list[str]] = [
            __expected_ingredient_on_hopper_names,
            __expected_ingredient_names,
        ]
        __received_get_edit: list[list[str]] = self.__data_object.get_data_ui("edit")

        __expected_get_new: list[list[str]] = [
            __expected_ingredient_names,
            __expected_recipe_names,
        ]
        __received_get_new: list[list[str]] = self.__data_object.get_data_ui("new")

        self.assertEqual(__expected_get_selection, __received_get_selection)
        self.assertEqual(__expected_get_edit, __received_get_edit)
        self.assertEqual(__expected_get_new, __received_get_new)


class TestDataInterfaceCreateMethod(unittest.TestCase):
    __configuration_ingredients: dict = {
        "test_ingredient_1": {"hopper_position": None, "amount": 100},
        "test_ingredient_2": {"hopper_position": 0, "amount": 200},
        "test_ingredient_3": {"hopper_position": 1, "amount": 300},
        "test_ingredient_4": {"hopper_position": None, "amount": 0},
    }

    __configuration_ingredient_file_path: str = absolute_path(
        join(dirname(realpath(__file__)), "test_json_data", "test_ingredients.json")
    )

    __configuration_recipe_file_path: str = absolute_path(
        join(dirname(realpath(__file__)), "test_json_data", "test_recipes.json")
    )

    __data_object: data_interface_module.DataInterface = (
        data_interface_module.DataInterface(
            __configuration_ingredients,
            __configuration_ingredient_file_path,
            __configuration_recipe_file_path,
        )
    )

    def test_create_recipe(self):
        __data: dict = {
            "test_recipe_3": {
                "test_ingredient_1": {"fill_amount": 100},
                "test_ingredient_3": {"fill_amount": 30},
            }
        }
        self.__data_object.create_recipe(__data)

        __expected_ingredient_on_hopper_names: list[str | None] = [None] * 12
        __expected_ingredient_on_hopper_names[0] = "test_ingredient_2"
        __expected_ingredient_on_hopper_names[1] = "test_ingredient_3"
        __expected_ingredient_names: list[str] = [
            "test_ingredient_1",
            "test_ingredient_2",
            "test_ingredient_3",
            "test_ingredient_4",
            "test_ingredient_5",
        ]
        __expected_recipe_names: list[str] = [
            "test_recipe_1",
            "test_recipe_2",
            "test_recipe_3",
        ]

        __expected_get_selection: list[str] = ["test_recipe_2"]
        __received_get_selection: list[str] = self.__data_object.get_data_ui(
            "selection"
        )

        __expected_get_edit: list[list[str]] = [
            __expected_ingredient_on_hopper_names,
            __expected_ingredient_names,
        ]
        __received_get_edit: list[list[str]] = self.__data_object.get_data_ui("edit")

        __expected_get_new: list[list[str]] = [
            __expected_ingredient_names,
            __expected_recipe_names,
        ]
        __received_get_new: list[list[str]] = self.__data_object.get_data_ui("new")

        self.assertEqual(__expected_get_selection, __received_get_selection)
        self.assertEqual(__expected_get_edit, __received_get_edit)
        self.assertEqual(__expected_get_new, __received_get_new)


if __name__ == "__main__":
    unittest.main()
