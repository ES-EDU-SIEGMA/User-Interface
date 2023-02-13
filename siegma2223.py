import PyQt5.QtWidgets as pyw
import PyQt5.QtCore as pyc
import cssTheme as css
import progressWindow as spw
import newCocktailWindow as ncw
import editHoppersWindow as ehw
import runtimeData as rtd
import serialCom as sc
import dbcon as dbcon
import scaleReader as sr
import sys
import globals as go
import time

## @package siegma2223
#   This Code implements the main landing page of the application
#
#   written by Tobias Mathena

## This pushbutton is used to display the mixable beverages
#
#  derived from QPushButton, hold the information of which beverage its representing via the information variable
class beveragePushButton(pyw.QPushButton):
    information : rtd.beverage
    m_index = -1
    ## constructor
    def __init__(self, __parent : pyw.QWidget, __beverageData : rtd.beverage):
        super().__init__()
        self.parentWidget = __parent
        self.setStyleSheet(f"background-color: {css.m_sndButtonBackgroundColor}; padding-top: 70%; padding-bottom: 70%; color: {css.m_standardTextColor}; margin: 5%; font-size: 11pt;")
        self.clicked.connect(lambda: self.parentWidget.qsDrinkButton_onClick(self.m_index, False))
        self.information = __beverageData
        self.setText(self.information.m_name)
        self.m_index = self.information.m_id

## This pushbutton is used to display the mixable mixdrinks
#
#  derived from QPushButton, hold the information of which mixdrink its representing via the information variable
class mixedDrinkPushButton(pyw.QPushButton):
    information : rtd.mixDrinkInformation
    ## constructor
    m_index = -1
    def __init__(self, __parent : pyw.QWidget, __beverageData : rtd.beverage):
        super().__init__()
        self.parentWidget = __parent 
        self.setStyleSheet(f"background-color: {css.m_sndButtonBackgroundColor}; padding-top: 70%; padding-bottom: 70%; color: {css.m_standardTextColor}; margin: 5%; font-size: 11pt;")
        self.clicked.connect(lambda: self.parentWidget.qsDrinkButton_onClick(self.m_index, True))
        self.information = __beverageData
        self.setText(self.information.m_name)
        self.m_index = self.information.m_id

## main landing page of the application
#
#  this class represents the main landing page of the application, every other sub window is called from this class
#  it contains the runtime data and controlls the flow of the application
class welcomeWindow(pyw.QWidget):
    ## stores the current beverages and mixdrinks which are available with the current hopper configuration
    m_runtimeData : rtd.runtimeData
    
    cocktailWindow : ncw.newCocktailWindow
    progressWindow : spw.mixingProgressWindow
    editHopperWindow : ehw.editHoppers

    ## constructor
    def __init__(self):
        super().__init__()
        self.setWindowTitle('SIEGMA_2223 - Test')
        self.initWidgets()
        #self.showMaximized()
        self.resize(1200, 800)
        self.showFullScreen()
        #self.integrationTest()
    ## Initializes the widgets used in the gui
    #
    # Gets called from the constructor
    def initWidgets(self):
        #define widgets
        self.setStyleSheet(f"background-color: {css.m_mainBackgroundColor};")

        ##############################################################################
        #       LABELS
        ##############################################################################

        self.headerLabel = pyw.QLabel('Drink Mixing Machine', self)
        self.headerLabel.setAlignment(pyc.Qt.AlignCenter)
        self.headerLabel.setStyleSheet(f"color: {css.m_standardTextColor}; font-size: 30pt; font-family: {css.font}; margin-top: 25%;")
        self.subheaderLabel = pyw.QLabel('SIEGMA-WS2223', self)
        self.subheaderLabel.setAlignment(pyc.Qt.AlignCenter)
        self.subheaderLabel.setStyleSheet(f"color: {css.m_buttonBackgroundColor}; font-size: 15pt; font-family: {css.font};")
        self.descriptionLabel = pyw.QLabel("Quick select for drinks:", self)
        self.descriptionLabel.setStyleSheet(f"color: {css.m_standardTextColor}; font-size: 12pt; font-family: {css.font};")

        ##############################################################################
        #       BUTTONS
        ##############################################################################

        self.exitBtn = pyw.QPushButton("Exit Application", self)
        self.exitBtn.setStyleSheet(f"background-color: {css.m_buttonBackgroundColor}; color: {css.m_standardTextColor}; padding: 60%; font-size: 11pt; border: 2px solid {css.m_borderColor}; border-radius: {css.borderRadius}px; margin-left: 20%;")
        self.exitBtn.clicked.connect(lambda: self.exitBtn_onClick())

        self.addNewCocktailBtn = pyw.QPushButton("New Cocktail", self)
        self.addNewCocktailBtn.setStyleSheet(f"background-color: {css.m_buttonBackgroundColor}; color: {css.m_standardTextColor}; padding: 60%; font-size: 11pt;border: 2px solid {css.m_borderColor};border-radius: {css.borderRadius}px; margin-left: 20%;")
        self.addNewCocktailBtn.clicked.connect(lambda: self.newCocktailBtn_onClick())

        self.editHopperOccupancyBtn = pyw.QPushButton("Change Drinks on Hopper", self)
        self.editHopperOccupancyBtn.setStyleSheet(f"background-color: {css.m_buttonBackgroundColor}; color: {css.m_standardTextColor}; padding: 60%; font-size: 11pt;border: 2px solid {css.m_borderColor};border-radius: {css.borderRadius}px; margin-left: 20%;")
        self.editHopperOccupancyBtn.clicked.connect(lambda: self.editHopperOccupancyBtn_onClick())

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
        self.allDrinksFrame.setStyleSheet(f"border: 0px solid {css.m_borderColor}; color: {css.m_standardTextColor};")
        self.allDrinksFrame.setWidget(self.wrapperWidget)

        ##############################################################################
        #       LAYOUT
        ##############################################################################

        self.mainGridLayout = pyw.QGridLayout(self)

        self.mainGridLayout.addWidget(self.headerLabel, 0 , 0, 1, 3)
        self.mainGridLayout.addWidget(self.subheaderLabel, 1, 0, 1, 3)
        self.mainGridLayout.addWidget(self.descriptionLabel, 2, 0)
        self.mainGridLayout.addWidget(self.addNewCocktailBtn, 4 , 2)
        self.mainGridLayout.addWidget(self.editHopperOccupancyBtn, 6, 2)
        self.mainGridLayout.addWidget(self.exitBtn, 8 , 2)
        self.mainGridLayout.addWidget(self.allDrinksFrame, 3, 0, 6, 2)

        self.setLayout(self.mainGridLayout)

