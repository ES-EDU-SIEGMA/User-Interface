from libs.drinkMixingMachine.programStates.iState import IState


class EditIngredientsState(IState):
    def get_descriptor(self) -> str:
        return "Edit Ingredients"

    def run(self) -> None:
        raise NotImplementedError()
