class Calculation:
    """ assumption_1: the speed for different hopper sizes is the same
        assumption_2: the required time can be approximated linearly
        assumption_3: a 40 ml hopper needs 6000 milliseconds
        -> 6000sec/40ml = 150 milliseconds/ml
        -> f(x):= x*150*<flow-speed>      where x is the ml-amount of a drink
        and f(x) the required time it takes to dispense the drink"""
    __MS_PER_ML = 150

    def __init__(self):
        pass

    def calculate_timing(self, __data: dict) -> list[int | list[int]]:
        # {<hopper-position>: {amount_ml: int, flow_speed: int}}

        __expected_weight: int = 0
        __timings: list[int] = []

        for __hopper_position in __data:
            __amount_ml = __data[__hopper_position]["fill_amount"]
            __flow_speed = __data[__hopper_position]["flow_speed"]

            __timing = __amount_ml * self.__MS_PER_ML * __flow_speed
            __timings.append(__timing)
            __expected_weight += __amount_ml
        return [__expected_weight, __timings]
