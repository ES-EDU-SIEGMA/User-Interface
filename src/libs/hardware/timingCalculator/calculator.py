from __future__ import annotations


class Calculator:
    __ms_per_ml: int
    __hopper_sizes: list[int | None]

    def __init__(self, ms_per_ml: int, hopper_sizes: list[int | None]):
        self.__ms_per_ml = ms_per_ml
        self.__hopper_sizes = hopper_sizes

    def calculate_timing(self, data: dict) -> (int, list[list[int]]):
        # __data: {<hopper-position>: {"fill_amount": int, "flow_speed": int}}

        __return_value: dict = {"expected_weight": None, "timings": []}
        __expected_weight: int = 0
        __timings: list[list[int]] = [[]] * 12

        for __hopper_position in data:
            __fill_amount = data[__hopper_position]["fill_amount"]
            __flow_speed = data[__hopper_position]["flow_speed"]

            __hopper_emptying_count: int
            __time_per_emptying: int

            __timing_data: list[int] = []

            if self.__hopper_sizes[int(__hopper_position)]:
                # check if there is an int or None
                # None := nothing on the hopper

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

        return __expected_weight, __timings
