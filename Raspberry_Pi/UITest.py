import PyUi
import PyQt5
from PyQt5 import QtWidgets
from OpenTurret_UI import MyWindow
import os

if __name__ == "__main__":
    import sys
    if sys.platform == 'darwin':
        os.environ['QT_MAC_WANTS_LAYER'] = '1'  # added to fix operation on mac
    app = QtWidgets.QApplication(sys.argv)
    ui = PyUi.Ui_MainWindow()
    #app.setStyle("fusion")
    gui = MyWindow(ui)
    ui.setupUi(gui)
    gui.startup_procedure()  # Startup app
    gui.show()
    sys.exit(app.exec_())
