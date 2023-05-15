import PyQt5.QtWidgets as PyQtWidgets
import PyQt5.QtCore as PyQtCore
import css as Css
import runtime_data as RuntimeData
import json_data as JsonData


class CurrentBeverageButton(PyQtWidgets.QPushButton):
    current_beverage_on_hopper: RuntimeData.Beverage

    def __init__(
            self, __parent: PyQtWidgets.QWidget, __current_beverage_on_hopper: RuntimeData.Beverage, __hopper_id: int
    ):
        super().__init__(__current_beverage_on_hopper.beverage_name, __parent)
        self.current_beverage_on_hopper = __current_beverage_on_hopper
        self.parentWidget = __parent
        self.clicked.connect(
            lambda: __parent.hopper_button_on_click(self.current_beverage_on_hopper, __hopper_id))

        self.setStyleSheet(
            f"background-color: {Css.m_second_button_background_color};"
            f"color: {Css.m_standard_text_color};border: 1px solid {Css.m_border_color};"
            f"padding-top: 20%;padding-bottom: 20%;padding-left: 40%; padding-right: 40%;")


# this custom push button is used for the drink list just so it can have a unique drink_to_add_id
class BeveragePushButton(PyQtWidgets.QPushButton):
    beverage: RuntimeData.Beverage
    beverage_id = -1

    def __init__(
            self,
            __parent: PyQtWidgets.QWidget,  # parent is main
            __beverage: RuntimeData.Beverage,
            __current_beverage: int,
            hopper_id: int, ):
        super().__init__()
        self.parentWidget = __parent
        self.setStyleSheet(
            f"background-color: {Css.m_second_button_background_color};"
            f"padding-top: 70%; padding-bottom: 70%; color: {Css.m_standard_text_color}; margin: 5%;")

        self.clicked.connect(
            lambda: __parent.drink_button_on_click(
                __current_beverage, __beverage.beverage_id, hopper_id))

        self.beverage = __beverage
        self.setText(self.beverage.beverage_name)
        self.beverage_id = self.beverage.beverage_id


