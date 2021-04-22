import json
import logging

from PyQt5.QtCore import QSortFilterProxyModel, QObject, QThread, pyqtSignal
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import *
import PyUi
from PyQt5 import QtWidgets, QtCore
from Sky_Tracking.turret_sky import *

callsigns = None
lat_min, lon_min, lat_max, lon_max = 51, 2, 54, 8  # Default is a box around the Netherlands
at = AirTraffic(lat_min, lon_min, lat_max, lon_max)  # Define air traffic scanning region

# Set logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] %(levelname)-8s: %(message)-50s  [%(lineno)d %(name)s]",
    datefmt='%H:%M:%S')


# Create a worker thread class for updating air traffic
class AirTrafficWorker(QObject):
    finished = pyqtSignal()
    currentLocation = None

    def __init__(self, currentLocation, time):
        self.currentLocation = currentLocation
        self.time = time
        super().__init__()

    def run(self):
        """Long-running task."""
        global callsigns, at

        try:
            at.update_airtraffic()  # Update Air Traffic information
            callsigns = at.get_airtraffic_callsigns(self.currentLocation, self.time)
        except requests.exceptions.ConnectionError or requests.exceptions.ConnectTimeout:
            print('Connection Error')
            self.finished.emit()
            return
        except requests.exceptions.ReadTimeout:
            print('Timeout Error')
            self.finished.emit()
            return
        except json.decoder.JSONDecodeError:
            print('JSONDecodeError')
            self.finished.emit()
            return
        self.finished.emit()
        print("Successfully fetched callsigns")


