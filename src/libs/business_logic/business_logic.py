from __future__ import annotations

from src.libs.ui import userinterface as ui_module
from src.libs.data import data_interface as data_module
from src.libs.hopper import hopper as hopper_module
from src.libs.scale import scale_interface as scale_module

from src.libs.business_logic.program_state import (
    state_selection as state_selection_module,
    state_edit as state_edit_module,
    state_new as state_new_module,
    state_progress as state_progress_module,
)


########################################################################################################################
# Business logic
########################################################################################################################


class BusinessLogic:
    __program_state_selection: state_selection_module.StateSelection
    __program_state_edit: state_edit_module.StateEdit
    __program_state_new: state_new_module.StateNew
    __program_state_progress: state_progress_module.StateProgress

    __program_state: (
        state_selection_module.StateSelection
        | state_edit_module.StateEdit
        | state_new_module.StateNew
        | state_progress_module.StateProgress
    )

    __data_object: data_module.DataInterface
    __scale_object: scale_module.Scale
    __hopper_object: hopper_module.Hopper

    __program_is_running: bool

    def __init__(self, __configuration: dict):
        __ui_object: ui_module.UserInterface = ui_module.UserInterface(
            __configuration["configure_ui_type"]
        )
        self.__data_object = data_module.DataInterface(
            __configuration["configure_ingredients"],
            __configuration["configure_ingredient_file_path"],
            __configuration["configure_recipe_file_path"],
        )

        self.__hopper_object = hopper_module.Hopper(
            __configuration["configure_mock_communication"],
            __configuration["configuration_ms_per_ml"],
            __configuration["configuration_hopper_sizes"],
            __configuration["configure_pico_identifier"],
            __configuration["configure_connection_pi_tiny"],
            __configuration["configure_max_serial_identifier_attempt"],
        )

        self.__scale_object = scale_module.Scale(
            __configuration["configure_mock_scale"],
            __configuration["configure_measurement_calculation_method"],
            __configuration["configure_measurements_per_scale_value"],
        )

        self.__program_state_selection = state_selection_module.StateSelection(
            __ui_object, self.__data_object, self.__hopper_object
        )
        self.__program_state_edit = state_edit_module.StateEdit(
            __ui_object, self.__data_object
        )
        self.__program_state_new = state_new_module.StateNew(
            __ui_object, self.__data_object
        )
        self.__program_state_progress = state_progress_module.StateProgress(
            __ui_object,
            self.__hopper_object,
            self.__scale_object,
            __configuration["configure_max_waiting_time"],
        )

        self.__program_state = self.__program_state_selection
        self.__program_is_running = True
        self.__program_loop()

    def __program_loop(self):
        while self.__program_is_running:
            __ui_cmd: dict = self.__program_state.call_ui()

            if __ui_cmd["cmd"] == "exit":
                self.__data_object.close()
                self.__hopper_object.close()
                self.__scale_object.close()
                self.__program_is_running = False
            elif __ui_cmd["cmd"] == "change_ui":
                self.__change_program_state(__ui_cmd["data"])
            elif __ui_cmd["cmd"] == "progress":
                if __ui_cmd["data"] == -1:
                    # dispense drink is finished return to selection
                    self.__program_state = self.__program_state_selection
                else:
                    self.__program_state.execute_command(__ui_cmd["data"])
            elif __ui_cmd["cmd"] == "edit":
                self.__program_state_edit.execute_command(__ui_cmd["data"])
            elif __ui_cmd["cmd"] == "new":
                self.__program_state_new.execute_command(__ui_cmd["data"])

    def __change_program_state(self, __new_state: str):
        if __new_state == "selection":
            self.__program_state = self.__program_state_selection
        elif __new_state == "edit":
            self.__program_state = self.__program_state_edit
        elif __new_state == "new":
            self.__program_state = self.__program_state_new
