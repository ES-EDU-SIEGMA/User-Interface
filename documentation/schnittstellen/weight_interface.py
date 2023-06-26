class ScaleInterface:
    """ This class is used to interact with the measuring device.
        Imagine we had another measuring device except the current scale.
        This class should only contain methods that are required
        for the weight taking procedure regardless of the measuring device used.

        This class is instantiated by the controller object.
        After instantiation, it instantiates the corresponding measuring object(hx711).
        Gets called to measure and return weight.
        Calls the measuring object to get the current weight.

        Questions for implementation:
        If we measure multiple times to calculate the average weight, should this be done
        in weight_interface or within the weight_object? (I suggest here in the weight_interface)
        Should we return error messages for something?
        The current weight object (hx711) has multiple measuring techniques(A and B), I suggest
        we implement them so that you can select them through the object instantiation as a parameter"""

    def __init__(self):
        pass

    def get_weight(self):
        """ returns the weight from the measuring device."""
