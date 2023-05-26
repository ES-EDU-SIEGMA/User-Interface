import PyQt5.QtWidgets as pyw
import PyQt5.QtCore as pyc
from src.libs import css as css, runtime_data as rtd, json_data as dbcon


# this button is used in the hopper overview
class CurrentBeverageBtn(pyw.QPushButton):
    currentBvgOnHopper: rtd.Beverage

    def __init__(
        self,
        __parent: pyw.QWidget,
        __current_bvg_on_hopper: rtd.Beverage,
        __hopper_id: int,
    ):
        super().__init__(__current_bvg_on_hopper.m_name, __parent)
        self.currentBvgOnHopper = __current_bvg_on_hopper
        self.parentWidget = __parent
        self.clicked.connect(
            lambda: __parent.hopper_btn_on_click(self.currentBvgOnHopper, __hopper_id)
        )
        self.setStyleSheet(
            f"background-color: {css.m_second_button_background_color}; color: {css.m_standard_text_color}; border: 1px solid {css.m_border_color}; padding-top: 20%;padding-bottom: 20%;padding-left: 40%; padding-right: 40%;"
        )


# this custom push button is used for the drink list just so it can have a unique id
class BeveragePushButton(pyw.QPushButton):
    information: rtd.Beverage
    m_index = -1

    def __init__(
        self,
        __parent: pyw.QWidget,
        __beverage_data: rtd.Beverage,
        __current_bvg_id: int,
        hopper_id: int,
    ):
        super().__init__()
        self.parentWidget = __parent
        self.setStyleSheet(
            f"background-color: {css.m_second_button_background_color}; padding-top: 70%; padding-bottom: 70%; color: {css.m_standard_text_color}; margin: 5%;"
        )
        self.clicked.connect(
            lambda: __parent.qs_drink_button_on_click(
                __current_bvg_id, __beverage_data.m_id, hopper_id
            )
        )
        self.information = __beverage_data
        self.setText(self.information.m_name)
        self.m_index = self.information.m_id


