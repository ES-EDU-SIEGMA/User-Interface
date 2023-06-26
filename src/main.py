#!/usr/bin/python3

import json
from os.path import abspath as absolute_path, join, dirname, realpath

from libs.business_logic import (
    business_logic as business_logic_module,
    business_logic_simple as business_logic_module_only_selection,
)


class Main:
    def __init__(self):
        __configuration_file_path: str = absolute_path(
            join(dirname(realpath(__file__)), "configuration.json")
        )
        __configuration_dict: dict

        try:
            with open(file=__configuration_file_path, mode="r") as __configuration_file:
                __configuration_dict = json.load(__configuration_file)

        except Exception as error:
            print(f"can't read in the configuration file. error: {error}")
            exit(1)

        __configuration_dict["configure_ingredient_file_path"] = absolute_path(
            join(
                dirname(realpath(__file__)),
                __configuration_dict["configure_ingredient_file_path"],
            )
        )
        __configuration_dict["configure_recipe_file_path"] = absolute_path(
            join(
                dirname(realpath(__file__)),
                __configuration_dict["configure_recipe_file_path"],
            )
        )

        if __configuration_dict["configuration_only_selection"]:
            business_logic_module_only_selection.BusinessLogic(__configuration_dict)
        else:
            business_logic_module.BusinessLogic(__configuration_dict)


if __name__ == "__main__":
    Main()
