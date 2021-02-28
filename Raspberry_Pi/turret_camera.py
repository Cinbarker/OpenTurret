import cv2
import numpy as np
import imutils


# import RPi.GPIO as GPIO

def get_laser_point(video_capture, lower, upper, threshold, show_video=False):
    # Capture a frame from camera
    ret, frame = video_capture.read()

    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frame_mask = cv2.inRange(frame_hsv, lower, upper)
    frame_comp = cv2.bitwise_and(frame, frame, mask=frame_mask)

    contour = get_best_contour(frame_mask, threshold)

    # Initialize center coordinates
    x, y = None, None

    if contour is not None:
        (x, y, w, h) = cv2.boundingRect(contour)
        # print('x', x, 'y', y)
        x = x + (w // 2)
        y = y + (h // 2)
        cross_size = (w + h) // 10
        cv2.line(frame_comp, (x - cross_size, y - cross_size), (x + cross_size, y + cross_size), (0, 0, 255), 2)
        cv2.line(frame_comp, (x - cross_size, y + cross_size), (x + cross_size, y - cross_size), (0, 0, 255), 2)
        cv2.rectangle(frame_comp, (x - (w // 2), y - (w // 2)), (x + (w // 2), y + (h // 2)), (0, 255, 0), 2)
    # Show live camera feed
    if show_video:
        cv2.imshow("Camera Feed", frame_comp)
        cv2.waitKey(1)
    return x, y


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
