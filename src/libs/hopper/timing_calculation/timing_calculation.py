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

    def calculate_timing(self, __data: list[int]):
        # __data:=[<amount-ml>,<flow-speed>];   len(__data)==2;  __data: list[int]
        __amount_ml = __data[0]
        __flow_speed = __data[1]
        __timing = __amount_ml * self.__MS_PER_ML * __flow_speed
        return __timing