class MyWindow(QtWidgets.QMainWindow):
    logger = logging.getLogger(__name__)
    currentLat, currentLon, currentAlt = +51.99737, +4.35430, +60
    currentLocation = wgs84.latlon(currentLat, currentLon, currentAlt)  # Coordinates of turret earth position

    ts = load.timescale()
    time = ts.now()  # Get current time

    spiCom = ''

    altOut, azOut, distOut = 0, 0, 0  # Define variables for target location

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

    def refreshButtonClicked(self):  # TODO Refresh aircraft can crash
        print('Refresh')
        self.ui.modelAir.clear()
        self.callsigns = self.update_air_traffic()

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
            self.time = QtCore.QTime(QtCore.QTime.currentTime())
            self.ui.timeEdit.setTime(self.time)
            self.ui.timeEdit.setEnabled(False)
            self.ui.timeEdit_1.setTime(self.time)
            self.ui.timeEdit_1.setEnabled(False)
            self.ui.timeEdit_2.setTime(self.time)
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
        global at
        selectedCallsign = callsign.data()
        if selectedCallsign == 'Click "Refresh Traffic"' or selectedCallsign == 'ERROR: Please try again':
            pass
        else:
            self.time = self.ts.now()  # Get and set current time
            self.altOut, self.azOut, self.distOut = at.get_airtraffic_altaz(selectedCallsign, self.currentLocation,
                                                                            self.time)
            # TODO Add background method that updates target position regularly
            self.ui.altTarget.setText(str(round(self.altOut, 4)))
            self.ui.azTarget.setText(str(round(self.azOut, 4)))
            self.ui.distanceTarget.setText(str(round(self.distOut, 4)))
        print("Callsign:", selectedCallsign)

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
        self.proxyModelStar = QSortFilterProxyModel()
        self.proxyModelStar.setSourceModel(self.ui.modelStar)
        self.proxyModelStar.setFilterFixedString(starInput)
        self.proxyModelStar.setFilterCaseSensitivity(0)
        self.ui.starList.setModel(self.proxyModelStar)
        self.ui.starList.show()
        print("starInput:", starInput)

    def objectInput(self, objectInput):
        self.proxyModelObj = QSortFilterProxyModel()
        self.proxyModelObj.setSourceModel(self.ui.modelObj)
        self.proxyModelObj.setFilterFixedString(objectInput)
        self.proxyModelObj.setFilterCaseSensitivity(0)
        self.ui.objectList.setModel(self.proxyModelObj)
        self.ui.objectList.show()
        print("objectInput:", objectInput)

    def satelliteInput(self, satelliteInput):
        self.proxyModelSat = QSortFilterProxyModel()
        self.proxyModelSat.setSourceModel(self.ui.modelSat)
        self.proxyModelSat.setFilterFixedString(satelliteInput)
        self.proxyModelSat.setFilterCaseSensitivity(0)
        self.ui.satelliteList.setModel(self.proxyModelSat)
        self.ui.satelliteList.show()
        print("satelliteInput:", satelliteInput)

    def callsignInput(self, callsignInput):
        self.proxyModelAir = QSortFilterProxyModel()
        self.proxyModelAir.setSourceModel(self.ui.modelAir)
        self.proxyModelAir.setFilterFixedString(callsignInput)
        self.proxyModelAir.setFilterCaseSensitivity(0)
        self.ui.airTrafficList.setModel(self.proxyModelAir)
        self.ui.airTrafficList.show()
        print("callsignInput:", callsignInput)

    def currentAlt(self, alt):
        self.currentAlt = alt
        print("Current Alt:", alt)

    def satelliteList(self, satellite):
        self.selectedSatellite = satellite.data()
        print("Satellite:", self.selectedSatellite)

    def objectList(self, object):
        self.selectedObject = object.data()
        print("Object:", self.selectedObject)

    def starList(self, star):
        self.selectedStarName = star.data()
        print("Star:", self.selectedStarName)

    def closeWindow(self):
        logging.info('Closing Application')
        self.close()

    def saveDefaults(self):
        logging.info('Saving Defaults')

    def resetDefaults(self):
        logging.info('Resetting Defaults')

    def altOut(self, altOut):
        self.altOut = altOut
        print(altOut)

    def azOut(self, azOut):
        self.azOut = azOut
        print(azOut)

    def mosquitoSize(self, mosquitoSize):
        print(mosquitoSize)

    def speedMode(self, speedMode):
        print("speedMode:", speedMode)

    # New Methods for actions

    def update_callsign_list(self):
        """ Update displayed list of callsigns with current callsign list """
        global callsigns
        if callsigns != None:
            self.ui.modelAir.appendColumn([QStandardItem(text) for text in callsigns])
            self.ui.airTrafficList.setModel(self.ui.modelAir)
            self.ui.airTrafficList.show()
            print("Refreshed Air Traffic List")
        else:
            errorMessage = QStandardItem('ERROR: Please try again')
            errorMessage.setEnabled(0)
            errorMessage.setSelectable(0)
            self.ui.modelAir.setItem(0, 0, errorMessage)
            self.ui.airTrafficList.show()
        self.ui.refreshButton.setEnabled(True)

    def update_air_traffic(self):
        """ Update Air Traffic information in a new thread. Uses worker class AirTrafficWorker """
        self.time = self.ts.now()  # Get and set current time
        # Create a QThread object
        self.thread = QThread()
        # Create a worker object
        self.worker = AirTrafficWorker(self.currentLocation, self.time)
        # Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        # Start the thread
        self.thread.start()

        # Final resets
        self.ui.refreshButton.setEnabled(False)
        self.thread.finished.connect(self.update_callsign_list)

    def startup_procedure(self):
        """ Method to run application setup """
        # Time Default
        self.time = QtCore.QTime(QtCore.QTime.currentTime())
        self.ui.timeEdit.setTime(self.time)
        self.ui.timeEdit_1.setTime(self.time)
        self.ui.timeEdit_2.setTime(self.time)

        # Air Traffic Default
        self.ui.modelAir = QStandardItemModel(self.ui.airTrafficList)
        refreshMessage = QStandardItem('Click "Refresh Traffic"')
        refreshMessage.setEnabled(0)
        refreshMessage.setSelectable(0)
        self.ui.modelAir.setItem(0, 0, refreshMessage)
        self.ui.airTrafficList.setModel(self.ui.modelAir)
        self.ui.airTrafficList.show()

        # Satellite Default
        self.ui.modelSat = QStandardItemModel(self.ui.satelliteList)
        self.ui.modelSat.appendColumn([QStandardItem(text) for text in get_satellites()])
        self.ui.satelliteList.setModel(self.ui.modelSat)
        self.ui.satelliteList.show()

        # Solar Objects Default
        self.ui.modelObj = QStandardItemModel(self.ui.objectList)
        self.ui.modelObj.appendColumn([QStandardItem(text) for text in get_objects()])
        self.ui.objectList.setModel(self.ui.modelObj)
        self.ui.objectList.show()

        # Star Default
        names, hips = get_stars()
        self.ui.modelStar = QStandardItemModel(self.ui.starList)
        self.ui.modelStar.appendColumn([QStandardItem(text) for text in names])
        self.ui.starList.setModel(self.ui.modelStar)
        self.ui.starList.show()

        # SPI Default
        commands = ['GoTo()', 'SetDir()']
        self.ui.spiCommand.clear()  # Clear previous satellites
        self.ui.modelSPI = QStandardItemModel()
        self.ui.modelSPI.appendColumn([QStandardItem(text) for text in commands])
        completerSPI = QCompleter(self.ui.modelSPI, self)
        self.ui.spiCommand.setCompleter(completerSPI)

        # GUI Default
        self.ui.skyMode.setCurrentIndex(0)
        self.ui.turretMode.setCurrentIndex(0)
        logging.info('Completed Setup Procedure')


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = PyUi.Ui_MainWindow()
    MainWindow = MyWindow(ui)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