# window to display all the options to change the Beverage to
class ChangeDrinkWindow(PyQtWidgets.QWidget):
    def __init__(self, __parent: PyQtWidgets.QWidget, __runtime_data_beverage: RuntimeData.Beverage, __hopper_id: int):
        super().__init__()
        self.runtime_data_beverage: RuntimeData.Beverage = __runtime_data_beverage
        self.beverages_not_on_hopper: list[RuntimeData.Beverage] = JsonData.get_all_other_beverages()
        self.parentWidget: PyQtWidgets.QWidget = __parent
        self.hopper_id: int = __hopper_id
        self.resize(1200, 800)
        self.showFullScreen()

        self.setStyleSheet(f"background-color: {Css.m_main_background_color};")

        ##############################################################################
        #       LABELS
        ##############################################################################

        self.headerLabel = PyQtWidgets.QLabel("Select the new Drink", self)
        self.headerLabel.setAlignment(PyQtCore.Qt.AlignLeft)
        self.headerLabel.setStyleSheet(
            f"color: {Css.m_standard_text_color}; font-size: 24pt; font-family: {Css.font};")
        self.informationLabel = PyQtWidgets.QLabel("", self)
        self.informationLabel.setAlignment(PyQtCore.Qt.AlignLeft)
        self.informationLabel.setStyleSheet(
            f"color: {Css.m_standard_text_color}; font-size: 12pt; font-family: {Css.font}; margin-top: 40%;")

        ##############################################################################
        #       BUTTONS
        ##############################################################################

        self.saveBtn = PyQtWidgets.QPushButton("Back", self)
        self.saveBtn.clicked.connect(lambda: self.save_button_on_click())
        self.saveBtn.setStyleSheet(
            f"background-color: {Css.m_button_background_color};"
            f"color: {Css.m_standard_text_color}; border: 1px solid {Css.m_border_color};"
            f"padding-top: 30%;padding-bottom: 30%;padding-left: 50%;padding-right: 50%;")

        ##############################################################################
        #       Layout
        ##############################################################################

        self.mainGrid = PyQtWidgets.QGridLayout(self)

        ##############################################################################
        #       ScrollArea
        ##############################################################################

        self.allDrinksFrame = PyQtWidgets.QScrollArea(self)
        self.wrapperWidget = PyQtWidgets.QWidget()
        self.scrollAreaVBox = PyQtWidgets.QVBoxLayout()

        ##############################################################################
        #       Get all available drinks and display them on the quick select
        ##############################################################################
        self.update_quick_select()

        self.wrapperWidget.setLayout(self.scrollAreaVBox)

        self.allDrinksFrame.setVerticalScrollBarPolicy(PyQtCore.Qt.ScrollBarAlwaysOn)
        self.allDrinksFrame.setHorizontalScrollBarPolicy(PyQtCore.Qt.ScrollBarAlwaysOff)
        self.allDrinksFrame.setWidgetResizable(True)
        self.allDrinksFrame.setStyleSheet(
            f"border: 1px solid {Css.m_border_color}; color: {Css.m_standard_text_color};")
        self.allDrinksFrame.setWidget(self.wrapperWidget)

        self.mainGrid.addWidget(self.headerLabel, 0, 0)
        self.mainGrid.addWidget(self.allDrinksFrame, 1, 0)
        self.mainGrid.addWidget(self.saveBtn, 2, 1)
        self.mainGrid.addWidget(self.informationLabel, 2, 0)

    def save_button_on_click(self):
        self.switch_view()

    # gets triggered when a drink is selected
    #
    #   changes the old Beverage on the hopper to the new one, this includes:
    #       -changes in the database
    #       -changes on the runtime_data
    def drink_button_on_click(self, current_id: int, to_change_id: int, hopper_id: int):
        assurance_window = PyQtWidgets.QMessageBox(self)
        assurance_window.resize(800, 600)
        assurance_window.setWindowTitle("Test title")
        assurance_window.setText("Are you sure you want to commit the change?")
        assurance_window.setStandardButtons(PyQtWidgets.QMessageBox.Yes | PyQtWidgets.QMessageBox.No)
        assurance_window.setIcon(PyQtWidgets.QMessageBox.Question)
        assurance_window.setStyleSheet(
            f"color: {Css.m_standard_text_color}; background-color: {Css.m_main_background_color};")
        resp = assurance_window.exec()

        if resp == PyQtWidgets.QMessageBox.No:
            return

        JsonData.change_beverage_on_hopper(current_id, to_change_id, hopper_id)

        # checks whether to_change_id refers to an empty drink button(:= -1)
        if to_change_id == -1:
            print("if")
            for beverage_on_hopper in self.parentWidget.runtime_data.beverages_on_hopper:
                if current_id == int(beverage_on_hopper.beverage_id):
                    # found the current Beverage
                    temp: CurrentBeverageButton = CurrentBeverageButton(
                        self.parentWidget,
                        RuntimeData.Beverage(-1, hopper_id, "EMPTY SLOT", 0),
                        hopper_id,
                    )

                    temp_beverage: RuntimeData.Beverage = RuntimeData.Beverage(-1, hopper_id, "EMPTY SLOT", 0)
                    self.runtime_data_beverage: RuntimeData.Beverage = temp_beverage
                    self.parentWidget.hopperList[hopper_id]: list[CurrentBeverageButton] = temp
                    self.informationLabel.setText(
                        f"Removed {self.parentWidget.runtime_data.beverages_on_hopper[beverage_on_hopper].beverage_name}"
                        f"from Hopper {hopper_id}"
                    )
                    del self.parentWidget.runtime_data.beverages_on_hopper[beverage_on_hopper]
                    self.beverages_not_on_hopper = JsonData.get_all_other_beverages()
                    break

        # to_change_id refers to a valid drink button
        else:
            # checks whether the current drink on the hopper is an empty button (:= -1)
            if current_id == -1:
                # find new Beverage in list
                for beverage_not_on_hopper in self.beverages_not_on_hopper:
                    if to_change_id == beverage_not_on_hopper.beverage_id:
                        beverage_not_on_hopper.beverage_hopper_id = hopper_id
                        self.informationLabel.setText(
                            f"Put {beverage_not_on_hopper.beverage_name} on hopper {hopper_id}")
                        self.runtime_data_beverage = beverage_not_on_hopper
                        self.parentWidget.hopperList[hopper_id] = CurrentBeverageButton(
                            self.parentWidget, beverage_not_on_hopper, hopper_id)
                        break

            # we are removing a non-empty drink button
            else:
                # find old Beverage
                for beverage_on_hopper in range(len(self.parentWidget.runtime_data.beverages_on_hopper)):
                    # found it
                    if current_id == self.parentWidget.runtime_data.beverages_on_hopper[beverage_on_hopper].beverage_id:
                        # find new Beverage
                        for x in range(len(self.beverages_not_on_hopper)):
                            if to_change_id == self.beverages_not_on_hopper[x].beverage_id:
                                # found it -> now update the runtime data and print an information to the
                                self.informationLabel.setText(
                                    f"Changed the drink from"
                                    f"{self.parentWidget.runtime_data.beverages_on_hopper[beverage_on_hopper].beverage_name}"
                                    f"to {self.beverages_not_on_hopper[x].beverage_name} on hopper {hopper_id}"
                                )
                                # set new hopper_id
                                self.beverages_not_on_hopper[x].beverage_hopper_id = hopper_id
                                # override all the old data
                                self.runtime_data_beverage = self.beverages_not_on_hopper[x]
                                self.parentWidget.runtime_data.beverages_on_hopper[
                                    beverage_on_hopper
                                ] = self.beverages_not_on_hopper[x]
                                self.parentWidget.hopperList[
                                    hopper_id
                                ] = CurrentBeverageButton(
                                    self.parentWidget,
                                    self.parentWidget.runtime_data.beverages_on_hopper[beverage_on_hopper],
                                    hopper_id,
                                )
                                # update beverages with hopper_id = null
                                self.beverages_not_on_hopper = JsonData.get_all_other_beverages()
                                break
        self.update_quick_select()

    def delete_old_buttons(self):
        for button_position in reversed(range(self.scrollAreaVBox.count())):
            self.scrollAreaVBox.takeAt(button_position).widget().setParent(None)

    def update_quick_select(self):
        self.delete_old_buttons()
        for i in range(len(self.beverages_not_on_hopper)):
            self.scrollAreaVBox.addWidget(
                BeveragePushButton(
                    self, self.beverages_not_on_hopper[i], self.runtime_data_beverage.beverage_id, self.hopper_id))

        self.scrollAreaVBox.addWidget(
            BeveragePushButton(
                self,
                RuntimeData.Beverage(-1, self.hopper_id, "EMPTY SLOT", 0),
                self.runtime_data_beverage.beverage_id,
                self.hopper_id, ))

    def switch_view(self):
        self.parentWidget.update_hopper_layout()
        self.parentWidget.show()
        self.close()


