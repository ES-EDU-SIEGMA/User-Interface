class Ui:
    """ The UI_module doesn't implement functions that can be called by other classes outside the UI_module

        The UI_module object gets instantiated by some other object or function.
        On instantiation the UI_module object instantiates one object per UI_module view (currently 3 view-objects).
        Each UI_module-view object refers to a certain functionality of the UI_module.
        The UI_module-view objects tell the UI_module object what the user wants to do.
        In response to the UI_module-view object, the UI_module object activates and deactivates different UI_module-view objects
        and sends cmds to the controller."""

    def __init__(self):
        pass
