#!/usr/bin/python3

from __future__ import annotations

import json
from argparse import ArgumentParser, Namespace

import RPi.GPIO as GPIO
from serial import Serial

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
from libs.hardware.tatobari_hx711.hx711 import HX711
from libs.hardware.timingCalculator.calculator import Calculator
from libs.ui.IUserInterface import IUserInterface
from libs.ui.cli.CliUserInterface import CliUserInterface

__serial_ports: list[Serial] = []


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
    # disable warnings for GPIO and use BCM for pin addressing
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    # init hardware library
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
    for serial_port in serial_ports:
        device = Serial(port=serial_port)
        __serial_ports.append(device)
        controller: IDispenserGroupController = DispenserGroupController(
            possible_identifiers=identifier,
            port=device,
            max_connection_attempts=max_connect_attempts,
        )
        controller_list.append(controller)

    calculator: Calculator = Calculator(ms_per_ml=ms_per_ml, hopper_sizes=hopper_sizes)
    return DispenseMechanism(controller=controller_list, timing_calculator=calculator)


def close_serial_ports():
    for serial_port in __serial_ports:
        serial_port.close()
        __serial_ports.remove(serial_port)


def setup_ui() -> IUserInterface:
    return CliUserInterface()
    # return GuidedUserInterface()


if __name__ == "__main__":
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
    close_serial_ports()
    print("EXIT APP")
