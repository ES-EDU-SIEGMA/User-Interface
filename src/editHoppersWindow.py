import PyQt5.QtWidgets as pyw
import PyQt5.QtCore as pyc
import cssTheme as css
import runtimeData as rtd
import dbcon as dbcon

# this button is used in the hopper overview
class currentBeverageBtn(pyw.QPushButton):
    currentBvgOnHopper : rtd.beverage
    def __init__(self, __parent : pyw.QWidget, __currentBvgOnHopper : rtd.beverage, __hopperid : int):
        super().__init__(__currentBvgOnHopper.m_name, __parent)
        self.currentBvgOnHopper = __currentBvgOnHopper
        self.parentWidget = __parent
        self.clicked.connect(lambda: __parent.hopperBtn_onClick(self.currentBvgOnHopper, __hopperid))
        self.setStyleSheet(f"background-color: {css.m_sndButtonBackgroundColor}; color: {css.m_standardTextColor}; border: 1px solid {css.m_borderColor}; padding-top: 20%;padding-bottom: 20%;padding-left: 40%; padding-right: 40%;")

# this custom push button is used for the drink list just so it can have a unique id
class beveragePushButton(pyw.QPushButton):
    information : rtd.beverage
    m_index = -1
    def __init__(self, __parent : pyw.QWidget, __beverageData : rtd.beverage, __currentBvgID : int, hopperid : int):
        super().__init__()
        self.parentWidget = __parent
        self.setStyleSheet(f"background-color: {css.m_sndButtonBackgroundColor}; padding-top: 70%; padding-bottom: 70%; color: {css.m_standardTextColor}; margin: 5%;")
        self.clicked.connect(lambda: __parent.qsDrinkButton_onClick(__currentBvgID, __beverageData.m_id, hopperid))
        self.information = __beverageData
        self.setText(self.information.m_name)
        self.m_index = self.information.m_id

