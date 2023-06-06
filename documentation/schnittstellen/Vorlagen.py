class Sigma:

    def __init__(self):
        pass
        """ Sigma initializes different objects and uses them as parameters for other objects."""


class Controller:

    def cmd_dispense_drink(self, __drink_name: str):
        """ a method that dispenses a drink by calling the hopper_interface object."""
        pass

    def cmd_get_weight(self) -> int:
        """ returns the weight on the measuring device"""
        pass


class HopperInterface:

    def dispense_drink(self, __placeholder_name: list[list[int]]):
        # todo change the parameter input
        """ This method activates multiple hoppers at once.
            Activating multiple hoppers at once helps us optimise the time it takes to dispense a drink.
            __placeholder_name:= list[list[<hopper-position>, <amount>, <flow-speed>]]"""
        pass


class ScaleInterface:

    def get_weight(self):
        """ returns the weight from the measuring device."""


class DataInterface:
    pass
    # todo change the data-interface


class Communication:

    def activate_hoppers(self, __hopper_positions: list[int], __timings: list[int]):
        """ sends communication to the hoppers to activate them
            input lists should be connected through their index
                __hopper_positions[i] -> __timings[i]"""
        pass

    def activate_hoppers_alternative_input(self, __hopper_positions_and_timings: list[list[int]]):
        """ sends communication to the hoppers to activate them
            input:= [<hopper-position>,<timing>]"""
        pass


class HopperTime:

    def calculate_time(self, __amount: int) -> int:
        """ calculates the time for a single hopper"""
        pass

    def calculate_multiple_timings(self, __amounts: list[int]) -> list[int]:
        """ Calculates the time for multiple hoppers.
            Input:= list[amount]
            The list input position should correspond to the list output position."""