##############################################################################
#       Window for the hopper overview
##############################################################################


class EditHoppers(PyQtWidgets.QWidget):
    def __init__(self, __parent: PyQtWidgets.QWidget, __runtime_data: RuntimeData.RuntimeData):
        super().__init__()
        self.m_change_drink_window: ChangeDrinkWindow
        self.parentWidget: PyQtWidgets.QWidget = __parent
        self.setWindowTitle("Edit Hopper Occupancy")
        self.runtime_data: RuntimeData.RuntimeData = __runtime_data
        self.resize(1200, 800)
        self.showFullScreen()

        ##############################################################################
        #       Main window style
        ##############################################################################
        self.setStyleSheet(f"background-color: {Css.m_main_background_color};")

        ##############################################################################
        #       Labels
        ##############################################################################
        self.headerLabel = PyQtWidgets.QLabel("Edit Hopper Occupancy", self)
        self.headerLabel.setStyleSheet(
            f"color: {Css.m_standard_text_color}; font-size: 24pt; font-family: {Css.font};")
        self.headerLabel.setAlignment(PyQtCore.Qt.AlignCenter)
        self.monitorLabel = PyQtWidgets.QLabel("Monitor is here", self)
        self.monitorLabel.setStyleSheet(f"color: {Css.m_standard_text_color};")
        self.monitorLabel.setAlignment(PyQtCore.Qt.AlignCenter)

        ##############################################################################
        #       Buttons
        ##############################################################################
        self.hopperList: list[CurrentBeverageButton] = []
        self.usedSlots: list[RuntimeData.Beverage.beverage_hopper_id] = []
        for beverage_on_hopper in self.runtime_data.beverages_on_hopper:
            temp = CurrentBeverageButton(
                self, beverage_on_hopper, beverage_on_hopper.beverage_hopper_id)
            self.hopperList.insert(beverage_on_hopper.beverage_hopper_id, temp)
            self.usedSlots.append(beverage_on_hopper.beverage_hopper_id)

        # fill all unused hopper slots with an empty slot Beverage
        if len(self.usedSlots) < 12:
            for hopper_id in range(12):
                if hopper_id not in self.usedSlots:
                    temp = CurrentBeverageButton(
                        self, RuntimeData.Beverage(-1, hopper_id, "EMPTY SLOT", 0), hopper_id
                    )
                    self.hopperList.insert(hopper_id, temp)

        self.back_button = PyQtWidgets.QPushButton("Back to Main menu", self)
        self.back_button.clicked.connect(lambda: self.back_button_on_click())
        self.back_button.setStyleSheet(
            f"background-color: {Css.m_button_background_color};"
            f"color: {Css.m_standard_text_color};border: 1px solid {Css.m_border_color};"
            f"padding-top: 30%;padding-bottom: 30%;padding-left: 50%;padding-right: 50%;")

        ##############################################################################
        #       Hopper Layout
        ##############################################################################
        self.hopper_frame = PyQtWidgets.QFrame(self)
        self.hopper_display_layout = PyQtWidgets.QGridLayout(self)
        self.hopper_display_layout.setColumnMinimumWidth(2, 15)
        self.hopper_display_layout.setColumnMinimumWidth(9, 15)
        self.update_hopper_layout()
        self.hopper_frame.setLayout(self.hopper_display_layout)

        ##############################################################################
        #       Main Layout
        ##############################################################################
        self.main_layout = PyQtWidgets.QGridLayout(self)
        self.main_layout.addWidget(self.headerLabel, 0, 0, 1, 5)
        self.main_layout.addWidget(self.monitorLabel, 7, 0, 1, 5)
        self.main_layout.addWidget(self.hopper_frame, 2, 0, 5, 5)
        self.main_layout.addWidget(self.back_button, 8, 4)

    def delete_drink_buttons(self):
        for i in reversed(range(self.hopper_display_layout.count())):
            self.hopper_display_layout.takeAt(i).widget().setParent(None)

    def update_hopper_layout(self):
        self.delete_drink_buttons()
        row = 0
        span = 2
        for i in range(12):
            if i < 4:
                self.hopper_display_layout.addWidget(
                    self.hopperList[i], row, 0, span, span)
            elif 4 <= i < 8:
                self.hopper_display_layout.addWidget(
                    self.hopperList[i], row, 10, span, span)
            else:
                if i == 10:  # top
                    self.hopper_display_layout.addWidget(
                        self.hopperList[i], 1, 5, span, span)
                elif i == 11:  # side left
                    self.hopper_display_layout.addWidget(
                        self.hopperList[i], 4, 3, span, span)
                elif i == 9:  # side right
                    self.hopper_display_layout.addWidget(
                        self.hopperList[i], 4, 7, span, span)
                elif i == 8:  # bottom
                    self.hopper_display_layout.addWidget(
                        self.hopperList[i], 7, 5, span, span)
            if row == 9:
                row = 0
            else:
                row += 3

    def hopper_button_on_click(
            self, __current_beverage_on_hopper: RuntimeData.Beverage, __hopper_id: int):

        self.m_change_drink_window = ChangeDrinkWindow(self, __current_beverage_on_hopper, __hopper_id)
        self.hide()

    def back_button_on_click(self):
        self.parentWidget.update_quick_select()
        self.parentWidget.show()
        self.close()
