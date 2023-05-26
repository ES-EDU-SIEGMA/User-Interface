# one object displays one tupel from in the database from the table beverage
class Beverage:
    # id of the hopper the beverage is in, None if its not in the machine
    m_hopper_id: int
    # name of the beverage
    m_name: str
    # id from database tupel
    m_id: int
    # flow speed of the beverage
    m_flow_speed: int

    # constructor
    def __init__(self, __id: int, __hopper_id: int, __name: str, __flow_speed: int):
        self.m_hopper_id = __hopper_id
        self.m_id = __id
        self.m_name = __name
        self.m_flow_speed = __flow_speed

    # to string
    def __str__(self):
        return f"[{self.m_name}, {self.m_id}]"


# represents the mixed drink
# it stores the beverages needed to mix the drink and all the other necessary information
class MixDrinkInformation:
    # list of the corresponding fill percentages,it's a list in the list
    # e.g. [[1,23], [2, 77]] where [x][0] is the id of the beverage and [x][1] is the fill percentage
    m_fill_percentage_to_beverage: [[int]] = []
    # name of the drink
    m_name: str
    # id of the mixed drink, comes from the table mixed drinks
    m_id: int

    # constructor
    def __init__(self, __id, __name, __fill_percentage_to_beverage):
        self.m_name = __name
        self.m_id = __id
        self.m_fill_percentage_to_beverage = __fill_percentage_to_beverage

    # returns the fill percentage to the given id
    def get_fill_percentage_to_id(self, __id: int) -> int:
        for ingredient_index in range(len(self.m_fill_percentage_to_beverage)):
            if __id == self.m_fill_percentage_to_beverage[ingredient_index][0]:
                return self.m_fill_percentage_to_beverage[ingredient_index][1]

    # set the fill percentage to the given id
    def set_fill_percentage_to_id(self, __id: int, __perc: int):
        for ingredient_index in range(len(self.m_fill_percentage_to_beverage)):
            if __id == self.m_fill_percentage_to_beverage[ingredient_index][0]:
                self.m_fill_percentage_to_beverage[ingredient_index][1] = __perc

    def __str__(self):
        return f"{self.m_name}, {self.m_id}"


# combines everything into one object
class RuntimeData:
    # list of all beverages currently on the machine
    m_beverage_list = None
    # list of all mix drinks which are currently mixable
    m_mixed_drink_list = None

    def __init__(self, __beverage_list, __mixed_drink_list):
        self.m_beverage_list = __beverage_list
        self.m_mixed_drink_list = __mixed_drink_list

    # find the mix drink to the given id
    #
    # PARAMS:
    #   _id: id of the element to be searched for
    #
    # RETURNS None if the mixed drink is not in the list, else the object
    def get_mixed_drink_to_id(self, _id: int):
        for i in range(len(self.m_mixed_drink_list)):
            if _id == self.m_mixed_drink_list[i].m_id:
                return self.m_mixed_drink_list[i]
        return None

    # see: getMixedDrinkToId
    def get_beverage_to_id(self, _id: int):
        for i in range(len(self.m_beverage_list)):
            if _id == self.m_beverage_list[i].m_id:
                return self.m_beverage_list[i]
        return None
