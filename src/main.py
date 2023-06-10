from libs.business_logic import business_logic as Business_logic_module
import json


class Main:

    def __init__(self):

        __configuration_dict: dict

        try:
            with open(file="configuration.json", mode="r") as __configuration_file:
                __configuration_dict = json.load(__configuration_file)

        except Exception as error:
            print(f"can't read in the configuration file. error: {error}")

        Business_logic_module.BusinessLogic(__configuration_dict)


if __name__ == "__main__":
    Main()
