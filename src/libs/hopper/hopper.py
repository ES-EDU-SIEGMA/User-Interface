from .timing_calculation import timing_calculation as Timing_calculation_module
from .communication_hardware import communication as Communication_module
from .communication_hardware import mock_communication as Mock_communication_module


class Hopper:
    __calculation_object: Timing_calculation_module.Calculation
    __communication_object: Mock_communication_module.Communication  # | Communication_module.Communication |

    def __init__(self, __mock_communication: bool, __hopper_sizes: list[int]):

        if __mock_communication:
            self.__communication_object = Mock_communication_module.Communication()
        else:
            self.__communication_object = Communication_module.Communication(__hopper_sizes)

        self.__calculation_object = Timing_calculation_module.Calculation()

    def dispense_drink(self, __data: list[list[int]]):
        # __data:= [[<amount-ml>, <flow-speed>]] position for each hopper is encoded into the list position.
        __timings: list[int] = []
        # __timings encodes hopper position into list position of the timing.
        for __element in __data:
            __timings.append(self.__calculation_object.calculate_timing(__element))

        self.__communication_object.send_timings(__timings)
