from ..ui import userinterface as UI_module
from ..data import data_interface as Data_module
from ..hopper import hopper as Hopper_module
from ..scale import scale_interface as Scale_module

from .program_state import state_selection as State_selection_module
from .program_state import state_progress as State_progress_module


########################################################################################################################
# Business logic
########################################################################################################################

class BusinessLogic:
    __program_state_selection: State_selection_module.StateSelection
    __program_state_progress: State_progress_module.StateProgress

    __program_state: (State_selection_module.StateSelection | State_progress_module.StateProgress)

    __data_object: Data_module.DataInterface
    __scale_object: Scale_module.Scale
    __hopper_object: Hopper_module.Hopper

    __program_is_running: bool

    def __init__(self, __configuration: dict):

        __ui_object: UI_module.UserInterface = UI_module.UserInterface(__configuration["configure_ui_type"])
        self.__data_object = Data_module.DataInterface(__configuration["configure_ingredients"],
                                                       __configuration["configure_ingredient_file_path"],
                                                       __configuration["configure_recipe_file_path"])

        self.__hopper_object = Hopper_module.Hopper(__configuration["configure_mock_communication"],
                                                    __configuration["configuration_ms_per_ml"],
                                                    __configuration["configuration_hopper_sizes"],
                                                    __configuration["configure_pico_identifier"],
                                                    __configuration["configure_connection_pi_tiny"],
                                                    __configuration["configure_max_serial_identifier_attempt"])

        self.__scale_object = Scale_module.Scale(__configuration["configure_mock_scale"],
                                                 __configuration["configure_measurement_calculation_method"],
                                                 __configuration["configure_measurements_per_scale_value"])

        self.__program_state_selection = State_selection_module.StateSelection(__ui_object,
                                                                               self.__data_object,
                                                                               self.__hopper_object)
        self.__program_state_progress = State_progress_module.StateProgress(__ui_object,
                                                                            self.__hopper_object,
                                                                            self.__scale_object,
                                                                            __configuration[
                                                                                "configure_max_waiting_time"])

        self.__program_state = self.__program_state_selection
        self.__program_is_running = True
        self.__program_loop()

    def __program_loop(self):

        while self.__program_is_running:

            __ui_cmd: dict = self.__program_state.call_ui()

            match __ui_cmd["cmd"]:
                case "exit":
                    self.__data_object.close()
                    self.__hopper_object.close()
                    self.__scale_object.close()
                    self.__program_is_running = False

                case "dispense":
                    self.__program_state_selection.execute_command(__ui_cmd["data"])
                    self.__program_state = self.__program_state_progress

                case "progress":
                    if __ui_cmd["data"] == -1:
                        # dispense drink is finished return to selection
                        self.__program_state = self.__program_state_selection
                    else:
                        self.__program_state.execute_command(__ui_cmd["data"])


