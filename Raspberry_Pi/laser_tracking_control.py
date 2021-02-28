# Load the gamepad, time, numpy, and gpio libraries
import Gamepad
import time
import atexit
from gpiozero import PWMOutputDevice

# Import local files
from turret_i2c import i2c_data
from turret_gamepad import TM_joystick