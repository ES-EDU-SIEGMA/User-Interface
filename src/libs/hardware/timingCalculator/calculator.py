from __future__ import annotations

from math import ceil


class IngredientNotAvailableException(Exception):
    pass


class Calculator:
    __ms_per_ml: int
    __hopper_sizes: list[int | None]

    def __init__(self, ms_per_ml: int, hopper_sizes: list[int | None]):
        """
        :param ms_per_ml: multiplier specifying the milliseconds to output one millilitre
        :param hopper_sizes: list defining the sizes of the hopper in centilitre
        """
        self.__ms_per_ml = ms_per_ml
        self.__hopper_sizes = hopper_sizes

    def calculate_timing(
        self, ingredients: list[(int, int, int)], volume: int
    ) -> (int, list[list[list[int]]]):
        """
        :param ingredients: list of triple (<hopper_for_ingredient>,
                                            <percentage_of_ingredient>,
                                            <flow_speed_of_ingredient>)
        :param volume: total volume of the drink in millilitre

        :return: tuple(<weight>, <list of runs <list of dispenser <list of <timings>>>)

        :raises IngredientNotAvailableException: if no hopper associated with ingredient or hopper size set to None
        """
        timings = []
        total_weight: int = 0

        self.__check_all_ingredients_are_available(ingredients)

        for hopper_id, percentage, flow_speed in ingredients:
            amount_of_ingredient: int = ceil(volume * (percentage / 100))
            required_fillings: int = ceil(
                amount_of_ingredient / self.__hopper_sizes[hopper_id]
            )
            timings_for_ingredient = [
                self.__hopper_sizes[hopper_id] * self.__ms_per_ml * flow_speed
            ] * required_fillings

            self.__add_timings_for_ingredient(
                timings_for_ingredient, hopper_id, timings
            )
            total_weight += required_fillings * self.__hopper_sizes[hopper_id]

        for index in range(0, len(timings)):
            timings[index] = self.__split(input_list=timings[index], chunk_length=4)

        return total_weight, timings

    def __check_all_ingredients_are_available(self, ingredients: list[(int, int, int)]):
        for hopper_id, _, _ in ingredients:
            if hopper_id is None:
                raise IngredientNotAvailableException("No Hopper associated")
            if self.__hopper_sizes[hopper_id] is None:
                raise IngredientNotAvailableException("Hopper not available!")

    def __add_timings_for_ingredient(
        self, timings_for_ingredient: list[int], hopper_id: int, timings
    ):
        for index in range(0, len(timings_for_ingredient) - len(timings)):
            timings.append([0] * len(self.__hopper_sizes))

        for index in range(0, len(timings_for_ingredient)):
            timings[index][hopper_id] = timings_for_ingredient[index]

    @staticmethod
    def __split(input_list: list, chunk_length: int) -> list:
        temp_list = []
        for index in range(0, len(input_list), chunk_length):
            temp_list.append(input_list[index : index + chunk_length])
        return temp_list
