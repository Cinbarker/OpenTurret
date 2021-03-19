import PyUi
from PyQt5 import QtWidgets
from Raspberry_Pi.OpenTurret_UI import MyWindow

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = PyUi.Ui_MainWindow()
    gui = MyWindow(ui)
    ui.setupUi(gui)
    #gui.updateAirTraffic(['Hello','Goodbye'])
    gui.show()
    sys.exit(app.exec_())

