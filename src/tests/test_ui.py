import PyQt5.QtWidgets as pyw
import PyQt5.QtCore as pyc
import test_serial as tsr
import serial_com as sc
#import serial_mock as sc
import css_test as css

# currently not used
#waitingRdy = None


class testGui(pyw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Test serial')
        self.resize(1200, 800)
        self.showFullScreen()


        self.sendTestMsgAll = pyw.QPushButton("sendTestMsgAll(timing: int)", self)
        self.sendTestMsgAll.setStyleSheet(css.btnStyle)
        self.sendTestMsgAll.clicked.connect(lambda: self.callSendTestMsgAll())

        self.sendTestMsgHopper = pyw.QPushButton("sendTestMsgHopper(hopperid: int, timing: int)", self)
        self.sendTestMsgHopper.setStyleSheet(css.btnStyle)
        self.sendTestMsgHopper.clicked.connect(lambda: self.callSendTestMsgHopper())

        self.sendTestMsgPico = pyw.QPushButton("sendTestMsgPico(hopperid:int, timing:int, timing:int, timing:int, timing:int)", self)
        self.sendTestMsgPico.setStyleSheet(css.btnStyle)
        self.sendTestMsgPico.clicked.connect(lambda: self.callsendTestMsgPico())

        #currently not used
        """ self.waitRdy = pyw.QPushButton("(Toggle) Not waiting for rdy signal", self)
        self.waitRdy.setStyleSheet(css.btnStyle)
        self.waitRdy.clicked.connect(lambda: self.callWaitRdyToggle()) """

        self.exitBtn = pyw.QPushButton("Exit Application", self)
        self.exitBtn.setStyleSheet(css.btnStyle)
        self.exitBtn.clicked.connect(lambda: self.exitBtn_onClick())

        self.currentValue = pyw.QLabel('(Input Int comma seperated) Current Value: ', self)
        self.currentValue.setStyleSheet(f"font-size: 30pt; font-family: {css.font}; margin-top: 25%;")
        self.currentValue.setAlignment(pyc.Qt.AlignCenter)
        

        self.line = pyw.QLineEdit(self)
        self.line.setStyleSheet(f"font-size: 30pt; font-family: {css.font}; margin-top: 25%;")
        self.line.textChanged.connect(lambda: self.currentValue.setText(f"(Input Int comma seperated) Current Value: {self.line.text()}") )

        
        self.mainGridLayout = pyw.QGridLayout(self)

        self.mainGridLayout.addWidget(self.sendTestMsgAll, 0 , 0, 1, 3)
        self.mainGridLayout.addWidget(self.sendTestMsgHopper, 1, 0, 1, 3)
        self.mainGridLayout.addWidget(self.sendTestMsgPico, 2, 0, 1, 3)
        self.mainGridLayout.addWidget(self.exitBtn, 3, 0, 1, 3)
        #self.mainGridLayout.addWidget(self.waitRdy, 4, 0, 1, 1)
        self.mainGridLayout.addWidget(self.line, 4 ,1, 1, 2)
        self.mainGridLayout.addWidget(self.currentValue, 5 , 0, 1, 3)

        self.setLayout(self.mainGridLayout)


    def callSendTestMsgAll(self):
        """ sends the same timing to all 12 hoppers """

        try:
            text = int(self.line.text())
            tsr.sendTestMsgAll(text)
            self.currentValue.setText(f"sending to all hoppers timing {text}")
        except Exception as e:
            self.currentValue.setText(f"{e}")



    def callSendTestMsgHopper(self):
        """ sends a timing to one hopper """

        try:
            text = [eval (i) for i in self.line.text().split(",")]
            if len(text) != 2 or type(text) != list:
                self.currentValue.setText("Wrong Number of arguments")
            else:
                tsr.sendTestMsgHopper(text[0],text[1])
                self.currentValue.setText(f"sending to hopper {text[0]} timing {text[1]}")
        except Exception as e:
            self.currentValue.setText(f"{e}")


    def callsendTestMsgPico(self):
        """ sends 4 indivual timings to one pico """

        try:
            text = [eval (i) for i in self.line.text().split(",")]
            if len(text) != 5 or type(text) != list:
                self.currentValue.setText("Wrong Number of arguments or a type error")
            else:
                tsr.sendTestMsgPico(text[0],text[1],text[2],text[3],text[4])
                self.currentValue.setText(f"sending to picoID {text[0]} timings {text[1]} {text[2]} {text[3]} {text[4]}")
        except Exception as e:
            self.currentValue.setText(f"{e}")


    #currently not used       
    """     def callWaitRdyToggle(self):
        

        global waitingRdy
        waitingRdy = not waitingRdy
        if waitingRdy:
            self.waitRdy.setText("(Toggle) Waiting for rdy signal")
        else :
            self.waitRdy.setText("(Toggle) Not waiting for rdy signal")"""
            


    def exitBtn_onClick(self):
        sc.close_connection()
        self.close()