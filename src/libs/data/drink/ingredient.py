class Ingredient:
    __id_: int
    name: str
    flow_speed: int
    dispenser_id: None

    def __init__(self, id_, name, flow_speed):
        self.__id_ = id_
        self.name = name
        self.flow_speed = flow_speed
        self.__base_value = 0

    def get_id(self) -> int:
        return self.__id_