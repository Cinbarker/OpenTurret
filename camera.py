from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
 
camera = PiCamera()
camera.resolution = (1920, 1080)
imageCapture = PiRGBArray(camera, size = (1920, 1080))
 
time.sleep(0.2)
 
camera.capture(imageCapture, format="bgr")
image = imageCapture.array
 
cv2.imshow("Captured Image", image)
cv2.waitKey(0)