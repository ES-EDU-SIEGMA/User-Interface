class HopperTime:
    """ This class is used to calculate the timings for each individual hopper.

        Gets called by a hopper_interface object.
        Calculates the timing for one or multiple hoppers.
        Returns those timings.

        amount is an integer measured in ml."""

    def __init__(self):
        pass

    def calculate_time(self, __amount: int) -> int:
        """ calculates the time for a single hopper"""
        pass

    def calculate_multiple_timings(self, __amounts: list[int]) -> list[int]:
        """ Calculates the time for multiple hoppers.
            Input:= list[amount]
            The list input position should correspond to the list output position."""