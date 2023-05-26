class Ui:
    """ The ui doesn't implement functions that can be called by other classes outside the ui

        The ui object gets instantiated by some other object or function.
        On instantiation the ui object instantiates one object per ui view (currently 3 view-objects).
        Each ui-view object refers to a certain functionality of the ui.
        The ui-view objects tell the ui object what the user wants to do.
        In response to the ui-view object, the ui object activates and deactivates different ui-view objects
        and sends cmds to the controller."""

    def __init__(self):
        pass
