import PyQt5.QtWidgets as PyQtWidgets
import PyQt5.QtCore as PyQtCore
import css.css_edit_hoper_window as Css


class EditHopper(PyQtWidgets.QWidget):
    __data_hopper_names: list[str]
    __data_beverage_names: list[str]
    __commands: list[str] = ["drinks", "edit", "new", "exit"]
    __return_value: str

    __header_label: PyQtWidgets.QLabel
    __monitor_label: PyQtWidgets.QLabel

    __hopper_button_list: list

    def __init__(self, __parent):
        super().__init__()
        self.parentWidget = __parent
        self.__init_widgets()

    def __init_widgets(self):
        self.resize(1200, 800)
        self.showFullScreen()
        self.setWindowTitle("Edit hopper window")
        self.setStyleSheet(Css.window_style)  # todo add css style

        # Labels

        self.__header_label = PyQtWidgets.QLabel("Edit Hopper Occupancy", self)
        self.__header_label.setStyleSheet(Css.style_ew_header_label)
        self.__header_label.setAlignment(PyQtCore.Qt.AlignCenter)

        self.__monitor_label = PyQtWidgets.QLabel("Monitor is here", self)
        self.__monitor_label.setStyleSheet(Css.style_ew_monitor_label)
        self.__monitor_label.setAlignment(PyQtCore.Qt.AlignCenter)

        self.back_button = PyQtWidgets.QPushButton("Back to Main menu", self)
        self.back_button.clicked.connect(lambda: self.back_button_on_click())  # todo change function
        self.back_button.setStyleSheet(Css.style_ew_button_back)

        # Hopper Layout

        self.hopper_frame = PyQtWidgets.QFrame(self)
        self.hopper_display_layout = PyQtWidgets.QGridLayout(self)
        self.hopper_display_layout.setColumnMinimumWidth(2, 15)
        self.hopper_display_layout.setColumnMinimumWidth(9, 15)
        self.hopper_frame.setLayout(self.hopper_display_layout)

        # Layout window

        self.main_layout = PyQtWidgets.QGridLayout(self)
        self.main_layout.addWidget(self.__header_label, 0, 0, 1, 5)
        self.main_layout.addWidget(self.__monitor_label, 7, 0, 1, 5)
        self.main_layout.addWidget(self.hopper_frame, 2, 0, 5, 5)
        self.main_layout.addWidget(self.back_button, 8, 4)

    def activate(self):
        self.__update_hopper_layout()
        self.show()

    def reactivate(self):
        self.show()

    def deactivate(self):
        self.hide()

    def __update_hopper_layout(self):
        # todo make deletion simpler
        for i in reversed(range(self.hopper_display_layout.count())):
            self.hopper_display_layout.takeAt(i).widget().setParent(None)
        for __beverage_button in self.__hopper_button_list:
            self.hopper_display_layout.addWidget(HopperButton())


class HopperButton:
    pass
