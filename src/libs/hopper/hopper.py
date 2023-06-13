from .timing_calculation import timing_calculation as Timing_calculation_module
# from .communication_hardware import communication as Communication_module
# todo remove comment
from .communication_hardware import mock_communication as Mock_communication_module


class Hopper:
    __calculation_object: Timing_calculation_module.Calculation
    __communication_object: Mock_communication_module.Communication  # | Communication_module.Communication

    __expected_weight: int

    def __init__(self,
                 __mock_communication: bool,

                 __ms_per_ml: int,
                 __hopper_sizes: list[int],

                 __pico_identifier: list[str],
                 __serial_connections: list[str],
                 __max_serial_identifier_attempt: int):

        if __mock_communication:
            # check if communication should be mocked

            self.__communication_object = Mock_communication_module.Communication()

        else:
            # normal communication with the hopper

            self.__communication_object = Communication_module.Communication(__pico_identifier,
                                                                             __serial_connections,
                                                                             __max_serial_identifier_attempt)
            # todo change this

        self.__calculation_object = Timing_calculation_module.Calculation(__ms_per_ml, __hopper_sizes)
        self.__expected_weight = 0

    def dispense_drink(self, __data: dict):

        __tmp: dict = self.__calculation_object.calculate_timing(__data)
        self.__expected_weight: int = __tmp["expected_weight"]

        self.__communication_object.send_timings(__tmp["timings"])

    def get_expected_weight(self) -> int:

        return self.__expected_weight

    def close(self):

        self.__communication_object.close_connection()
