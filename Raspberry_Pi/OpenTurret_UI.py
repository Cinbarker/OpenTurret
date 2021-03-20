import PyUi
from PyQt5 import QtWidgets, QtCore
import Sky_Tracking.turret_sky as sky
from skyfield.api import load, wgs84
from Sky_Tracking.turret_sky import AirTraffic


class MyWindow(QtWidgets.QMainWindow):
    currentLat, currentLon, currentAlt = +51.99737, +4.35430, +60
    currentLocation = wgs84.latlon(currentLat, currentLon, currentAlt)  # Coordinates of turret earth position

    lat_min, lon_min, lat_max, lon_max = 51, 2, 54, 8  # Default is the Netherlands
    at = AirTraffic(lat_min, lon_min, lat_max, lon_max)  # Define air traffic scanning region
    spiCom = ''

    def __init__(self, ui):
        super().__init__()
        self.ui = ui

    # Abstract Methods from parent

    def stopButtonClicked(self):
        print('EMERGENCY STOP')

    def updateButtonClicked(self):
        print('Update')

    def sendButtonClicked(self):
        self.spiCom = self.ui.spiCommand.text()
        self.ui.spiCommand.clear()
        print('Sent', self.spiCom)

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
        if mode == 'Custom':
            self.ui.timeEdit.setEnabled(True)
            self.ui.timeEdit_1.setEnabled(True)
            self.ui.timeEdit_2.setEnabled(True)
        else:
            time = QtCore.QTime(QtCore.QTime.currentTime())
            self.ui.timeEdit.setTime(time)
            self.ui.timeEdit.setEnabled(False)
            self.ui.timeEdit_1.setTime(time)
            self.ui.timeEdit_1.setEnabled(False)
            self.ui.timeEdit_2.setTime(time)
            self.ui.timeEdit_2.setEnabled(False)
        print("Time Mode:", mode)

    def manualOverride(self, mode):
        print("Manual Override:", mode)

    def turretMode(self, mode=0):
        print("Turret Mode:", mode)

    def currentLat(self, lat):
        self.currentLat = lat
        print("Current Lat:", lat)

    def currentLon(self, lon):
        self.currentLon = lon
        print("Current Lon:", lon)

    def time(self, time):
        print("Time:", time)

    def spiCommand(self, command):
        print("SPI Command:", command)

    def airTraffic(self, callsign):
        print("Callsign:", callsign)

    def maxSpeed(self, maxSpeed):
        print("Max Speed:", maxSpeed)

    def minSpeed(self, minSpeed):
        print("Min Speed:", minSpeed)

    def acc(self, acc):
        print("Acceleration:", acc)

    def dec(self, dec):
        print("Deceleration:", dec)

    def fsSpeed(self, fsSpeed):
        print("Full Step Speed:", fsSpeed)

    def ocdTh(self, ocdTh):
        print("OCD Threshold:", ocdTh)

    def stallTh(self, stallTh):
        print("Stall Threshold:", stallTh)

    def stepMode(self, stepMode):
        print("Step Mode:", stepMode)

    def oscSel(self, oscSel):
        print("OSC Select:", oscSel)

    def extClk(self, extClk):
        print("EXT Clock:", extClk)

    def swMode(self, swMode):
        print("SW Mode:", swMode)

    def enVscomp(self, enVscomp):
        print("EN VS Compensation:", enVscomp)

    def ocSd(self, ocSd):
        print("OC SD:", ocSd)

    def powSr(self, powSr):
        print("POW_SR:", powSr)

    def fPwmDec(self, fPwmDec):
        print("fPwmDec:", fPwmDec)

    def fPwmInt(self, fPwmInt):
        print("fPwmInt:", fPwmInt)

    def minLat(self, minLat):
        self.lat_min = minLat
        print("minLat:", minLat)

    def minLon(self, minLon):
        self.lon_min = minLon
        print("minLon:", minLon)

    def maxLat(self, maxLat):
        self.lat_max = maxLat
        print("maxLat:", maxLat)

    def maxLon(self, maxLon):
        self.lon_max = maxLon
        print("maxLon:", maxLon)

    def starInput(self, starInput):
        print("starInput:", starInput)

    def objectInput(self, objectInput):
        print("objectInput:", objectInput)

    def satelliteInput(self, satelliteInput):
        print("satelliteInput:", satelliteInput)

    def currentAlt(self, alt):
        self.currentAlt = alt
        print("Current Alt:", alt)

    # New Methods for actions

    def updateAirTraffic(self):
        ts = load.timescale()
        time = ts.now()  # Get current time
        self.at.update_airtraffic()  # Update Air Traffic information
        callsigns = self.at.get_airtraffic_callsigns(self.currentLocation, time)
        self.ui.airTrafficList.clear()  # Clear previous callsigns
        self.ui.airTrafficList.addItems(callsigns)
        print("Refreshed Air Traffic List")

    def setDefaults(self):
        time = QtCore.QTime(QtCore.QTime.currentTime())
        self.ui.timeEdit.setTime(time)
        self.ui.timeEdit_1.setTime(time)
        self.ui.timeEdit_2.setTime(time)

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = PyUi.Ui_MainWindow()
    MainWindow = MyWindow(ui)
    ui.setupUi(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())
