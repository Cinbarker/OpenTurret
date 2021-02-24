# This is the I2C management file.
#

from smbus2 import SMBus


class i2c_data:
    address = 0
    panSpeed = 0
    tiltSpeed = 0
    panDir = 0
    tiltDir = 0
    calibrate = 0
    laserPower = 0
    laserOn = 0
    returnToHome = 0
    bus = None

    def __init__(self, address):
        self.address = address
        self.bus = SMBus(1)  # indicates /dev/ic2-1

    def send_data(self):
        data = [self.panSpeed,
                self.tiltSpeed,
                self.panDir,
                self.tiltDir,
                self.calibrate,
                self.laserPower,
                self.laserOn,
                self.returnToHome]
        try:
            self.bus.write_i2c_block_data(self.address, 0x00, data)
        except OSError:
            print('Codefarted')

    def set_panSpeed(self, panSpeed):
        self.panSpeed = panSpeed

    def set_tiltSpeed(self, tiltSpeed):
        self.tiltSpeed = tiltSpeed

    def set_panDir(self, panDir):
        self.panDir = panDir

    def set_tiltDir(self, tiltDir):
        self.tiltDir = tiltDir

    def set_calibrate(self, calibrate):
        self.calibrate = calibrate

    def set_laserPower(self, laserPower):
        self.laserPower = laserPower

    def set_laserOn(self, laserOn):
        self.laserOn = laserOn

    def set_returnToHome(self, returnToHome):
        self.returnToHome = returnToHome

    def reset(self):
        self.panSpeed = 0
        self.tiltSpeed = 0
        self.panDir = 0
        self.tiltDir = 0
        self.calibrate = 0
        self.laserPower = 0
        self.laserOn = 0
        self.returnToHome = 0

