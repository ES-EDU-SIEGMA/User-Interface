import PyQt5.QtWidgets as PyQtWidgets
import PyQt5.QtCore as PyQtCore
import PyQt5.QtGui as PyQtGui
import time
from libs import json_data as JsonData
from libs import runtime_data as RuntimeData
from libs import create_cocktail as CreateCocktail
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

        # Labels

        self.__available_list_label = PyQtWidgets.QLabel("Available beverages")
        self.__available_list_label.setAlignment(PyQtCore.Qt.AlignCenter)

        self.__selected_list_label = PyQtWidgets.QLabel("Selected beverages")
        self.__selected_list_label.setAlignment(PyQtCore.Qt.AlignCenter)

        self.__recipe_label = PyQtWidgets.QLabel("Name of recipe:")
        self.__recipe_label.setStyleSheet(css.style_ndw_recipe_label)

        # Buttons

        self.__accept_button: PyQtWidgets.QPushButton = PyQtWidgets.QPushButton("Accept")
        self.__accept_button.clicked.connect(self.on_accept)
        # the accept button checks whether the cocktail meets certain criteria

        self.__cancel_button: PyQtWidgets.QPushButton = PyQtWidgets.QPushButton("Cancel")
        self.__cancel_button.clicked.connect(self.on_cancel)
        # the cancel button functions like a back button
        # todo the cancel button should call control and change the view or it should change the view automatically

        self.__view_cocktails_button: PyQtWidgets.QPushButton = PyQtWidgets.QPushButton("Cocktails")
        self.__view_cocktails_button.clicked.connect(self.view_cocktails_button_on_click)
        # the view cocktails button opens a new window that shows all available cocktails
        # todo the connect function should call the window directly or redirect to controller

        # Line-edit for the new recipe name

        self.__enter_recipe_name: PyQtWidgets.QLineEdit = PyQtWidgets.QLineEdit()
        self.__enter_recipe_name.setStyleSheet(css.style_ndw_line_edit_recipe_name)

        # QListWidgets to select beverages for the recipe

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

        self.setLayout(self.__grid_layout)

    def activate(self, __data_beverage_names: list[str], __data_recipe_names: list[str]) -> str:
        self.__data_available_beverage_names = __data_beverage_names
        self.__data_recipe_names = __data_recipe_names
        self.__return_value = ""
        self.__selected_drinks_and_fill_amounts = []
        self.__sum_fill_amounts = 0
        self.__update_available_beverages_list()
        self.show()
        while self.return_value == "":  # that's not rly good code. got to revisit this one later
            time.sleep(1)
        return self.return_value

    def reactivate(self):
        self.__return_value = ""
        self.__selected_drinks_and_fill_amounts = []
        self.__sum_fill_amounts = 0
        self.__update_available_beverages_list()
        while self.return_value == "":  # that's not rly good code. got to revisit this one later
            time.sleep(1)
        return self.return_value

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