##############################################################################
#       CUSTOM FUNCTIONS
##############################################################################
    ## Clears the Buttons from the allDrinkFrame
    #
    #
    def deleteDrinkButtons(self):
        for i in reversed(range(self.scrollAreadVBox.count())): 
            self.scrollAreadVBox.takeAt(i).widget().setParent(None)
    
    ## Fills the allDrinksFrame with the mixable beverages and mixdrinks
    #
    #  uses a database call to get the current available beverages and mixdrinks
    def updateQuickSelect(self):
        self.deleteDrinkButtons()
        allBeverages = dbcon.getAllAvailableBeverages()
        allMixedDrinks = dbcon.getAllAvailableMixedDrinks()
        self.m_runtimeData = rtd.runtimeData(allBeverages, allMixedDrinks)
        
        for i in range(len(self.m_runtimeData.m_beverageList)):
            self.scrollAreadVBox.addWidget(beveragePushButton(self, allBeverages[i]))
        
        for i in range(len(self.m_runtimeData.m_mixeddrinkList)):
            self.scrollAreadVBox.addWidget(mixedDrinkPushButton(self, allMixedDrinks[i]))
            
    ## closing function
    #
    def exitBtn_onClick(self):
        sc.close_connection()
        dbcon.close_connection()
        self.close()

    ## opens the newCocktailWindow when the corresponding Button gets clicked
    #
    def newCocktailBtn_onClick(self):
        self.cocktailWindow = ncw.newCocktailWindow(self)
        self.hide()

    ## opens the progressWindow when one of the custom pushbuttons get clicked
    #
    def qsDrinkButton_onClick(self, index : int, mixeddrink : bool):
        #find the fitting beverage or mixeddrink
        if mixeddrink:
            self.progressWindow = spw.mixingProgressWindow(self, None, self.m_runtimeData.getMixedDrinkToId(index))
        else:
            self.progressWindow = spw.mixingProgressWindow(self, self.m_runtimeData.getBeverageToId(index), None)
    
    ## opens the editHoppers - Window when the corresponding Button gets clicked
    #
    def editHopperOccupancyBtn_onClick(self):
        self.editHopperWindow = ehw.editHoppers(self, self.m_runtimeData)
        self.hide()

    ## integration test, emptys each hopper once and compares the actual weight with the expected one
    #
    def integrationTest(self):
        fullWeight = 0
        emptyGlassWeight = 0

        correctHoppers = 0

        emptyGlassWeight = sr.getCurrentWeight()

        fullWeight += emptyGlassWeight

        for i in range(len(self.m_runtimeData.m_beverageList)):
            hoppers = [0,0,0,0]
            currentHopper = self.m_runtimeData.m_beverageList[i].m_hopperid
            hoppers[currentHopper%4] = int(go.standardActivationTime * self.m_runtimeData.m_beverageList[i].m_flowspeed * 1000)
            picoid = 0
            if currentHopper < 5:
                picoid = 1
            elif currentHopper >= 5 and currentHopper < 9:
                picoid = 0
            else:
                picoid = 2
            sc.send_msg(picoid, f"{hoppers[0]};{hoppers[1]};{hoppers[2]};{hoppers[3]};\n")
            time.sleep(hoppers[currentHopper%4] / 1000)
            hoppersize = 30
            if currentHopper > 8:
                hoppersize = 40
            currentWeight = 0
            currentWeight = sr.getCurrentWeight()
            if (currentWeight - fullWeight) in range(hoppersize-5, hoppersize+5):
                correctHoppers += 1
            fullWeight = currentWeight
        return correctHoppers == len(self.m_runtimeData.m_beverageList)     


## window to display any occuring error and exception
#
class errorWindow(pyw.QWidget):
    def __init__(self, __errorMsg):
        super().__init__()
        self.setWindowTitle('ERROR')
        self.error = pyw.QLabel(__errorMsg.__str__(), self)
        self.error.setStyleSheet("font-size: 20pt; color: red; font-family: Arial;")
        self.error.setAlignment(pyc.Qt.AlignCenter)
        self.error.move(0, 30)
        self.showFullScreen()
    

if __name__ == '__main__':
    #return;
    #time.sleep(5) # give the pi enough time to setup the usb ports and everything
    app = pyw.QApplication(sys.argv)
    try:
        sc.__init__()
        dbcon.__init__()
        sr.__init__()
        m_startPage = welcomeWindow()
        sys.exit(app.exec())
    except Exception as error:
        m_error = errorWindow(error)
        sys.exit(app.exec())
        