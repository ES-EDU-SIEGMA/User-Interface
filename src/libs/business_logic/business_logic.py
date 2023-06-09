from ..ui import userinterface as UI_module
from ..drink_data import new_data_interface as Data_module
from ..hopper import hopper as Hopper_communication_module


# todo implement the Hopper class or something along the lines of hopper


class BusinessLogic:
    __program_state: str
    # __program_state is one of ["selection", "edit", "new"]
    __program_is_running: bool
    __ui_object: UI_module.UserInterface
    __data_object: Data_module.DataInterface
    __hopper_object: Hopper_communication_module.Hopper

    def __init__(self,
                 __configuration_dict: dict,
                 __hopper_configuration: dict,
                 __hopper_sizes: list[int]):

        self.__data_object = Data_module.DataInterface(__hopper_configuration)
        self.__ui_object = UI_module.UserInterface(__configuration_dict["ui_console"], self.__data_object)
        self.__hopper_object = Hopper_communication_module.Hopper(__configuration_dict["mock_communication"],
                                                                  __hopper_sizes)

        self.__program_is_running = True
        self.__program_state = "selection"
        self.__program_loop()

    def __program_loop(self):

        while self.__program_is_running:

            __cmd: list[str] = self.__ui_object.select_view(self.__program_state)

            if __cmd:
                self.__execute_command(__cmd)

            else:
                # exit the program if __cmd is an empty list
                self.__program_is_running = False

    def __execute_command(self, __cmd: list[str]):

        match __cmd.pop(0):

            case "change_view":
                self.__program_state = __cmd.pop(0)

            case "dispense_drink":
                self.__dispense_drink(__cmd)
            case "edit_hopper":
                self.__edit_hopper(__cmd)
            case "new_recipe":
                self.__new_recipe(__cmd)

    def __dispense_drink(self, __cmd: list[str]):

        __data: list[list[int]] = self.__data_object.get_data_logic(self.__program_state, __cmd[0])
        # __data:= [[<amount-ml>, <flow-speed>]] position for each hopper is encoded into the list position
        self.__hopper_object.dispense_drink(__data)
        # todo implement get_hopper_status

    # question: should the selection be disabled until a new drink can be dispensed
    # question: should a progress state during the dispensing process be implemented

    def __edit_hopper(self, __cmd: list[str]):
        # the ui already checked whether the input is valid
        self.__data_object.set_hopper(int(__cmd[0]), __cmd[1])

    def __new_recipe(self, __new_recipe_information: list[str]):

        self.__data_object.create_recipe(__new_recipe_information)
        # todo add create_recipe input

    # maybe create a callback to change the program state from the gui? Problem: state is then inside the gui
