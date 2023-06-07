class Hopper:
    """ This class is used to interact with the different Hoppers
        Imagine we had another communication protocol that isn't serial.
        This class should only contain methods that are required
        for the communication to the hopper.

        On Instantiation this class Initiates calculate_hopper_time object.
        On Instantiation this class Instantiates the communication_protocol.
        Gets called by the Controller object to dispense a drink through a hopper.
        Calls the calculate_hopper_time object to calculate the time for one or more hopper.
        Calls the communication_protocol object with the required timings.

        Question for implementation:
        Should the hopper_interface know about the hopper-layout?
        Should the hopper_interface optimise its calls to the communication_protocol in
        regard to parallel hopper activation?
        Should the hopper_interface take status updates from the communication_protocol?
        Should the hopper_interface wait with each call until the communication_protocol
        says its rdy or should we implement a backlog in communication_protocol that
        stores call with input it still needs to execute?"""

    def __init__(self):
        pass

    def dispense_drink(self, __hopper_position: list[int], __amount: list[int], __flow_speed: list[int]):
        """ This method activates multiple hopper at once.
            Activating multiple hopper at once helps us optimise the time it takes to dispense a drink."""
        pass

    def dispense_multiple_drink(self, __hopper_position_and_amount: list[list[int]]):
        """ This method works similarly to the previous just with a different input of type:
            input list[list[int]] := list[<hopper_position>,<amount>,<flow_speed]"""
        pass
