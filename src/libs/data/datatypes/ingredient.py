from __future__ import annotations


class Ingredient:
    __ingredient_id: int = None
    name: str = None
    flow_speed: int = None
    dispenser_id: int | None = None

    def __init__(
        self, ingredient_id: int, name: str, flow_speed: int, dispenser_id: int | None
    ):
        self.__ingredient_id = ingredient_id
        self.name = name
        self.flow_speed = flow_speed
        self.dispenser_id = dispenser_id

    def get_id(self) -> int:
        return self.__ingredient_id