# window to display all the options to change the beverage to
class changeDrinkWindow(pyw.QWidget):
    def __init__(self, __parent : pyw.QWidget, __bvg : rtd.beverage, __hopperid : int):
        super().__init__()
        self.m_currentBvg = __bvg
        self.m_allBeverages = dbcon.getAllOtherBeverages()
        self.parentWidget = __parent
        self.hopperid = __hopperid
        self.initWidgets()
        self.resize(1200, 800)
        self.showFullScreen()
    
    def initWidgets(self):
        self.setStyleSheet(f"background-color: {css.m_mainBackgroundColor};")

        ##############################################################################
        #       LABELS
        ##############################################################################

        self.headerLabel = pyw.QLabel('Select the new Drink', self)
        self.headerLabel.setAlignment(pyc.Qt.AlignLeft)
        self.headerLabel.setStyleSheet(f"color: {css.m_standardTextColor}; font-size: 24pt; font-family: {css.font};")
        self.informationLabel = pyw.QLabel('', self)
        self.informationLabel.setAlignment(pyc.Qt.AlignLeft)
        self.informationLabel.setStyleSheet(f"color: {css.m_standardTextColor}; font-size: 12pt; font-family: {css.font}; margin-top: 40%;")

        ##############################################################################
        #       BUTTONS
        ##############################################################################

        self.saveBtn = pyw.QPushButton("Back", self)
        self.saveBtn.clicked.connect(lambda: self.saveBtn_onClick())
        self.saveBtn.setStyleSheet(f"background-color: {css.m_buttonBackgroundColor}; color: {css.m_standardTextColor}; border: 1px solid {css.m_borderColor}; padding-top: 30%;padding-bottom: 30%;padding-left: 50%;padding-right: 50%;")

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
        self.updateQuickSelect()

        self.wrapperWidget.setLayout(self.scrollAreadVBox)

        self.allDrinksFrame.setVerticalScrollBarPolicy(pyc.Qt.ScrollBarAlwaysOn)
        self.allDrinksFrame.setHorizontalScrollBarPolicy(pyc.Qt.ScrollBarAlwaysOff)
        self.allDrinksFrame.setWidgetResizable(True)
        self.allDrinksFrame.setStyleSheet(f"border: 1px solid {css.m_borderColor}; color: {css.m_standardTextColor};")
        self.allDrinksFrame.setWidget(self.wrapperWidget)

        self.mainGrid.addWidget(self.headerLabel, 0, 0)
        self.mainGrid.addWidget(self.allDrinksFrame, 1, 0)
        self.mainGrid.addWidget(self.saveBtn, 2, 1)
        self.mainGrid.addWidget(self.informationLabel, 2, 0)

    def saveBtn_onClick(self):
        self.switchView()

    ## gets triggered when a drink is selected
    #
    #   changes the old beverage on the hopper to the new one, this includes:
    #       -changes in the database
    #       -changes on the runtimedata
    def qsDrinkButton_onClick(self, currentID : int, toChangeID : int, hopperid : int):
        assuranceWindow = pyw.QMessageBox(self)
        assuranceWindow.resize(800, 600)
        assuranceWindow.setWindowTitle("Test title")
        assuranceWindow.setText("Are you sure you want to commit the change?")
        assuranceWindow.setStandardButtons(pyw.QMessageBox.Yes | pyw.QMessageBox.No)
        assuranceWindow.setIcon(pyw.QMessageBox.Question)
        assuranceWindow.setStyleSheet(f"color: {css.m_standardTextColor}; background-color: {css.m_mainBackgroundColor};")
        resp = assuranceWindow.exec()

        if(resp == pyw.QMessageBox.No):
            return

        dbcon.changeBeverageOnHopper(currentID, toChangeID, hopperid)

        if toChangeID == -1:
            for i in range(len(self.parentWidget.rtData.m_beverageList)):
                if currentID == self.parentWidget.rtData.m_beverageList[i].m_id:
                    #found the current beverage
                    temp = currentBeverageBtn(self.parentWidget, rtd.beverage(-1, hopperid, "EMPTY SLOT", 0), hopperid)
                    tempBvg = rtd.beverage(-1, hopperid, "EMPTY SLOT", 0)
                    self.m_currentBvg = tempBvg
                    self.parentWidget.hopperList[hopperid] = temp
                    self.informationLabel.setText(f"Removed {self.parentWidget.rtData.m_beverageList[i].m_name} from Hopper {hopperid}")
                    del self.parentWidget.rtData.m_beverageList[i]
                    self.m_allBeverages = dbcon.getAllOtherBeverages()
                    break
        else:
            if currentID == -1:
                #find new beverage in list
                for i in range(len(self.m_allBeverages)):
                    if toChangeID == self.m_allBeverages[i].m_id:   #found it
                        tempBvg = self.m_allBeverages[i]
                        tempBvg.m_hopperid = hopperid
                        self.informationLabel.setText(f"Put {tempBvg.m_name} on hopper {hopperid}")
                        self.m_currentBvg = tempBvg
                        self.parentWidget.hopperList[hopperid] = currentBeverageBtn(self.parentWidget, tempBvg, hopperid)
                        break
            else:
                #find old beverage
                for i in range(len(self.parentWidget.rtData.m_beverageList)):
                    #found it
                    if currentID == self.parentWidget.rtData.m_beverageList[i].m_id:
                        #find new beverage
                        for x in range(len(self.m_allBeverages)):
                            if toChangeID == self.m_allBeverages[x].m_id:
                                #found it -> now update the runtime data and print an information to the 
                                self.informationLabel.setText(f"Changed the drink from {self.parentWidget.rtData.m_beverageList[i].m_name} to {self.m_allBeverages[x].m_name} on hopper {hopperid}")
                                #set new hopperid
                                self.m_allBeverages[x].m_hopperid = hopperid
                                #override all the old data
                                self.m_currentBvg = self.m_allBeverages[x]
                                self.parentWidget.rtData.m_beverageList[i] = self.m_allBeverages[x]
                                self.parentWidget.hopperList[hopperid] = currentBeverageBtn(self.parentWidget, self.parentWidget.rtData.m_beverageList[i], hopperid)
                                #update beverages with hopperid = null
                                self.m_allBeverages = dbcon.getAllOtherBeverages()
                                break
        self.updateQuickSelect()

    def deleteOldBtns(self):
        for i in reversed(range(self.scrollAreadVBox.count())): 
            self.scrollAreadVBox.takeAt(i).widget().setParent(None)

    def updateQuickSelect(self):
        self.deleteOldBtns()
        for i in range(len(self.m_allBeverages)):
            self.scrollAreadVBox.addWidget(beveragePushButton(self, self.m_allBeverages[i], self.m_currentBvg.m_id, self.hopperid))
        self.scrollAreadVBox.addWidget(beveragePushButton(self, rtd.beverage(-1, self.hopperid, "EMPTY SLOT", 0), self.m_currentBvg.m_id, self.hopperid))

    def switchView(self):
        self.parentWidget.updateHopperLayout()
        self.parentWidget.show()
        self.close()



##############################################################################
#       WINDOW FOR THE HOPPER OVERVIEW
##############################################################################

