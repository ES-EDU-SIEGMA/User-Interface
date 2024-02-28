from __future__ import annotations

from libs.data.data import Data
from libs.drinkMixingMachine.programStates.dispenseDrink import DispenseDrinkState
from libs.drinkMixingMachine.programStates.editDrinks import EditDrinksState
from libs.drinkMixingMachine.programStates.editIngredients import EditIngredientsState
from libs.drinkMixingMachine.programStates.iState import IState
from libs.hardware.dispenseMechanism.dispenseMechanism import DispenseMechanism
from libs.hardware.scale.scale import Scale
from libs.ui.IUserInterface import IUserInterface


class DrinkMixingMachine:
    __states: list[IState] = None
    __data: Data = None
    __userInterface: IUserInterface = None
    __dispenseMechanism: DispenseMechanism = None
    __scale: Scale = None

    def __init__(
        self,
        scale: Scale,
        ui: IUserInterface,
        dispense_mechanism: DispenseMechanism,
        data: Data,
    ):
        self.__data = data
        self.__dispense_mechanism = dispense_mechanism
        self.__ui = ui
        self.__scale = scale
        self.__create_states()

    def run(self) -> None:
        while True:
            offset, state_list = self.__create_state_selection_list()
            selection: int = self.__ui.display_list_and_wait_for_user_selection(
                state_list
            )
            if selection == 0:
                break
            else:
                self.__execute_state(self.__states[selection - offset])
        self.__on_exit()

    def __on_exit(self) -> None:
        self.__ui.exit_ui()

    def __create_state_selection_list(self) -> (int, list[str]):
        state_selection_list = ["Exit Application"]
        for state in self.__states:
            state_selection_list.append(state.get_descriptor())
        return 1, state_selection_list

    def __create_states(self) -> None:
        self.__states = []
        self.__states.append(
            DispenseDrinkState(
                ui=self.__ui,
                scale=self.__scale,
                dispense_mechanism=self.__dispense_mechanism,
                data=self.__data,
            )
        )
        self.__states.append(EditDrinksState())
        self.__states.append(EditIngredientsState())

    @staticmethod
    def __execute_state(state: IState) -> None:
        try:
            state.run()
        except Exception:
            # TODO add proper logging!
            print("State not available")
