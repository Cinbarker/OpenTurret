import cv2
from numba import jit
import numpy as np
import imutils


# import RPi.GPIO as GPIO

#def img_process():


def get_laser_point(video_capture, lower, upper, threshold, show_video=False):
    # Capture a frame from camera
    ret, frame = video_capture.read()

    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    if lower[0] > upper[0]: # Fix for wrapping around the Hue Spectrum. Useful for red colors
        up = upper[0]
        upper[0] = 180
        frame_mask = cv2.inRange(frame_hsv, lower, upper)
        lower[0] = 0
        upper[0] = up
        frame_mask = frame_mask + cv2.inRange(frame_hsv, lower, upper)
    else:
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


if __name__ == '__main__':
    while True:
        lower_green = np.array([36, 00, 20])
        upper_green = np.array([86, 250, 255])
        lower_red = np.array([175, 0, 100])
        upper_red = np.array([179, 255, 200])
        camera_port = 0
        thresh_red = 5
        thresh_green = 200

        video_capture = cv2.VideoCapture(camera_port)
        get_laser_point(video_capture, lower_red, upper_red, thresh_red, show_video=True)

    video_capture.release()
    cv2.destroyAllWindows()
