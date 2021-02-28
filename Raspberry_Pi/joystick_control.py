#!/usr/bin/env python
# coding: utf-8
# This file is the main operating one

# Load  libraries
import Gamepad
import time
import atexit
from gpiozero import PWMOutputDevice

# Import local files
from turret_i2c import I2cData
from turret_gamepad import TMJoystick

# Define GPIO output pins
laserOutput = PWMOutputDevice(18, True, 0, 1000, None)

# Create instance of i2c_data class
i2cd = I2cData(0x8)

# Gamepad settings
gamepad_type = TMJoystick
button_trigger = 'TRIGGER'
button_center = 'CENTER'
button_exit = 'BACK'
button_RTH = 'RIGHT'
joystick_pan = 'JOY-X'
joystick_tilt = 'JOY-Y'
slider_power = 'SLIDER'
dpad_x = 'DPAD-X'
dpad_y = 'DPAD-Y'

pollInterval = 0.1

# Wait for a connection
if not Gamepad.available():
    print('Please connect your gamepad...')
    while not Gamepad.available():
        time.sleep(1.0)
gamepad = gamepad_type()
print('Gamepad connected')

# Set initial states
global running
global center_on
global laser_power
laser_power = 0
running = True
center_on = False


# Create callback functions
def trigger_button_pressed():
    i2cd.set_laser_on(1)
    i2cd.send_data()
    i2cd.set_laser_on(0)


def trigger_button_released():
    pass


def center_button_pressed():
    i2cd.set_calibrate(1)
    i2cd.send_data()
    i2cd.set_calibrate(0)
    print("CALIBRATED")


def exit_button_pressed():
    global running
    print('EXIT')
    running = False


def rth_button_pressed():
    i2cd.set_return_to_home(1)
    i2cd.send_data()
    i2cd.set_return_to_home(0)


def pan_axis_moved(pan_speed):
    i2cd.set_pan_dir(0 if pan_speed < 0 else 1)
    i2cd.set_pan_speed(abs(int(pan_speed * 255)))
    i2cd.send_data()
    print('Pan: ' + str(round(pan_speed, 3)))


def tilt_axis_moved(tilt_speed):
    i2cd.set_tilt_dir(0 if tilt_speed < 0 else 1)
    i2cd.set_tilt_speed(abs(int(tilt_speed * 255)))
    print('Tilt: ' + str(round(tilt_speed, 3)))
    i2cd.send_data()


def power_axis_moved(laser):
    global laser_power
    laser_power = int((-laser + 1) * 255 / 2)
    i2cd.set_laser_power(laser_power)
    i2cd.send_data()
    print('Laser _power: ' + str(round(laser_power, 3)))


def dpad_x_axis_moved(direction):
    if direction == 1:
        output = 2
        dir_x = 'RIGHT'
    elif direction == -1:
        output = 0
        dir_x = 'LEFT'
    else:
        output = 1
        dir_x = 'MID'
    i2cd.set_dpad(output)
    i2cd.send_data()
    print('dPad-X: ' + dir_x)


def dpad_y_axis_moved(direction):
    if direction == 1:
        output = 5
        dir_y = 'DOWN'
    elif direction == -1:
        output = 4
        dir_y = 'UP'
    else:
        output = 3
        dir_y = 'MID'
    i2cd.set_dpad(output)
    i2cd.send_data()
    print('dPad-Y: ' + dir_y)


# Start the background updating
gamepad.startBackgroundUpdates()

# Register the callback functions
gamepad.addButtonPressedHandler(button_trigger, trigger_button_pressed)
gamepad.addButtonReleasedHandler(button_trigger, trigger_button_released)
gamepad.addButtonPressedHandler(button_center, center_button_pressed)
gamepad.addButtonPressedHandler(button_exit, exit_button_pressed)
gamepad.addButtonPressedHandler(button_RTH, rth_button_pressed)
gamepad.addAxisMovedHandler(joystick_pan, pan_axis_moved)
gamepad.addAxisMovedHandler(joystick_tilt, tilt_axis_moved)
gamepad.addAxisMovedHandler(slider_power, power_axis_moved)
gamepad.addAxisMovedHandler(dpad_x, dpad_x_axis_moved)
gamepad.addAxisMovedHandler(dpad_y, dpad_y_axis_moved)


def exit_handler():
    i2cd.reset()
    i2cd.send_data()
    print('EXIT!')


atexit.register(exit_handler)

# Keep running while joystick updates are handled by the callbacks
try:
    while running and gamepad.isConnected():
        # Show the current pan and tilt
        # print('%+.1f %% pan_speed, %+.1f %% tilt_speed' % (pan_speed * 100, tilt_speed * 100))
        # Sleep for our polling interval
        time.sleep(pollInterval)
finally:
    # Ensure the background thread is always terminated when we are done
    gamepad.disconnect()
