from libs.drinkMixingMachine.programStates.iState import IState


class EditDrinksState(IState):
    def get_descriptor(self) -> str:
        return "Edit Drinks"

    def run(self) -> None:
        raise NotImplementedError()
