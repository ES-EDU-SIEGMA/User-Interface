import time

import PyQt5.QtWidgets as PyQtWidgets
import PyQt5.QtCore as PyQtCore
import PyQt5.QtGui as PyQtGui
from ...libs import json_data as JsonData
from ...libs import runtime_data as RuntimeData
from ...libs import create_cocktail as CreateCocktail
import css_new_drink_window as css


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

class NewCocktailWindow(PyQtWidgets.QWidget):
    listSize = (450, 450)

    def __init__(self, __parent_window: PyQtWidgets.QWidget, __runtime_data: RuntimeData.RuntimeData):
        # not sure whether control implements a QWidget class
        super().__init__()
        self.parentWidget = __parent_window

        # need the following information for this class: all beverage names

        # the following code fputs all available beverages into beverage_list
        self.beverage_list = []
        for beverage in __runtime_data.beverages_on_hopper:
            # runtime data needs to consists of all beverages
            self.beverage_list.append(beverage)
        self.new_mix_drink = None
        # need the following information for this class: all beverage names
        # todo change the access from an object to only needing names.

        # runtime_data isn't enough as we need every beverage not only those on the hopper.
        # currently runtime_data is names available Beverages, but it shouldn't be a problem to
        # use runtime data with all beverages regardless of whether they are on the hopper.
        # in the following i assume that runtime_data consists of all beverages

        self.resize(1280, 800)  # Is resize necessary if u use showFullScreen() afterwards?
        self.showFullScreen()
        self.setWindowTitle("New Cocktail Recipe")  # I don't think u can see the title maybe remove title?
        self.setStyleSheet(css.window_style)  # defines the styles for every item in the window

        ################################################################################################################
        # set up Lists and ListWidgets
        ################################################################################################################

        self.available_beverages = []

        # available_beverage_list is a list of beverage buttons displayed on the screen
        # if a beverage button is double-clicked the beverage button is transferred to selected_beverage_list
        # available in available_beverage_list doesn't refer to the beverages being on the hopper
        self.available_beverage_list: PyQtWidgets.QListWidget = PyQtWidgets.QListWidget(self)
        self.available_beverage_list.setFixedSize(self.listSize[0], self.listSize[1])
        self.available_beverage_list.setMinimumHeight(550)
        self.available_beverage_list.setFont(PyQtGui.QFont("Arial", 15))
        self.available_beverage_list.itemDoubleClicked.connect(self.on_available_select)
        # connect calls a method that puts the selected beverage into the selected_beverage_list

        # selected_beverage_list is a list of beverage buttons displayed on the screen
        # if a beverage button is clicked the beverage is returned to the available_beverage_list
        self.selected_beverage_list: PyQtWidgets.QListWidget = PyQtWidgets.QListWidget(self)
        self.selected_beverage_list.setFixedSize(self.listSize[0], self.listSize[1])
        self.selected_beverage_list.setMinimumHeight(550)
        self.selected_beverage_list.setFont(PyQtGui.QFont("Arial", 15))
        self.selected_beverage_list.itemDoubleClicked.connect(self.on_selected_select)
        # connect calls a method that puts the selected beverage into the available_beverage_list

        ################################################################################################################
        # set up Buttons
        ################################################################################################################

        self.accept_button: PyQtWidgets.QPushButton = PyQtWidgets.QPushButton("Accept")
        self.accept_button.clicked.connect(self.on_accept)
        # the accept button checks whether the cocktail meets certain criteria

        self.cancel_button: PyQtWidgets.QPushButton = PyQtWidgets.QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.on_cancel)
        # the cancel button functions like a back button
        # todo the cancel button should call control and change the view or it should change the view automatically

        self.view_cocktails_button: PyQtWidgets.QPushButton = PyQtWidgets.QPushButton("Cocktails")
        self.view_cocktails_button.clicked.connect(self.view_cocktails_button_on_click)
        # the view cocktails button opens a new window that shows all available cocktails
        # todo the connect function should call the window directly or redirect to controller

        ################################################################################################################
        # set up Labels
        ################################################################################################################

        self.available_list_label: PyQtWidgets.QLabel = PyQtWidgets.QLabel("Available beverages")
        self.available_list_label.setAlignment(PyQtCore.Qt.AlignCenter)

        self.selected_list_label: PyQtWidgets.QLabel = PyQtWidgets.QLabel("Selected beverages")
        self.selected_list_label.setAlignment(PyQtCore.Qt.AlignCenter)

        self.recipe_label: PyQtWidgets.QLabel = PyQtWidgets.QLabel("Name of recipe:")
        self.recipe_label.setStyleSheet(css.style_ndw_recipe_label)

        ################################################################################################################
        # Set up line edit widget
        ################################################################################################################

        self.enterRecipeName: PyQtWidgets.QLineEdit = PyQtWidgets.QLineEdit()
        self.enterRecipeName.setStyleSheet(css.style_ndw_line_edit_recipe_name)
        # the line edit widget allows the user to insert a recipe name

        ################################################################################################################
        # Set up the layout of the window elements
        ################################################################################################################

        self.grid_layout: PyQtWidgets.QGridLayout = PyQtWidgets.QGridLayout(self)
        self.grid_layout.setRowStretch(0, 1)
        self.grid_layout.setRowStretch(3, 1)
        self.grid_layout.setColumnStretch(1, 1)
        self.grid_layout.setColumnStretch(3, 1)

        self.grid_layout.addWidget(self.available_list_label, 0, 0)
        self.grid_layout.addWidget(self.selected_list_label, 0, 2)
        self.grid_layout.addWidget(self.available_beverage_list, 2, 0)
        self.grid_layout.addWidget(self.selected_beverage_list, 2, 2)

        wrapper: PyQtWidgets.QWidget = PyQtWidgets.QWidget()
        wrapper_layout: PyQtWidgets.QVBoxLayout = PyQtWidgets.QVBoxLayout()
        wrapper_layout.addWidget(self.recipe_label)
        wrapper_layout.addWidget(self.enterRecipeName)
        wrapper_layout.addWidget(self.accept_button)
        wrapper_layout.addWidget(self.cancel_button)
        wrapper_layout.addWidget(self.view_cocktails_button)
        wrapper.setLayout(wrapper_layout)

        self.grid_layout.addWidget(wrapper, 2, 4)

        self.setLayout(self.grid_layout)

        fill_list(self.available_beverage_list, self.beverage_list)

    ####################################################################################################################
    # Events
    ####################################################################################################################

    def on_available_select(self, widget_item: PyQtWidgets.QListWidgetItem):
        dialog = EnterIntDialogWindow("Enter Int Dialog Title", "Enter fill percentage drink")
        # opens a new window to enter the fill percentage of the beverage.
        # The new window lies on top of the already existing window.

        if not dialog.exec_():
            if dialog.cancel:
                return
            else:
                # if dialog didn't return an integer and the user didn't cancel send an error message
                error_message = PyQtWidgets.QMessageBox.critical(
                    self,
                    "Error", "Please enter an integer value.",
                    buttons=PyQtWidgets.QMessageBox.Discard,
                    defaultButton=PyQtWidgets.QMessageBox.Discard, )
                return

        elif dialog.exec_():
            result = dialog.int

            # item is a special pyqt5 object. Therefore, we are using text()
            beverage = get_beverage_by_name(self.available_beverages, widget_item.text())

            # we need a datastructure that hold beverages and their percentages lists
            self.mix_drink.mix_drink_needed_beverages.append(beverage)  # append beverage
            self.mix_drink.mix_drink_fill_perc_beverages.append([beverage.beverage_id, result])  # append list[beverage_id, fill_perc]
            # todo change the creation of an object to a dict

            self.selected_beverage_list.addItem(f"{beverage.beverage_name} - {result}%")  # change the beverage list
            self.available_beverages.remove(beverage)  # change the available_beverage_list

            self.available_beverage_list.clear()  # deletes all items in available_beverage_list
            fill_list(self.available_beverage_list, self.available_beverages)  # rebuilds available_beverage_list
            # todo instead of rebuilding the entire beverage list removing one element might be better

    def on_selected_select(self, item: PyQtWidgets.QListWidgetItem):
        # get Beverage
        name = item.text().split()[0]
        beverage = get_beverage_by_name(self.mix_drink.mix_drink_needed_beverages, name)
        index = self.mix_drink.mix_drink_needed_beverages.index(beverage)

        # remove Beverage from selected_beverage_list
        self.selected_beverage_list.takeItem(index)
        self.mix_drink.mix_drink_needed_beverages.remove(beverage)
        fill_perc = self.mix_drink.get_fill_perc(beverage.beverage_id)
        self.mix_drink.mix_drink_fill_perc_beverages.remove([beverage.beverage_id, fill_perc])

        # add Beverage back to availableList
        self.available_beverages.append(beverage)
        fill_list(self.available_beverage_list, self.available_beverages)

    def on_accept(self):
        # checking whether the new_cocktail fulfills certain drink criteria

        result = 0
        print(self.mix_drink.mix_drink_fill_perc_beverages)  # do we need a print here?
        for beverage in self.mix_drink.mix_drink_needed_beverages:
            result += self.mix_drink.get_fill_perc(beverage.beverage_id)

        if result != 100:
            error_message = PyQtWidgets.QMessageBox.critical(
                self,
                "Error", "Your Drink holds an insufficient amount.",
                buttons=PyQtWidgets.QMessageBox.Discard,
                defaultButton=PyQtWidgets.QMessageBox.Discard)
            return
        # checks if the mix_drink beverages combine to 100% fill_perc

        self.mix_drink.mix_drink_name = self.enterRecipeName.text()
        print(self.mix_drink)

        if not JsonData.save_cocktails(self.mix_drink):
            error_message = PyQtWidgets.QMessageBox.critical(
                self,
                "Error", "Name for Mixed Drink is already in use.",
                buttons=PyQtWidgets.QMessageBox.Discard,
                defaultButton=PyQtWidgets.QMessageBox.Discard)
            return
        # checks if the name for the mix_drink is available

        self.back_button_on_click()

    def on_cancel(self):
        self.back_button_on_click()

    def back_button_on_click(self):
        self.parentWidget.update_quick_select()
        self.parentWidget.show()
        self.hide()

    def view_cocktails_button_on_click(self):
        self.created_cocktails_window = CreateCocktail.CreatedCocktailsWindow(self)
        self.hide()


