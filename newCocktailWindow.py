import PyQt5.QtWidgets as pyw
import PyQt5.QtCore as pyc
import PyQt5.QtGui as pyg
import dbcon as db
import runtimeData
import cssTheme as css
import createdCocktailsWindow as ccw


class newCocktailWindow(pyw.QWidget):
    
    #fixed size for the QListwidgets
    listSize = (450,450)

    #constructor
    def __init__(self, __parentWindow : pyw.QWidget):
        super().__init__()
        self.parentWidget = __parentWindow
        self.setWindowTitle("New Cocktail Recipe")
        self.resize(1280, 800)
        self.mixDrink = runtimeData.mixDrinkInformation( 0, "", [],[])
        self.initWidgets()
        self.showFullScreen()
    
    #declares widgets, sets their style, and adds layout to the Window
    def initWidgets(self):

        self.setStyleSheet(css.windowStyle)

        # set up Lists and ListWidgets        
        self.availableBeverages = []
        self.availableBeverageList = pyw.QListWidget(self)
        self.availableBeverageList.setFixedSize(self.listSize[0], self.listSize[1])
        self.availableBeverageList.itemDoubleClicked.connect(self.onAvailableSelect)
        self.selectedBeverageList = pyw.QListWidget(self)
        self.selectedBeverageList.setFixedSize(self.listSize[0], self.listSize[1])
        self.selectedBeverageList.itemDoubleClicked.connect(self.onSelectedSelect)
        self.availableBeverageList.setMinimumHeight(550)
        self.selectedBeverageList.setMinimumHeight(550)

        self.availableBeverageList.setFont(pyg.QFont("Arial", 15))
        self.selectedBeverageList.setFont(pyg.QFont("Arial", 15))

        

        #set up Buttons
        self.acceptBtn = pyw.QPushButton("Accept")
        self.acceptBtn.setText("Accept")
        self.acceptBtn.clicked.connect(self.onAccept)
        
        self.cancelBtn = pyw.QPushButton("Cancel")
        self.cancelBtn.clicked.connect(self.onCancel)
        
        self.viewCocktailsBtn = pyw.QPushButton("Cocktails")
        self.viewCocktailsBtn.clicked.connect(self.viewCocktailsBtn_onClick)

        #set up Labels
        self.availableListLable = pyw.QLabel("Available beverages")
        self.availableListLable.setAlignment(pyc.Qt.AlignCenter)
        
        self.selectedListLable = pyw.QLabel("Selected beverages")
        self.selectedListLable.setAlignment(pyc.Qt.AlignCenter)
        
        self.recipeLabel = pyw.QLabel("Name of recipe:")
        self.recipeLabel.setStyleSheet(f"color: {css.m_standardTextColor}; font-size: 15pt; font-family: {css.font};")


        #set up LineEdit
        self.enterRecipeName = pyw.QLineEdit()
        self.enterRecipeName.setStyleSheet(f"color: {css.m_standardTextColor}; font-size: 10pt;")


        #set up Layouts
        self.gridLayout = pyw.QGridLayout(self)
        
        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(3, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(3, 1)

        self.gridLayout.addWidget(self.availableListLable, 0, 0,)
        self.gridLayout.addWidget(self.selectedListLable, 0, 2)
        self.gridLayout.addWidget(self.availableBeverageList, 2, 0)
        self.gridLayout.addWidget(self.selectedBeverageList , 2, 2)

        wrapper = pyw.QWidget()
        wrapperLayout = pyw.QVBoxLayout()
        wrapperLayout.addWidget(self.recipeLabel)
        wrapperLayout.addWidget(self.enterRecipeName)
        wrapperLayout.addWidget(self.acceptBtn)
        wrapperLayout.addWidget(self.cancelBtn)
        wrapperLayout.addWidget(self.viewCocktailsBtn)
        wrapper.setLayout(wrapperLayout)

        self.gridLayout.addWidget(wrapper, 2 ,4)

        self.setLayout(self.gridLayout)

        self.availableBeverages = db.getAllAvailableBeverages()
        self.availableBeverages += db.getAllOtherBeverages()
        self.fillList(self.availableBeverageList, self.availableBeverages)


    ################################
    #   Functions to handle data   #
    ################################

    #return the beverage of giving name out of a provided list
    def getBeverageByName(self, beverages: list, name: str) -> runtimeData.beverage:
        for beverage in beverages:
            if beverage.m_name == name:
                return beverage

    #fills a QListwidget whith beverages out of a given list
    def fillList(self, list : pyw.QListWidget, beverages):
        for beverage in beverages:
            list.addItem(beverage.m_name)


    ################################
    #           Events             #
    ################################

    #This event handles the process of puting an ingredient into the new Recipe by launching an Dialog Window,
    # that takes the needed remaining informations in
    def onAvailableSelect(self, item : pyw.QListWidgetItem):
        
        dialog = EnterIntDialog("Enter Int Dialog Title", "Enter Int Dialog Label")

        if dialog.exec_():
            result = dialog.int
        else:
            if dialog.cancel:
                return

            errorMessage = pyw.QMessageBox.critical(
                self,
                "Error",
                "Please enter an integer value.",
                buttons= pyw.QMessageBox.Discard,
                defaultButton= pyw.QMessageBox.Discard,
            )

            return
        
        #item is special pyqt object, so you have to use text()
        beverage = self.getBeverageByName(self.availableBeverages, item.text())

        self.mixDrink.m_neededBeverages.append(beverage)
        self.mixDrink.m_fillpercToBvg.append((beverage.m_id, result))

        self.selectedBeverageList.addItem(f"{beverage.m_name} - {result}%")
        self.availableBeverages.remove(beverage)

        self.availableBeverageList.clear()
        self.fillList(self.availableBeverageList, self.availableBeverages)

    #An event to remove selected Beverages from the new Recipe
    def onSelectedSelect(self, item : pyw.QListWidgetItem):

        #get beverage
        name = item.text().split()[0]
        beverage = self.getBeverageByName(self.mixDrink.m_neededBeverages, name)
        index = self.mixDrink.m_neededBeverages.index(beverage)

        #remove beverage from selectedBeveregesList
        self.selectedBeverageList.takeItem(index)
        self.mixDrink.m_neededBeverages.remove(beverage)
        fillPerc = self.mixDrink.getFillPercToId(beverage.m_id)
        self.mixDrink.m_fillpercToBvg.remove((beverage.m_id, fillPerc))

        #add beverage back to availableList
        self.availableBeverages.append(beverage)
        self.fillList(self.availableBeverageList, self.availableBeverages)


    #The event to be called when the process of selecting beverages is finished.
    #It checks, if the beverages cover 100% of the proposed mixeddrink and if the entered Name is unique. When the Constains hold, the new Recipe and Mixeddrink are created in the Databank
    def onAccept(self):
        res = 0
        print(self.mixDrink.m_fillpercToBvg)
        for beverage in self.mixDrink.m_neededBeverages:
            res += self.mixDrink.getFillPercToId(beverage.m_id)

        if res != 100:
            errorMessage = pyw.QMessageBox.critical(
                self,
                "Error",
                "Your Drink holds an insuffitioned amount.",
                buttons= pyw.QMessageBox.Discard,
                defaultButton= pyw.QMessageBox.Discard,
            )
            return

        self.mixDrink.m_name = self.enterRecipeName.text()
        print(self.mixDrink)

        if not db.saveCocktails(self.mixDrink):
            errorMessage = pyw.QMessageBox.critical(
               self,
               "Error",
               "Name for Mixed Drink is already in use.",
               buttons= pyw.QMessageBox.Discard,
               defaultButton= pyw.QMessageBox.Discard,
               )
            return
        
        self.backBtn_onClick()


    #An event to cancel the process and Close the Window
    def onCancel(self):
        self.parentWidget.updateQuickSelect()
        self.parentWidget.show()
        self.close()

    #An event to open a Window, that shows the already created Mixeddrinks
    def viewCocktailsBtn_onClick(self):
        self.createdCocktailsWindow = ccw.CreatedCocktailsWindow(self)
        self.hide()

#A helper class, that inherets from the Standard QDialog class, to Implement costom functionality.
#It asks the user for an integer value, that represents the percantage amount of the beveragwe in the Drink
class EnterIntDialog(pyw.QDialog):

    #constructor that also setups the Widgets, Layout and stylesheet of the dialog
    def __init__(self, title = "", label = ""):
        super().__init__()
        self.cancel = False

        self.setStyleSheet(css.dialogStyle)
        self.setWindowTitle(title)

        self.int = 0
        QBtn = pyw.QDialogButtonBox.Ok | pyw.QDialogButtonBox.Cancel

        layout = pyw.QVBoxLayout(self)

        self.label = pyw.QLabel()
        self.label.setText(label)
        self.enterInt = pyw.QLineEdit()
        self.enterInt.maxLength = 3

        layout.addWidget(self.label)
        layout.addWidget(self.enterInt)

        self.buttonBox = pyw.QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.exit)
        self.buttonBox.rejected.connect(self.reject)

        layout.addWidget(self.buttonBox)

    #An event, that checks if the input of the QLineEdit is valid.
    #If valid it saves the Integer and closes the itself with a success status, else it closes itself whith an unsuccessful status
    def exit(self):
        text = self.enterInt.text()
        if text.isdigit()==True:
            self.int = int(text)
            print(self.int)
            self.accept()
        else:
            super().reject()