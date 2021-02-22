#!/usr/bin/env python
# coding: utf-8
# This file is the main operating one

# Load the gamepad, time, numpy, and gpio libraries
import Gamepad
import time
import numpy
from time import sleep
from gpiozero import DigitalOutputDevice

# Import local files
from turret_i2c import i2c_data
from turret_gamepad import TM_joystick

# Define GPIO output pins
laserGun = DigitalOutputDevice(26)

# Create instance of i2c_data class
i2cd = i2c_data(0x8)

# Gamepad settings
gamepadType   = TM_joystick
buttonTrigger = 'TRIGGER'
buttonFire    = 'FIRE'
buttonExit    = 'BACK'
joystickPan   = 'JOY-X'
joystickTilt  = 'JOY-Y'
sliderPower   = 'SLIDER'
pollInterval  = 0.2

# Wait for a connection
if not Gamepad.available():
    print('Please connect your gamepad...')
    while not Gamepad.available():
        time.sleep(1.0)
gamepad = gamepadType()
print('Gamepad connected')

# Set some initial state
global running
global fireOn
running = True
fireOn = False

# Create some callback functions
def triggerButtonPressed():
    laserGun.on()
    time.sleep(0.001)
    laserGun.off()
    print('Triggered')

def triggerButtonReleased():
    print('All Good')

def fireButtonPressed():
    global fireOn
    laserGun.on()
    time.sleep(0.001)
    laserGun.off()
    print("Boom boom boom boom. I want you in my room.")

def exitButtonPressed():
    global running
    print('EXIT')
    running = False

def panAxisMoved(panSpeed):
    i2cd.set_panDir(0 if panSpeed < 0 else 1)
    i2cd.set_panSpeed(abs(int(panSpeed*255)))
    i2cd.send_data()
    print(panSpeed)

def tiltAxisMoved(tiltSpeed):
    i2cd.set_tiltDir(0 if tiltSpeed > 0 else 1)
    i2cd.set_tiltSpeed(abs(int(tiltSpeed*255)))
    print(tiltSpeed)
    i2cd.send_data()

# Start the background updating
gamepad.startBackgroundUpdates()

# Register the callback functions
gamepad.addButtonPressedHandler(buttonTrigger, triggerButtonPressed)
gamepad.addButtonReleasedHandler(buttonTrigger, triggerButtonReleased)
gamepad.addButtonPressedHandler(buttonFire, fireButtonPressed)
gamepad.addButtonPressedHandler(buttonExit, exitButtonPressed)
gamepad.addAxisMovedHandler(joystickPan, panAxisMoved)
gamepad.addAxisMovedHandler(joystickTilt, tiltAxisMoved)

# Keep running while joystick updates are handled by the callbacks
try:
    while running and gamepad.isConnected():
        # Show the current pan and tilt
        #print('%+.1f %% panSpeed, %+.1f %% tiltSpeed' % (panSpeed * 100, tiltSpeed * 100))
        pass

        # Sleep for our polling interval
        time.sleep(pollInterval)
finally:
    # Ensure the background thread is always terminated when we are done
    gamepad.disconnect()
