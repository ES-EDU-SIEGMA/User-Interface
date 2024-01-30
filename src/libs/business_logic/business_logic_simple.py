from __future__ import annotations
import time

from libs.business_logic.program_state import (
    state_selection as state_selection_module,
    state_progress as state_progress_module,
)

from libs.ui import userinterface as ui_module
from libs.data import data_interface as data_module

from libs.hardware.tatobari_hx711.hx711 import HX711
from RPi.GPIO import GPIO
from libs.hardware.scale.scale import Scale

from libs.hardware.timingCalculator.calculator import Calculator
from serial import Serial
from libs.hardware.dispenserGroupController.dispenserGroupController import (
    DispenserGroupController,
)
from libs.hardware.dispenserGroupController.iDispenserGroupController import (
    IDispenserGroupController,
)
from libs.hardware.dispenseMechanism.dispenseMechanism import DispenseMechanism


########################################################################################################################
# Business logic
########################################################################################################################


class BusinessLogic:
    __program_state_selection: state_selection_module.StateSelection
    __program_state_progress: state_progress_module.StateProgress

    __program_state: (
        state_selection_module.StateSelection | state_progress_module.StateProgress
    )

    __ui_object: ui_module.UserInterface
    __data_object: data_module.DataInterface

    __scale_hardware: HX711
    __scale_object: Scale

    __dispenser_mechanism: DispenseMechanism
    __timing_calculator: Calculator
    __dispenser_array_controller: list[IDispenserGroupController]

    __program_is_running: bool

    PICO_BAUDRATE = 115200

    def __init__(self, __configuration: dict):
        ################################################################################################################
        # initialize program objects
        ################################################################################################################

        self.__ui_object = ui_module.UserInterface(__configuration["configure_ui_type"])
        self.__data_object = data_module.DataInterface(
            __configuration["configure_ingredients"],
            __configuration["configure_ingredient_file_path"],
            __configuration["configure_recipe_file_path"],
        )

        self.__timing_calculator = Calculator(
            ms_per_ml=__configuration["configuration_ms_per_ml"],
            hopper_sizes=__configuration["configuration_hopper_sizes"],
        )
        self.__dispenser_array_controller = []
        for port in __configuration["configure_connection_pi_tiny"]:
            serial = Serial(port=port, baudrate=self.PICO_BAUDRATE)
            self.__dispenser_array_controller.append(
                DispenserGroupController(
                    possible_identifiers=__configuration["configure_pico_identifier"],
                    port=serial,
                    max_connection_attempts=__configuration[
                        "configure_max_serial_identifier_attempt"
                    ],
                )
            )
        self.__dispenser_mechanism = DispenseMechanism(
            controller=self.__dispenser_array_controller,
            timing_calculator=self.__timing_calculator,
        )

        self.__scale_hardware = self.__init_scale_hardware(
            gpio_data=5, gpio_sck=6, reference_unit=870298
        )
        self.__scale_object = Scale(
            hardware=self.__scale_hardware,
            number_of_measurements=__configuration[
                "configure_measurements_per_scale_value"
            ],
        )

        ################################################################################################################
        # initialize program state objects
        ################################################################################################################

        self.__program_state_selection = state_selection_module.StateSelection(
            self.__ui_object, self.__data_object, self.__dispenser_mechanism
        )
        self.__program_state_progress = state_progress_module.StateProgress(
            self.__ui_object,
            self.__dispenser_mechanism,
            self.__scale_object,
            __configuration["configure_max_waiting_time"],
        )

        ################################################################################################################
        # start the program
        ################################################################################################################

        self.__program_state = self.__program_state_selection
        self.__program_is_running = True
        self.__program_loop()

    @staticmethod
    def __init_scale_hardware(gpio_data, gpio_sck, reference_unit: int) -> HX711:
        # disable warnings for GPIO and use BCM for pin addressing
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        # init library
        scale_hardware: HX711 = HX711(gpio_data, gpio_sck)
        scale_hardware.set_reading_format("MSB", "MSB")
        scale_hardware.set_reference_unit(reference_unit)

        # reset hardware
        scale_hardware.reset()
        scale_hardware.tare()

        return scale_hardware

    ####################################################################################################################
    # main program loop
    ####################################################################################################################

    def __program_loop(self):
        while self.__program_is_running:
            __ui_cmd: dict = self.__program_state.call_ui()
            # call_ui() returns dict{"cmd": str, "data": some_data}

            if __ui_cmd["cmd"] == "exit":
                self.__data_object.close()
                self.__scale_hardware.power_down()
                time.sleep(1)
                GPIO.cleanup()
                self.__program_is_running = False

            elif __ui_cmd["cmd"] == "dispense":
                self.__program_state_selection.execute_command(__ui_cmd["data"])
                self.__program_state = self.__program_state_progress

            elif __ui_cmd["cmd"] == "progress":
                if __ui_cmd["data"] == -1:
                    # dispense drink is finished return to selection
                    self.__program_state = self.__program_state_selection
                else:
                    self.__program_state.execute_command(__ui_cmd["data"])
