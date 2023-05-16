import PyQt5.QtWidgets as PyQtWidgets
import PyQt5.QtCore as PyQtCore
from ...libs import runtime_data as RuntimeData
import css_selection_window as css
import sys


class SelectionWindow(PyQtWidgets.QWidget):

    def __init__(
            self,
            __runtime_data: RuntimeData.RuntimeData):

        super().__init__()
        self.beverages_and_mix_drinks: RuntimeData.RuntimeData = __runtime_data
        # __runtime_data should consist of available beverages and available mix drinks

        self.setWindowTitle("SIEGMA_2223")
        self.resize(1200, 800)
        self.showFullScreen()

        self.setStyleSheet(css.style_selection_window)

        # Labels

        self.header_label = PyQtWidgets.QLabel("Drink Mixing Machine", self)
        self.header_label.setAlignment(PyQtCore.Qt.AlignCenter)
        self.header_label.setStyleSheet(css.style_sw_header_label)

        self.sub_header_label = PyQtWidgets.QLabel("SIEGMA-WS2223", self)
        self.sub_header_label.setAlignment(PyQtCore.Qt.AlignCenter)
        self.sub_header_label.setStyleSheet(css.style_sw_sub_header_label)

        self.description_label = PyQtWidgets.QLabel("Quick select for drinks:", self)
        self.description_label.setStyleSheet(css.style_sw_description_label)

        # Buttons

        self.exit_btn = PyQtWidgets.QPushButton("Exit Application", self)
        self.exit_btn.setStyleSheet(css.style_sw_exit_button)
        self.exit_btn.clicked.connect(lambda: self.exit_button_on_click())
        # todo create a connect function that calls control with the cmd to terminate the application

        self.new_cocktail_btn = PyQtWidgets.QPushButton("New Cocktail", self)
        self.new_cocktail_btn.setStyleSheet(css.style_sw_new_cocktail_button)
        self.new_cocktail_btn.clicked.connect(lambda: self.new_cocktail_button_on_click())
        # todo create a connect function that calls control with the cmd to add a new cocktail

        self.edit_hoppers_btn = PyQtWidgets.QPushButton("Change Drinks on Hopper", self)
        self.edit_hoppers_btn.setStyleSheet(css.style_sw_edit_hoppers_button)
        self.edit_hoppers_btn.clicked.connect(lambda: self.edit_hopper_occupancy_btn_on_click())
        # todo create a connect function that calls control with the cmd to change the drinks on the hopper

        # Scroll area

        self.all_drinks_frame = PyQtWidgets.QScrollArea(self)
        self.wrapper_widget = PyQtWidgets.QWidget()
        self.scroll_area_vbox = PyQtWidgets.QVBoxLayout()

        self.update_quick_select()

        self.wrapper_widget.setLayout(self.scroll_area_vbox)

        self.all_drinks_frame.setVerticalScrollBarPolicy(PyQtCore.Qt.ScrollBarAlwaysOn)
        self.all_drinks_frame.setHorizontalScrollBarPolicy(PyQtCore.Qt.ScrollBarAlwaysOff)
        self.all_drinks_frame.setWidgetResizable(True)
        self.all_drinks_frame.setStyleSheet(css.style_sw_all_drinks_frame)
        self.all_drinks_frame.setWidget(self.wrapper_widget)

        # Layout

        self.mainGridLayout = PyQtWidgets.QGridLayout(self)
        self.mainGridLayout.addWidget(self.headerLabel, 0, 0, 1, 3)
        self.mainGridLayout.addWidget(self.subHeaderLabel, 1, 0, 1, 3)
        self.mainGridLayout.addWidget(self.description_label, 2, 0)
        self.mainGridLayout.addWidget(self.new_cocktail_btn, 4, 2)
        self.mainGridLayout.addWidget(self.edit_hoppers_btn, 6, 2)
        self.mainGridLayout.addWidget(self.exit_btn, 8, 2)
        self.mainGridLayout.addWidget(self.all_drinks_frame, 3, 0, 6, 2)
        self.setLayout(self.mainGridLayout)

    def update_quick_select(self):
        # deletes all drink_buttons in the quick select and rebuilds scroll_area_vbox
        # completely new

        # deletes all drink_buttons
        for drink_button_position in reversed(range(self.scrollAreaVBox.count())):
            self.scrollAreaVBox.takeAt(drink_button_position).widget().setParent(None)

        # fills scroll_area_vbox with buttons that represent every available
        # beverage or mix drink
        # fills in all beverage buttons
        for i in range(len(self.beverages_and_mix_drinks.beverages_on_hopper)):
            self.scroll_area_vbox.addWidget(
                SelectionWindowBeverageButton(
                    self, self.beverages_and_mix_drinks.beverages_on_hopper[i]))

        # fills in all mix drink buttons
        for i in range(len(self.beverages_and_mix_drinks.mix_drinks_dispensable)):
            self.scroll_area_vbox.addWidget(
                SelectionWindowPushButtonMixDrink(
                    self, self.beverages_and_mix_drinks.mix_drinks_dispensable[i]))

    # todo: remove get_drink and put it into the controller class see button classes in this file
    def get_drink(self, index: int, is_mix_drink: bool):
        if is_mix_drink:
            pass
            # controller.get_drink(index: int)
        else:
            pass
            # controller.get_drink(index: int)


class SelectionWindowBeverageButton(PyQtWidgets.QPushButton):
    beverage: RuntimeData.Beverage
    beverage_id = -1

    def __init__(self, __parent: PyQtWidgets.QWidget, __beverage: RuntimeData.Beverage):
        super().__init__()
        self.parentWidget = __parent
        self.beverage = __beverage
        self.beverage_id = self.beverage.beverage_id

        self.setStyleSheet(css.style_sw_beverage_button)
        self.setText(self.beverage.beverage_name)
        self.clicked.connect(lambda: self.parentWidget.get_drink(self.beverage_id, False))
    # todo create a connect function that calls control with a cmd to dispense a drink with the given drink id


class SelectionWindowPushButtonMixDrink(PyQtWidgets.QPushButton):
    mix_drink: RuntimeData.MixDrinkInformation
    mix_drink_id = -1

    def __init__(self, __parent: PyQtWidgets.QWidget, __mix_drink: RuntimeData.MixDrinkInformation):
        super().__init__()
        self.parentWidget = __parent
        self.mix_drink = __mix_drink
        self.mix_drink_id = self.mix_drink.mix_drink_id

        self.setStyleSheet(css.style_sw_mix_drink_button)
        self.setText(self.mix_drink.mix_drink_name)
        self.clicked.connect(lambda: self.parentWidget.get_drink(self.mix_drink_id, True))
        # todo create a connect function that calls control with a cmd to dispense a drink with the given drink id
