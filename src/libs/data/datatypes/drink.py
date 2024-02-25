from __future__ import annotations


class Drink:
    __drink_id: int = None
    __ingredients: list[(int, int)] = None
    """tuple(<ingredient_id>, <percentage>)"""
    name: str = None

    def __init__(self, drink_id, name, ingredients):
        self.__drink_id = drink_id
        self.name = name
        self.__ingredients = ingredients

    def get_id(self) -> int:
        return self.__drink_id

    def get_ingredients(self) -> list[(int, int)]:
        """
        :return: list of ingredients: tuple(<ingredient_id>, <percentage>)
        """
        return self.__ingredients

    def add_ingredient(self, ingredient_id: int, percentage: int) -> None:
        """
        :param ingredient_id: ID of ingredient to add
        :param percentage: Percentage of ingredient to add
        """
        foo_dict = dict(self.__ingredients)
        foo_list_keys = list(foo_dict.keys())

        if ingredient_id not in foo_list_keys:
            sum_ingredients_before = sum(foo_dict.values())
            foo_dict[ingredient_id] = percentage
            x_sum = (100-percentage) / sum_ingredients_before

            for y in range(len(foo_list_keys)):
                foo_dict[foo_list_keys[y]] *= x_sum
                foo_dict[foo_list_keys[y]] = round(foo_dict[foo_list_keys[y]])

            # If the sum is more then 100, subtract this what is more from the ingredient with the highest value
            if sum(foo_dict.values()) > 100:
                foo_dict[max(foo_dict, key=foo_dict.get)] -= sum(foo_dict.values()) - 100

            self.__ingredients = [(k, v) for k, v in foo_dict.items()]

    def remove_ingredient(self, ingredient_id: int):
        """
        :param ingredient_id: ingredient ID to remove
        """
        foo_dict = dict(self.__ingredients)
        foo_list_keys = list(foo_dict.keys())

        if ingredient_id in foo_list_keys:
            removed_percent = foo_dict[ingredient_id]
            foo_dict.pop(ingredient_id)
            foo_list_keys = list(foo_dict.keys())

            # If only two ingredients in one drink:
            if len(foo_list_keys) == 1:
                foo_dict[foo_list_keys[0]] += removed_percent
            else:
                x_sum = 100 / sum(foo_dict.values())
                for y in range(len(foo_list_keys)):
                    foo_dict[foo_list_keys[y]] *= x_sum
                    foo_dict[foo_list_keys[y]] = round(foo_dict[foo_list_keys[y]])

            # If the sum is more then 100, subtract this what is more from the ingredient with the highest value
            if sum(foo_dict.values()) > 100:
                foo_dict[max(foo_dict, key=foo_dict.get)] -= sum(foo_dict.values()) - 100

            self.__ingredients = [(k, v) for k, v in foo_dict.items()]

    def adjust_amount(self, ingredient_id: int, percentage: int):
        """
        :param ingredient_id: ID of ingredient to update
        :param percentage: new percentage of ingredient
        """
        # TODO: Adjust percentage of other ingredients
        # TODO: Adjust percentage of given ingredient
        raise NotImplementedError()
