from __future__ import annotations

from libs.data.data import Data
from libs.data.datatypes.drink import Drink
from libs.data.datatypes.ingredient import Ingredient
from libs.drinkMixingMachine.programStates.iState import IState
from libs.hardware.dispenseMechanism.dispenseMechanism import DispenseMechanism
from libs.hardware.scale.scale import Scale
from libs.ui.IUserInterface import IUserInterface


class DispenseDrinkState(IState):
    __ui: IUserInterface = None
    __dispenseMechanism: DispenseMechanism = None
    __scale: Scale = None
    __data: Data = None

    def __init__(
        self,
        ui: IUserInterface,
        dispense_mechanism: DispenseMechanism,
        scale: Scale,
        data: Data,
    ):
        self.__ui = ui
        self.__dispenseMechanism = dispense_mechanism
        self.__scale = scale
        self.__data = data

    def get_descriptor(self) -> str:
        return "Select a Drink"

    def run(self) -> None:
        drink = self.__select_drink()
        if drink is not None:
            self.__dispenseMechanism.dispense_drink(
                ingredients_to_dispense=self.__get_ingredients_for_drink(drink)
            )

    @staticmethod
    def __create_drink_selection_list(drinks: list[Drink]):
        drink_selection: list[str] = []
        for drink in drinks:
            drink_selection.append(drink.name)
        return drink_selection

    def __select_drink(self) -> Drink | None:
        drinks = self.__data.get_drinks()
        selection_list: list[str] = self.__create_drink_selection_list(drinks=drinks)
        selection_list.append("Exit State")
        selected_drink: int = self.__ui.display_list_and_wait_for_user_selection(
            input_data=selection_list
        )
        if selected_drink == len(drinks):
            return None
        else:
            return drinks[selected_drink]

    def __get_ingredients_for_drink(self, drink: Drink) -> list[(int, int, int)]:
        ingredients: list[(int, int, int)] = []
        available_ingredients: list[Ingredient] = self.__data.get_ingredients()
        for ingredient_id, percentage in drink.get_ingredients():
            ingredient = self.__get_ingredient(
                ingredient_id=ingredient_id, ingredients=available_ingredients
            )
            if ingredient is None:
                ingredients.append((None, percentage, None))
            else:
                ingredients.append(
                    (ingredient.dispenser_id, percentage, ingredient.flow_speed)
                )
        return ingredients

    @staticmethod
    def __get_ingredient(
        ingredient_id: int, ingredients: list[Ingredient]
    ) -> Ingredient | None:
        for ingredient in ingredients:
            if ingredient.get_id() == ingredient_id:
                return ingredient
        return None
