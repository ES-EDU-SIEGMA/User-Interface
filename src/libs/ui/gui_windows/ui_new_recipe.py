import sys

import PyQt5.QtWidgets as PyQtWidgets
import PyQt5.QtCore as PyQtCore
import PyQt5.QtGui as PyQtGui
import time
from libs import runtime_data as RuntimeData
from libs.ui.gui_windows.css import css_new_drink_window as css


########################################################################################################################
# Functions to handle data
########################################################################################################################
def get_beverage_by_name(beverages: list[RuntimeData.Beverage], name: str) -> RuntimeData.Beverage:
    for beverage in beverages:
        if beverage.beverage_name == name:
            return beverage


def fill_list(widget_list: PyQtWidgets.QListWidget, beverages: list[RuntimeData.Beverage]):
    for beverage in beverages:
        widget_list.addItem(beverage.beverage_name)


########################################################################################################################
# Window where you can create a new cocktail recipe
########################################################################################################################

class NewRecipe(PyQtWidgets.QWidget):
    __data_available_beverage_names: list[str] = None
    __data_selected_beverage_names: list[str] = None
    __data_recipe_names: list[str] = None
    __commands: list[str] = ["help", "recipes", "beverage", "my-recipe", "selection", "new", "exit"]
    __return_value: str = None

    __selected_drinks_and_fill_amounts: list[str] = None
    __sum_fill_amounts: int = None
    MAX_FILL_AMOUNT: int = 350

    __not_selected_beverages: list[str] = []

    __available_list_label: PyQtWidgets.QLabel
    __selected_list_label: PyQtWidgets.QLabel
    __recipe_label: PyQtWidgets.QLabel
    __available_beverage_list: PyQtWidgets.QListWidget
    __selected_beverage_list: PyQtWidgets.QListWidget
    __grid_layout: PyQtWidgets.QGridLayout
    __wrapper: PyQtWidgets.QWidget
    __wrapper_widget_layout: PyQtWidgets.QVBoxLayout

    def __init__(self, __parent_window: PyQtWidgets.QWidget):
        super().__init__()
        self.parentWidget = __parent_window
        self.__init_widgets()

    def __init_widgets(self):
        self.resize(1280, 800)  # todo Is resize necessary if we use showFullScreen() afterwards?
        self.showFullScreen()
        self.setWindowTitle("New Cocktail Recipe")  # todo I don't think u can see the title maybe remove title?
        self.setStyleSheet(css.window_style)  # todo rework the css

        # new stuff

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

        # Labels

        """self.__available_list_label = PyQtWidgets.QLabel("Available ingredients")
        self.__available_list_label.setAlignment(PyQtCore.Qt.AlignCenter)

        self.__selected_list_label = PyQtWidgets.QLabel("Selected ingredients")
        self.__selected_list_label.setAlignment(PyQtCore.Qt.AlignCenter)

        self.__recipe_label = PyQtWidgets.QLabel("Name of recipe:")
        self.__recipe_label.setStyleSheet(css.style_ndw_recipe_label)

        # Buttons

        self.__accept_button: PyQtWidgets.QPushButton = PyQtWidgets.QPushButton("Accept")
        self.__accept_button.clicked.connect(lambda: print("test_accept"))
        # the accept button checks whether the cocktail meets certain criteria

        self.__cancel_button: PyQtWidgets.QPushButton = PyQtWidgets.QPushButton("Cancel")
        self.__cancel_button.clicked.connect(lambda: print("test_cancel"))
        # the cancel button functions like a back button
        # todo the cancel button should call control and change the view or it should change the view automatically

        self.__view_cocktails_button: PyQtWidgets.QPushButton = PyQtWidgets.QPushButton("Cocktails")
        self.__view_cocktails_button.clicked.connect(lambda: print("test_cocktails"))
        # the view cocktails button opens a new window that shows all available cocktails
        # todo the connect function should call the window directly or redirect to controller

        # Line-edit for the new recipe name

        self.__enter_recipe_name: PyQtWidgets.QLineEdit = PyQtWidgets.QLineEdit()
        self.__enter_recipe_name.setStyleSheet(css.style_ndw_line_edit_recipe_name)

        # QListWidgets to select ingredients for the recipe

        self.__available_beverage_list = PyQtWidgets.QListWidget(self)
        self.__available_beverage_list.setFixedSize(self.listSize[0], self.listSize[1])
        self.__available_beverage_list.setMinimumHeight(550)
        self.__available_beverage_list.setFont(PyQtGui.QFont("Arial", 15))
        self.__available_beverage_list.itemDoubleClicked.connect(self.__beverage_selected)

        self.__selected_beverage_list = PyQtWidgets.QListWidget(self)
        self.__selected_beverage_list.setFixedSize(self.listSize[0], self.listSize[1])
        self.__selected_beverage_list.setMinimumHeight(550)
        self.__selected_beverage_list.setFont(PyQtGui.QFont("Arial", 15))
        self.__selected_beverage_list.itemDoubleClicked.connect(self.__beverage_deselected)

        # Layout of the Widgets in the window

        self.__grid_layout = PyQtWidgets.QGridLayout(self)
        self.__grid_layout.setRowStretch(0, 1)
        self.__grid_layout.setRowStretch(3, 1)
        self.__grid_layout.setColumnStretch(1, 1)
        self.__grid_layout.setColumnStretch(3, 1)

        self.__grid_layout.addWidget(self.__available_list_label, 0, 0)
        self.__grid_layout.addWidget(self.__selected_list_label, 0, 2)
        self.__grid_layout.addWidget(self.__available_beverage_list, 2, 0)
        self.__grid_layout.addWidget(self.__selected_beverage_list, 2, 2)

        __wrapper_widget = PyQtWidgets.QWidget()
        __wrapper_widget_layout = PyQtWidgets.QVBoxLayout()
        __wrapper_widget_layout.addWidget(self.__recipe_label)
        __wrapper_widget_layout.addWidget(self.__enter_recipe_name)
        __wrapper_widget_layout.addWidget(self.__accept_button)
        __wrapper_widget_layout.addWidget(self.__cancel_button)
        __wrapper_widget_layout.addWidget(self.__view_cocktails_button)
        __wrapper_widget.setLayout(__wrapper_widget_layout)
        self.__grid_layout.addWidget(__wrapper_widget, 2, 4)

        self.setLayout(self.__grid_layout)"""

    def activate(self, __data_beverage_names: list[str], __data_recipe_names: list[str]) -> str:
        self.__data_available_beverage_names = __data_beverage_names
        self.__data_recipe_names = __data_recipe_names
        self.__return_value = ""
        self.__selected_drinks_and_fill_amounts = []
        self.__sum_fill_amounts = 0
        self.__update_available_beverages_list()
        self.show()

    def deactivate(self):
        self.hide()

    def __update_beverage_lists(self):
        self.__available_beverage_list.clear()
        for __beverage_name in self.__data_available_beverage_names:
            self.__available_beverage_list.addItem(__beverage_name)

        self.__selected_beverage_list.clear()
        for __beverage_name in self.__data_selected_beverage_names:
            self.__selected_beverage_list.addItem(__beverage_name)

    def __beverage_selected(self, __widget_item: PyQtWidgets.QListWidgetItem):
        dialog = EnterIntDialogWindow("Enter Int Dialog Title", "Enter fill percentage drink")

        # todo change if statements to check the positive case first.
        if not dialog.exec_():  # if no int value
            if dialog.cancel:  # if input window closed
                return
            else:
                # if dialog didn't return an integer and the user didn't cancel send an error message
                PyQtWidgets.QMessageBox.critical(
                    self,
                    "Error", "Please enter an integer value.",
                    buttons=PyQtWidgets.QMessageBox.Discard,
                    defaultButton=PyQtWidgets.QMessageBox.Discard, )  # todo try to remove last , without parameter
                return

        elif dialog.exec_():  # int value. probably don't need to check for int value
            __input_fill_amount: str = str(dialog.int)
            __selected_drink_name: str = __widget_item.text()

            self.__selected_beverage_list.addItem(f"{__selected_drink_name} - {__input_fill_amount}%")
            self.__selected_drinks_and_fill_amounts.append(__selected_drink_name)
            self.__selected_drinks_and_fill_amounts.append(__input_fill_amount)
            self.__data_available_beverage_names.remove(__selected_drink_name)
            self.__data_selected_beverage_names.append(__selected_drink_name)
            self.__update_beverage_lists()

    def __beverage_deselected(self, __widget_item: PyQtWidgets.QListWidgetItem):
        __deselected_drink_name: str = __widget_item.text()
        __index: int = self.__selected_drinks_and_fill_amounts.index(__deselected_drink_name)
        self.__selected_drinks_and_fill_amounts.pop(__index)  # remove the drink name
        self.__selected_drinks_and_fill_amounts.pop(__index)  # remove the drink fill amount
        self.__data_selected_beverage_names.remove(__deselected_drink_name)
        self.__data_available_beverage_names.append(__deselected_drink_name)
        self.__update_beverage_lists()


