from __future__ import annotations

from PySide6.QtCore import Signal, QTimer, Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QListWidget,
    QDialog,
    QDialogButtonBox,
    QLabel,
    QVBoxLayout,
    QListWidgetItem,
)


class SelectionDialog(QDialog):
    def __init__(self, parent, options: list[str]):
        super().__init__(parent)
        self.setModal(False)
        self.setWindowFlag(Qt.FramelessWindowHint)

        btn = QDialogButtonBox.Ok
        self.buttonbox = QDialogButtonBox(btn)
        self.buttonbox.accepted.connect(self.accept)
        self.buttonbox.accepted.connect(self.result)

        self.layout = QVBoxLayout()
        selection_label = QLabel("Please select your option:")
        self.selection_list = QListWidget()
        for option in options:
            self.selection_list.addItem(QListWidgetItem(option))
        self.layout.addWidget(selection_label)
        self.layout.addWidget(self.selection_list)
        self.layout.addWidget(self.buttonbox)
        self.setLayout(self.layout)

    def result(self):
        selected_items = self.selection_list.selectedIndexes()
        return selected_items[0].row()


class MainWindow(QMainWindow):
    selection_signal = Signal(list)
    status_signal = Signal(str)
    message_signal = Signal(str)
    response_signal = Signal(int)

    def __init__(self, width, height):
        super().__init__()

        self.width = width
        self.height = height

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.resize(width, height)

        central_label = QLabel("DRINK MIXING MACHINE")
        central_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(central_label)

        self.selection_signal.connect(self.show_selection)
        self.status_signal.connect(self.show_status)
        self.message_signal.connect(self.show_message)

    def show_selection(self, selection: list[str]) -> None:
        msg: SelectionDialog = SelectionDialog(self, selection)
        msg.resize(self.width / 2, self.height)
        msg.exec()
        result = msg.result()
        self.response_signal.emit(result)

    def show_status(self, message: str) -> None:
        msg: QMessageBox = QMessageBox(self)
        msg.setWindowFlag(Qt.FramelessWindowHint)
        msg.resize(self.width / 2, self.height / 2)
        msg.setText(message)
        msg.setModal(True)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.setIcon(QMessageBox.Icon.Information)
        QTimer(msg, singleShot=True, interval=5000, timeout=msg.close).start()
        msg.exec()

    def show_message(self, message: str) -> None:
        msg: QMessageBox = QMessageBox(self)
        msg.setWindowFlag(Qt.FramelessWindowHint)
        msg.resize(self.width / 2, self.height / 2)
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.exec()
        self.response_signal.emit(-1)
