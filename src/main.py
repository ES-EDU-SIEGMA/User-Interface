from libs.business_logic import business_logic as Business_logic_module
from libs.business_logic import business_logic_simple as Business_logic_module_only_selection
from libs.cli_hardware import cli_hardware as Cli_hardware_module
import json


class Main:

    def __init__(self):

        __configuration_dict: dict

        try:
            with open(file="configuration.json", mode="r") as __configuration_file:
                __configuration_dict = json.load(__configuration_file)

        except Exception as error:
            print(f"can't read in the configuration file. error: {error}")

        if __configuration_dict["configuration_only_selection"]:
            Business_logic_module_only_selection.BusinessLogic(__configuration_dict)
        elif __configuration_dict["configuration_cli_hardware"]:
            Cli_hardware_module.CliHardware(__configuration_dict)
        else:
            Business_logic_module.BusinessLogic(__configuration_dict)


if __name__ == "__main__":
    Main()