# window to display all the options to change the beverage to
class ChangeDrinkWindow(pyw.QWidget):
    def __init__(self, __parent: pyw.QWidget, __bvg: rtd.Beverage, __hopper_id: int):
        super().__init__()
        self.m_currentBvg = __bvg
        self.m_allBeverages = dbcon.get_all_other_beverages()
        self.parentWidget = __parent
        self.hopper_id = __hopper_id
        self.init_widgets()
        self.resize(1200, 800)
        self.showFullScreen()

    def init_widgets(self):
        self.setStyleSheet(f"background-color: {css.m_main_background_color};")

        ##############################################################################
        #       LABELS
        ##############################################################################

        self.headerLabel = pyw.QLabel("Select the new Drink", self)
        self.headerLabel.setAlignment(pyc.Qt.AlignLeft)
        self.headerLabel.setStyleSheet(
            f"color: {css.m_standard_text_color}; font-size: 24pt; font-family: {css.font};"
        )
        self.informationLabel = pyw.QLabel("", self)
        self.informationLabel.setAlignment(pyc.Qt.AlignLeft)
        self.informationLabel.setStyleSheet(
            f"color: {css.m_standard_text_color}; font-size: 12pt; font-family: {css.font}; margin-top: 40%;"
        )

        ##############################################################################
        #       BUTTONS
        ##############################################################################

        self.saveBtn = pyw.QPushButton("Back", self)
        self.saveBtn.clicked.connect(lambda: self.save_btn_on_click())
        self.saveBtn.setStyleSheet(
            f"background-color: {css.m_button_background_color}; color: {css.m_standard_text_color}; border: 1px solid {css.m_border_color}; padding-top: 30%;padding-bottom: 30%;padding-left: 50%;padding-right: 50%;"
        )

        ##############################################################################
        #       LAYOUT
        ##############################################################################

        self.mainGrid = pyw.QGridLayout(self)

        ##############################################################################
        #       SCROLLAREA
        ##############################################################################

        self.allDrinksFrame = pyw.QScrollArea(self)
        self.wrapperWidget = pyw.QWidget()
        self.scrollAreadVBox = pyw.QVBoxLayout()

        ##############################################################################
        #       GET ALL AVAILABLE DRINKS AND DISPLAY THEM ON THE QUICK SELECT
        ##############################################################################
        self.update_quick_select()

        self.wrapperWidget.setLayout(self.scrollAreadVBox)

        self.allDrinksFrame.setVerticalScrollBarPolicy(pyc.Qt.ScrollBarAlwaysOn)
        self.allDrinksFrame.setHorizontalScrollBarPolicy(pyc.Qt.ScrollBarAlwaysOff)
        self.allDrinksFrame.setWidgetResizable(True)
        self.allDrinksFrame.setStyleSheet(
            f"border: 1px solid {css.m_border_color}; color: {css.m_standard_text_color};"
        )
        self.allDrinksFrame.setWidget(self.wrapperWidget)

        self.mainGrid.addWidget(self.headerLabel, 0, 0)
        self.mainGrid.addWidget(self.allDrinksFrame, 1, 0)
        self.mainGrid.addWidget(self.saveBtn, 2, 1)
        self.mainGrid.addWidget(self.informationLabel, 2, 0)

    def save_btn_on_click(self):
        self.switch_view()

    ## gets triggered when a drink is selected
    #
    #   changes the old beverage on the hopper to the new one, this includes:
    #       -changes in the database
    #       -changes on the runtimedata
    def qs_drink_button_on_click(
        self, current_id: int, to_change_id: int, hopper_id: int
    ):
        assuranceWindow = pyw.QMessageBox(self)
        assuranceWindow.resize(800, 600)
        assuranceWindow.setWindowTitle("Test title")
        assuranceWindow.setText("Are you sure you want to commit the change?")
        assuranceWindow.setStandardButtons(pyw.QMessageBox.Yes | pyw.QMessageBox.No)
        assuranceWindow.setIcon(pyw.QMessageBox.Question)
        assuranceWindow.setStyleSheet(
            f"color: {css.m_standard_text_color}; background-color: {css.m_main_background_color};"
        )
        resp = assuranceWindow.exec()

        if resp == pyw.QMessageBox.No:
            return

        dbcon.change_beverage_on_hopper(current_id, to_change_id, hopper_id)

        if to_change_id == -1:
            for i in range(len(self.parentWidget.rtData.m_beverage_list)):
                if current_id == self.parentWidget.rtData.m_beverage_list[i].m_id:
                    # found the current beverage
                    temp = CurrentBeverageBtn(
                        self.parentWidget,
                        rtd.beverage(-1, hopper_id, "EMPTY SLOT", 0),
                        hopper_id,
                    )
                    tempBvg = rtd.Beverage(-1, hopper_id, "EMPTY SLOT", 0)
                    self.m_currentBvg = tempBvg
                    self.parentWidget.hopperList[hopper_id] = temp
                    self.informationLabel.setText(
                        f"Removed {self.parentWidget.rtData.m_beverage_list[i].m_name} from Hopper {hopper_id}"
                    )
                    del self.parentWidget.rtData.m_beverage_list[i]
                    self.m_allBeverages = dbcon.get_all_other_beverages()
                    break
        else:
            if current_id == -1:
                # find new beverage in list
                for i in range(len(self.m_allBeverages)):
                    if to_change_id == self.m_allBeverages[i].m_id:  # found it
                        tempBvg = self.m_allBeverages[i]
                        tempBvg.m_hopper_id = hopper_id
                        self.informationLabel.setText(
                            f"Put {tempBvg.m_name} on hopper {hopper_id}"
                        )
                        self.m_currentBvg = tempBvg
                        self.parentWidget.hopperList[hopper_id] = CurrentBeverageBtn(
                            self.parentWidget, tempBvg, hopper_id
                        )
                        break
            else:
                # find old beverage
                for i in range(len(self.parentWidget.rtData.m_beverage_list)):
                    # found it
                    if current_id == self.parentWidget.rtData.m_beverage_list[i].m_id:
                        # find new beverage
                        for x in range(len(self.m_allBeverages)):
                            if to_change_id == self.m_allBeverages[x].m_id:
                                # found it -> now update the runtime data and print an information to the
                                self.informationLabel.setText(
                                    f"Changed the drink from {self.parentWidget.rtData.m_beverage_list[i].m_name} to {self.m_allBeverages[x].m_name} on hopper {hopper_id}"
                                )
                                # set new hopperid
                                self.m_allBeverages[x].m_hopper_id = hopper_id
                                # override all the old data
                                self.m_currentBvg = self.m_allBeverages[x]
                                self.parentWidget.rtData.m_beverage_list[
                                    i
                                ] = self.m_allBeverages[x]
                                self.parentWidget.hopperList[
                                    hopper_id
                                ] = CurrentBeverageBtn(
                                    self.parentWidget,
                                    self.parentWidget.rtData.m_beverage_list[i],
                                    hopper_id,
                                )
                                # update beverages with hopperid = null
                                self.m_allBeverages = dbcon.get_all_other_beverages()
                                break
        self.update_quick_select()

    def delete_old_btns(self):
        for i in reversed(range(self.scrollAreadVBox.count())):
            self.scrollAreadVBox.takeAt(i).widget().setParent(None)

    def update_quick_select(self):
        self.delete_old_btns()
        for i in range(len(self.m_allBeverages)):
            self.scrollAreadVBox.addWidget(
                BeveragePushButton(
                    self, self.m_allBeverages[i], self.m_currentBvg.m_id, self.hopper_id
                )
            )
        self.scrollAreadVBox.addWidget(
            BeveragePushButton(
                self,
                rtd.Beverage(-1, self.hopper_id, "EMPTY SLOT", 0),
                self.m_currentBvg.m_id,
                self.hopper_id,
            )
        )

    def switch_view(self):
        self.parentWidget.update_hopper_layout()
        self.parentWidget.show()
        self.close()


##############################################################################
#       WINDOW FOR THE HOPPER OVERVIEW
##############################################################################


