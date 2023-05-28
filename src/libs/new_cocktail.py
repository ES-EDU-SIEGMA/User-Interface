import PyQt5.QtWidgets as pyw
import PyQt5.QtCore as pyc
import PyQt5.QtGui as pyg
from . import (
    runtime_data as runtimeData,
    css as css,
    created_cocktail as ccw,
    json_data as db,
)


class NewCocktailWindow(pyw.QWidget):
    listSize = (450, 450)

    def __init__(self, __parentWindow: pyw.QWidget):
        super().__init__()
        self.parentWidget = __parentWindow
        self.setWindowTitle("New Cocktail Recipe")
        self.resize(1280, 800)
        self.mixDrink = runtimeData.MixDrinkInformation(0, "", [])
        self.initWidgets()
        self.showFullScreen()

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

        # set up Buttons
        self.acceptBtn = pyw.QPushButton("Accept")
        self.acceptBtn.setText("Accept")
        self.acceptBtn.clicked.connect(self.onAccept)

        self.cancelBtn = pyw.QPushButton("Cancel")
        self.cancelBtn.clicked.connect(self.onCancel)

        self.viewCocktailsBtn = pyw.QPushButton("Cocktails")
        self.viewCocktailsBtn.clicked.connect(self.viewCocktailsBtn_onClick)

        # set up Labels
        self.availableListLable = pyw.QLabel("Available beverages")
        self.availableListLable.setAlignment(pyc.Qt.AlignCenter)

        self.selectedListLable = pyw.QLabel("Selected beverages")
        self.selectedListLable.setAlignment(pyc.Qt.AlignCenter)

        self.recipeLabel = pyw.QLabel("Name of recipe:")
        self.recipeLabel.setStyleSheet(
            f"color: {css.m_standard_text_color}; font-size: 15pt; font-family: {css.font};"
        )

        # set up LineEdit
        self.enterRecipeName = pyw.QLineEdit()
        self.enterRecipeName.setStyleSheet(
            f"color: {css.m_standard_text_color}; font-size: 10pt;"
        )

        # set up Layouts
        self.gridLayout = pyw.QGridLayout(self)

        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(3, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(3, 1)

        self.gridLayout.addWidget(
            self.availableListLable,
            0,
            0,
        )
        self.gridLayout.addWidget(self.selectedListLable, 0, 2)
        self.gridLayout.addWidget(self.availableBeverageList, 2, 0)
        self.gridLayout.addWidget(self.selectedBeverageList, 2, 2)

        wrapper = pyw.QWidget()
        wrapperLayout = pyw.QVBoxLayout()
        wrapperLayout.addWidget(self.recipeLabel)
        wrapperLayout.addWidget(self.enterRecipeName)
        wrapperLayout.addWidget(self.acceptBtn)
        wrapperLayout.addWidget(self.cancelBtn)
        wrapperLayout.addWidget(self.viewCocktailsBtn)
        wrapper.setLayout(wrapperLayout)

        self.gridLayout.addWidget(wrapper, 2, 4)

        self.setLayout(self.gridLayout)

        self.availableBeverages = db.get_all_available_beverages()
        self.availableBeverages += db.get_all_other_beverages()
        self.fillList(self.availableBeverageList, self.availableBeverages)
        self.selectedBeverages: [runtimeData.Beverage] = []

    ################################
    #   Functions to handle data   #
    ################################

    def getBeverageByName(self, beverages: list, name: str) -> runtimeData.Beverage:
        for beverage in beverages:
            if beverage.m_name == name:
                return beverage

    def fillList(self, list: pyw.QListWidget, beverages):
        for beverage in beverages:
            list.addItem(beverage.m_name)

    ################################
    #           Events             #
    ################################

    def onAvailableSelect(self, item: pyw.QListWidgetItem):
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
                buttons=pyw.QMessageBox.Discard,
                defaultButton=pyw.QMessageBox.Discard,
            )

            return

        # item ist spezielles pyqt5 objekt, deshalb text() darauf aufrufen.
        beverage = self.getBeverageByName(self.availableBeverages, item.text())
        # todo: hier die setFillPercentage rausschmeißen
        self.mixDrink.m_fill_percentage_to_beverage.append((beverage.m_id, result))

        self.selectedBeverageList.addItem(f"{beverage.m_name} - {result}%")
        self.availableBeverages.remove(beverage)
        self.selectedBeverages.append(beverage)

        self.availableBeverageList.clear()
        self.fillList(self.availableBeverageList, self.availableBeverages)

    def onSelectedSelect(self, item: pyw.QListWidgetItem):
        # get beverage
        name = item.text().split()[0]
        beverage = self.getBeverageByName(self.selectedBeverages, name)

        # remove beverage from selectedBeveregesList
        index = self.selectedBeverageList.indexFromItem(item).row()
        self.selectedBeverageList.takeItem(index)
        self.selectedBeverages.remove(beverage)

        fillPerc = self.mixDrink.get_fill_percentage_to_id(beverage.m_id)
        for ingredient_index in range(len(self.mixDrink.m_fill_percentage_to_beverage)):
            if (
                beverage.m_id
                == self.mixDrink.m_fill_percentage_to_beverage[ingredient_index][0]
            ):
                del self.mixDrink.m_fill_percentage_to_beverage[ingredient_index]
                break

        # add beverage back to availableList
        self.availableBeverages.append(beverage)
        self.fillList(self.availableBeverageList, self.availableBeverages)

    def onAccept(self):
        res = 0
        print(self.mixDrink.m_fill_percentage_to_beverage)
        for ingredient in self.mixDrink.m_fill_percentage_to_beverage:
            res += ingredient[1]

        if res != 100:
            errorMessage = pyw.QMessageBox.critical(
                self,
                "Error",
                "Your Drink holds an insuffitioned amount.",
                buttons=pyw.QMessageBox.Discard,
                defaultButton=pyw.QMessageBox.Discard,
            )
            return

        self.mixDrink.m_name = self.enterRecipeName.text()
        print(self.mixDrink)

        if not db.save_cocktails(self.mixDrink):
            errorMessage = pyw.QMessageBox.critical(
                self,
                "Error",
                "Name for Mixed Drink is already in use.",
                buttons=pyw.QMessageBox.Discard,
                defaultButton=pyw.QMessageBox.Discard,
            )
            return

        self.backBtn_onClick()

    def onCancel(self):
        self.backBtn_onClick()

    def backBtn_onClick(self):
        self.parentWidget.update_quick_select()
        self.parentWidget.show()
        self.close()

    def viewCocktailsBtn_onClick(self):
        self.createdCocktailsWindow = ccw.CreatedCocktailsWindow(self)
        self.hide()


class EnterIntDialog(pyw.QDialog):
    def __init__(self, title="", label=""):
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

    def exit(self):
        text = self.enterInt.text()
        if text.isdigit() == True:
            self.int = int(text)
            print(self.int)
            self.accept()
        else:
            super().reject()

    def reject(self):
        self.cancel = True
        super().reject()

    def setLable(self, text=""):
        self.label.setText(text)
