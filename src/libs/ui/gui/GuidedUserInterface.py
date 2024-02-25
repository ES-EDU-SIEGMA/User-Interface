from __future__ import annotations

from queue import Queue
from time import sleep

from libs.ui.IUserInterface import IUserInterface
from libs.ui.gui.pySerias6App.app import UiApp, MessageType


class GuidedUserInterface(IUserInterface):
    __queue_to_ui: Queue = None
    __queue_from_ui: Queue = None
    __ui: UiApp = None
    __counter: int = 0

    def __init__(self):
        self.__queue_to_ui = Queue()
        self.__queue_from_ui = Queue()

        self.__ui = UiApp(messages=self.__queue_to_ui, responses=self.__queue_from_ui)
        self.__ui.start()
        sleep(5)

    def display_list_and_wait_for_user_selection(self, input_data: list[str]) -> int:
        self.__queue_to_ui.put((MessageType.SELECTION, input_data))
        selection = self.__queue_from_ui.get()
        return selection

    def display_message_and_wait_for_acknowledgement(self, input_data: str) -> None:
        self.__queue_to_ui.put((MessageType.MESSAGE, input_data))
        self.__queue_from_ui.get()

    def display_status(self, input_data: str) -> None:
        self.__queue_to_ui.put((MessageType.STATUS, input_data))


if __name__ == "__main__":
    ui = GuidedUserInterface()
    result = ui.display_list_and_wait_for_user_selection(["1","2","3"])
    print(f"Result: {result}")
    while True:
        print("RUNNING")
        sleep(60)
