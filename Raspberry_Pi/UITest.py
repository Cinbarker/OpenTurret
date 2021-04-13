import PyUi
import PyQt5
from PyQt5 import QtWidgets
from OpenTurret_UI import MyWindow

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = PyUi.Ui_MainWindow()
    #app.setStyle("fusion")
    gui = MyWindow(ui)
    ui.setupUi(gui)
    gui.setDefaults()  # Set my default values
    gui.show()
    sys.exit(app.exec_())
