 PyQt5.QtWidgets as PyQtWidgets
import PyQt5.QtCore as PyQtCore
import sys
import time
from src.libs import (
    globals as go,
    progress as ProgressWindow,
    new_cocktail as NewCocktailWindow,
    edit_hopper as EditHopperWindow,
    css as Css,
    runtime_data as RuntimeData,
    mock_serial as SerialCommunication,
    scale as Scale,
)
import libs.data.json_data as JsonData


class BeveragePushButton(PyQtWidgets.QPushButton):
    beverage: RuntimeData.Beverage
    beverage_id = -1

    def __init__(self, __parent: PyQtWidgets.QWidget, __beverage: RuntimeData.Beverage):
        super().__init__()
        self.parent_widget = __parent
        self.setStyleSheet(
            f"background-color: {Css.m_second_button_background_color};"
            f"padding-top: 70%; padding-bottom: 70%; color: {Css.m_standard_text_color};"
            f"margin: 5%; font-size: 11pt;"
        )
        self.clicked.connect(
            lambda: self.parent_widget.qsDrinkButton_onClick(self.beverage_id, False)
        )
        self.beverage = __beverage
        self.setText(self.information.beverage_name)
        self.beverage_id = self.beverage.beverage_id


class MixedDrinkPushButton(PyQtWidgets.QPushButton):
    mix_drink: RuntimeData.MixDrinkInformation
    # constructor
    mix_drink_id = -1

    def __init__(
        self,
        __parent: PyQtWidgets.QWidget,
        __mix_drink: RuntimeData.MixDrinkInformation,
    ):
        super().__init__()
        self.parentWidget = __parent
        self.setStyleSheet(
            f"background-color: {Css.m_second_button_background_color};"
            f"padding-top: 70%; padding-bottom: 70%; color: {Css.m_standard_text_color};"
            f"margin: 5%; font-size: 11pt;"
        )
        self.clicked.connect(
            lambda: self.parentWidget.qsDrinkButton_onClick(self.mix_drink_id, True)
        )
        self.mix_drink = __mix_drink
        self.setText(self.mix_drink.mix_drink_name)
        self.mix_drink_id = self.mix_drink.mix_drink_id