class EnterIntDialogWindow(PyQtWidgets.QDialog):
    def __init__(self, __title: str = "", __label: str = ""):
        super().__init__()
        # todo change layout of the QDialog window
        self.cancel = False  # the cancel variable is potentially useless
        self.int = 0

        self.setStyleSheet(css.dialog_style)
        self.setWindowTitle(__title)

        qt_button = PyQtWidgets.QDialogButtonBox.Ok | PyQtWidgets.QDialogButtonBox.Cancel
        layout = PyQtWidgets.QVBoxLayout(self)

        self.label = PyQtWidgets.QLabel()
        self.label.setText(__label)
        self.enterInt = PyQtWidgets.QLineEdit()
        self.enterInt.maxLength = 3

        layout.addWidget(self.label)
        layout.addWidget(self.enterInt)

        self.buttonBox = PyQtWidgets.QDialogButtonBox(qt_button)
        self.buttonBox.accepted.connect(self.exit)
        self.buttonBox.rejected.connect(self.reject)

        layout.addWidget(self.buttonBox)

    def exit(self):
        text = self.enterInt.text()
        if text.isdigit():
            self.int = int(text)
            print(self.int)
            self.accept()
        else:
            super().reject()

    def reject(self):
        self.cancel = True
        super().reject()

    def set_label(self, text=""):
        self.label.setText(text)
