from __future__ import annotations

from enum import Enum
from queue import Queue
from threading import Thread

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QScreen

from libs.ui.gui.pySerias6App.mainWindow import MainWindow


class MessageType(Enum):
    SELECTION = 0
    MESSAGE = 1
    STATUS = 2


class UiApp(Thread):
    __main_window: MainWindow = None
    __output_queue: Queue = None

    def __init__(self, messages: Queue, responses: Queue):
        Thread.__init__(self)
        self.daemon = True
        self.__input_thread = Thread(
            target=self.__input_handle, kwargs={"input_queue": messages}
        )
        self.__output_queue = responses

    def run(self):
        self.__input_thread.start()

        app = QApplication([])
        width, height = app.screens()[0].size().toTuple()
        self.__main_window = MainWindow(width, height)
        self.__main_window.show()
        self.__main_window.response_signal.connect(self.__output_handle)
        app.exec()

    def __input_handle(self, input_queue: Queue):
        while True:
            msg_type, data = input_queue.get()
            if msg_type == MessageType.SELECTION:
                self.display_selection(data)
            elif msg_type == MessageType.MESSAGE:
                self.display_message(data)
            elif msg_type == MessageType.STATUS:
                self.display_status(data)
            else:
                raise NotImplementedError()

    def __output_handle(self, response: int):
        self.__output_queue.put(response)

    def display_selection(self, message: list[str]):
        self.__main_window.selection_signal.emit(message)

    def display_message(self, message: str):
        self.__main_window.message_signal.emit(message)

    def display_status(self, message: str):
        self.__main_window.status_signal.emit(message)
