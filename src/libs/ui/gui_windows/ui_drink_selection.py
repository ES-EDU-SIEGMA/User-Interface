from .. import userinterface as CallBack
import PyQt5.QtWidgets as PyQtWidgets
import PyQt5.QtCore as PyQtCore
import time
from libs.ui.gui_windows.css import css_selection_window as css
import sys


class Selection(PyQtWidgets.QWidget):
    __data_drink_names: list[str] = None
    call_back_object: CallBack.UserInterface
    return_value: str = None

    __header_label: PyQtWidgets.QLabel
    __sub_header_label: PyQtWidgets.QLabel
    __description_label: PyQtWidgets.QLabel

    __exit_btn: PyQtWidgets.QPushButton
    __new_cocktail_btn: PyQtWidgets.QPushButton
    __edit_hoppers_btn: PyQtWidgets.QPushButton

    __all_drinks_frame: PyQtWidgets.QScrollArea
    __wrapper_widget: PyQtWidgets.QWidget
    __scroll_area_drinks: PyQtWidgets.QVBoxLayout
    __window_layout: PyQtWidgets.QGridLayout

    def __init__(self, __callback_object, __parent_window: PyQtWidgets.QWidget):

        super().__init__()
        self.parentWidget = __parent_window
        self.__init_widgets()
        print("init")

    def __init_widgets(self):
        self.setWindowTitle("SIEGMA_2223")
        self.resize(1200, 800)
        self.showFullScreen()
        self.setStyleSheet(css.style_selection_window)

        # Labels

        self.__header_label = PyQtWidgets.QLabel("Drink Mixing Machine", self)
        self.__header_label.setAlignment(PyQtCore.Qt.AlignCenter)
        self.__header_label.setStyleSheet(css.style_sw_header_label)

        self.__sub_header_label = PyQtWidgets.QLabel("SIEGMA-WS2223", self)
        self.__sub_header_label.setAlignment(PyQtCore.Qt.AlignCenter)
        self.__sub_header_label.setStyleSheet(css.style_sw_sub_header_label)

        self.__description_label = PyQtWidgets.QLabel("Quick select for drinks:", self)
        self.__description_label.setStyleSheet(css.style_sw_description_label)

        # Buttons

        self.__exit_btn = PyQtWidgets.QPushButton("Exit Application", self)
        self.__exit_btn.setStyleSheet(css.style_sw_exit_button)
        self.__exit_btn.clicked.connect(self.call_back_object.call_back_pyqt("exit"))
        # todo create a connect function that calls control with the cmd to terminate the application

        self.__new_cocktail_btn = PyQtWidgets.QPushButton("New Cocktail", self)
        self.__new_cocktail_btn.setStyleSheet(css.style_sw_new_cocktail_button)
        self.__new_cocktail_btn.clicked.connect(self.call_back_object.call_back_pyqt("change_window;new"))
        # todo create a connect function that calls control with the cmd to add a new cocktail

        self.__edit_hoppers_btn = PyQtWidgets.QPushButton("Change Drinks on Hopper", self)
        self.__edit_hoppers_btn.setStyleSheet(css.style_sw_edit_hoppers_button)
        self.__edit_hoppers_btn.clicked.connect(self.call_back_object.call_back_pyqt("change_window;edit"))
        # todo create a connect function that calls control with the cmd to change the drinks on the hopper

        # Scroll area widget that holds the available drink buttons

        self.__all_drinks_frame = PyQtWidgets.QScrollArea(self)
        self.__wrapper_widget = PyQtWidgets.QWidget()
        self.__scroll_area_drinks = PyQtWidgets.QVBoxLayout()

        # self.update_quick_select()

        self.__wrapper_widget.setLayout(self.__scroll_area_drinks)

        self.__all_drinks_frame.setVerticalScrollBarPolicy(PyQtCore.Qt.ScrollBarAlwaysOn)
        self.__all_drinks_frame.setHorizontalScrollBarPolicy(PyQtCore.Qt.ScrollBarAlwaysOff)
        self.__all_drinks_frame.setWidgetResizable(True)
        self.__all_drinks_frame.setStyleSheet(css.style_sw_all_drinks_frame)
        self.__all_drinks_frame.setWidget(self.__wrapper_widget)

        # Layout of the widgets inside the window

        self.__window_layout = PyQtWidgets.QGridLayout(self)
        self.__window_layout.addWidget(self.__header_label, 0, 0, 1, 3)
        self.__window_layout.addWidget(self.__sub_header_label, 1, 0, 1, 3)
        self.__window_layout.addWidget(self.__description_label, 2, 0)
        self.__window_layout.addWidget(self.__new_cocktail_btn, 4, 2)
        self.__window_layout.addWidget(self.__edit_hoppers_btn, 6, 2)
        self.__window_layout.addWidget(self.__exit_btn, 8, 2)
        self.__window_layout.addWidget(self.__all_drinks_frame, 3, 0, 6, 2)
        self.setLayout(self.__window_layout)

    def activate(self, __data_drink_names: list[str]) -> str:
        self.__data_drink_names = __data_drink_names
        self.return_value = ""
        self.__update_button_layout()
        self.show()
        while self.return_value == "":  # that's not rly good code. got to revisit this one later
            time.sleep(1)
        return self.return_value

    def reactivate(self) -> str:
        self.return_value = ""
        # self.show()  # todo : don't know whether this is needed maybe show is already active
        while self.return_value == "":  # that's not rly good code. got to revisit this one later
            time.sleep(1)
        return self.return_value

    def deactivate(self):
        self.hide()

    def __update_button_layout(self):
        # deletes all drink_buttons in __scroll_area_drinks and rebuilds the widget completely new

        # deletes all drink_buttons.
        # doesn't work without reversed() in some cases.
        for __drink_button_position in reversed(range(self.__scroll_area_drinks.count())):
            self.__scroll_area_drinks.takeAt(__drink_button_position).widget().setParent(None)

        # fills __scroll_area_drinks with buttons that represent every available drink.
        for __drink_name in self.__data_drink_names:
            self.__scroll_area_drinks.addWidget(
                DrinkButton(self, __drink_name))


class DrinkButton(PyQtWidgets.QPushButton):
    # holds the available drinks as a button
    __drink_name: str

    def __init__(self, __parent_window: PyQtWidgets.QWidget, __drink_name):
        super().__init__()
        self.parentWidget = __parent_window
        self.__drink_name = __drink_name
        self.setStyleSheet(css.style_selection_window_drink_button)

        self.setText(self.__drink_name)
        self.clicked.connect(lambda: self.__set_return_value())

    def __set_return_value(self):
        Selection.call_back_object.call_back_pyqt(f"command;selection;{self.__drink_name}")


if __name__ == "__main__":
    """ used to test out the pyqt window selection without functionality"""
    print("main")
    __app = PyQtWidgets.QApplication(sys.argv)
    selection = Selection(__app)
    sys.exit(__app.exec())