class WelcomeWindow(PyQtWidgets.QWidget):
    # stores the current beverages and mix_drinks which are available with the current hopper configuration
    m_runtimeData: RuntimeData.RuntimeData

    cocktail_window: NewCocktailWindow.NewCocktailWindow
    progressWindow: ProgressWindow.MixingProgressWindow
    editHopperWindow: EditHopperWindow.EditHoppers

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SIEGMA_2223 - Test")
        self.resize(1200, 800)
        self.showFullScreen()

        self.setStyleSheet(f"background-color: {Css.m_main_background_color};")

        ##############################################################################
        #       LABELS
        ##############################################################################

        self.headerLabel = PyQtWidgets.QLabel("Drink Mixing Machine", self)
        self.headerLabel.setAlignment(PyQtCore.Qt.AlignCenter)
        self.headerLabel.setStyleSheet(
            f"color: {Css.m_standard_text_color}; font-size: 30pt; font-family: {Css.font}; margin-top: 25%;"
        )
        self.subHeaderLabel = PyQtWidgets.QLabel("SIEGMA-WS2223", self)
        self.subHeaderLabel.setAlignment(PyQtCore.Qt.AlignCenter)
        self.subHeaderLabel.setStyleSheet(
            f"color: {Css.m_button_background_color}; font-size: 15pt; font-family: {Css.font};"
        )
        self.descriptionLabel = PyQtWidgets.QLabel("Quick select for drinks:", self)
        self.descriptionLabel.setStyleSheet(
            f"color: {Css.m_standard_text_color}; font-size: 12pt; font-family: {Css.font};"
        )

        ##############################################################################
        #       BUTTONS
        ##############################################################################

        self.exitBtn = PyQtWidgets.QPushButton("Exit Application", self)
        self.exitBtn.setStyleSheet(
            f"background-color: {Css.m_button_background_color}; color: {Css.m_standard_text_color};"
            f"padding: 60%; font-size: 11pt; border: 2px solid {Css.m_border_color};"
            f"border-radius: {Css.border_radius}px; margin-left: 20%;"
        )
        self.exitBtn.clicked.connect(lambda: self.exit_button_on_click())

        self.addNewCocktailBtn = PyQtWidgets.QPushButton("New Cocktail", self)
        self.addNewCocktailBtn.setStyleSheet(
            f"background-color: {Css.m_button_background_color}; color: {Css.m_standard_text_color};"
            f"padding: 60%; font-size: 11pt;border: 2px solid {Css.m_border_color};"
            f"border-radius: {Css.border_radius}px; margin-left: 20%;"
        )
        self.addNewCocktailBtn.clicked.connect(
            lambda: self.new_cocktail_button_on_click()
        )

        self.editHopperOccupancyBtn = PyQtWidgets.QPushButton(
            "Change Drinks on Hopper", self
        )
        self.editHopperOccupancyBtn.setStyleSheet(
            f"background-color: {Css.m_button_background_color}; color: {Css.m_standard_text_color};"
            f"padding: 60%; font-size: 11pt;border: 2px solid {Css.m_border_color};"
            f"border-radius: {Css.border_radius}px; margin-left: 20%;"
        )
        self.editHopperOccupancyBtn.clicked.connect(
            lambda: self.edit_hopper_occupancy_btn_on_click()
        )

        ##############################################################################
        #       ScrollArea
        ##############################################################################

        self.allDrinksFrame = PyQtWidgets.QScrollArea(self)
        self.wrapperWidget = PyQtWidgets.QWidget()
        self.scrollAreaVBox = PyQtWidgets.QVBoxLayout()

        ##############################################################################
        #       Get all available drink and display them on the quick select
        ##############################################################################

        self.update_quick_select()

        self.wrapperWidget.setLayout(self.scrollAreaVBox)

        self.allDrinksFrame.setVerticalScrollBarPolicy(PyQtCore.Qt.ScrollBarAlwaysOn)
        self.allDrinksFrame.setHorizontalScrollBarPolicy(PyQtCore.Qt.ScrollBarAlwaysOff)
        self.allDrinksFrame.setWidgetResizable(True)
        self.allDrinksFrame.setStyleSheet(
            f"border: 0px solid {Css.m_border_color}; color: {Css.m_standard_text_color};"
        )
        self.allDrinksFrame.setWidget(self.wrapperWidget)

        ##############################################################################
        #       Layout
        ##############################################################################

        self.mainGridLayout = PyQtWidgets.QGridLayout(self)

        self.mainGridLayout.addWidget(self.headerLabel, 0, 0, 1, 3)
        self.mainGridLayout.addWidget(self.subHeaderLabel, 1, 0, 1, 3)
        self.mainGridLayout.addWidget(self.descriptionLabel, 2, 0)
        self.mainGridLayout.addWidget(self.addNewCocktailBtn, 4, 2)
        self.mainGridLayout.addWidget(self.editHopperOccupancyBtn, 6, 2)
        self.mainGridLayout.addWidget(self.exitBtn, 8, 2)
        self.mainGridLayout.addWidget(self.allDrinksFrame, 3, 0, 6, 2)

        self.setLayout(self.mainGridLayout)

    ##############################################################################
    #       Custom functions
    ##############################################################################
    # Clears the Buttons from the allDrinkFrame
    #
    #
    def delete_drink_buttons(self):
        for drink_button_position in reversed(range(self.scrollAreaVBox.count())):
            self.scrollAreaVBox.takeAt(drink_button_position).widget().setParent(None)

    # Fills the all_drinks_frame with the mixable beverages and mix_drinks
    #
    #  uses a database call to get the current available beverages and mix_drinks
    def update_quick_select(self):
        self.delete_drink_buttons()
        print("testUpdateQuickSelectBefore")
        all_available_beverages: list[
            RuntimeData.Beverage
        ] = JsonData.get_all_available_beverages()
        all_available_mix_drinks: list[
            RuntimeData.MixDrinkInformation
        ] = JsonData.get_all_available_mixed_drinks()
        print("testUpdateQuickSelectAfter")
        self.m_runtimeData = RuntimeData.RuntimeData(
            all_available_beverages, all_available_mix_drinks
        )

        for i in range(len(self.m_runtimeData.beverages_on_hopper)):
            self.scrollAreaVBox.addWidget(
                BeveragePushButton(self, all_available_beverages[i])
            )

        for i in range(len(self.m_runtimeData.mix_drinks_dispensable)):
            self.scrollAreaVBox.addWidget(
                MixedDrinkPushButton(self, all_available_mix_drinks[i])
            )

    def exit_button_on_click(self):
        SerialCommunication.close_connection()
        JsonData.close_connection()
        self.close()

    def new_cocktail_button_on_click(self):
        self.cocktail_window = NewCocktailWindow.NewCocktailWindow(self)
        self.hide()

    def drink_button_on_click(self, index: int, is_mix_drink: bool):
        # find the fitting Beverage or is_mix_drink
        if is_mix_drink:
            self.progressWindow = ProgressWindow.MixingProgressWindow(
                self, None, self.m_runtimeData.get_mix_drink(index)
            )
        else:
            self.progressWindow = ProgressWindow.MixingProgressWindow(
                self, self.m_runtimeData.get_beverage(index), None
            )

    def edit_hopper_occupancy_btn_on_click(self):
        self.editHopperWindow = EditHopperWindow.EditHoppers(self, self.m_runtimeData)
        self.hide()

    # integration test, empty's each hopper once and compares the actual weight with the expected one
    #
    def integration_test(self):
        full_weight = 0
        empty_glass_weight = 0

        correct_hoppers = 0

        empty_glass_weight = Scale.get_current_weight()

        full_weight += empty_glass_weight

        for i in range(len(self.m_runtimeData.beverages_on_hopper)):
            hoppers = [0, 0, 0, 0]
            current_hopper = self.m_runtimeData.beverages_on_hopper[i].beverage_id
            hoppers[current_hopper % 4] = int(
                go.standardActivationTime
                * self.m_runtimeData.beverages_on_hopper[i].beverage_flow_speed
                * 1000
            )
            pico_id = 0
            if current_hopper < 5:
                pico_id = 1
            elif 5 <= current_hopper < 9:
                pico_id = 0
            else:
                pico_id = 2
            SerialCommunication.send_msg(
                pico_id, f"{hoppers[0]};{hoppers[1]};{hoppers[2]};{hoppers[3]};\n"
            )
            time.sleep(hoppers[current_hopper % 4] / 1000)
            hopper_size = 30
            if current_hopper > 8:
                hopper_size = 40
            current_weight = 0
            current_weight = Scale.get_current_weight()
            if (current_weight - full_weight) in range(
                hopper_size - 5, hopper_size + 5
            ):
                correct_hoppers += 1
            full_weight = current_weight
        return correct_hoppers == len(self.m_runtimeData.beverages_on_hopper)


# window to display any occurring error and exception
#
class ErrorWindow(PyQtWidgets.QWidget):
    def __init__(self, __error_msg):
        super().__init__()
        self.setWindowTitle("ERROR")
        self.error = PyQtWidgets.QLabel(__error_msg.__str__, self)
        self.error.setStyleSheet("font-size: 20pt; color: red; font-family: Arial;")
        self.error.setAlignment(PyQtCore.Qt.AlignCenter)
        self.error.move(0, 30)
        self.showFullScreen()


if __name__ == "__main__":
    app = PyQtWidgets.QApplication(sys.argv)
    try:
        JsonData.__init__()
        Scale.__init__()
        SerialCommunication.__init__()
        print("testSerialCom")
        m_startPage = WelcomeWindow()
        print("testStartPage")
        sys.exit(app.exec())
    except Exception as error:
        m_error = ErrorWindow(error)
        sys.exit(app.exec())
