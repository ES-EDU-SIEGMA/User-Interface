class Controller:
    """ a class that is called when hardware components get accessed.

        Is instantiated by some other class or object.
        On Instantiation this class Instantiates the hopper_interface object.
        On Instantiation this class Instantiates the weight_interface object
        Gets called from the UI object to dispense a drink.
        Calls the hopper_interface to dispense a drink.

        Question for implementation:
        Should the controller determine when a drink is finished by reading out the scale?
        Should the controller return a status update when the drink is finished?
        The controller should probably take the remaining fill_amount of the bottle into consideration.
        What happens if the controller determines a drink can't be dispensed fully because of
        empty ingredients?"""

    def __init__(self):
        pass

    def cmd_dispense_drink(self, __drink_name: str):
        """ a method that dispenses a drink by calling the hopper_interface object."""
        pass

    def cmd_get_weight(self) -> int:
        """ returns the weight on the measuring device"""
        pass
