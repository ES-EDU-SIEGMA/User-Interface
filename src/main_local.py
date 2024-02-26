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
from libs.hardware.scale.scale import Scale
from libs.hardware.tatobari_hx711.emulated_hx711 import HX711
from libs.hardware.timingCalculator.calculator import Calculator
from libs.ui.IUserInterface import IUserInterface
from libs.ui.cli.CliUserInterface import CliUserInterface

__serial_ports: list[Serial] = []


class Serial:
    __identifier: str = ""
    __last_send_message: str = ""
    __last_was_identifier: str = False
    __timing_pattern: re.Pattern = None

    def __init__(self, identifier: str):
        self.timing_pattern: re.Pattern = re.compile(
            r"[0-9]+;[0-9]+;[0-9]+;[0-9]+;", re.IGNORECASE
        )
        self.__identifier: str = identifier

    def write(self, data_input: bytes) -> None:
        # store for read handling
        self.__last_send_message = data_input.decode("utf-8").rstrip()

    def readline(self) -> bytes:
        # define answer to return
        if self.__last_send_message is "i":
            answer = self.__identifier
        elif self.__last_send_message is "" and self.__last_was_identifier:
            answer = "CALIBRATED"
        elif self.__timing_pattern.match(self.__last_send_message):
            answer = "READY"
        else:
            answer = "F"

        # reset last message
        self.__last_send_message = ""

        return answer.encode("utf-8")


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
    return Data(datahandler=data_handler)


def setup_scale(number_of_measurements: int) -> Scale:
    # init hardware library (test double)
    scale_hardware: HX711 = HX711(dout=5, pd_sck=6)
    scale_hardware.set_reading_format(byte_format="MSB", bit_format="MSB")
    scale_hardware.set_reference_unit(reference_unit=870298)

    # reset hardware
    scale_hardware.reset()
    scale_hardware.tare()

    return Scale(hardware=scale_hardware, number_of_measurements=number_of_measurements)


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


if __name__ == "__main__":
    """
    dummies:
        - scale hardware (HX711 emulated)
        - serial ports (Serial)
    """
    args = arg_parser()
    config = load_config(path_to_config=args.config)

    data: Data = setup_data(
        path_to_ingredients=args.ingredients,
        path_to_drinks=args.drinks,
    )

    scale: Scale = setup_scale(
        number_of_measurements=config["scale"]["measurements_per_value"]
    )

    dispense_mechanism: DispenseMechanism = setup_dispenser(
        serial_ports=config["serial"]["port"],
        identifier=config["serial"]["identifier"],
        max_connect_attempts=config["serial"]["max_connectio_attempts"],
        ms_per_ml=config["dispenser"]["ms_per_ml"],
        hopper_sizes=config["dispenser"]["hopper_sizes"],
    )

    ui: IUserInterface = setup_ui()

    dmm = DrinkMixingMachine(
        scale=scale, dispense_mechanism=dispense_mechanism, data=data, ui=ui
    )
    dmm.run()
