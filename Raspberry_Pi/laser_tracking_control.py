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

lower = np.array([36, 20, 150])
upper = np.array([86, 100, 255])
camera_port = 0
threshold = 400

video_capture = cv2.VideoCapture(camera_port)
while True:
    turret_camera.get_laser_point(video_capture, lower, upper, threshold, show_video=True)

video_capture.release()
cv2.destroyAllWindows()
