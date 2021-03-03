# Load libraries
import time
import numpy as np
import cv2
import atexit
from gpiozero import PWMOutputDevice

# Import local files
import turret_camera
from turret_i2c import I2cData
from turret_gamepad import TMJoystick

# Initialize turret
address = 0x8
i2cd = I2cData(address)
i2cd.set_calibrate(1)
i2cd.send_data()
i2cd.set_calibrate(0)

# Turn turret laser on
i2cd.set_laser_power(255)
i2cd.send_data()

lower_green = np.array([36, 00, 20])
upper_green = np.array([86, 250, 255])
lower_red = np.array([175, 0, 100])
upper_red = np.array([179, 255, 200])
camera_port = 0
thresh_red = 5
thresh_green = 200

video_capture = cv2.VideoCapture(camera_port)
while True:
    red_x, red_y = turret_camera.get_laser_point(video_capture, lower_red, upper_red, thresh_red, show_video=False)
    green_x, green_y = turret_camera.get_laser_point(video_capture, lower_green, upper_green, thresh_green, show_video=False)
    print
    if (red_x==None or green_x == None):
        i2cd.set_pan_speed(0)
        i2cd.send_data()
        continue
    if (red_x<green_x):
        i2cd.set_pan_dir(1)
        i2cd.set_pan_speed(200)
        i2cd.send_data()
        i2cd.set_pan_speed(0)
    if (red_x>green_x):
        i2cd.set_pan_dir(0)
        i2cd.set_pan_speed(200)
        i2cd.send_data()
        i2cd.set_pan_speed(0)
    
video_capture.release()
cv2.destroyAllWindows()
