from timing_calculation import timing_calculation as Timing_calculation_module
from communication_hardware import communication as Communication_module


class Hopper:
    __timing_calculation_object: Timing_calculation_module.Calculation
    __communication_object: Communication_module.Communication

    def __init__(self,
                 __timing_calculation_object: Timing_calculation_module.Calculation,
                 __communication_object: Communication_module.Communication):
        self.__timing_calculation_object = __timing_calculation_object
        self.__communication_object = __communication_object

    def dispense_drink(self, __data: list[list[int]]):
        # __data:= [[<amount-ml>, <flow-speed>]] position for each hopper is encoded into the list position.
        __timings: list[int] = []
        # __timings encodes hopper position into list position of the timing.
        for __element in __data:
            __timings.append(self.__timing_calculation_object.calculate_timing(__element))

        self.__communication_object.send_timings(__timings)
