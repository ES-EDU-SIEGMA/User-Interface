import PyQt5.QtWidgets as pyw
import test_ui as tui
#import serial_com as sc
import serial_mock as sc
import sys



if __name__ == "__main__":
    app = pyw.QApplication(sys.argv)
    try:
        #sr.__init__()
        sc.__init__()
        test_page = tui.testGui()
        sys.exit(app.exec())
    except Exception as error:
        print(f"error: {error}")
        sys.exit(app.exec())