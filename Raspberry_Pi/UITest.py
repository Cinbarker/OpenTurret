import qdarkstyle
import PyUi
from PyQt5 import QtWidgets
from OpenTurret_UI import MyWindow

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = PyUi.Ui_MainWindow()
    #app.setStyleSheet(qdarkstyle.load_stylesheet())  # Set Dark Theme
    gui = MyWindow(ui)
    ui.setupUi(gui)
    gui.setDefaults()  # Set my default values
    gui.show()
    sys.exit(app.exec_())
