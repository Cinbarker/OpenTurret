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

lower_green = np.array([36, 100, 0])
upper_green = np.array([86, 200, 255])
lower_red = np.array([170, 40, 230])
upper_red = np.array([180, 80, 255])
camera_port = 0
threshold = 100

video_capture = cv2.VideoCapture(camera_port)
while True:
    turret_camera.get_laser_point(video_capture, lower_red, upper_red, threshold, show_video=True)

video_capture.release()
cv2.destroyAllWindows()
