from __future__ import annotations


class Calculation:
    """assumption_1: the speed for different hopper sizes is the same
    assumption_2: the required time can be approximated linearly
    assumption_3: a 40 ml hopper needs 6000 milliseconds
    -> 6000sec/40ml = 150 milliseconds/ml
    -> f(x):= x*150*<flow-speed>      where x is the ml-amount of a drink
    and f(x) the required time it takes to dispense the drink"""

    __ms_per_ml: int
    __hopper_sizes: list[int | None]

    def __init__(self, __ms_per_ml: int, __hopper_sizes: list[int | None]):
        # len(__hopper_sizes) = highest_hopper_number - 1
        self.__ms_per_ml = __ms_per_ml
        self.__hopper_sizes = __hopper_sizes

    def calculate_timing(self, __data: dict) -> dict:
        # __data: {<hopper-position>: {fill_amount: int, flow_speed: int}}
        # return {expected_weight: int, timings: [[<hopper_emptying_count>, <time_per_emptying>]]}

        __return_value: dict = {"expected_weight": None, "timings": []}
        __expected_weight: int = 0
        __timings: list[list[int]] = [[]] * 12

        for __hopper_position in __data:
            __fill_amount = __data[__hopper_position]["fill_amount"]
            __flow_speed = __data[__hopper_position]["flow_speed"]

            __hopper_emptying_count: int
            __time_per_emptying: int

            __timing_data: list[int] = []

            if self.__hopper_sizes[int(__hopper_position)]:
                # check if there is an int or None

                __hopper_size: int = self.__hopper_sizes[int(__hopper_position)]
                __time_per_emptying = __hopper_size * self.__ms_per_ml * __flow_speed

                __hopper_emptying_count = __fill_amount // __hopper_size
                if __hopper_emptying_count == 0:
                    # make sure every ingredient gets dispensed even if it doesn't fill an entire hopper
                    __hopper_emptying_count = 1

                __timing_data.append(__hopper_emptying_count)
                __timing_data.append(__time_per_emptying)

            __expected_weight += __fill_amount

            __timings[int(__hopper_position)] = __timing_data

        for __index in range(len(__timings)):
            # add [0,0] to every timing that is []

            if not __timings[__index]:
                __timings[__index] = [0, 0]

        __return_value["expected_weight"] = __expected_weight
        __return_value["timings"] = __timings

        return __return_value