class editHoppers(pyw.QWidget):
    def __init__(self, __parent : pyw.QWidget, __rtd : rtd.runtimeData):
        super().__init__()
        self.parentWidget = __parent
        self.setWindowTitle("Edit Hopper Occupancy")
        self.rtData = __rtd
        self.initWidgets()
        self.resize(1200, 800)
        self.showFullScreen()
        
    def initWidgets(self):
        ##############################################################################
        #       MAIN WINDOW STYLE
        ##############################################################################
        self.setStyleSheet(f"background-color: {css.m_mainBackgroundColor};")
        
        ##############################################################################
        #       LABELS
        ##############################################################################
        self.headerLabel = pyw.QLabel("Edit Hopper Occupancy", self)
        self.headerLabel.setStyleSheet(f"color: {css.m_standardTextColor}; font-size: 24pt; font-family: {css.font};")
        self.headerLabel.setAlignment(pyc.Qt.AlignCenter)
        self.monitorLabel = pyw.QLabel("Monitor is here", self)
        self.monitorLabel.setStyleSheet(f"color: {css.m_standardTextColor};")
        self.monitorLabel.setAlignment(pyc.Qt.AlignCenter)

        ##############################################################################
        #       BUTTONS
        ##############################################################################
        self.hopperList = []
        self.usedSlots = []
        for i in range(len(self.rtData.m_beverageList)):
            temp = currentBeverageBtn(self, self.rtData.m_beverageList[i], self.rtData.m_beverageList[i].m_hopperid)
            self.usedSlots.append(self.rtData.m_beverageList[i].m_hopperid)
            self.hopperList.insert(self.rtData.m_beverageList[i].m_hopperid, temp)

        if len(self.usedSlots) < 12:
            for i in range(12):
                if i not in self.usedSlots:
                    temp = currentBeverageBtn(self, rtd.beverage(-1, i, "EMPTY SLOT", 0), i)
                    self.hopperList.insert(i, temp)

        self.backBtn = pyw.QPushButton("Back to Mainmenu", self)
        self.backBtn.clicked.connect(lambda: self.backBtn_onClick())
        self.backBtn.setStyleSheet(f"background-color: {css.m_buttonBackgroundColor}; color: {css.m_standardTextColor}; border: 1px solid {css.m_borderColor}; padding-top: 30%;padding-bottom: 30%;padding-left: 50%;padding-right: 50%;")
        
        ##############################################################################
        #       HOPPER LAYOUT
        ##############################################################################
        self.hopperFrame = pyw.QFrame(self)
        self.hopperDisplayLayout = pyw.QGridLayout(self)
        self.hopperDisplayLayout.setColumnMinimumWidth(2, 15)
        self.hopperDisplayLayout.setColumnMinimumWidth(9, 15)
        self.updateHopperLayout()
        self.hopperFrame.setLayout(self.hopperDisplayLayout)

        ##############################################################################
        #       MAIN LAYOUT
        ##############################################################################
        self.mainLayout = pyw.QGridLayout(self)
        self.mainLayout.addWidget(self.headerLabel, 0, 0, 1, 5)
        self.mainLayout.addWidget(self.monitorLabel, 7, 0, 1, 5)
        self.mainLayout.addWidget(self.hopperFrame, 2, 0, 5, 5)
        self.mainLayout.addWidget(self.backBtn, 8, 4)

    def deleteDrinkButtons(self):
        for i in reversed(range(self.hopperDisplayLayout.count())): 
            self.hopperDisplayLayout.takeAt(i).widget().setParent(None)
    
    def updateHopperLayout(self):
        self.deleteDrinkButtons()
        row = 0
        span = 2
        for i in range(12):
            if i < 4:
                self.hopperDisplayLayout.addWidget(self.hopperList[i], row, 0, span, span)
            elif i >= 4 and i < 8:
                self.hopperDisplayLayout.addWidget(self.hopperList[i], row, 10, span, span)
            else:
                if i == 10:    #top
                    self.hopperDisplayLayout.addWidget(self.hopperList[i], 1, 5, span, span)
                elif i == 11:  #side left
                    self.hopperDisplayLayout.addWidget(self.hopperList[i], 4, 3, span, span)
                elif i == 9: #side right
                    self.hopperDisplayLayout.addWidget(self.hopperList[i], 4, 7, span, span)
                elif i == 8: #bottom
                    self.hopperDisplayLayout.addWidget(self.hopperList[i], 7, 5, span, span)
            if row == 9:
                row = 0
            else:
                row += 3

    def hopperBtn_onClick(self, __currentBeverageOnHopper : rtd.beverage, __hopperid : int):
        self.m_cdw = changeDrinkWindow(self, __currentBeverageOnHopper, __hopperid)
        self.hide()

    def backBtn_onClick(self):
        self.parentWidget.updateQuickSelect()
        self.parentWidget.show()
        self.close()