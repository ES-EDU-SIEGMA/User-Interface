class Data:
    """ Is instantiated by any object that wants to access data.

        <beverage>:= any type of liquid that can be dispensed.
        <recipe>:= a combination of beverages that form a drink.
        not every <beverage> needs to be a <recipe> but it can be.

        Questions for implementation:
        Are the following function enough too much or do we need different functions to access data?
        Where and how should we store data about beverage, recipe usage?
        (potentially in beverage and recipe data as another data section)
        Where and how should we store data about hopper usage?
        Should the persistent drink-data allways be up-to-date with the runtime data or do we only
        want to explicitly or periodically update the persistent data?"""
    pass

    def __init__(self):
        pass

    def get_beverage_names(self) -> list[str]:
        """ returns a list of all beverages"""
        pass

    def get_recipe_names(self) -> list[str]:
        """ returns a list of all recipe names"""
        pass

    def get_recipe_dispensable_names(self) -> list[str]:
        """ returns a list of all recipe names that are dispensable"""
        pass

    def get_beverage_on_hopper_names(self) -> list[str]:
        """ returns a list of all beverages that are on the hopper"""
        pass

    def get_beverage(self, __name: str) -> list[str]:
        """ Returns the information of a beverage encoded as a string.
            Each list-position refers to one section of information about a beverage.
            Each section of information is encoded into a string separated by semicolons

            return_value:=[<name>, <hopper-position>,<remaining-amount-bottle>]
            <name>:= one string value
            <hopper-position>:= one integer value encoded as a string
            <remaining-amount-bottle>:= one integer value encoded as a string"""
        pass

    def get_recipe(self, __name: str) -> list[str]:
        """ Returns the information of a recipe encoded as a string.
            Each list-position refers to one section of information about a recipe.
            Each section of information is encoded into a string separated by semicolons

            return_value:=[<name>, <ids-fill-amount>]
            <name>:= one string value
            <ids-fill-amount>:= a list of integers encoded as a string
                <id>;<fill-amount>;<id>;<fill-amount> ...
                Example: 5;40;2;100;
                <ids-fill-amount> consists of at least one pair of <id> and <fill-amount>"""
        pass

    ##############################################################################################################
    # Sections with functions where a bit more thought needs to be invested
    ##############################################################################################################

    def set_hopper(self):
        """ changes the hopper-position for beverages.
            Not sure about input and output right now.

            Maybe make the assumption that a new beverage is also a full beverage."""
        pass

    def change_beverage_information(self):
        """ idea: function that is able to change already existing beverage information"""
        pass

    def change_recipe_information(self):
        """ idea: function that is able to change already existing recipe information"""
        pass