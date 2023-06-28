from __future__ import annotations

from libs.ui import userinterface as ui_module
from libs.data import data_interface as data_module
from libs.hopper import hopper as hopper_module
from libs.scale import scale_interface as scale_module

from libs.business_logic.program_state import (
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

    __ui_object: ui_module.UserInterface
    __data_object: data_module.DataInterface
    __scale_object: scale_module.Scale
    __hopper_object: hopper_module.Hopper

    __program_is_running: bool

    def __init__(self, __configuration: dict):

        ################################################################################################################
        # initialize program objects
        ################################################################################################################

        self.__ui_object = ui_module.UserInterface(
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
            __configuration["configure_measurements_per_scale_value"],
        )

        ################################################################################################################
        # initialize program state objects
        ################################################################################################################

        self.__program_state_selection = state_selection_module.StateSelection(
            self.__ui_object, self.__data_object, self.__hopper_object
        )
        self.__program_state_edit = state_edit_module.StateEdit(
            self.__ui_object, self.__data_object
        )
        self.__program_state_new = state_new_module.StateNew(
            self.__ui_object, self.__data_object
        )
        self.__program_state_progress = state_progress_module.StateProgress(
            self.__ui_object,
            self.__hopper_object,
            self.__scale_object,
            __configuration["configure_max_waiting_time"],
        )

        ################################################################################################################
        # start the program
        ################################################################################################################

        self.__program_state = self.__program_state_selection
        self.__program_is_running = True
        self.__program_loop()

    ####################################################################################################################
    # main program loop
    ####################################################################################################################

    def __program_loop(self):
        while self.__program_is_running:

            __ui_cmd: dict = self.__program_state.call_ui()
            # call_ui() returns dict{"cmd": str, "data": some_data}

            if __ui_cmd["cmd"] == "exit":
                self.__data_object.close()
                self.__hopper_object.close()
                self.__scale_object.close()
                self.__program_is_running = False

            elif __ui_cmd["cmd"] == "change_ui":
                self.__change_program_state(__ui_cmd["data"])

            elif __ui_cmd["cmd"] == "progress":
                if __ui_cmd["data"] == -1:
                    # progress of dispense drink is finished return to selection
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
