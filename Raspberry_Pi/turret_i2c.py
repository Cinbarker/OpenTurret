# This is the I2C management file.
#

from smbus2 import SMBus

class i2c_data:
    address   = 0
    panSpeed  = 0
    tiltSpeed = 0
    panDir    = 0
    tiltDir   = 0
    calibrate   = 0
    bus = None
    
    def __init__(self, address):
        self.address = address
        self.bus = SMBus(1) # indicates /dev/ic2-1

    def send_data(self):
        data = [self.panSpeed, self.tiltSpeed, self.panDir, self.tiltDir, self.calibrate]
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

