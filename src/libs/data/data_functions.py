import data_objects


class DataInterface:
    def __init__(self):
        pass

    # todo check which functions are used
    def get_beverage_names(self) -> list[str]:
        pass

    def get_recipe_names(self) -> list[str]:
        pass

    def get_beverage_hopper_names(self) -> list[str]:
        pass

    def get_dispensable_drinks(self) -> list[str]:
        pass

    def get_drink_names(self) -> list[str]:
        pass

    # todo maybe return bool on set cmds
    def create_recipe(self, __name: str, __name_and_amount: list[str]):
        pass

    # currently set_beverage is not supported
    def create_beverage(self):
        pass

    # todo don't know whether this name1,2 thing is good
    def set_beverage_hopper(self, __name_old, __name_new):
        pass

    # idea for this is to create functionality that allows to manipulate already existing drinks
    def change_beverage(self):
        pass

    def change_recipe(self):
        pass
