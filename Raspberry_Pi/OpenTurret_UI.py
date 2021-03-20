import PyUi
from PyQt5 import QtWidgets
import Sky_Tracking.turret_sky as sky
from skyfield.api import load, wgs84
from Sky_Tracking.turret_sky import AirTraffic


class MyWindow(QtWidgets.QMainWindow):
    currentLat, currentLon, currentAlt = +51.99737, +4.35430, +60
    currentLocation = wgs84.latlon(currentLat, currentLon, currentAlt)  # Coordinates of turret earth position

    lat_min, lon_min, lat_max, lon_max = 51, 2, 54, 8   # Default is the Netherlands
    at = AirTraffic(lat_min, lon_min, lat_max, lon_max)  # Define air traffic scanning region

    def __init__(self, ui):
        super().__init__()
        self.ui = ui

    # Abstract Methods from parent

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
        print('Refresh')
        self.updateAirTraffic()

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

    # New Methods for actions

    def updateAirTraffic(self):
        ts = load.timescale()
        time = ts.now()  # Get current time
        self.at.update_airtraffic()  # Update Air Traffic information
        callsigns = self.at.get_airtraffic_callsigns(self.currentLocation, time)
        self.ui.airTrafficList.clear()  # Clear previous callsigns
        self.ui.airTrafficList.addItems(callsigns)
        print("Refreshed Air Traffic List")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = PyUi.Ui_MainWindow()
    MainWindow = MyWindow(ui)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
