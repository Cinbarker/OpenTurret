import threading

from Raspberry_Pi.turret_camera import get_laser_point


def _calibrate_camera_thread(video_capture, lower, upper, thresh):
    """
    Thread that calibrates camera.
    """
    while True:
        get_laser_point(video_capture, lower, upper, thresh, show_video=True)


def start_calibrate_camera_thread(video_capture, lower, upper, thresh):
    """
    Method to start thread that calibrates camera.
    """
    calibrate_camera_thread = threading.Thread(target=_calibrate_camera_thread, args=(video_capture, lower, upper, thresh),
                                     daemon=True,
                                     name="Camera Calibrate")
    calibrate_camera_thread.start()
    return calibrate_camera_thread