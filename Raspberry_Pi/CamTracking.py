import cv2
import time
import atexit
import sys
import termios
import contextlib
import numpy as np

import imutils


# import RPi.GPIO as GPIO

def live_video(camera_port=0):

    video_capture = cv2.VideoCapture(camera_port)

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        # Display the resulting frame
        # print(frame)
        lower = np.array([36, 20, 150])
        upper = np.array([86, 100, 255])
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        frame_mask = cv2.inRange(frame_hsv, lower, upper)
        frame_comp = cv2.bitwise_and(frame, frame, mask=frame_mask)

        c = VideoUtils.get_best_contour(frame_mask, 400)

        if c is not None:
            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            # print(c)
            print('x', x, 'y', y)
            x = x + (w // 2)
            y = y + (h // 2)
            sz = (w+h)//10
            cv2.line(frame_comp, (x - sz, y - sz), (x + sz, y + sz), (0, 0, 255), 2)
            cv2.line(frame_comp, (x - sz, y + sz), (x + sz, y - sz), (0, 0, 255), 2)
            # cv2.rectangle(frame_comp, (x, y), (x+w, y+h), (0, 255, 0), 2)
        # print(c)
        cv2.imshow("Live From Nic's Lab", frame_comp)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()

def get_best_contour(imgmask, threshold):
    contours, hierarchy = cv2.findContours(imgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    best_area = threshold
    best_cnt = None
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > best_area:
            best_area = area
            best_cnt = cnt
    return best_cnt


VideoUtils.live_video()
