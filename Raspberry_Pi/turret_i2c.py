# This is the I2C management file.
#

from smbus2 import SMBus
from CustomExceptions import *

class I2cData:
    address = 0
    pan_speed = 0
    tilt_speed = 0
    pan_dir = 0
    tilt_dir = 0
    calibrate = 0
    laser_power = 0
    laser_on = 0
    return_to_home = 0
    bus = None
    pad_x = 1
    pad_y = 1
    calibrated = False

    def __init__(self, address):
        self.address = address
        self.bus = SMBus(1)  # indicates /dev/ic2-1

    def send_data(self):
        if self.calibrated:
            data = [self.pan_speed,
                    self.tilt_speed,
                    self.pan_dir,
                    self.tilt_dir,
                    self.calibrate,
                    self.laser_power,
                    self.laser_on,
                    self.return_to_home,
                    self.pad_x,
                    self.pad_y]
            try:
                self.bus.write_i2c_block_data(self.address, 0x00, data)
            except OSError:
                logging.error('I2C BUS NOT OPEN')

    def set_pan_speed(self, pan_speed):
        self.pan_speed = pan_speed

    def set_tilt_speed(self, tilt_speed):
        self.tilt_speed = tilt_speed

    def get_pan_speed(self):
        return self.pan_speed

    def get_tilt_speed(self):
        return self.tilt_speed

    def set_pan_dir(self, pan_dir):
        self.pan_dir = pan_dir

    def set_tilt_dir(self, tilt_dir):
        self.tilt_dir = tilt_dir

    def set_calibrate(self, calibrate):
        self.calibrated = True
        self.calibrate = calibrate

    def set_laser_power(self, laser_power):
        self.laser_power = laser_power

    def set_laser_on(self, laser_on):
        self.laser_on = laser_on

    def set_return_to_home(self, return_to_home):
        self.return_to_home = return_to_home

    def set_dpad_x(self, pad_x):
        self.pad_x = pad_x

    def set_dpad_y(self, pad_y):
        self.pad_y = pad_y

    def reset(self):
        self.pan_speed = 0
        self.tilt_speed = 0
        self.pan_dir = 0
        self.tilt_dir = 0
        self.calibrate = 0
        self.laser_power = 0
        self.laser_on = 0
        self.return_to_home = 0
        self.pad_x = 1
        self.pad_y = 1
        self.send_data()
