#!/usr/bin/python3

from __future__ import annotations

import json
import re
from argparse import ArgumentParser, Namespace

from libs.data.data import Data
from libs.data.data_handler.IDatahandler import IDatahandler
from libs.data.data_handler.JsonDatahandler import JSONDatahandler
from libs.drinkMixingMachine.drinkMixingMachine import DrinkMixingMachine
from libs.hardware.dispenseMechanism.dispenseMechanism import DispenseMechanism
from libs.hardware.dispenserGroupController.dispenserGroupController import (
    DispenserGroupController,
)
from libs.hardware.dispenserGroupController.iDispenserGroupController import (
    IDispenserGroupController,
)
from libs.hardware.timingCalculator.calculator import Calculator
from libs.ui.IUserInterface import IUserInterface
from libs.ui.cli.CliUserInterface import CliUserInterface

__serial_ports: list[Serial] = []


class Serial:
    __identifier: str = ""
    __last_send_message: str = ""
    __last_was_identifier: bool = False
    __timing_pattern: re.Pattern = None

    def __init__(self, identifier: str):
        self.__timing_pattern: re.Pattern = re.compile(
            r"[0-9]+;[0-9]+;[0-9]+;[0-9]+;", re.IGNORECASE
        )
        self.__identifier: str = identifier

    def reset_input_buffer(self):
        pass

    def reset_output_buffer(self):
        pass

    def write(self, data_input: bytes) -> None:
        print(f"send to controller: '{data_input.decode('utf-8').rstrip()}'")
        # store for read handling
        self.__last_send_message = data_input.decode("utf-8").rstrip()

    def readline(self) -> bytes:
        # define answer to return
        if self.__last_send_message is "i":
            answer = self.__identifier
            self.__last_was_identifier = True
        elif self.__last_send_message is "" and self.__last_was_identifier:
            answer = "CALIBRATED"
            self.__last_was_identifier = False
        elif self.__timing_pattern.match(self.__last_send_message):
            answer = "READY"
        else:
            answer = "F"

        # reset last message
        self.__last_send_message = ""

        print(f"answer: {answer}")
        return answer.encode("utf-8")


class Scale:
    __base_value: int = None

    def __init__(self, hardware, number_of_measurements: int = 3):
        """
        :param hardware: scale object to retrieve data from
        :param number_of_measurements: number of real measurements to average for result
                                       (default: 3)
        """
        self.__base_value = 0

    def tare(self) -> None:
        self.__base_value = 10

    def get_weight(self) -> int:
        """
        :return: measured weight in gramm
        """
        measurement = 90 - self.__base_value
        return measurement


def arg_parser() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        description="Start the Drink Mixing Machine"
    )
    parser.add_argument(
        "--config", type=str, help="Absolute path to the config file", required=True
    )
    parser.add_argument(
        "--ingredients",
        type=str,
        help="Absolute path to the ingredients file",
        required=True,
    )
    parser.add_argument(
        "--drinks", type=str, help="Absolute path to the drinks file", required=True
    )
    return parser.parse_args()


def load_config(path_to_config: str) -> dict:
    with open(path_to_config, "r") as config_file:
        configuration = json.load(config_file)

    return configuration


def setup_data(path_to_ingredients: str, path_to_drinks: str) -> Data:
    data_handler: IDatahandler = JSONDatahandler(
        path_to_ingredients=path_to_ingredients, path_to_drinks=path_to_drinks
    )
    return Data(data_handler=data_handler)


def setup_scale(number_of_measurements: int) -> Scale:
    return Scale(hardware=None, number_of_measurements=number_of_measurements)


def setup_dispenser(
    serial_ports: list[str],
    identifier: list[str],
    max_connect_attempts: int,
    ms_per_ml: int,
    hopper_sizes: list[int],
) -> DispenseMechanism:
    controller_list: list[IDispenserGroupController] = []
    for name in identifier:
        device = Serial(identifier=name)
        controller: IDispenserGroupController = DispenserGroupController(
            possible_identifiers=identifier,
            port=device,
            max_connection_attempts=max_connect_attempts,
        )
        controller_list.append(controller)

    calculator: Calculator = Calculator(ms_per_ml=ms_per_ml, hopper_sizes=hopper_sizes)
    return DispenseMechanism(controller=controller_list, timing_calculator=calculator)


def setup_ui() -> IUserInterface:
    return CliUserInterface()
    # return GuidedUserInterface()


if __name__ == "__main__":
    """
    dummies:
        - scale hardware (Scale)
        - serial ports (Serial)
    """
    args = arg_parser()
    config = load_config(path_to_config=args.config)
    print("CONFIG LOADED")

    data: Data = setup_data(
        path_to_ingredients=args.ingredients,
        path_to_drinks=args.drinks,
    )
    print("SETUP DATA SOURCES")

    scale: Scale = setup_scale(
        number_of_measurements=config["scale"]["measurements_per_value"]
    )
    print("SETUP SCALE")

    dispense_mechanism: DispenseMechanism = setup_dispenser(
        serial_ports=config["serial"]["port"],
        identifier=config["serial"]["identifier"],
        max_connect_attempts=config["serial"]["max_connection_attempts"],
        ms_per_ml=config["dispenser"]["ms_per_ml"],
        hopper_sizes=config["dispenser"]["hopper_sizes"],
    )
    print("SETUP DISPENSER")

    ui: IUserInterface = setup_ui()
    print("SETUP UI")

    dmm = DrinkMixingMachine(
        scale=scale, dispense_mechanism=dispense_mechanism, data=data, ui=ui
    )
    print("SETUP COMPLETE")

    dmm.run()
    print("EXIT APP")
