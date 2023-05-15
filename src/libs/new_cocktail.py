import time

import PyQt5.QtWidgets as PyQtWidgets
import PyQt5.QtCore as PyQtCore
import PyQt5.QtGui as PyQtGui
import json_data as JsonData
import runtime_data as RuntimeData
import create_cocktail as CreateCocktail
import css as Css


class NewCocktailWindow(PyQtWidgets.QWidget):
    listSize = (450, 450)

    def __init__(self, __parent_window: PyQtWidgets.QWidget):
        super().__init__()
        self.parentWidget = __parent_window
        self.setWindowTitle("New Cocktail Recipe")
        self.resize(1280, 800)
        self.mix_drink = RuntimeData.MixDrinkInformation(0, "", [], [])
        self.showFullScreen()

        self.setStyleSheet(Css.windowStyle)

        # set up Lists and ListWidgets
        self.available_beverages = []
        self.available_beverage_list: PyQtWidgets.QListWidget = PyQtWidgets.QListWidget(self)
        self.available_beverage_list.setFixedSize(self.listSize[0], self.listSize[1])
        self.available_beverage_list.itemDoubleClicked.connect(self.on_available_select)
        self.available_beverage_list.setMinimumHeight(550)
        self.available_beverage_list.setFont(PyQtGui.QFont("Arial", 15))

        self.selected_beverage_list: PyQtWidgets.QListWidget = PyQtWidgets.QListWidget(self)
        self.selected_beverage_list.setFixedSize(self.listSize[0], self.listSize[1])
        self.selected_beverage_list.itemDoubleClicked.connect(self.on_selected_select)
        self.selected_beverage_list.setMinimumHeight(550)
        self.selected_beverage_list.setFont(PyQtGui.QFont("Arial", 15))

        # set up Buttons
        self.accept_button: PyQtWidgets.QPushButton = PyQtWidgets.QPushButton("Accept")
        self.accept_button.setText("Accept")  # is this needed?
        self.accept_button.clicked.connect(self.on_accept)

        self.cancel_button: PyQtWidgets.QPushButton = PyQtWidgets.QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.on_cancel)

        self.view_cocktails_button: PyQtWidgets.QPushButton = PyQtWidgets.QPushButton("Cocktails")
        self.view_cocktails_button.clicked.connect(self.view_cocktails_button_on_click)

        # set up Labels
        self.available_list_label: PyQtWidgets.QLabel = PyQtWidgets.QLabel("Available beverages")
        self.available_list_label.setAlignment(PyQtCore.Qt.AlignCenter)

        self.selected_list_label: PyQtWidgets.QLabel = PyQtWidgets.QLabel("Selected beverages")
        self.selected_list_label.setAlignment(PyQtCore.Qt.AlignCenter)

        self.recipe_label: PyQtWidgets.QLabel = PyQtWidgets.QLabel("Name of recipe:")
        self.recipe_label.setStyleSheet(
            f"color: {Css.m_standard_text_color}; font-size: 15pt; font-family: {Css.font};")

        # set up LineEdit
        self.enterRecipeName: PyQtWidgets.QLineEdit = PyQtWidgets.QLineEdit()
        self.enterRecipeName.setStyleSheet(
            f"color: {Css.m_standard_text_color}; font-size: 10pt;")

        # set up Layouts
        self.grid_layout: PyQtWidgets.QGridLayout = PyQtWidgets.QGridLayout(self)
        self.grid_layout.setRowStretch(0, 1)
        self.grid_layout.setRowStretch(3, 1)
        self.grid_layout.setColumnStretch(1, 1)
        self.grid_layout.setColumnStretch(3, 1)

        self.grid_layout.addWidget(self.available_list_label, 0, 0, )
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

        self.available_beverages = JsonData.get_all_available_beverages()
        self.available_beverages += JsonData.get_all_other_beverages()
        self.fill_list(self.available_beverage_list, self.available_beverages)

    ################################
    #   Functions to handle data   #
    ################################

    def get_beverage_by_name(self, beverages: list, name: str) -> RuntimeData.Beverage:
        for beverage in beverages:
            if beverage.beverage_name == name:
                return beverage

    def fill_list(self, widget_list: PyQtWidgets.QListWidget, beverages):
        for beverage in beverages:
            widget_list.addItem(beverage.beverage_name)

    ################################
    #           Events             #
    ################################

    def on_available_select(self, widget_item: PyQtWidgets.QListWidgetItem):
        dialog = EnterIntDialog("Enter Int Dialog Title", "Enter Int Dialog Label")

        if dialog.exec_():
            result = dialog.int
        else:
            if dialog.cancel:
                return

            error_message = PyQtWidgets.QMessageBox.critical(
                self,
                "Error", "Please enter an integer value.",
                buttons=PyQtWidgets.QMessageBox.Discard,
                defaultButton=PyQtWidgets.QMessageBox.Discard,)

            return

        # item is a special pyqt5 object. Therefore, we are using text()
        beverage = self.get_beverage_by_name(self.available_beverages, widget_item.text())

        self.mix_drink.mix_drink_needed_beverages.append(beverage)
        self.mix_drink.mix_drink_fill_perc_beverages.append([beverage.beverage_id, result])

        self.selected_beverage_list.addItem(f"{beverage.beverage_name} - {result}%")
        self.available_beverages.remove(beverage)

        self.available_beverage_list.clear()
        self.fill_list(self.available_beverage_list, self.available_beverages)

    def on_selected_select(self, item: PyQtWidgets.QListWidgetItem):
        # get Beverage
        name = item.text().split()[0]
        beverage = self.get_beverage_by_name(self.mix_drink.mix_drink_needed_beverages, name)
        index = self.mix_drink.mix_drink_needed_beverages.index(beverage)

        # remove Beverage from selected_beverage_list
        self.selected_beverage_list.takeItem(index)
        self.mix_drink.mix_drink_needed_beverages.remove(beverage)
        fill_perc = self.mix_drink.get_fill_perc(beverage.beverage_id)
        self.mix_drink.mix_drink_fill_perc_beverages.remove([beverage.beverage_id, fill_perc])

        # add Beverage back to availableList
        self.available_beverages.append(beverage)
        self.fill_list(self.available_beverage_list, self.available_beverages)

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


class EnterIntDialog(PyQtWidgets.QDialog):
    def __init__(self, title="", label=""):
        super().__init__()
        self.cancel = False

        self.setStyleSheet(Css.dialogStyle)
        self.setWindowTitle(title)

        self.int = 0
        qt_button = PyQtWidgets.QDialogButtonBox.Ok | PyQtWidgets.QDialogButtonBox.Cancel

        layout = PyQtWidgets.QVBoxLayout(self)

        self.label = PyQtWidgets.QLabel()
        self.label.setText(label)
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
