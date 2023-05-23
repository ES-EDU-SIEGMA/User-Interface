import PyQt5.QtWidgets as PyQtWidgets
import PyQt5.QtGui as PyQtGui
import json_data as JsonData
import css as Css


# This class implements the view to see which Mixed_drinks were already created,
# and what contents they hold on selection.
# Created by Jan Haase
class CreatedCocktailsWindow(PyQtWidgets.QWidget):
    def __init__(self, __parent_window: PyQtWidgets.QWidget):
        super().__init__()
        self.parentWidget = __parent_window
        self.setWindowTitle("Created Cocktails")
        self.resize(1280, 800)
        self.showFullScreen()

    # declares widgets, sets their style, and adds layout to the Window

        self.setStyleSheet(Css.windowStyle)

        self.back_button = PyQtWidgets.QPushButton("Cancel")
        self.back_button.clicked.connect(self.back_button_on_click)

        self.mixDrinkList = PyQtWidgets.QListWidget(self)
        self.mixDrinkList.itemDoubleClicked.connect(
            lambda item: self.show_mixed_drink_contents(item.text())
        )
        self.contentsList = PyQtWidgets.QListWidget(self)

        self.mixDrinkList.setFont(PyQtGui.QFont("Arial", 15))
        self.contentsList.setFont(PyQtGui.QFont("Arial", 15))

        self.mixedDrinks = JsonData.get_all_mixed_drinks()

        self.mixedDrinksNames = []
        for drink in self.mixedDrinks:
            self.mixDrinkList.addItem(drink.mix_drink_name)
            self.mixedDrinksNames.append(drink.mix_drink_name)

        self.mixedDrinkListLabel = PyQtWidgets.QLabel("Cocktails")
        self.contentsListLabel = PyQtWidgets.QLabel("Contents")

        self.gridLayout = PyQtWidgets.QGridLayout()

        self.gridLayout.addWidget(self.mixedDrinkListLabel, 0, 0)
        self.gridLayout.addWidget(self.contentsListLabel, 0, 2)
        self.gridLayout.addWidget(self.mixDrinkList, 2, 0)
        self.gridLayout.addWidget(self.contentsList, 2, 2)
        self.gridLayout.addWidget(self.back_button, 4, 4)

        self.setLayout(self.gridLayout)

    # function to fill the contentsList with the contents of a Mixed_drink, given the name of the drink
    def show_mixed_drink_contents(self, drink_name):
        index = self.mixedDrinksNames.index(drink_name)
        drink = self.mixedDrinks[index]

        self.contentsList.clear()

        for beverage in drink.mix_drink_needed_beverages:
            self.contentsList.addItem(
                f"{beverage.beverage_name} - {drink.get_fill_perc(beverage.beverage_id)}%"
            )

    # An event to close the window
    def back_button_on_click(self):
        self.parentWidget.show()
        self.close()
