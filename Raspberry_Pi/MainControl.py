#!/usr/bin/env python
# coding: utf-8
# This file is the main operating one

# Load the gamepad, time, numpy, and gpio libraries
import Gamepad
import time
import atexit
from gpiozero import PWMOutputDevice

# Import local files
from turret_i2c import i2c_data
from turret_gamepad import TM_joystick

# Define GPIO output pins
laserOutput = PWMOutputDevice(18, True, 0, 1000, None)

# Create instance of i2c_data class
i2cd = i2c_data(0x8)

# Gamepad settings
gamepadType = TM_joystick
buttonTrigger = 'TRIGGER'
buttonCenter = 'CENTER'
buttonExit = 'BACK'
joystickPan = 'JOY-X'
joystickTilt = 'JOY-Y'
sliderPower = 'SLIDER'
pollInterval = 0.1

# Wait for a connection
if not Gamepad.available():
    print('Please connect your gamepad...')
    while not Gamepad.available():
        time.sleep(1.0)
gamepad = gamepadType()
print('Gamepad connected')

# Set some initial state
global running
global centerOn
global laserPower
laserPower = 0
running = True
centerOn = False


# Create some callback functions
def triggerButtonPressed():
    i2cd.set_laserOn(1)
    i2cd.send_data()
    i2cd.set_laserOn(0)


def triggerButtonReleased():
    pass


def centerButtonPressed():
    i2cd.set_calibrate(1)
    i2cd.send_data()
    print("CALIBRATED")


def centerButtonReleased():
    i2cd.set_calibrate(0)
    i2cd.send_data()


def exitButtonPressed():
    global running
    print('EXIT')
    running = False


def panAxisMoved(panSpeed):
    i2cd.set_panDir(0 if panSpeed < 0 else 1)
    i2cd.set_panSpeed(abs(int(panSpeed * 255)))
    i2cd.send_data()
    print('Pan: ' + str(round(panSpeed, 3)))


def tiltAxisMoved(tiltSpeed):
    i2cd.set_tiltDir(0 if tiltSpeed < 0 else 1)
    i2cd.set_tiltSpeed(abs(int(tiltSpeed * 255)))
    print('Tilt: ' + str(round(tiltSpeed, 3)))
    i2cd.send_data()


def powerAxisMoved(laser):
    global laserPower
    laserPower = int((-laser + 1) * 255 / 2)
    i2cd.set_laserPower(laserPower)
    i2cd.send_data()
    print('Laser Power: ' + str(round(laserPower, 3)))


# Start the background updating
gamepad.startBackgroundUpdates()

# Register the callback functions
gamepad.addButtonPressedHandler(buttonTrigger, triggerButtonPressed)
gamepad.addButtonReleasedHandler(buttonTrigger, triggerButtonReleased)
gamepad.addButtonPressedHandler(buttonCenter, centerButtonPressed)
gamepad.addButtonReleasedHandler(buttonCenter, centerButtonReleased)
gamepad.addButtonPressedHandler(buttonExit, exitButtonPressed)
gamepad.addAxisMovedHandler(joystickPan, panAxisMoved)
gamepad.addAxisMovedHandler(joystickTilt, tiltAxisMoved)
gamepad.addAxisMovedHandler(sliderPower, powerAxisMoved)


def exit_handler():
    i2cd.reset()
    i2cd.send_data()
    print('EXIT!')


atexit.register(exit_handler)

# Keep running while joystick updates are handled by the callbacks
try:
    while running and gamepad.isConnected():
        # Show the current pan and tilt
        # print('%+.1f %% panSpeed, %+.1f %% tiltSpeed' % (panSpeed * 100, tiltSpeed * 100))
        # Sleep for our polling interval
        time.sleep(pollInterval)
finally:
    # Ensure the background thread is always terminated when we are done
    gamepad.disconnect()
