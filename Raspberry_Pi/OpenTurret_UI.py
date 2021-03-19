import PyUi
from PyQt5 import QtWidgets
import Sky_Tracking.turret_sky as sky
from skyfield.api import load, wgs84
from Sky_Tracking.turret_sky import AirTraffic

currentLocation = wgs84.latlon(+51.99737, +4.35430, +60)  # Coordinates of turret earth position

lat_min, lon_min, lat_max, lon_max = 51, 2, 54, 8  # Define air traffic scanning region

ts = load.timescale()
time = ts.now()  # Get current time

at = AirTraffic(lat_min, lon_min, lat_max, lon_max)


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui

    def stopButtonClicked(self):
        print('EMERGENCY STOP')

    def updateButtonClicked(self):
        print('Update')

    def sendButtonClicked(self):
        print('Send')

    def restoreDefaultsButtonClicked(self):
        print('Restore Defaults')

    def copyDriversButtonClicked(self):
        print('Copy Drivers')

    def updateSettingsButtonClicked(self):
        print('Update Settings')

    def refreshButtonClicked(self):
        callsigns = at.get_airtraffic_callsigns(currentLocation, time)
        self.updateAirTraffic(callsigns)
        print('Refresh')

    def calibrateButtonClicked(self):
        print('Calibrate')

    def homeButtonClicked(self):
        print('Home')

    def fireButtonClicked(self):
        print('Fire')

    def powerOffButtonClicked(self):
        print('Power Off')

    def skyMode(self, mode=0):
        print("Sky Mode:", mode)

    def timeMode(self, mode="Current"):
        print("Time Mode:", mode)

    def manualOverride(self, mode):
        print("Manual Override:", mode)

    def turretMode(self, mode=0):
        print("Turret Mode:", mode)

    def currentLat(self, lat):
        print("Current Lat:", lat)

    def currentLong(self, long):
        print("Current Long:", long)

    def time(self, time):
        print("Time:", time)

    def spiCommand(self, command):
        print("SPI Command:", command)

    def airTraffic(self, callsign):
        print("Callsign:", callsign)

    # Methods

    def updateAirTraffic(self, callsigns):
        self.ui.airTrafficList.addItems(callsigns)
        print("Added Items:", callsigns)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = PyUi.Ui_MainWindow()
    MainWindow = MyWindow(ui)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