class EditHoppers(pyw.QWidget):
    def __init__(self, __parent: pyw.QWidget, __rtd: rtd.RuntimeData):
        super().__init__()
        self.parentWidget = __parent
        self.setWindowTitle("Edit Hopper Occupancy")
        self.rtData = __rtd
        self.init_widgets()
        self.resize(1200, 800)
        self.showFullScreen()

    def init_widgets(self):
        ##############################################################################
        #       MAIN WINDOW STYLE
        ##############################################################################
        self.setStyleSheet(f"background-color: {css.m_main_background_color};")

        ##############################################################################
        #       LABELS
        ##############################################################################
        self.headerLabel = pyw.QLabel("Edit Hopper Occupancy", self)
        self.headerLabel.setStyleSheet(
            f"color: {css.m_standard_text_color}; font-size: 24pt; font-family: {css.font};"
        )
        self.headerLabel.setAlignment(pyc.Qt.AlignCenter)
        self.monitorLabel = pyw.QLabel("Monitor is here", self)
        self.monitorLabel.setStyleSheet(f"color: {css.m_standard_text_color};")
        self.monitorLabel.setAlignment(pyc.Qt.AlignCenter)

        ##############################################################################
        #       BUTTONS
        ##############################################################################
        self.hopperList = []
        self.usedSlots = []
        for i in range(len(self.rtData.m_beverage_list)):
            temp = CurrentBeverageBtn(
                self,
                self.rtData.m_beverage_list[i],
                self.rtData.m_beverage_list[i].m_hopper_id,
            )
            self.usedSlots.append(self.rtData.m_beverage_list[i].m_hopper_id)
            self.hopperList.insert(self.rtData.m_beverage_list[i].m_hopper_id, temp)

        if len(self.usedSlots) < 12:
            for i in range(12):
                if i not in self.usedSlots:
                    temp = CurrentBeverageBtn(
                        self, rtd.Beverage(-1, i, "EMPTY SLOT", 0), i
                    )
                    self.hopperList.insert(i, temp)

        self.backBtn = pyw.QPushButton("Back to Mainmenu", self)
        self.backBtn.clicked.connect(lambda: self.back_btn_on_click())
        self.backBtn.setStyleSheet(
            f"background-color: {css.m_button_background_color}; color: {css.m_standard_text_color}; border: 1px solid {css.m_border_color}; padding-top: 30%;padding-bottom: 30%;padding-left: 50%;padding-right: 50%;"
        )

        ##############################################################################
        #       HOPPER LAYOUT
        ##############################################################################
        self.hopperFrame = pyw.QFrame(self)
        self.hopperDisplayLayout = pyw.QGridLayout(self)
        self.hopperDisplayLayout.setColumnMinimumWidth(2, 15)
        self.hopperDisplayLayout.setColumnMinimumWidth(9, 15)
        self.update_hopper_layout()
        self.hopperFrame.setLayout(self.hopperDisplayLayout)

        ##############################################################################
        #       MAIN LAYOUT
        ##############################################################################
        self.mainLayout = pyw.QGridLayout(self)
        self.mainLayout.addWidget(self.headerLabel, 0, 0, 1, 5)
        self.mainLayout.addWidget(self.monitorLabel, 7, 0, 1, 5)
        self.mainLayout.addWidget(self.hopperFrame, 2, 0, 5, 5)
        self.mainLayout.addWidget(self.backBtn, 8, 4)

    def delete_drink_buttons(self):
        for i in reversed(range(self.hopperDisplayLayout.count())):
            self.hopperDisplayLayout.takeAt(i).widget().setParent(None)

    def update_hopper_layout(self):
        self.delete_drink_buttons()
        row = 0
        span = 2
        for i in range(12):
            if i < 4:
                self.hopperDisplayLayout.addWidget(
                    self.hopperList[i], row, 0, span, span
                )
            elif i >= 4 and i < 8:
                self.hopperDisplayLayout.addWidget(
                    self.hopperList[i], row, 10, span, span
                )
            else:
                if i == 10:  # top
                    self.hopperDisplayLayout.addWidget(
                        self.hopperList[i], 1, 5, span, span
                    )
                elif i == 11:  # side left
                    self.hopperDisplayLayout.addWidget(
                        self.hopperList[i], 4, 3, span, span
                    )
                elif i == 9:  # side right
                    self.hopperDisplayLayout.addWidget(
                        self.hopperList[i], 4, 7, span, span
                    )
                elif i == 8:  # bottom
                    self.hopperDisplayLayout.addWidget(
                        self.hopperList[i], 7, 5, span, span
                    )
            if row == 9:
                row = 0
            else:
                row += 3

    def hopper_btn_on_click(
        self, __currentBeverageOnHopper: rtd.Beverage, __hopperid: int
    ):
        self.m_cdw = ChangeDrinkWindow(self, __currentBeverageOnHopper, __hopperid)
        self.hide()

    def back_btn_on_click(self):
        self.parentWidget.update_quick_select()
        self.parentWidget.show()
        self.close()
