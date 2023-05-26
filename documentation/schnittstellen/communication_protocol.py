class Communication:
    """ This class is used to communicate with the hoppers.

        On Instantiation this class instantiates any protocol objects it might need (Example serial).
        Gets called by the hopper_interface object with the hopper_position and hopper_timings
        Optionally: returns a value if needed to indicate whether the communication was successful

        Questions for implementation:
        See hopper_interface for questions in regard to implementation

        Should the communication_protocol return status updates (Example: rdy, error, failed, success)?"""

    def __init__(self):
        pass

    def activate_hoppers(self, __hopper_positions: list[int], __timings: list[int]):
        """ sends communication to the hoppers to activate them
            input lists should be connected through their index
                __hopper_positions[i] -> __timings[i]"""
        pass

    def activate_hoppers_alternative_input(self, __hopper_positions_and_timings: list[list[int]]):
        """ sends communication to the hoppers to activate them
            input:= [<hopper-position>,<timing>]"""
        pass
