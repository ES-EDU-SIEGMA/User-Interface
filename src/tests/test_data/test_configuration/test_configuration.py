from __future__ import annotations

import unittest
import json
from os.path import abspath as absolute_path, join, dirname, realpath


class TestConfigurationFile(unittest.TestCase):
    __path_to_configuration = absolute_path(
        join(dirname(realpath(__file__)), "..", "..", "..", "configuration.json")
    )
    __path_to_ingredients = absolute_path(
        join(
            dirname(realpath(__file__)),
            "..",
            "..",
            "..",
            "libs",
            "data",
            "data_json",
            "ingredients.json",
        )
    )

    __configuration: dict
    __ingredients: dict

    with open(__path_to_configuration, "r") as __configuration_json:
        __configuration = json.load(__configuration_json)

    with open(__path_to_ingredients, "r") as __ingredients_json:
        __ingredients = json.load(__ingredients_json)

    def test_configure_glass_size(self):
        __glass_size: int = self.__configuration["configure_glass_size"]
        self.assertIs(type(__glass_size), int, "glass_size should be type int")
        self.assertGreaterEqual(
            __glass_size, 0, "glass_size should be greater or equal to 0"
        )

    def test_configure_measurements_per_scale_value(self):
        __measurements_per_scale_value: int = self.__configuration[
            "configure_measurements_per_scale_value"
        ]
        self.assertIs(
            type(__measurements_per_scale_value), int, "scale_value should be type int"
        )
        self.assertGreaterEqual(
            __measurements_per_scale_value,
            0,
            "scale_value should be greater or equal to 0",
        )

    def test_configure_mock_communication(self):
        __mock_communication: bool = self.__configuration[
            "configure_mock_communication"
        ]
        self.assertIs(
            type(__mock_communication), bool, "mock_communication should be type bool"
        )

    def test_configuration_max_waiting_time(self):
        __max_waiting_time: int = self.__configuration["configure_max_waiting_time"]
        self.assertIs(
            type(__max_waiting_time), int, "max_waiting_time should be type int"
        )
        self.assertGreaterEqual(__max_waiting_time, 0)

    def test_configure_ui_type(self):
        __ui_type: str = self.__configuration["configure_ui_type"]
        __known_ui_types: list[str] = ["ui_console"]
        self.assertIs(type(__ui_type), str, "ui_type should be type str")
        self.assertIn(
            __ui_type,
            __known_ui_types,
            f"unknown ui_type only the following ui types are allowed{__known_ui_types}",
        )

    def test_configure_ingredient_file_path(self):
        __ingredient_file_path: str = self.__configuration[
            "configure_ingredient_file_path"
        ]
        self.assertIs(
            type(__ingredient_file_path), str, "ingredient_file_path should be type str"
        )

    def test_configure_recipe_file_path(self):
        __recipe_file_path: str = self.__configuration["configure_recipe_file_path"]
        self.assertIs(
            type(__recipe_file_path), str, "recipe_file_path should be type str"
        )

    def test_configure_pico_identifier(self):
        __pico_identifier: list[str] = self.__configuration["configure_pico_identifier"]
        __known_pico_identifiers: list[str] = ["LEFT", "RIGHT", "RONDELL"]

        self.assertIs(
            type(__pico_identifier),
            list,
            "wrong type, pico_identifiers should be stored in a list",
        )
        if __pico_identifier:
            self.assertIs(
                type(__pico_identifier[0]), str, "pico_identifiers should be type str"
            )
        for __pico_identifier_element in __pico_identifier:
            self.assertIn(
                __pico_identifier_element,
                __known_pico_identifiers,
                f"unknown pico_identifier, pico_identifier should be element of {__known_pico_identifiers}",
            )

    def test_configuration_ms_per_ml(self):
        __ms_per_ml: int = self.__configuration["configuration_ms_per_ml"]
        self.assertIs(type(__ms_per_ml), int, "ms_per_ml should be type int")
        self.assertGreaterEqual(__ms_per_ml, 0)

    def test_configuration_hopper_sizes(self):
        __hopper_sizes: list[int | None] = self.__configuration[
            "configuration_hopper_sizes"
        ]
        self.assertIs(
            type(__hopper_sizes),
            list,
            "wrong type, hopper_sizes should be stored in a list",
        )
        for __hopper_size_index in range(len(__hopper_sizes)):
            if __hopper_sizes[__hopper_size_index]:
                self.assertIs(
                    type(__hopper_sizes[__hopper_size_index]),
                    int,
                    "hopper_sizes should have type int or None",
                )
            else:
                self.assertIs(
                    type(__hopper_sizes[__hopper_size_index]),
                    type(None),
                    "hopper_sizes should have type int or None",
                )
        self.assertEqual(
            len(__hopper_sizes),
            12,
            "wrong number of hoppers in hopper_sizes. len(hopper_sizes) should be 12",
        )

    def test_configure_connection_pi_tiny(self):
        __connection_pi_tiny: list[str] = self.__configuration[
            "configure_connection_pi_tiny"
        ]
        __known_serial_connections: list[str] = [
            "/dev/ttyACM0",
            "/dev/ttyACM1",
            "/dev/ttyACM2",
        ]

        self.assertIs(
            type(__connection_pi_tiny),
            list,
            "wrong type for configure_connection_pi_tiny. type should be list",
        )
        if __connection_pi_tiny:
            self.assertIs(
                type(__connection_pi_tiny[0]),
                str,
                "serial connection should be type str",
            )
        for __connection_element in __connection_pi_tiny:
            self.assertIn(
                __connection_element,
                __known_serial_connections,
                f"serial connections should be element of {__known_serial_connections}",
            )

    def test_configure_max_serial_identifier_attempt(self):
        __max_serial_identifier_attempt: int = self.__configuration[
            "configure_max_serial_identifier_attempt"
        ]
        self.assertIs(
            type(__max_serial_identifier_attempt),
            int,
            "max_serial_identifier_attempt should be of type int",
        )
        self.assertGreaterEqual(
            __max_serial_identifier_attempt,
            0,
            "max_serial_identifier_attempt should be greater or equal to 0",
        )

    def test_configure_ingredients(self):
        __ingredient_configuration: dict = self.__configuration["configure_ingredients"]
        self.assertIs(
            type(__ingredient_configuration),
            dict,
            "configure_ingredients should be type dict",
        )

        __ingredient_names: list[str] = list(__ingredient_configuration.keys())
        __ingredient_names_reference: list[str] = list(self.__ingredients.keys())
        for __ingredient_name in __ingredient_names:
            self.assertIs(
                type(__ingredient_name), str, "ingredient names should be type str"
            )
            self.assertIn(
                __ingredient_name,
                __ingredient_names_reference,
                f"configuration of an unknown ingredient name, please make sure that the ingredient name: {__ingredient_name} exists",
            )

            self.assertEqual(
                list((__ingredient_configuration[__ingredient_name]).keys()),
                ["hopper_position", "amount"],
                f"ingredient name: {__ingredient_name} uses the wrong dict keys",
            )

            self.assertIs(
                type(__ingredient_configuration[__ingredient_name]["hopper_position"]),
                int,
                "wrong type hopper_position value, should be int",
            )
            self.assertGreaterEqual(
                __ingredient_configuration[__ingredient_name]["hopper_position"],
                0,
                "hopper_position should be greate or equal to 0",
            )
            self.assertLessEqual(
                __ingredient_configuration[__ingredient_name]["hopper_position"],
                11,
                "max hopper position number is 11, number should be lower",
            )

            self.assertIs(
                type(__ingredient_configuration[__ingredient_name]["amount"]),
                int,
                "wrong type amount value, should be int",
            )
            self.assertGreaterEqual(
                __ingredient_configuration[__ingredient_name]["amount"],
                0,
                "amount should be greate or equal to 0",
            )


if __name__ == "__main__":
    unittest.main()
