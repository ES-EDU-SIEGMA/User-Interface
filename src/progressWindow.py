import PyQt5.QtWidgets as pyw
import PyQt5.QtCore as pyc
import PyQt5.QtGui as pyg
import runtimeData as rtd
import cssTheme as css
import serialCom as sc
import scaleReader as sr
import globals as go
import time

CF_LITER_ML 	= 1000
CF_SEC_MILLISEC = 1000
PERODIC_WEIGHT_CHECK_IN_SECONDS = 8
HOPPER_SIZE_SMALL   = 30   
HOPPER_SIZE_LARGE   = 40   

## window to start and view the mixing progress
#
class mixingProgressWindow(pyw.QWidget):
    m_beverageToMix: rtd.beverage
    m_mixedDrinkToMix: rtd.mixDrinkInformation
    m_mixedDrinkMode: bool
    m_mixing: bool

    # constructor
    def __init__(
        self,
        __parentWindow: pyw.QWidget,
        __bvg: rtd.beverage,
        __md: rtd.mixDrinkInformation,
    ):
        super().__init__()
        self.parentWidget = __parentWindow
        self.setWindowTitle("Mixing Progress")
        self.setStyleSheet(f"background-color: {css.m_mainBackgroundColor};")
        self.m_mixing = False
        self.m_beverageToMix = __bvg
        self.m_mixedDrinkToMix = __md
        self.m_mixedDrinkMode = self.m_beverageToMix is None
        self.standardActivationTime = go.standardActivationTime
        self.initWidgets()
        self.showFullScreen()

    # initializes all the widgets on the gui, sets their style and position
    def initWidgets(self):
        ##############################################################################
        #       LABELS
        ##############################################################################
        self.drinkSizeLabel = pyw.QLabel("Select the Size of your Drink:", self)
        self.drinkSizeLabel.setStyleSheet(
            f"color: {css.m_standardTextColor}; font-size: 11pt;"
        )

        self.headerLabel = pyw.QLabel(f"", self)
        if self.m_mixedDrinkMode:
            self.headerLabel.setText(f"Mixing {self.m_mixedDrinkToMix.m_name}")
        else:
            self.headerLabel.setText(f"Mixing {self.m_beverageToMix.m_name}")
        self.headerLabel.setStyleSheet(
            f"color: {css.m_standardTextColor}; font-size: 14pt;"
        )
        self.headerLabel.setAlignment(pyc.Qt.AlignCenter)

        self.informationLabel = pyw.QLabel("", self)
        self.informationLabel.setStyleSheet(f"color: {css.m_standardTextColor};")

        ##############################################################################
        #       BUTTONS
        ##############################################################################
        self.backBtn = pyw.QPushButton("Back to Main Menu", self)
        self.backBtn.clicked.connect(lambda: self.backBtn_onClick())
        self.backBtn.setStyleSheet(
            f"background-color: {css.m_buttonBackgroundColor}; padding-top: 30%; padding-bottom: 30%; padding-left: 40%; padding-right: 40%; color: {css.m_standardTextColor}; margin: 5%; border: 1px solid #ffffff;"
        )

        self.startMixingBtn = pyw.QPushButton("Start Mixing", self)
        self.startMixingBtn.clicked.connect(lambda: self.startMixingBtn_onClick())
        self.startMixingBtn.setStyleSheet(
            f"background-color: {css.m_buttonBackgroundColor}; padding-top: 30%; padding-bottom: 30%; padding-left: 40%; padding-right: 40%; color: {css.m_standardTextColor}; margin: 5%; border: 1px solid #ffffff;"
        )

        ##############################################################################
        #       COMBOBOX
        ##############################################################################
        """
        	These elementes represent the available drink sizes guest can select,
        	but should not used further - have changed it for now ...
        """
        sizes: List[str] = ["0.1 L", "0.2 L", "0.3 L", "0.4 L", "0.5 L"]
        self.drinkSizeSelect = pyw.QComboBox(self)
        for index, size in enumerate(sizes):
        	self.drinkSizeSelect.instertItem(index, size)
        	
       
        self.drinkSizeSelect.setStyleSheet(
            f"color: {css.m_standardTextColor}; background-color: {css.m_buttonBackgroundColor}; border: 1px solid {css.m_borderColor}; padding-top: 25%; padding-bottom: 25%; padding-left: 40%; padding-right: 40%; font-size: 14pt;"
        )

        ##############################################################################
        #       PROGRESSBAR
        ##############################################################################
        self.mixingProgress = pyw.QProgressBar(self)
        self.mixingProgress.setStyleSheet(f"color: {css.m_standardTextColor};")
        self.mixingProgress.setMinimum(0)
        self.mixingProgress.setMaximum(100)
        self.mixingProgress.setValue(0)

        ##############################################################################
        #       LAYOUT
        ##############################################################################
        self.mainLayout = pyw.QGridLayout(self)
        self.mainLayout.addWidget(self.headerLabel, 0, 0, 1, 2)
        self.mainLayout.addWidget(self.drinkSizeLabel, 1, 0)
        self.mainLayout.addWidget(self.drinkSizeSelect, 1, 1)
        self.mainLayout.addWidget(self.mixingProgress, 2, 0, 2, 2)
        self.mainLayout.addWidget(self.informationLabel, 3, 0, 1, 2)
        self.mainLayout.addWidget(self.backBtn, 4, 1)
        self.mainLayout.addWidget(self.startMixingBtn, 4, 0)

    # gets triggered when the start mixing button gets clicked
    # starts either the beverage or the mixdrink mixing progress
    def startMixingBtn_onClick(self):
        self.backBtn.setEnabled(False)
        self.startMixingBtn.setEnabled(False)
        self.drinkSizeSelect.setEnabled(False)
        expectedWeight = 0
        emptyDrinkWeight = sr.getCurrentWeight()

        currentDrinkSizeIndex = self.drinkSizeSelect.currentIndex()
        multip = (1 + currentDrinkSizeIndex) / 10

        currentDrinkName = ""
        if self.m_mixedDrinkMode:
            currentDrinkName = self.m_mixedDrinkToMix.m_name
        else:
            currentDrinkName = self.m_beverageToMix.m_name

        self.informationLabel.setText(
            f"Mixing {currentDrinkName}, {multip} L. Please do not touch the display or the machine!"
        )
        self.m_mixing = True  # set mixing to true

        if self.m_mixedDrinkMode:
            expectedWeight = self.mixMixDrink(self.m_mixedDrinkToMix, multip)
        else:
            expectedWeight = self.mixBeverage(self.m_beverageToMix, multip)

        expectedWeightFull = expectedWeight + emptyDrinkWeight
        self.waitForDrinkFinish(expectedWeight, expectedWeightFull, emptyDrinkWeight)
        self.m_mixing = False

        self.backBtn.setEnabled(True)
        self.startMixingBtn.setEnabled(True)
        self.drinkSizeSelect.setEnabled(True)
        self.informationLabel.setText(
            "The Drink is finished. Please remove your drink from the machine."
        )

    # reads out the scale and sets the value of the progressbar accordingly - if the value hasnt changed in 8 secs -> quit
    def waitForDrinkFinish(
        self, expectedWeight: int, expectedWeightFull: int, emptyDrinkWeight: int
    ):
        currentWeight = sr.getCurrentWeight()
        timeval = time.time()
        currentWeightComp = currentWeight
        while (
            currentWeight not in range(expectedWeightFull - 5, expectedWeightFull + 5)
            and self.m_mixing
        ):  # a little bit of breathing room
            if (
                time.time() - timeval >= PERODIC_WEIGHT_CHECK_IN_SECONDS
            ):  # check each 8 seconds if the value has changed
                if currentWeightComp == currentWeight:  # value is the same -> quit
                    self.mixing = False
                    break
                else:
                    timeval = time.time()
                    currentWeightComp = currentWeight
            self.mixingProgress.setValue(
                int(((currentWeight - emptyDrinkWeight) / expectedWeight) * 100)
            )
            currentWeight = sr.getCurrentWeight()
            time.sleep(0.5)
        self.mixingProgress.setValue(100)

    # calculates and sends the timings which are needed to mix the given beverage for the given drinksize
    def mixBeverage(self, __bvgToMix: rtd.beverage, _multi: int):
        cupSize = _multi * CF_LITER_ML
        hopperSize = HOPPER_SIZE_SMALL
        picoid = 0
        strToSend = ""

        if __bvgToMix.m_hopperid > 8:
            hopperSize = HOPPER_SIZE_LARGE

        hopperTimings = [0, 0, 0, 0]

        picoid = self.getPicoIdToHopperId(__bvgToMix.m_hopperid)

        res = self.calcTimeForActivation(__bvgToMix, cupSize, 100, hopperSize)

        for i in range(len(res) - 1):
            hopperTimings[__bvgToMix.m_hopperid % 4] = res[i + 1]
            strToSend = f"{hopperTimings[0]};{hopperTimings[1]};{hopperTimings[2]};{hopperTimings[3]};\n"
            sc.send_msg(picoid, strToSend)
        return (len(res) - 1) * hopperSize

    # calculates the time and iteration amounts needed to mix a given beverages
    def calcTimeForActivation(
        self, __bvg: rtd.beverage, cupSize: int, __fillperc: int, hoppersize: int
    ):
        activationAmountFull = int((cupSize * (__fillperc / 100)) // hoppersize)
        # activationAmountRest = ((cupSize * (__fillperc / 100)) % hoppersize) / hoppersize
        activationTimeFull = int(self.standardActivationTime * __bvg.m_flowspeed * CF_SEC_MILLISEC)
        # activationTimeRest = int(self.standardActivationTime * __bvg.m_flowspeed * activationAmountRest * CF_SEC_MILLISEC)
        temp = []

        if activationAmountFull == 0:
            activationTimeFull = 0
        # if activationAmountRest > 0:
        #     activationAmountRest = 1

        temp.append(__bvg.m_hopperid)
        for _ in range(activationAmountFull):
            temp.append(activationTimeFull)

        # if activationAmountRest > 0:
        #     temp.append(activationTimeRest)
        return temp

    # calculates all the information needed to mix the given mixdrink and sends them to the corresponding picos
    def mixMixDrink(self, __mixDrinkToMix: rtd.mixDrinkInformation, __multip: int):
        cupSize = __multip * CF_LITER_ML
        hoppersize = HOPPER_SIZE_SMALL
        timeList = []
        picoid = 0

        # calculate the time, each bvg needs and add them to the list
        for i in range(len(__mixDrinkToMix.m_neededBeverages)):
            if __mixDrinkToMix.m_neededBeverages[i].m_hopperid > 8:
                hoppersize = HOPPER_SIZE_LARGE
            timeList.append(
                self.calcTimeForActivation(
                    __mixDrinkToMix.m_neededBeverages[i],
                    cupSize,
                    __mixDrinkToMix.getFillPercToId(
                        __mixDrinkToMix.m_neededBeverages[i].m_id
                    ),
                    hoppersize,
                )
            )
            hoppersize = HOPPER_SIZE_SMALL

        cmdList = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

        iterCounter = 1
        timings = self.getTimingsToPico(timeList)
        longestListLen = self.getLongestListLength(timings)

        expectedWeight = self.getEstimatedWeight(timeList)

        # runs through the list and puts the timings into the corresponding hopper cmdS
        while not (iterCounter == longestListLen):
            for picoid in range(3):  # run through each pico entry
                for i in range(
                    len(timings[picoid])
                ):  # run through each timing and place in the corresponding list entry
                    temp = timings[picoid]
                    hopperid = temp[i][0] % 4

                    if iterCounter < len(temp[i]):
                        cmdList[picoid][hopperid] = temp[i][iterCounter]
                    else:
                        cmdList[picoid][hopperid] = 0

            pico0Cmd = (
                f"{cmdList[0][0]};{cmdList[0][1]};{cmdList[0][2]};{cmdList[0][3]};\n"
            )
            pico1Cmd = (
                f"{cmdList[1][0]};{cmdList[1][1]};{cmdList[1][2]};{cmdList[1][3]};\n"
            )
            pico2Cmd = (
                f"{cmdList[2][0]};{cmdList[2][1]};{cmdList[2][2]};{cmdList[2][3]};\n"
            )

            sc.send_msg(0, pico0Cmd)
            sc.send_msg(1, pico1Cmd)
            sc.send_msg(2, pico2Cmd)
            print(f"left {pico0Cmd}right {pico1Cmd}rondell {pico2Cmd}")
            iterCounter += 1
        return expectedWeight

    # returns the length of the longest list
    def getLongestListLength(self, __timelist):
        longest = 0
        for i in range(len(__timelist)):
            for y in range(len(__timelist[i])):
                currentlen = len(__timelist[i][y])
                if currentlen > longest:
                    longest = currentlen
        return longest

    # seperates the beverage timings to their corresponding pico
    def getTimingsToPico(self, __timeList):
        res = [[], [], []]
        for i in range(len(__timeList)):
            picoid = self.getPicoIdToHopperId(__timeList[i][0])
            res[picoid].append(__timeList[i])
        return res

    # returns the id of the pico which is responsible for the hopper
    def getPicoIdToHopperId(self, __hopperid: int):
        picoid = 0
        if __hopperid < 4:
            picoid = 1
        elif __hopperid >= 4 and __hopperid < 8:
            picoid = 0
        else:
            picoid = 2
        return picoid

    # returns the estimated weight of the drink after its mixed -> 1ml = 1g
    def getEstimatedWeight(self, __timeList):
        res = 0
        for i in range(len(__timeList)):
            hoppersize = HOPPER_SIZE_SMALL
            if __timeList[i][0] > 8:
                hoppersize = HOPPER_SIZE_LARGE
            for y in range(len(__timeList[i]) - 1):
                res += hoppersize
        return res

    def backBtn_onClick(self):
        if not self.m_mixing:
            self.close()