class EnterIntDialogWindow(PyQtWidgets.QDialog):
    cancel: bool
    __input_int: int

    __qt_button: int
    __label: PyQtWidgets.QLabel
    __line_edit: PyQtWidgets.QLineEdit
    __button_box: PyQtWidgets.QDialogButtonBox

    def __init__(self, __title: str, __label: str):
        super().__init__()
        # todo change layout of the QDialog window
        self.cancel = False
        self.__input_int = 0

        self.setStyleSheet(css.dialog_style)  # todo change css rules
        self.setWindowTitle(__title)

        __qt_button = PyQtWidgets.QDialogButtonBox.Ok | PyQtWidgets.QDialogButtonBox.Cancel
        layout = PyQtWidgets.QVBoxLayout(self)

        self.__label = PyQtWidgets.QLabel()
        self.__label.setText(__label)
        self.__line_edit = PyQtWidgets.QLineEdit()
        self.__line_edit.maxLength = 3

        layout.addWidget(self.__label)
        layout.addWidget(self.__line_edit)

        self.__button_box = PyQtWidgets.QDialogButtonBox(__qt_button)
        self.__button_box.accepted.connect(self.exit)
        self.__button_box.rejected.connect(self.reject)

        layout.addWidget(self.__button_box)

    def exit(self):
        __input_str: str = self.__line_edit.text()
        if __input_str.isdigit():
            self.__input_int = int(__input_str)
            self.accept()
        else:
            super().reject()

    def reject(self):
        self.cancel = True
        super().reject()

    def set_label(self, text=""):
        self.__label.setText(text)


if __name__ == "__main__":
    """ used to test out the pyqt window selection without functionality"""
    print("main")
    __app = PyQtWidgets.QApplication(sys.argv)
    selection = NewRecipe(__app)
    sys.exit(__app.exec())
