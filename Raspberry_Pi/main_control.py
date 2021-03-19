# This is the default file for selecting which modes to enable
import Raspberry_Pi
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 button - pythonspot.com'
        self.left = 300
        self.top = 400
        self.width = 800
        self.height = 500
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        button = QPushButton('PyQt5 button', self)
        button.setToolTip('This is an example button')
        button.move(self.width*0.5, self.height*0.5)
        button.clicked.connect(self.on_click)

        self.show()

    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())



# run_joystick_control = 0
# run_laser_tracking_control = 0
# run_space_control = 0
#
# print('(1. Joystick) (2. Laser Track) (3. Space Track)')
# mode = input('Enter Mode Number: ')
#
# if mode == '1':
#     run_joystick_control = 1
# elif mode != '1':
#     run_joystick_control = input('Enable Joystick Control (0/1): ')
#     if int(run_joystick_control) < 0 or int(run_joystick_control) > 1:
#         print('Invalid Selection')
#         exit(0)
#
# if mode == '2':
#     run_laser_tracking_control = 1
# elif mode == '3':
#     run_space_control = 1
# else:
#     print('Invalid Selection')
#     exit(0)
