class Beverage:
    beverage_hopper_id: int
    beverage_name: str
    beverage_id: int
    beverage_flow_speed: int

    def __init__(self, __beverage_id: int, __beverage_hopper_id: int, __beverage_name: str, __beverage_flow_speed: int):
        self.beverage_hopper_id = __beverage_hopper_id
        self.beverage_id = __beverage_id
        self.beverage_name = __beverage_name
        self.beverage_flow_speed = __beverage_flow_speed

    def __str__(self):
        return f"[{self.beverage_name}, {self.beverage_id}]"


class MixDrinkInformation:
    mix_drink_name: str
    mix_drink_id: int
    mix_drink_needed_beverages: list[Beverage] = []
    mix_drink_fill_perc_beverages: list[list[int]] = []

    def __init__(self, __mix_drink_id: int, __mix_drink_name: str,__mix_drink_needed_beverages: list[Beverage],
                 __mix_drink_fill_perc_beverages: list[[int]]):
        self.mix_drink_needed_beverages = __mix_drink_needed_beverages
        self.mix_drink_name = __mix_drink_name
        self.mix_drink_id = __mix_drink_id
        self.mix_drink_fill_perc_beverages = __mix_drink_fill_perc_beverages

    def get_fill_perc(self, __beverage_id: int) -> int:
        for beverage_id in range(len(self.mix_drink_fill_perc_beverages)):
            if __beverage_id == self.mix_drink_fill_perc_beverages[beverage_id][0]:
                return self.mix_drink_fill_perc_beverages[beverage_id][1]

    def set_fill_perc(self, __beverage_id: int, __fill_perc: int):
        for i in range(len(self.mix_drink_fill_perc_beverages)):
            if __beverage_id == self.mix_drink_fill_perc_beverages[i][0]:
                self.mix_drink_fill_perc_beverages[i][1] = __fill_perc

    def __str__(self):
        return f"{self.mix_drink_name}, {self.mix_drink_id}"


class RuntimeData:
    beverages_on_hopper: list[Beverage] = None
    mix_drinks_dispensable: list[MixDrinkInformation] = None

    def __init__(self, __beverages_on_hopper, __mix_drinks_dispensable):
        self.beverages_on_hopper = __beverages_on_hopper
        self.mix_drinks_dispensable = __mix_drinks_dispensable

    def get_mix_drink(self, __mix_drink_id: int):
        for mix_drink in range(len(self.mix_drinks_dispensable)):
            if __mix_drink_id == self.mix_drinks_dispensable[mix_drink].mix_drink_id:
                return self.mix_drinks_dispensable[mix_drink]
        return None

    def get_beverage(self, __beverage_id: int):
        for beverage in range(len(self.beverages_on_hopper)):
            if __beverage_id == self.beverages_on_hopper[beverage].beverage_id:
                return self.beverages_on_hopper[beverage]
        return None
