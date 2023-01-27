import PyQt5.QtWidgets as pyw
import PyQt5.QtCore as pyc
import PyQt5.QtGui as pyg
import dbcon as db
import runtimeData
import cssTheme as css

#This class implements the view to see which Mixeddrinks were already created, and what contents they hold on selection.
#Created by Jan Haase
class CreatedCocktailsWindow(pyw.QWidget):

    def __init__(self, __parentWindow : pyw.QWidget):
        super().__init__()
        self.parentWidget = __parentWindow
        self.setWindowTitle("Created Cocktails")
        self.resize(1280, 800)
        self.initWidgets()
        self.showFullScreen()

    #declares widgets, sets their style, and adds layout to the Window
    def initWidgets(self):
        self.setStyleSheet(css.windowStyle)

        self.backBtn = pyw.QPushButton("Cancel")
        self.backBtn.clicked.connect(self.backBtn_onClick)

        self.mixDrinkList = pyw.QListWidget(self)
        self.mixDrinkList.itemDoubleClicked.connect(lambda item : self.showMixedDrinkContents(item.text()))
        self.contentsList = pyw.QListWidget(self)

        self.mixDrinkList.setFont(pyg.QFont("Arial", 15))
        self.contentsList.setFont(pyg.QFont("Arial", 15))

        self.mixedDrinks = db.getAllMixedDrinks()

        self.mixedDrinksNames = []
        for drink in self.mixedDrinks:
            self.mixDrinkList.addItem(drink.m_name)
            self.mixedDrinksNames.append(drink.m_name)
        
        self.mixedDrinkListLabel = pyw.QLabel("Cocktails")
        self.contentsListLabel = pyw.QLabel("Contents")

        self.gridLayout = pyw.QGridLayout()

        self.gridLayout.addWidget(self.mixedDrinkListLabel, 0, 0)
        self.gridLayout.addWidget(self.contentsListLabel, 0, 2)
        self.gridLayout.addWidget(self.mixDrinkList, 2, 0)
        self.gridLayout.addWidget(self.contentsList, 2, 2)
        self.gridLayout.addWidget(self.backBtn, 4, 4)        
        
        self.setLayout(self.gridLayout)

    #function to fill the contentsList with the contents of a mixeddrink, given the name of the drink
    def showMixedDrinkContents(self, drinkName):
        index = self.mixedDrinksNames.index(drinkName)
        drink = self.mixedDrinks[index]

        self.contentsList.clear()
        
        for beverage in drink.m_neededBeverages:
            self.contentsList.addItem(f"{beverage.m_name} - {drink.getFillPercToId(beverage.m_id)}%")

    #An eeent to close the window
    def backBtn_onClick(self):
        self.parentWidget.show()
        self.close()
        